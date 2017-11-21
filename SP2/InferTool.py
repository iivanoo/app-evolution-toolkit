"""
Will run the Infer analysis. Must pass project folder name as argument,
for now. 
Assumes Gradle build. SDK folder must be defined in local.properties in 
the app folder. SDK and Build tools versions must match the app.
"""

import os, sys, subprocess, shutil, csv

# Constants
LOCALPROPERTIES = "local.properties"
SDKPATH = "sdk.dir=/Users/chris/Library/Android/sdk"
BUGDIRECTORY = "infer-out/"
BUGFILE = "bugs.txt"
BUILDDIRECTORY = "build"


def main():
	appDir = sys.argv[1]
	inferAnalysis(appDir)

# Runs the infer analysis via terminal
def inferAnalysis(appDir):
	os.chdir(appDir)
	removePreviousBuild()

	if appDir[0:3] == "IOS":
		inferAnalysisIOS(appDir)
		
	elif appDir[0:3] == "And":
		inferAnalysisAndroid(appDir)
		

# Infer analysis for android apps
def inferAnalysisAndroid(appDir):
	writeLocalProperties()
	subprocess.call('./gradlew clean', shell=True)
	subprocess.call('infer run -- ./gradlew build', shell=True)
	readBugReport()

# Infer analysis for iOS apps
def inferAnalysisIOS(appDir):
	appName = appDir[4:]
	callString = 'infer run --no-xcpretty -- xcodebuild -target ' + appName + ' -configuration Debug -sdk iphonesimulator'
	test = 'infer run --no-xcpretty -- xcodebuild  -workspace Telegram.xcworkspace -scheme Telegram'
	subprocess.call(callString, shell=True)
	readBugReport()

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

# reads the bug report, prepares it so it can be exported to csv file
def readBugReport():
	os.chdir(BUGDIRECTORY)
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

			# Bug File path
			filePath = bugPath[0]
			
			# Bug line number
			lineNumber = bugPath[1]
			
			# Bug type
			bugType = bugBundle[1]
			
			# Bug description
			bugDescription = bugsArray[1]

			bugsToCSVArray.append([str(bugIndex), bugType, filePath, lineNumber, bugDescription])


			bugIndex+=1
		writeBugsToCSV(bugsToCSVArray)


# writes the bugs to the csv file
def writeBugsToCSV(bugs_array):
	with open('app_bugs.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
		for bug in bugs_array:
			writer.writerow(["ID: " + bug[0]] + ["BUG_TYPE: " + bug[1]] + ["FILE_PATH: " + bug[2]] + ["LINE_NUMBER: " + bug[3]] + ["BUG_DESCRIPTION: " + bug[4]])

if __name__ == '__main__':
    main()

