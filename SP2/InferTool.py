"""
Will run the Infer analysis. Must pass project folder name as argument,
for now. 
Assumes Gradle build. SDK folder must be defined in local.properties in 
the app folder. SDK and Build tools versions must match the app.
"""

import os, sys, subprocess, shutil, csv, time
import classes
#from classes import Bug

# Constants
LOCALPROPERTIES = "local.properties"
SDKPATH = "sdk.dir=/Users/chris/Library/Android/sdk"
BUGFILEDIR = "/Users/chris/Downloads/app-evolution-toolkit/SP2/BUGFiles/"
BUGDIRECTORY = "infer-out/"
BUGFILE = "bugs.txt"
BUILDDIRECTORY = "build"


def main():
	appDir = sys.argv[1]
	#inferAnalysis(appDir)
	loopedAnalysis()


# Analysis mode that will loop between 2 folders, IOS and Android
def loopedAnalysis():
	start = time.time()
	os.chdir("Android")
	for dirs in os.listdir("."):
		if os.path.isdir(dirs):
			os.chdir(dirs)
			inferAnalysisAndroid(dirs, "1")
			os.chdir("..")

	os.chdir("..")
	os.chdir("IOS")
	for dirs in os.listdir("."):
		if os.path.isdir(dirs):
			os.chdir(dirs)
			inferAnalysisIOS("1")
			os.chdir("..")
	os.chdir("..")

	end = time.time()
	print("Time elapsed: " + str(end-start) + " seconds")


# Runs the infer analysis via terminal
def inferAnalysis(appDir, commitIndex):
	start = time.time()
	removePreviousBuild()
	# if appDir[0:3] == "IOS":
	# 	inferAnalysisIOS()
		
	# elif appDir[0:3] == "And":
	# 	inferAnalysisAndroid(appDir)

	if os.path.exists("gradlew"): 
		inferAnalysisAndroid(appDir, commitIndex)

	else:		# assumes if not android, it is ios, in ios analysis a check will be made to see if it is really an ios app
		inferAnalysisIOS(commitIndex)

	end = time.time()
	print("Time elapsed: " + str(end-start) + " seconds")
	
		

# Infer analysis for android apps
def inferAnalysisAndroid(appDir, commitIndex):

	writeLocalProperties()
	FNULL = open(os.devnull, 'w')
	print("Initializing analysis of " + appDir + " ...")
	subprocess.call('./gradlew clean', shell=True)#, stdout=FNULL, stderr=subprocess.STDOUT)
	subprocess.call('infer run -- ./gradlew build', shell=True)#, stdout=FNULL, stderr=subprocess.STDOUT)
	readBugReport(appDir, commitIndex)
	#readBugReport(appDir, "Android")

# Infer analysis for iOS apps
def inferAnalysisIOS(commitIndex):
	appName = findProjectName()
	if appName != "false":
		callString = 'infer run --no-xcpretty -- xcodebuild -target ' + appName + ' -configuration Debug -sdk iphonesimulator'
		test = 'infer run --no-xcpretty -- xcodebuild  -workspace Telegram.xcworkspace -scheme Telegram'
		FNULL = open(os.devnull, 'w')
		print("Initializing analysis of " + appName + " ...")
		subprocess.call(callString, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
		readBugReport(appName, commitIndex)

	else: 
		print("No working app found")

# Rewrites local.properties in order to make android builds work
def writeLocalProperties(): 
	if os.path.isfile(LOCALPROPERTIES):
		os.remove(LOCALPROPERTIES)

	propfile = open(LOCALPROPERTIES, 'w')
	propfile.write(SDKPATH)
	propfile.close()

# removes older build of iOS app, to ensure latest build is used
def removePreviousBuild() : 
	if os.path.isdir(BUILDDIRECTORY):
		shutil.rmtree(BUILDDIRECTORY, ignore_errors=False, onerror=None)

def removeInferOutFolder() : 
	if os.path.isdir(BUGDIRECTORY):
		shutil.rmtree(BUGDIRECTORY, ignore_errors=False, onerror=None)	

# reads the bug report, prepares it so it can be exported to csv file
def readBugReport(appName, commitIndex):
	timestamp = str(time.time())
	os.chdir(BUGDIRECTORY)
	currDir = os.getcwd()
	if os.path.isfile(BUGFILE):
		bugreport = open(BUGFILE, "r")
		bugsToCSVArray = []
		bugreportText = bugreport.read()

		# splits bugs.txt so that only the bugs are in the array
		splitReport = bugreportText.split('\n\n')
		splitReport = splitReport[1:-2]

		# index for unique id
		bugIndex = 1

		# separates the bug into different parts
		for bug in splitReport:
			bugsArray = bug.split('\n')
			bugBundle = bugsArray[0].split(" error: ")
			bugPath = bugBundle[0].split(":")

			# Unique ID
			uniqueID = timestamp + "___" + str(bugIndex)

			# Bug File path
			filePath = bugPath[0]
			
			# Bug line number
			lineNumber = bugPath[1]
			
			# Bug type
			bugType = bugBundle[1]
			
			# Bug description
			bugDescription = bugsArray[1]

			newBug = classes.Bug(uniqueID, bugType, filePath, lineNumber, bugDescription)
			bugsToCSVArray.append(newBug)

			#bugsToCSVArray.append([uniqueID, bugType, filePath, lineNumber, bugDescription])


			bugIndex+=1
		
		
		writeBugsToCSV(bugsToCSVArray, currDir, appName, commitIndex)
		print ("+ Analysis complete for " + appName)

	else:
		print("- Analysis failed for " + appName)
	###os.chdir("..")

# writes the bugs to the csv file

def writeBugsToCSV(bugs_array, currentDirectory, appName, commitIndex):
	#os.chdir(BUGFILEDIR)
	os.chdir("..")
	cwd = os.getcwd()
	print(cwd)
	csvFileString = cwd.split('/')[-1] + '_' + commitIndex + ".csv"

	with open(csvFileString, 'a', newline='') as csvfile:
		fieldnames = ['ID', 'BUG_TYPE', 'FILE_PATH', 'LINE_NUMBER', 'BUG_DESCRIPTION']
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
		for bug in bugs_array:
			bug.writeBugs(writer)

	removeInferOutFolder()
	#####os.chdir(currentDirectory)

def findProjectName():
	for file in os.listdir('.'):
		if file.endswith('.xcodeproj'):
			return str(file[0:-10])
	return "false"

if __name__ == '__main__':
    main()


