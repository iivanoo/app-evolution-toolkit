"""
Will run the Infer analysis. Must pass project folder name as argument,
for now. 
Assumes Gradle build. SDK folder must be defined in local.properties in 
the app folder. SDK and Build tools versions must match the app.
"""

import os, sys, subprocess

# Constants
LOCALPROPERTIES = "local.properties"
SDKPATH = "sdk.dir=/Users/chris/Library/Android/sdk"
BUGDIRECTORY = "infer-out/"
BUGFILE = "bugs.txt"

def main():
	appDir = sys.argv[1]
	inferAnalysis(appDir)

# Runs the infer analysis via terminal
def inferAnalysis(appDir):
	os.chdir(appDir)
	writeLocalProperties()
	subprocess.call('./gradlew clean', shell=True)
	subprocess.call('infer run -- ./gradlew build', shell=True)
	readBugReport()

def writeLocalProperties(): 
	if os.path.isfile(LOCALPROPERTIES):
		os.remove(LOCALPROPERTIES)

	propfile = open(LOCALPROPERTIES, 'w')
	propfile.write(SDKPATH)
	propfile.close()

def readBugReport():
	os.chdir(BUGDIRECTORY)
	if os.path.isfile(BUGFILE):
		bugreport = open(BUGFILE, "r")
		bugreportText = bugreport.read()
		splitReport = bugreportText.split('\n\n')
		print(splitReport[1])

if __name__ == '__main__':
    main()

