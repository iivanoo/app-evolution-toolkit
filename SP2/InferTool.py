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

def main():
	appDir = sys.argv[1]
	inferAnalysis(appDir)

def inferAnalysis(appDir):
	os.chdir(appDir)
	writeLocalProperties()
	subprocess.call('./gradlew clean', shell=True)
	subprocess.call('infer run -- ./gradlew build', shell=True)

def writeLocalProperties(): 
	if os.path.isfile(LOCALPROPERTIES):
		os.remove(LOCALPROPERTIES)

	propfile = open(LOCALPROPERTIES, 'w')
	propfile.write(SDKPATH)
	propfile.close()


if __name__ == '__main__':
    main()

