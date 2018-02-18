'''
This file will iterate through repositories from GitHub.

Made by:
Bob van den Berg
Vrije Universiteit Amsterdam
'''


import os
import csv
import git
from git import Repo
from pathlib import Path
from shutil import copy
import sys
import glob
#import InferTool


# Download GitHub repositories from a csv row:
def read_csv_and_clone_github_repositories():
    with open('csv/example_github_repos.csv', "rt", encoding="utf8") as csv_file:
        # Csv file rows are cut into pieces using ';'. Change if needed.
        csv_file_data = csv.reader(csv_file, delimiter=";")
        url = []
        path = []
        for rows in csv_file_data:
            # In example_github_repos.csv file the repositories are stored in the 0 position in a row. Change if needed.
            repository = rows[0]
            # Put urls and paths in lists.
            # Append with the repository extension and set the repository path in the repo_subfolder.
            url.append('git://github.com/' + repository + '.git')
            repository_path = 'repo_subfolder/' + repository
            path.append(repository_path)
    clone_repositories(url, path)


def clone_repositories(url, path):
    # Skip first row (header) and clone the repositories. (Max 100 per run allowed by GitHub)
    for i in range(2, 3):
        Repo.clone_from(url[i], path[i])


fieldnames = [
    'ID',
    'REPO_ID',
    'FILE_PATH',
    'LINE_NUMBER',
    'BUG_DESCRIPTION',
    'LHDIFF_LINE_TRACING',
    'START_COMMIT_ID',
    'START_COMMIT_MSG',
    'START_COMMIT_TIMESTAMP'
]


def bugs_csv_location():
    cwd = os.getcwd()
    DATA_FOLDER = Path(cwd + "/csv")
    return DATA_FOLDER / "bugs.csv"


def write_csv_header_for_bugs_csv():
    # Write bugs.csv
    file_to_open = bugs_csv_location()
    with open(file_to_open, 'w') as csvfile:
        fieldnames = [
            'ID',
            'REPO_ID',
            'FILE_PATH',
            'LINE_NUMBER',
            'BUG_DESCRIPTION',
            'LHDIFF_LINE_TRACING',
            'START_COMMIT_ID',
            'START_COMMIT_MSG',
            'START_COMMIT_TIMESTAMP'
        ]
        writer = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
        writer.writeheader()


def write_bugs(bug_id, repository):
    file_to_open = bugs_csv_location()
    with open(file_to_open, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
        # FOR FUTURE NEED, we use InferTool.readBugReport now.
        # Write the data.
        # writer.writerow({
        #     'ID': bug_id,
        #      'REPO_ID': repository,
        #      'FILE_PATH': 'test',
        #      'LINE_NUMBER': 'test',
        #      'BUG_DESCRIPTION': 'test',
        #      'LHDIFF_LINE_TRACING': 'test',
        #      'START_COMMIT_ID': 'test',
        #      'START_COMMIT_MSG': 'test',
        #      'START_COMMIT_TIMESTAMP': 'test'
        #      })


# def write_lhdiff_input():
#     with open('csv/lhdiff_input.csv', 'w') as csvfile:
#         fieldnames = ['ID', 'REPO_ID', '']


def mine_repositories():
    rootdir = 'repo_subfolder'
    bug_id = 1
    write_csv_header_for_bugs_csv()
    for subdir, dirs, files in os.walk(rootdir):    # We do a walk in order to get the repository name.
        if subdir.count(os.sep) <= 1 and subdir.count(os.sep) > 0:  # If there are subdirectories...
            #print(subdir)
            repository_path = get_repository_path(subdir, dirs)
            a_repo = git.Repo(repository_path, odbt=git.GitCmdObjectDB)
            g = git.Git(repository_path)
            # loginfo = g.log()
            os.chdir(repository_path)
            commit_checkout_iterator(bug_id, g, a_repo, repository_path, subdir)   # Iterate each commit of a repository.


def get_repository_path(subdir, dirs):
    repository_path = str(subdir) + '\\' + str(dirs[0])  # Here we have the git folder string equal to repository.
    return repository_path


def get_repository_name(repository_path):
    repository_name = repository_path.split('repo_subfolder\\')
    return str(repository_name[-1])


def get_commit_csv_name(repository_path, subdir, commit_index):
    repository_name = repository_path.split(subdir)
    return str(repository_name[-1]) + '_' + str(commit_index) + '.csv'


def read_repository_csv_location(repository_path, subdir, commit_index):
    DATA_PATH = Path(os.getcwd())
    print(DATA_PATH)
    path = str(DATA_PATH) + str(get_commit_csv_name(repository_path, subdir, commit_index))
    print(path)
    return path


def read_commit_csv(repository_path, subdir, commit_index):
    # The csv to be read from is example: TedHoryczun/One-Rep-Max-Calculator/One-Rep-Max-Calculator_1.csv
    file_to_open = read_repository_csv_location(repository_path, subdir, commit_index)
    bug_list = []
    with open(file_to_open, 'r') as repository_commit_csvfile:
        for row in repository_commit_csvfile:
            row = row.strip('\n')   # Maybe not very neat.
            bug_list.append(row)
        return bug_list


def bug_list_splitter(bug_list):
    bug_id = []
    bug_type = []
    file_path = []
    line_number = []
    bug_description = []
    for data in bug_list[1:]:
        data = data.split(',')
        bug_id.append(data[0])
        bug_type.append(data[1])
        file_path.append(data[2])
        line_number.append(data[3])
        bug_description.append(data[4])
    return bug_id, bug_type, file_path, line_number, bug_description


def copy_to_old_folder(relevant_files):
    lhdiff_old_path = Path("../../../LHDiff/old_files")     # This goes up to SP1 (SP1/repo_subfolder/user/repo)
    #if not os.path.exists(lhdiff_old_path):
    #    os.makedirs(lhdiff_old_path)
    #else:
    #    print('already there')
    if isinstance(relevant_files, list):
        for file_path in relevant_files:    # If one file, it does a for-loop over a string. Therefore if-statement.
            src = Path(file_path)
            copy(src, lhdiff_old_path)
    else:
        src = Path(relevant_files)
        copy(src, lhdiff_old_path)


def commit_checkout_iterator(bug_id, g, a_repo, repository_path, dirs):
    commit_index = 1
    # # FOR LOOP HERE:
    # for commit in list(a_repo.iter_commits()):  # NOTE: repo subfolder HAS to be empty. Else only last commit will be read.
        # g.checkout(commit)

        # # RUN INFER AND CREATE CSV
        # InferTool.inferAnalysis("Android")

        # # GET CSV PATH AND READ CSV
    get_commit_csv_name(repository_path, dirs, commit_index)
    bug_list = read_commit_csv(repository_path, dirs, commit_index)

    bug_list_splitted = bug_list_splitter(bug_list)
    print(bug_list_splitted)
        # # READ FROM bug_list FILE_PATH

        # # COPY RELEVANT FILES IN OLD-FOLDER
    relevant_files = bug_list_splitted[2][0]
    print(relevant_files)
    copy_to_old_folder(relevant_files)
        # # IF NEW FOLDER IS FILLED OR DIFFERENT RUN LHDIFF

        # # PUT DATA IN bugs.csv, CLEAR OLD_FOLDER AND PUT NEW_FOLDER CONTENTS IN OLD_FOLDER, CLEAR NEW_FOLDER
        # write_bugs(bug_id, repository, file_path, line_number, bug_description, lhdiff_line_tracing, start_commit_id, start_commit_msg, start_commit_timestamp)
    #print(bug_list_splitted)

        # g.checkout(commit)
        # read_commit_csv(repository)
        # csv.reader(repository + '/csv_for_app_evolution_toolkit_folder')
        # write_bugs(bug_id,repository)
        # print(commit)
        # str(dirs[0])
        # InferTool.inferAnalysis(str(dirs[0]), str(commit_index))
        # commit_index += 1
        # subprocess.call("C:/Users/Bob/PycharmProjects/app-evolution-toolkit/SP1/LHDiff/testscript.sh", shell=True)
        # BUG TYPE
        # BUG DESCRIPTION
        # REMOVE write_bugs(bug_id, repository)
        # if bug_has_been_found():
        #     bug_id += 1
        # else:
        #     continue

        # subprocess.call(['java', '-jar', 'C:/Users/Bob/PycharmProjects/app-evolution-toolkit/SP1/LHDiff/lhdiff.jar'])


# Example 1

# Path
# C:\Users\Bob\PycharmProjects\app-evolution-toolkit\SP1\repo_subfolder\TedHoryczun\One-Rep-Max-Calculator\app\src\main\java\com\repmax\devlanding\onerepmaxcalculator\calculator\OneRepMaxTemplate.java
# Relative Path
# SP1/repo_subfolder/TedHoryczun/One-Rep-Max-Calculator/app/src/main/java/com/repmax/devlanding/onerepmaxcalculator/calculator/OneRepMaxTemplate.java

# Example file 2
# Path
# C:\Users\Bob\PycharmProjects\app-evolution-toolkit\SP1\repo_subfolder\TedHoryczun\One-Rep-Max-Calculator\app\src\main\java\com\repmax\devlanding\onerepmaxcalculator\calculator\PercentRepMax.java
# Relative Path
# SP1/repo_subfolder/TedHoryczun/One-Rep-Max-Calculator/app/src/main/java/com/repmax/devlanding/onerepmaxcalculator/calculator/PercentRepMax.java

# read_csv_and_clone_github_repositories()             # To read a csv with a list of repositories to clone and then iterate through. (Remove first #) repo_subfolder HAS to be empty.
# write_csv_header_for_bugs_csv()
# search_files()         # For finding all infer-compatible files recursively in the repo_subfolder.
mine_repositories()     # Mining repositories



'''
#APPENDIX (Don't need this code anymore)
extensions = [
            'java',
            'c',
            'cc',
            'cpp',
            'm',
            'xml'
            ]


for extension in extensions:
    #glob repositories
    
def search_files():
    for i in extensions:
        IterateThroughFiles.find_infer_files('repo_subfolder', i) # For finding all infer-compatible files recursively in the repo_subfolder.


import subprocess
sys.path.insert(0, '../SP2')



class IterateThroughFiles:
    # Thanks to: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    # Find file extensions (java/c/cc/cpp/m) that can be analysed by Infer.
    def __init__(self):
        self.files = []

    # Find Java, C, CC, CPP and M files
    def find_infer_files(self, extensions):
        file_list = []
        pathlist = Path('repo_subfolder/').glob('**/*.' + extensions)
        for path in pathlist:
            print(path)
            # because path is object not string
            path_in_str = str(path)
            file_list.append(path_in_str)
        print(file_list)


#    def append_infer_files_list(self, path_in_str):
#        with open('csv/infer_files_list', "wb", encoding="utf8") as infer_files_list:
#            infer_files_list.append(path_in_str)
'''

'''
write_back = input("Would you like to clone all repositories in this csv?")
if write_back == y:
    clone_repositories(url, path)
else:
    print("Quitting after saving url and path")
'''

'''
repository: GitHub repository in the form <username>/<repository_id>
Example: “duckduckgo/Android”
DONE
repository_subfolder: path within the repository to focus on (and recursively on all its subfolders). For example, in the DuckDuckGo GitHub repository, we want to focus on the “app/src/main” folder because the source code of the Android app is there, all the other folders contain other resources that we do not care about

keep_temp_data: boolean, if true, all the intermediate files and data produced by the static analyzer will be kept in a dedicated folder

output_path: the path in the file system where the output bugs.csv file will be created

output_folder_path: the folder in the file system where to put all the other generated files which may be useful

analyzer: the path in the file system where to find the main Python script for running the static analyzer
(Infer in the case of SP2, but it can be any)

'''