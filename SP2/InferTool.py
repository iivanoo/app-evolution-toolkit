"""
Will run the Infer analysis. Must pass project folder name as argument,
for now. 
Assumes Gradle build. SDK folder must be defined in local.properties in 
the app folder. SDK and Build tools versions must match the app.
"""

import os, sys, subprocess, shutil

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

def readBugReport():
	os.chdir(BUGDIRECTORY)
	if os.path.isfile(BUGFILE):
		bugreport = open(BUGFILE, "r")
		bugreportText = bugreport.read()
		splitReport = bugreportText.split('\n\n')
		print(splitReport[1])

if __name__ == '__main__':
    main()

