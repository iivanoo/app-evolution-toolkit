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
import shutil
import subprocess
import sys
import glob
import time
import dateutil.parser
sys.path.insert(0, '../SP2')
import InferTool    # Might give an error outside IDE

LHDIFF_PATH = str(Path('../../../../SP1/LHDiff/lhdiff.jar'))
LHDIFF_OLD_PATH = str(Path("../../../LHDiff/old_files/"))
LHDIFF_NEW_PATH = str(Path("../../../LHDiff/new_files/"))

extensions = [
            '.java',
            '.c',
            '.cc',
            '.cpp',
            '.m',
            '.xml'
            ]


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


def write_bugs(bug_id, repository, file_path, line_number, bug_description, lhdiff_line_tracing, start_commit_id, start_commit_msg, start_commit_timestamp):
    file_to_open = bugs_csv_location()
    with open(file_to_open, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
        # FOR FUTURE NEED, we use InferTool.readBugReport now.
        # Write the data.
        writer.writerow({
            'ID': bug_id,
            'REPO_ID': repository,
            'FILE_PATH': file_path,
            'LINE_NUMBER': line_number,
            'BUG_DESCRIPTION': bug_description,
            'LHDIFF_LINE_TRACING': lhdiff_line_tracing,
            'START_COMMIT_ID': start_commit_id,
            'START_COMMIT_MSG': start_commit_msg,
            'START_COMMIT_TIMESTAMP': start_commit_timestamp
            })


def get_commit_author_date_message_changed_files(git_log_string, git_log_file_changes):
    splitted_git_log = []
    for i in range(0, len(git_log_string), 2):
        commit_author_date = git_log_string[i].splitlines()

        # Commit
        commit_from_git_log = commit_author_date[0].split('commit ')[-1]

        # Author
        if commit_author_date[1][:1] == 'A':            # Had to do this because of a bug when a merge had happened, the log looks different.
            author_from_git_log = commit_author_date[1].split('Author: ')[-1]
        elif commit_author_date[2][:1] == 'A':
            author_from_git_log = commit_author_date[2].split('Author: ')[-1]

        # Date
        if commit_author_date[2][:1] == 'D':            # Had to do this because of a bug when a merge had happened, the log looks different.
            date_from_git_log = commit_author_date[2].split('Date:   ')[-1]
        elif commit_author_date[3][:1] == 'D':
            date_from_git_log = commit_author_date[3].split('Date:   ')[-1]

        dt = dateutil.parser.parse(date_from_git_log)
        unix_date_from_git_log = time.mktime(dt.timetuple())

        # Message
        message_from_commit = git_log_string[i+1].split('    ')[-1]

        # Files (STILL WORKING ON THIS)
        changed_files = get_file_changes_for_commit(git_log_file_changes, i)
        # print(changed_files)
        splitted_git_log.append([commit_from_git_log, author_from_git_log, unix_date_from_git_log, message_from_commit])

    return splitted_git_log


# def get_file_changes_for_commit(git_log_file_changes, i):
#     file_changes = []
#     # print(git_log_file_changes)
#     files_log_per_commit = git_log_file_changes.split('\n\n')     # Still need to add at which commit file was changed.
#     # print(files_log_per_commit, sep="\n")
#     for e in range(0, len(files_log_per_commit)):
#         # print(files_log_per_commit)
#         # print(e)
#         for i in files_log_per_commit[e].splitlines():
#             i = i.split('\t')
#             if any(extension in i[-1][-5:] for extension in extensions):
#                 # This could be optimized since extensions include for example .cfg or .csv
#                 if i[0][:1] == 'M':
#                     file_was = 'modified'
#                 elif i[0][:1] == 'A':
#                     file_was = 'added'
#                 elif i[0][:1] == 'D':
#                     file_was = 'deleted'
#                 elif i[0][:1] == 'R':
#                     file_was = 'renamed'
#             elif i[0][:1] == "'":
#
#                 print(i, file_was)
#                 file_changes.append(i)
#     return file_changes

def get_file_changes_for_commit(git_log_file_changes, i):
    file_changes = []
    commit_counter = 0
    # print(git_log_file_changes)
    files_log_per_commit = git_log_file_changes.split('\n\n')  # Still need to add at which commit file was changed.
    # print(files_log_per_commit, sep="\n")
    for e in range(0, len(files_log_per_commit)):
        # print(files_log_per_commit)
        # print(e)
        # commits = count(i[0][:1] == "'")
        for i in files_log_per_commit[e].splitlines():
            if i.lower().endswith(('.java', '.c', '.cc', '.cpp', '.m', '.xml')):
                # This could be optimized since extensions include for example .cfg or .csv
                print(i)
                if i[0][:1] == 'M':
                    file_was = 'modified'
                elif i[0][:1] == 'A':
                    file_was = 'added'
                elif i[0][:1] == 'D':
                    file_was = 'deleted'
                elif i[0][:1] == 'R':
                    file_was = 'renamed'
                print(file_was)
            elif i[0][:1] == "'":
                commit_counter += 1
                file_was = 'commit'
                print(file_was, i)
                file_changes.append(i)
            # print(i)
    # print(os.getcwd())
                # elif i[0][:1] == "'":
                #     print(i)
                #     # commit.append(i[0])

                # print(sum(range(len(commit))))
                # print(i, file_was)
    return file_changes




        # print(i, file_was)
            # print(i, file_was)
    # for e in range(0, len(files_log_per_commit), 3):
    #     commit = files_log_per_commit[e]
    #
    # for e in range(1, len(files_log_per_commit), 3):
    #     # print(files_log_per_commit)
    #     renamed_files = files_log_per_commit[e].splitlines()
    #     for i in range(0, len(renamed_files), 2):       # To get the commit out
    #
    #         renamed_files_splitted = renamed_files[i].split('\t')
    #         # print(renamed_files_splitted)
    #         if renamed_files_splitted[0][:1] == 'M':
    #             file_was = 'modified'
    #         elif renamed_files_splitted[0][:1] == 'A':
    #             file_was = 'added'
    #         elif renamed_files_splitted[0][:1] == 'D':
    #             file_was = 'deleted'
    #         elif renamed_files_splitted[0][:1] == 'R':
    #             # print(renamed_files_splitted)
    #             file_was = 'renamed'
    #         else:
    #             file_was = 'none'
    #         # print(file_was)

        # if commit_has_changed_files(files_log_per_commit[e]):
        #     changed_file_name = files_log_per_commit[e].replace('}', "{").split('{')[1]
        #     changed_file = changed_file_name.split(' => ')
        #     changed_file_from = changed_file[0]
        #     changed_file_to = changed_file[1]
        #     file_changes.append([changed_file_from, changed_file_to])
    # return file_changes


def get_git_log_data(g):
    git_log_string = str(g.log())
    git_log_file_changes = str(g.log("--name-status", "--format='%H'"))
    git_log_string = git_log_string.split('\n\n')
    commit_author_date_message_changedfiles = get_commit_author_date_message_changed_files(git_log_string, git_log_file_changes)
    return commit_author_date_message_changedfiles


# def commit_has_changed_files(files_log_per_commit):
#     if ' => ' in str(files_log_per_commit):
#         return True
#     else:
#         return False

def mine_repositories():
    rootdir = 'repo_subfolder'
    write_csv_header_for_bugs_csv()
    for subdir, dirs, files in os.walk(rootdir):    # We do a walk in order to get the repository name.
        if subdir.count(os.sep) <= 1 and subdir.count(os.sep) > 0:  # If there are subdirectories...
            repository_path = get_repository_path(subdir, dirs)
            a_repo = git.Repo(repository_path, odbt=git.GitCmdObjectDB)
            g = git.Git(repository_path)
            # print(os.getcwd(), subdir, dirs, files)
            commit_author_date_message_changedfiles = get_git_log_data(g)
            # print(commit_author_date_message_changedfiles)                  # STILL NEED TO WORK THIS OUT

            os.chdir(repository_path)
            # print(a_repo)
            commit_checkout_iterator(g, a_repo, repository_path, subdir)   # Iterate each commit of a repository.


def get_repository_path(subdir, dirs):
    repository_path = str(Path(subdir + '/' + dirs[0]))
    # repository_path = str(subdir) + '\\' + str(dirs[0])  # Here we have the git folder string equal to repository.
    return repository_path


def get_repository_name(repository_path):
    repository_name = repository_path.split('repo_subfolder\\')
    return str(repository_name[-1])


def get_commit_csv_name(repository_path, subdir, commit_index):
    repository_name = repository_path.split(subdir)
    return str(repository_name[-1]) + '_' + str(commit_index) + '.csv'  # For example repo_1.csv -> HelloWorld_1.csv


def read_repository_csv_location(repository_path, subdir, commit_index):
    DATA_PATH = Path(os.getcwd())
    path = str(DATA_PATH) + str(get_commit_csv_name(repository_path, subdir, commit_index))
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


def copy_to_old_folder(relevant_file):
    if not os.path.exists(LHDIFF_OLD_PATH):                 # If this folder doesn't exist: create it.
        os.makedirs(LHDIFF_OLD_PATH)
    src = Path(relevant_file)
    copy(src, LHDIFF_OLD_PATH)


def copy_to_new_folder(relevant_file):
    if not os.path.exists(LHDIFF_NEW_PATH):                 # If this folder doesn't exist: create it.
        os.makedirs(LHDIFF_NEW_PATH)
    src = Path(relevant_file)
    copy(src, LHDIFF_NEW_PATH)


def there_are_files_in_new_files_folder():
    files = glob.glob(LHDIFF_NEW_PATH + '*')
    if len(files) >= 1:
        return True
    else:
        print('no files in new folder')


def clear_old_files_folder():
    files = glob.glob(str(Path(LHDIFF_OLD_PATH + '/*')))
    for file in files:
        os.remove(file)


def clear_new_files_folder():
    files = glob.glob(str(Path(LHDIFF_NEW_PATH + '/*')))
    for file in files:
        os.remove(file)


def copy_new_files_to_old_files_folder():
    files = glob.glob(str(Path(LHDIFF_NEW_PATH + '/*')))
    for file in files:
        copy(file, LHDIFF_OLD_PATH)


def call_lhdiff(relevant_file, relevant_files_loc):
    oldfile = str(Path(LHDIFF_OLD_PATH + '/' + relevant_file))
    newfile = str(Path(LHDIFF_NEW_PATH + '/' + relevant_file))      # NEEDS TO BE BUGTESTED / CHANGED FOR MISSING BUG OR FILE.
    # BUG: Both files have to be named exactly the same. git log should be checked for name-changes.
    lhdiff_output = subprocess.check_output(['java', '-jar', LHDIFF_PATH, oldfile, newfile])
    data = lhdiff_output.split()
    for old_and_new_loc in data[9:]:  # From 9 to remove the introduction words from LHDiff.
        # print(old_and_new_loc)
        old_and_new_loc = str(old_and_new_loc).strip('b').strip("'").split(',')  # To clean the returned LHDiff output.
        # print(old_and_new_loc)
        old_file_loc = int(old_and_new_loc[0])
        new_file_loc = int(old_and_new_loc[1])
        # if old_file_loc == relevant_files_loc:  # This needs to be changed into new_file_loc or relevant_files_loc?
        #     print('%s : line of code (input: %s) %s is the same as %s' % (relevant_file, relevant_files_loc, old_file_loc, new_file_loc))
        # else:
        #     print('%s : line of code (input: %s) %s has become %s' % (relevant_file, relevant_files_loc, old_file_loc, new_file_loc))
            # write back to bugs.csv or return values?. # NEEDS TO BE BUGTESTED

def call_lhdiff_for_renamed_file(relevant_file, renamed_file, relevant_file_loc ):
    print('test')



def commit_checkout_iterator(g, a_repo, repository_path, dirs):
    commit_index = 1
    # FOR LOOP HERE:
    for commit in list(a_repo.iter_commits()):  # NOTE: repo subfolder HAS to be empty. Else only last commit will be read.
        # g.checkout(commit)    # Checkout the commit of the version of the repo that we analyse.
        # print(commit)

        # RUN INFER AND CREATE CSV
        # InferTool.inferAnalysis("Android", str(commit_index))

        # GET CSV PATH AND READ CSV
        get_commit_csv_name(repository_path, dirs, commit_index)
        bug_list = read_commit_csv(repository_path, dirs, commit_index)
        # print(bug_list)
        bug_list_splitted = bug_list_splitter(bug_list)

        # READ FROM bug_list FILE_PATH

        # COPY RELEVANT FILES IN OLD-FOLDER
        relevant_files_list = []
        # print(relevant_files_list)
        for i in range(len(bug_list_splitted[0])):
            # For i in all bugs found in the csv
            # Might be able to remove newlines and headers from csv with a split or strip.
            # I want to have a list with paths, loc and files. Possible bug when there are more or less bugs in old/new
            # print(bug_list_splitted[2])
            file_path = bug_list_splitted[2][i]
            file_name = bug_list_splitted[2][i].split('/')[-1]
            line_of_code = bug_list_splitted[3][i]
            relevant_files_list.append([file_path, file_name, line_of_code])

        for i in range(len(relevant_files_list)):
            file_path = relevant_files_list[i][0]
            file_name = relevant_files_list[i][1]
            line_of_code = relevant_files_list[i][2]
            # print('Scanning file: %s with bug in loc %s' % (file_name, line_of_code))
            if commit_index == 1:
                # print(file_path)
                copy_to_old_folder(file_path)         # possible bug: Need to check if this works with the repo_subfolder walk.
            else:
                print(relevant_files_list[i][0])    # HERE PUT IF FILE IS CHANGED
                # if file_was_renamed():
                #     relevant_file = relevant_files_list[i - 1][0]) # DIT KLOPT NIET -> Moet uit git log de renamed file halen
                #     renamed_file = relevant_files_list[i][0]
                #     call_lhdiff_for_renamed_file(relevant_file, renamed_file, line_of_code)
                # elif file_was_removed():
                #
                # # AND DO SOMETHING FOR BUGS.CSV?
                # elif file_was_added():
                #     copy_to_new_folder(file_path)

                # # AND DO SOMETHING FOR BUGS.CSV
                # elif file_was_modified:
                #     copy_to_new_folder(relevant_files_list[i][0])
                #     call_lhdiff(file_name, line_of_code)
                print(line_of_code)
                copy_to_new_folder(relevant_files_list[i][0])
                # IF NEW FOLDER IS FILLED OR DIFFERENT RUN LHDIFF
                # if there_are_files_in_new_files_folder():
                #     call_lhdiff(file_name, line_of_code)


        # PUT DATA IN bugs.csv
        # write_bugs(bug_id, repository, file_path, line_number, bug_description, lhdiff_line_tracing, start_commit_id, start_commit_msg, start_commit_timestamp)
        # CLEAR OLD_FOLDER
        if commit_index >= 2:
            clear_old_files_folder()
        # PUT NEW_FOLDER CONTENTS IN OLD_FOLDER
        copy_new_files_to_old_files_folder()
        # CLEAR NEW_FOLDER
        clear_new_files_folder()
        # RESTART ON NEXT COMMIT IN FOR-LOOP
        commit_index += 1

# read_csv_and_clone_github_repositories()             # To read a csv with a list of repositories to clone and then iterate through. (Remove first #) repo_subfolder HAS to be empty.
# write_csv_header_for_bugs_csv()
# search_files()         # For finding all infer-compatible files recursively in the repo_subfolder.
mine_repositories()     # Mining repositories



'''
#APPENDIX (Don't need this code anymore)



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

'''
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

'''