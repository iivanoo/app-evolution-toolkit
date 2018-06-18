"""
Will run the Infer analysis. Must pass project folder name as argument,
for now. 
Assumes Gradle build. SDK folder must be defined in local.properties in 
the app folder. SDK and Build tools versions must match the app.
"""

import os, sys, subprocess, shutil, csv, time, glob, re
from pathlib import Path
import classes

# from classes import Bug

# Constants
LOCALPROPERTIES = "local.properties"

# BOB SDKPATH
# SDKPATH = "sdk.dir=/Users/sylviastolwijk/Library/Android/sdk"
# BUGFILEDIR = "/Users/sylviastolwijk/Downloads/app-evolution-toolkit/SP2/BUGFiles/"

# CHRIS SDKPATH
SDKPATH = "sdk.dir=/Users/chris/app-evolution-toolkit/SP2/sdk"
BUGFILEDIR = "/Users/chris/Downloads/app-evolution-toolkit/SP2/BUGFiles/"
BUGDIRECTORY = "infer-out/"
BUGFILE = "bugs.txt"
BUILDDIRECTORY = "build"

#Bug attributes
BUG_TYPE = "bugType"
UNIQUE_ID = "uniqueID"
FILE_PATH = "filePath"
LINE_NUMBER = "lineNumber"
BUG_DESCRIPTION = "bugDescription"
RESOURCE_LEAK = "RESOURCE_LEAK"

#Global files
parent_directory = ""
home_directory = ""


def main():
    loopedAnalysis()


# Analysis mode that will loop between 2 folders, IOS and Android
def loopedAnalysis():
    start = time.time()
    os.chdir("Android")
    for dirs in os.listdir("."):
        if os.path.isdir(dirs):
            os.chdir(dirs)
            infer_success_android = inferAnalysisAndroid(dirs, "1")
            os.chdir("..")

    os.chdir("..")
    os.chdir("IOS")
    for dirs in os.listdir("."):
        if os.path.isdir(dirs):
            os.chdir(dirs)
            infer_success_ios = inferAnalysisIOS("1")
            os.chdir("..")
    os.chdir("..")

    end = time.time()
    print("Time elapsed: " + str(end - start) + " seconds")


# Runs the infer analysis via terminal
def inferAnalysis(appDir, commitIndex):
    start = time.time()
    removePreviousBuild()

    if os.path.exists("gradlew"):
        infer_success = inferAnalysisAndroid(appDir, commitIndex)

    else:  # assumes if not android, it is ios, in ios analysis a check will be made to see if it is really an ios app
        infer_success = inferAnalysisIOS(commitIndex)

    end = time.time()
    print("Time elapsed: " + str(end - start) + " seconds")


# Infer analysis for android apps
def inferAnalysisAndroid(appDir, commitIndex):
    global parent_directory, home_directory
    home_directory = os.getcwd()
    parent_directory = Path(os.path.abspath(os.pardir))
    print(parent_directory)
    root_folder = find_root_folder("Android")
    removePreviousBuild()

    if root_folder == "empty":
        print("- No gradlew file found, no working app")
        return False
    else:
        os.chdir(root_folder)
        writeLocalProperties()
        FNULL = open(os.devnull, 'w')
        print("Initializing analysis of " + appDir + " ...")
        subprocess.call('find ~/.gradle -type f -name "*.lock" | while read f; do rm $f; done', shell=True)
        subprocess.call('chmod +x gradlew', shell=True)
        subprocess.call('./gradlew clean', shell=True)#, stdout=FNULL, stderr=subprocess.STDOUT)
        subprocess.call('infer run -- ./gradlew build -x lint', shell=True)#, stdout=FNULL, stderr=subprocess.STDOUT)

    os.chdir(home_directory)
    infer_success = readBugReport(appDir, commitIndex)
    return infer_success


# Infer analysis for iOS apps
def inferAnalysisIOS(commitIndex):
    global parent_directory, home_directory
    home_directory = os.getcwd()
    parent_directory = Path(os.path.abspath(os.pardir))
    root_folder = find_root_folder("IOS")
    if root_folder == "empty":
        print("- No xcodeproj found, no working app")
        return False
    else:
        os.chdir(root_folder)

        appName = findProjectName()
        rewrittenAppName = rewriteSpacesInProjectName(appName)
        if appName != "false":
            
            # OPTIONS: Add options to end of cleanString and callString
            # -arch i386 to change used architecture (can also be armv7, armv7s, etc)
            # IPHONEOS_DEPLOYMENT_TARGET=8.0 (to change deployment target, which helps for older apps)

            cleanString = 'xcodebuild -target ' + rewrittenAppName + ' -configuration Debug -sdk iphonesimulator clean IPHONEOS_DEPLOYMENT_TARGET=8.0'
            callString = 'infer run -- xcodebuild -target ' + rewrittenAppName + ' -configuration Debug -sdk iphonesimulator IPHONEOS_DEPLOYMENT_TARGET=8.0'
            
            FNULL = open(os.devnull, 'w')
            print("Initializing analysis of " + appName + " ...")
            subprocess.call(cleanString, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
            subprocess.call(callString, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

        else: 
            print("- No working app found")
            return False
    infer_success = readBugReport(appName, commitIndex)
    os.chdir(home_directory)
    return infer_success


# Rewrites local.properties in order to make android builds work
def writeLocalProperties():
    if os.path.isfile(LOCALPROPERTIES):
        os.remove(LOCALPROPERTIES)

    propfile = open(LOCALPROPERTIES, 'w')
    propfile.write(SDKPATH)
    propfile.close()


# removes older build of iOS app, to ensure latest build is used
def removePreviousBuild():
    if os.path.isdir(BUILDDIRECTORY):
        shutil.rmtree(BUILDDIRECTORY, ignore_errors=False, onerror=None)


def removeInferOutFolder():
    if os.path.isdir(BUGDIRECTORY):
        shutil.rmtree(BUGDIRECTORY, ignore_errors=False, onerror=None)


# reads the bug report, prepares it so it can be exported to csv file
def readBugReport(appName, commitIndex):
    timestamp = str(time.time())
    bugsToCSVArray = []
    currDir = os.getcwd()
    if os.path.isdir(BUGDIRECTORY):
        os.chdir(BUGDIRECTORY)
        
        
        if os.path.isfile(BUGFILE):
            bugreport = open(BUGFILE, "r")
            
            bugreportText = bugreport.read()

            # splits bugs.txt so that only the bugs are in the array
            splitReport = bugreportText.split('\n\n')
            splitReport = splitReport[1:-2]

            # index for unique id
            bugIndex = 1

            # separates the bug into different parts
            for bug in splitReport:
                bug_info = parse_bug(bug, bugIndex, timestamp)
                if len(bug_info) > 0:
                    if bug_info[BUG_TYPE] == RESOURCE_LEAK:

                        newBug = classes.Bug(bug_info[UNIQUE_ID], bug_info[BUG_TYPE], bug_info[FILE_PATH], bug_info[LINE_NUMBER], bug_info[BUG_DESCRIPTION])
                        bugsToCSVArray.append(newBug)

                        bugIndex += 1
                # else:
                #     print("No bugs found in this commit! \n")

            #writeBugsToCSV(bugsToCSVArray, currDir, appName, commitIndex)
            print("+ Analysis complete for " + appName)
            success = True

        else:
            print("- Analysis failed for " + appName)
            success = False

        os.chdir("..")
        shutil.rmtree(BUGDIRECTORY)
    writeBugsToCSV(bugsToCSVArray, commitIndex)
    return success


# writes the bugs to the csv file
def writeBugsToCSV(bugs_array, commitIndex):
    global parent_directory, home_directory
    # os.chdir(BUGFILEDIR)
    csvFileString = str(parent_directory) + "/" + str(home_directory).split('/')[-1] + '_' + commitIndex + ".csv"
    print(csvFileString)
    with open(csvFileString, 'a', newline='') as csvfile:
        fieldnames = ['ID', 'BUG_TYPE', 'FILE_PATH', 'LINE_NUMBER', 'BUG_DESCRIPTION']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for bug in bugs_array:
            bug.writeBugs(writer)


# copy_to_parent_folder()

# os.chdir(currentDirectory)

def parse_bug(bug, bugIndex, timestamp):

    bugsArray = bug.split('\n')
    bugBundle = bugsArray[0].split(" error: ")
    
    if len(bugBundle) <= 0:
        bugBundle = bugsArray[0].split(" warning: ")

    if len(bugBundle) > 1:
        bug_info = create_bug_info(bugIndex, timestamp, bugBundle, bugsArray)
    else: 
        bug_info = {}
    return bug_info


def create_bug_info(bugIndex, timestamp, bugBundle, bugsArray):
    bug_info = {}
    
    bugPath = bugBundle[0].split(":")

    # Unique ID
    bug_info[UNIQUE_ID] = timestamp + "___" + str(bugIndex)

    # Bug File path
    bug_info[FILE_PATH] = bugPath[0]

    # Bug line number
    bug_info[LINE_NUMBER] = bugPath[1]

    # Bug type
    bug_info[BUG_TYPE] = bugBundle[1]

    # Bug description
    bug_info[BUG_DESCRIPTION] = bugsArray[1]

    return bug_info


def findProjectName():
    for file in os.listdir('.'):
        if file.endswith('.xcodeproj'):
            try:
                output_string = subprocess.check_output('xcodebuild -list', shell=True)
            except subprocess.CalledProcessError:
                return "false"

            first_target = output_string.decode().split("Targets:\n")[1].split("\n")[0].replace('        ', '')
            return first_target
    return "false"


# Rewrites the project name of an iOS app, in a way that it can be used by Infer
def rewriteSpacesInProjectName(appName):
    splitApp = appName.split(" ")
    numberOfWords = len(splitApp)
    if numberOfWords <= 1:
        return appName
    else:
        newString = ""
        for i in range(numberOfWords):
            if i != (numberOfWords - 1):
                newString = newString + splitApp[i] + "\ "
            else:
                newString = newString + splitApp[i] + " "
        return newString


def copy_to_parent_folder():
    root = os.getcwd()
    os.chdir("..")
    os.mkdir(BUGDIRECTORY)
    os.chdir(root)

    for filename in os.listdir(os.path.join(root, BUGDIRECTORY)):
        shutil.move(os.path.join(root, BUGDIRECTORY, filename), os.path.join(os.pardir + "/" + BUGDIRECTORY, filename))


def find_root_folder(mode):
    if mode == "Android":
        fileArray = []
        for filename in glob.iglob('**/gradlew', recursive=True):
            folder = str(filename).split("gradlew")
            fileArray.append(folder[0])

        if len(fileArray) > 0:
            if fileArray[0] != "":
                return fileArray[0]
            else:
                return os.getcwd()
        else:
            return "empty"

    elif mode == "IOS":
        fileArray = []
        for filename in glob.iglob('**/*.xcodeproj', recursive=True):
            fileArray.append(filename)
        if len(fileArray) > 0:
            path = re.split('\w*.xcodeproj', fileArray[0])[0]
            if path != "":
                return path
            else:
                return os.getcwd()
        else:
            return "empty"

if __name__ == '__main__':
    main()
