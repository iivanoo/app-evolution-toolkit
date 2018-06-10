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
import pandas as pd

sys.path.insert(0, '../SP2')
import InferTool    # Might give an error outside IDE

BUGS_CSV_LOCATION = str(Path(os.path.abspath("csv/bugs.csv")))
LHDIFF_PATH = str(Path(os.path.abspath('LHDiff/lhdiff.jar')))
LHDIFF_OLD_PATH = str(Path(os.path.abspath("LHDiff/old_files/")))
LHDIFF_NEW_PATH = str(Path(os.path.abspath("LHDiff/new_files/")))

BUG_IS_ACTIVE = "active"
BUG_IS_SOLVED = "solved"
BUG_HAS_NOT_CHANGED = "Bug has not been changed"

bug_counter = 0

bug_id = 1
solved_bug_archive = []
bug_tracking_dict = {}

files_that_have_been_renamed = {}
deleted_files_that_have_been_renamed = {}
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
    'BUG_ID',
    'REPO_ID',
    'BUG_TYPE',
    'FILE_PATH',
    'LINE_NUMBER',
    'BUG_DESCRIPTION',
    'LHDIFF_LINE_TRACING',
    'START_COMMIT_ID',
    'START_COMMIT_MSG',
    'START_COMMIT_TIMESTAMP',
    'END_COMMIT_MSG',
    'END_COMMIT_TIMESTAMP',
    'END_COMMIT_ID',
    'REMOVAL_COMMIT_ID',
    'REMOVAL_COMMIT_MSG',
    'REMOVAL_COMMIT_TIMESTAMP'
]


def bugs_csv_location():
    cwd = os.getcwd()
    DATA_FOLDER = Path(cwd + "/csv")
    print(DATA_FOLDER)
    return DATA_FOLDER / "bugs.csv"
    # return Path('C:/Users/BovandenBerg/Documents/Vrije Universiteit/Bachelor Project IMM/app-evolution-toolkit/SP1/csv/bugs.csv')



def write_csv_header_for_bugs_csv():
    # Write bugs.csv
    file_to_open = BUGS_CSV_LOCATION
    with open(file_to_open, 'w') as csvfile:
        fieldnames = [
            'BUG_ID',
            'REPO_ID',
            'BUG_TYPE',
            'FILE_PATH',
            'LINE_NUMBER',
            'BUG_DESCRIPTION',
            'LHDIFF_LINE_TRACING',
            'START_COMMIT_ID',
            'START_COMMIT_MSG',
            'START_COMMIT_TIMESTAMP',
            'END_COMMIT_MSG',
            'END_COMMIT_TIMESTAMP',
            'END_COMMIT_ID',
            'REMOVAL_COMMIT_ID',
            'REMOVAL_COMMIT_MSG',
            'REMOVAL_COMMIT_TIMESTAMP'
        ]
        writer = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
        writer.writeheader()


def read_bugs():
    file_to_open = BUGS_CSV_LOCATION
    df = pd.read_csv(file_to_open)
    saved_column = df['REPO_ID']  # you can also use df['column_name']
    # print(saved_column)
    # with open(file_to_open, 'r') as csvfile:
    #     for row in reader:
    #         content = list(row[i] for i in included_cols)
    #     print(content)

def read_bugs_for_lhdiff(relevant_file, old_file_loc):
    # print(relevant_file, old_file_loc)
    with open(BUGS_CSV_LOCATION, 'r') as csvfile:
        reader = csv.reader(csvfile, lineterminator='\n')
        for row in reader:  # MUST BE IN REVERSE
            if relevant_file == str(split_file_from_full_path(row[3])) and str(old_file_loc) == str(row[4]):
                # print('same bug')
                previous_bug_id = row[0]
                return True, previous_bug_id

        return False, "NULL"


def write_bugs(bug_id, repository, bug_type, file_path, line_number, bug_description, lhdiff_line_tracing, start_commit_id, start_commit_msg, start_commit_timestamp, end_commit_msg, end_commit_timestamp, end_commit_id, removal_commit_id, removal_commit_msg, removal_commit_timestamp):
    file_to_open = BUGS_CSV_LOCATION
    with open(file_to_open, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
        # FOR FUTURE NEED, we use InferTool.readBugReport now.
        # Write the data.
        writer.writerow({
            'BUG_ID': bug_id,
            'REPO_ID': repository,
            'BUG_TYPE': bug_type,
            'FILE_PATH': file_path,
            'LINE_NUMBER': line_number,
            'BUG_DESCRIPTION': bug_description,
            'LHDIFF_LINE_TRACING': lhdiff_line_tracing,
            'START_COMMIT_ID': start_commit_id,
            'START_COMMIT_MSG': start_commit_msg,
            'START_COMMIT_TIMESTAMP': start_commit_timestamp,
            'END_COMMIT_MSG': end_commit_msg,
            'END_COMMIT_TIMESTAMP': end_commit_timestamp,
            'END_COMMIT_ID': end_commit_id,
            'REMOVAL_COMMIT_ID': removal_commit_id,
            'REMOVAL_COMMIT_MSG': removal_commit_msg,
            'REMOVAL_COMMIT_TIMESTAMP': removal_commit_timestamp
            })

def split_file_from_full_path(path):
    split_path = path.split('/')
    return split_path[-1]

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

        # Files
        splitted_git_log.append([commit_from_git_log, author_from_git_log, unix_date_from_git_log, message_from_commit])
    changed_files = get_file_changes_for_commit(git_log_file_changes, i)

    for i in range(len(changed_files)):
        for e in range(len(changed_files[i])):
            for o in range(len(splitted_git_log)):                      # I work through the matrices to merge the git log and --name-status logfiles.
                if splitted_git_log[o][0] == changed_files[i][e][0]:    # If the commmit equals the other commit
                    # print(splitted_git_log[o], changed_files[i][e][1:][0])
                    splitted_git_log[o].append(changed_files[i][e][1:][0])
    splitted_git_log.reverse()  # Do this to reverse the list: last commit first -> initial commit first.
    return splitted_git_log


def get_file_changes_for_commit(git_log_file_changes, i):
    files_deleted = []
    files_added = []
    files_renamed = []
    files_modified = []
    files_log_per_commit = git_log_file_changes.split('\n\n')
    for e in range(0, len(files_log_per_commit)):
        for i in files_log_per_commit[e].splitlines():
            i = i.split('\t')
            if i[-1].lower().endswith(('.java', '.c', '.cc', '.cpp', '.m', '.xml')):
                # Returns if those interesting infer files are modified/added/deleted/renamed.
                # print(i)
                if i[0][:1] == 'M':
                    files_modified.append([commit, i])
                elif i[0][:1] == 'A':
                    files_added.append([commit, i])
                elif i[0][:1] == 'D':
                    files_deleted.append([commit, i])
                elif i[0][:1] == 'R':
                    # i[0] = 'R'
                    files_renamed.append([commit, i])

            elif i[0][:1] == "'":
                commit = i[0].split("'")[1]
    return [files_modified, files_added, files_deleted, files_renamed]


def get_git_log_data(g):
    git_log_string = str(g.log())
    git_log_file_changes = str(g.log("--name-status", "--format='%H'"))
    # print(git_log_file_changes)
    git_log_string = git_log_string.split('\n\n')
    commit_author_date_message_changedfiles = get_commit_author_date_message_changed_files(git_log_string, git_log_file_changes)
    return commit_author_date_message_changedfiles


def mine_repositories():
    sub_problem_dir = str(os.path.abspath('app-evolution-toolkit/SP1'))
    rootdir = str(Path('repo_subfolder'))
    write_csv_header_for_bugs_csv()
    list_of_authors = os.listdir(rootdir)
    # print(list_of_authors)
    for author in list_of_authors:
        author_path = Path(rootdir + '/' + author)
        # if author != list_of_authors[0]: #  and os.path.isdir(author_path) This needs to be fixed if more authors
        #     os.chdir(Path(os.getcwd()).parents[2]) # Need this to go back to the rootdir to continue on the next author.
        if os.path.isdir(author_path):
            repositories_list = os.listdir(author_path)
            for directory in repositories_list:
                repository_path = Path(str(author_path) + '/' + directory)
                # print(repository_path)
                if os.path.isdir(repository_path):
                    # print(repository_path)
                    # os.chdir(Path(os.getcwd()))  # Need this to go back to author to continue to next repo.
                    print("We're now in the repository: {}".format(repository_path))
                    repository_path = str(repository_path)

                    a_repo = git.Repo(repository_path, odbt=git.GitCmdObjectDB)
                    g = git.Git(repository_path)
                    # print(os.getcwd(), subdir, dirs, files)
                    commit_author_date_message_changedfiles = get_git_log_data(g)
                    # print(commit_author_date_message_changedfiles)     # STILL NEED TO WORK THIS OUT NEATLY
                    os.chdir(repository_path)
                    # print(os.getcwd())

                    commit_checkout_iterator(g, a_repo, repository_path, str(author_path), commit_author_date_message_changedfiles)   # Iterate each commit of a repository.
                    # print(os.getcwd())
                    # os.chdir(Path(os.getcwd()).parent)        # BUG HERE, CAN'T ITERATE REPOS. NEED HELP. SOS.
                    # print(os.getcwd())

def get_repository_path(item):

    repository_path = str(Path(item + '/' + os.listdir(item)))
    # repository_path = str(Path(subdir + '/' + dirs[0]))
    # print(repository_path)
    # repository_path = str(subdir) + '\\' + str(dirs[0])  # Here we have the git folder string equal to repository.
    return repository_path


def get_repository_name(repository_path):
    repository_name = repository_path.split('repo_subfolder\\')
    return str(repository_name[-1])


def get_commit_csv_name(repository_path, subdir, commit_index):
    repository_name = repository_path.split(subdir)
    return Path(str(repository_name[-1]) + '_' + str(commit_index) + '.csv')  # For example repo_1.csv -> HelloWorld_1.csv


def read_repository_csv_location(repository_path, subdir, commit_index):
    # DATA_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    # THIS WAS ADJUSTED TO BE ABLE TO WORK WITH NEW DIR STRUCTURE, NOT SURE IF BEST WAY
    DATA_PATH = os.path.abspath(Path(os.getcwd()).parent)
    path = Path(str(DATA_PATH) + str(get_commit_csv_name(repository_path, subdir, commit_index)))
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
    for data in bug_list:
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
    cwd = os.getcwd()
    # print(cwd)
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

# THIS FUNCTION CAN BE REMOVED AS IT ISNT USED ANYWHERE
def clear_file_from_old_files_folder(file):
    os.remove(file)


def clear_new_files_folder():
    files = glob.glob(str(Path(LHDIFF_NEW_PATH + '/*')))
    for file in files:
        os.remove(file)

def clear_old_files_folder():
    files = glob.glob(str(Path(LHDIFF_OLD_PATH + '/*')))
    for file in files:
        os.remove(file)

def copy_new_files_to_old_files_folder():
    files = glob.glob(str(Path(LHDIFF_NEW_PATH + '/*')))
    for file in files:
        copy(Path(file), LHDIFF_OLD_PATH)

def call_lhdiff_for_modified_case(relevant_file, relevant_files_loc):
    oldfile = str(Path(LHDIFF_OLD_PATH + '/' + relevant_file))
    newfile = str(Path(LHDIFF_NEW_PATH + '/' + relevant_file))      # NEEDS TO BE BUGTESTED / CHANGED FOR MISSING BUG OR FILE.
    # BUG: Both files have to be named exactly the same. git log should be checked for name-changes.

    if os.path.isfile(oldfile) and os.path.isfile(newfile):
        lhdiff_output = subprocess.check_output(['java', '-jar', LHDIFF_PATH, oldfile, newfile])
        data = lhdiff_output.split()

        for old_and_new_loc in data[9:]:  # From 9 to remove the introduction words from LHDiff.
            # print(old_and_new_loc)
            old_and_new_loc = str(old_and_new_loc).strip('b').strip("'").split(',')  # To clean the returned LHDiff output.
            old_file_loc = str(old_and_new_loc[0])
            new_file_loc = str(old_and_new_loc[1])
            # print(str(old_file_loc), str(new_file_loc), str(relevant_files_loc))
            # IF OLD_FILE_LOC IS FOUND PREVIOUSLY IN BUGS.CSV, THEN IT IS THE SAME BUG. ELSE IT IS A NEW BUG.
            if new_file_loc == str(relevant_files_loc):
                # print('JAAAA')# This needs to be changed into new_file_loc or relevant_files_loc?
                this_is_the_same_bug_as_a_previous_bug, previous_bug_id = read_bugs_for_lhdiff(relevant_file, old_file_loc)
                if this_is_the_same_bug_as_a_previous_bug: # Search for old_file_location for file in bugs.csv, return boolean
                    # print(previous_bug_id)
                    print("same bug")
                    if old_file_loc != new_file_loc:
                        return previous_bug_id
                    else:
                        return BUG_HAS_NOT_CHANGED
                    # line_tracing = new_file_loc
                # else:
                    # print('verschillende bugs')


            #     print('%s : line of code (input: %s) %s is the same as %s' % (relevant_file, relevant_files_loc, old_file_loc, new_file_loc))
            # else:
            #     print('%s : line of code (input: %s) %s has become %s' % (relevant_file, relevant_files_loc, old_file_loc, new_file_loc))
                # write back to bugs.csv or return values?. # NEEDS TO BE BUGTESTED


def call_lhdiff_for_renamed_file(relevant_file, renamed_file, relevant_file_loc):
    oldfile = str(Path(LHDIFF_OLD_PATH + '/' + relevant_file))
    newfile = str(Path(LHDIFF_NEW_PATH + '/' + renamed_file))
    lhdiff_output = subprocess.check_output(['java', '-jar', LHDIFF_PATH, oldfile, newfile])
    data = lhdiff_output.split()
    for old_and_new_loc in data[9:]:  # From 9 to remove the introduction words from LHDiff tool.
        # print(old_and_new_loc)
        old_and_new_loc = str(old_and_new_loc).strip('b').strip("'").split(',')  # To clean the returned LHDiff output.
        # print(old_and_new_loc)
        old_file_loc = str(old_and_new_loc[0])  # Line of code in old file
        new_file_loc = str(old_and_new_loc[1])  # Line of code in new file

        if new_file_loc == str(relevant_file_loc):
            # print('JAAAA')# This needs to be changed into new_file_loc or relevant_files_loc?
            this_is_the_same_bug_as_a_previous_bug, previous_bug_id = read_bugs_for_lhdiff(relevant_file, old_file_loc)
            if this_is_the_same_bug_as_a_previous_bug: # Search for old_file_location for file in bugs.csv, return boolean
                # print(previous_bug_id)
                return previous_bug_id
                # line_tracing = new_file_loc
            # else:
            #     print('verschillende bugs')

        # print(old_file_loc, new_file_loc, relevant_file_loc)
        # if old_file_loc == relevant_file_loc:  # This needs to be changed into new_file_loc or relevant_files_loc?
        #     print('%s : line of code (input: %s) %s is the same as %s' % (relevant_file, relevant_file_loc, old_file_loc, new_file_loc))
        # else:
        #     print('%s : line of code (input: %s) %s has become %s' % (relevant_file, relevant_file_loc, old_file_loc, new_file_loc))
    # return new_file_loc

def relevant_file_is_the_same_as_the_git_file(changed_files_for_this_commit, file_path, e):
    return changed_files_for_this_commit[e][1] == file_path

def relevant_file_is_not_in_git_log(changed_files_for_this_commit, bug_list_splitted, e):
    return changed_files_for_this_commit[e][1] not in bug_list_splitted[2]


def this_file_is_changed_and_has_a_resource_leak(changed_file_git, file_path_infer):
    if changed_file_git[-1] == file_path_infer:
        return True


def renamed_file_case_function(file_name, renamed_file, repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp):
    # print(changed_files_for_this_commit[e][1])
    # old_file = changed_files_for_this_commit[e][1]
    # print(old_file)
    global bug_tracking_dict
    copy_to_new_folder(renamed_file)
    file_name = file_name.split('/')[-1]
    renamed_file = renamed_file.split('/')[-1]
    # print(renamed_file)
    # if old_file == relevant_files_list[i][0]:
    # print(old_file, new_file)
    bug_id = call_lhdiff_for_renamed_file(file_name, renamed_file, line_number)
    if not bug_id: #If no previous bug id has been assigned, create new bug id
        global bug_counter
        bug_id = repository + '_' + str(bug_counter)
        bug_counter += 1
        bug_tracking_dict[bug_id] = BUG_IS_ACTIVE

    write_bugs(bug_id, repository, bug_type, file_path_bug_infer, line_number, bug_description, 'NULL', start_commit_id, start_commit_msg, start_commit_timestamp, 'END_COMMIT_MSG', 'END_COMMIT_TIMESTAMP', 'END_COMMIT_ID', 'REMOVAL_COMMIT_ID', 'REMOVAL_COMMIT_MSG', 'REMOVAL_COMMIT_TIMESTAMP')


    # print(bug_id, repository, bug_type, file_path_bug_infer, line_number,
    #       bug_description, 'LHDIFF_LINE_TRACING', start_commit_id, start_commit_msg,
    #       start_commit_timestamp, 'END_COMMIT_MSG', 'END_COMMIT_TIMESTAMP',
    #       'END_COMMIT_ID', 'REMOVAL_COMMIT_ID', 'REMOVAL_COMMIT_MSG',
    #       'REMOVAL_COMMIT_TIMESTAMP')


def added_file_case_function(g, changed_files_for_this_commit, repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp):
    global bug_tracking_dict
    new_file_to_be_checked = changed_files_for_this_commit
    copy_to_new_folder(new_file_to_be_checked)  # But don't run lhdiff yet, as there should be nothing to compare.
    # print('This file was Added and has a (new) resource leak.')

    changed_filename_tuple = renamed_file_case_parsing(g, changed_files_for_this_commit, start_commit_id)
    # if changed_filename_tuple is empty, it means that no filename change has occured
    if len(changed_filename_tuple) > 0:
        renamed_file_case_function(changed_filename_tuple[0], changed_filename_tuple[1], repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp)
    else:
        global bug_counter
        bug_id = repository + '_' + str(bug_counter)
        bug_counter += 1
        bug_tracking_dict[bug_id] = BUG_IS_ACTIVE

        # CODE BOB NET TOEGEVOEGD
        # g_log_for_file = g.log("--follow", "--name-status", "--format='%H'", str(os.path.abspath(new_file_to_be_checked))).split('\n')
        #     # for commit_0_file_2 in range(0, len(g_log_for_file), 3):
        #     #     if g_log_for_file[commit_0_file_2] == start_commit_id and g_log_for_file[commit_0_file_2 + 2][0] == 'R':
        #     #         print('This is a renamed file!', g_log_for_file[commit_0_file_2 + 2])

        #[-1].split('\t')?

        write_bugs(bug_id, repository, bug_type, file_path_bug_infer, line_number, bug_description, 'NULL', start_commit_id, start_commit_msg, start_commit_timestamp, 'END_COMMIT_MSG', 'END_COMMIT_TIMESTAMP', 'END_COMMIT_ID', 'REMOVAL_COMMIT_ID', 'REMOVAL_COMMIT_MSG', 'REMOVAL_COMMIT_TIMESTAMP')



        # write_bugs(bug_id, repository, bug_type, file_path_bug_infer, line_number, bug_description, 'NULL',
        #       start_commit_id, start_commit_msg, start_commit_timestamp, 'NULL', 'NULL',
        #       'NULL', 'NULL', 'NULL', 'NULL')

# THIS FUNCTION CAN BE REMOVED AS IT IS NOT USED ANYWHERE.
def deleted_file_case_function(changed_files_for_this_commit, repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp):
    # print(changed_files_for_this_commit)
    old_file_that_is_to_be_removed = changed_files_for_this_commit  # Clean the file from old_files
    clear_file_from_old_files_folder(old_file_that_is_to_be_removed)
    # print(bug_id, repository, bug_type, file_path_bug_infer, line_number, bug_description, 'LHDIFF_LINE_TRACING', start_commit_id, start_commit_msg, start_commit_timestamp, 'END_COMMIT_MSG', 'END_COMMIT_TIMESTAMP', 'END_COMMIT_ID', 'REMOVAL_COMMIT_ID', 'REMOVAL_COMMIT_MSG', 'REMOVAL_COMMIT_TIMESTAMP')  # Here I should add end/removal data.


def modified_file_case_function(changed_files_for_this_commit, e, repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp):
    # print('DO SOMETHING FOR MODIFIED FILE CASE')
    global bug_tracking_dict
    copy_to_new_folder(Path(file_path_bug_infer))  # Just copy the things that infer returned
    file_name = file_path_bug_infer.split('/')[-1]

    # old_file_path_in_git_log = changed_files_for_this_commit[e][1]
    # new_file_path_in_git_log = changed_files_for_this_commit[e][2]
    bug_id = call_lhdiff_for_modified_case(file_name, line_number)
    if bug_id != BUG_HAS_NOT_CHANGED:
        if not bug_id: #If no previous bug id has been assigned, create new bug id
            global bug_counter
            bug_id = repository + '_' + str(bug_counter)
            bug_counter += 1

        bug_tracking_dict[bug_id] = BUG_IS_ACTIVE


        write_bugs(bug_id, repository, bug_type, file_path_bug_infer, line_number, bug_description, 'NULL', start_commit_id, start_commit_msg, start_commit_timestamp, 'END_COMMIT_MSG', 'END_COMMIT_TIMESTAMP', 'END_COMMIT_ID', 'REMOVAL_COMMIT_ID', 'REMOVAL_COMMIT_MSG', 'REMOVAL_COMMIT_TIMESTAMP')

def files_that_were_deleted_this_commit(commit, commit_author_date_message_changedfiles):
    deleted_files_for_this_commit = []
    # print(commit_author_date_message_changedfiles)
    for i in range(len(commit_author_date_message_changedfiles)):
        if str(commit) == str(commit_author_date_message_changedfiles[i][0]):  # If the commit equals the commit of the git log
            # print(str(commit_author_date_message_changedfiles[i][4:]))
            for e in range(len(commit_author_date_message_changedfiles[i][4:])):
                if commit_author_date_message_changedfiles[i][4:][e][0] == 'D':
                    # print(commit_author_date_message_changedfiles[i][4:][e][0])
                    deleted_files_for_this_commit.append(commit_author_date_message_changedfiles[i][4:][e][1])
    return deleted_files_for_this_commit

def check_if_deleted_file_had_a_bug(deleted_file_list_for_this_commit):
    global files_that_have_been_renamed, deleted_files_that_have_been_renamed
    with open(BUGS_CSV_LOCATION, 'r') as csvfile:
        reader = csv.reader(csvfile, lineterminator='\n')
        removed_bugs_in_deleted_file = {}
        # print("\n\n")
        # print(deleted_file_list_for_this_commit)
        counter = 1
        for row in list(reader)[1:]:
            # print(row)
            for deleted_file in deleted_file_list_for_this_commit:
                if deleted_file == row[3] and deleted_file not in files_that_have_been_renamed.keys():
                    removed_bugs_in_deleted_file[row[0]] = row
                    deleted_files_that_have_been_renamed[deleted_file] = ""
            # print(removed_bugs_in_deleted_file.keys())
            counter = counter + 1
        return removed_bugs_in_deleted_file


def check_if_bugs_have_been_removed(bug_array, commit, end_commit_id, end_commit_timestamp, end_commit_msg):
    not_removed_bugs_dict = {}
    removed_bugs_array = []
    global solved_bug_archive
    global bug_tracking_dict
    with open(BUGS_CSV_LOCATION, 'r') as csvfile:
        reader = csv.reader(csvfile, lineterminator='\n')
        for row in reversed(list(reader)[1:]):
            for i in range(len(bug_array[0])):
                if str(row[3]) == str(bug_array[2][i]) and str(row[4]) == str(bug_array[3][i]):
                    # print("*****\nBUG FOUND AGAIN \n*****")
                    not_removed_bugs_dict[str(row[0])] = ""
            if not str(row[0]) in not_removed_bugs_dict.keys() and bug_tracking_dict[str(row[0])] != BUG_IS_SOLVED and renamed_file_has_not_been_deleted((str(row[3]))):
                # print('IK GA HEM NU TOEVOEGEN')

                removed_bugs_array.append(row)
        if len(removed_bugs_array) > 0:
            for bug_row in removed_bugs_array:
                dt = dateutil.parser.parse(str(commit.committed_datetime))
                unix_date_for_removed_bug_in_modified_file = time.mktime(dt.timetuple())
                # If bug was not previously marked as solved
                write_bugs(bug_row[0], bug_row[1], bug_row[2], bug_row[3], bug_row[4], bug_row[5], bug_row[6], bug_row[7], bug_row[8], bug_row[9], end_commit_msg, end_commit_timestamp, end_commit_id, str(commit), str(commit.message).replace("\n", ""), str(unix_date_for_removed_bug_in_modified_file))
                solved_bug_archive.append(bug_row[0])
                bug_tracking_dict[bug_row[0]] = BUG_IS_SOLVED


def parse_git_log_follow_output(follow_log, start_commit_id):
    for g_log_value in range(len(follow_log)):
        if follow_log[g_log_value - 1].replace("'", "") == str(start_commit_id) and follow_log[g_log_value][0] == "R":
            filename_change_log_value = follow_log[g_log_value].split("\t")
            previous_file_name = filename_change_log_value[1]
            new_file_name = filename_change_log_value[2].split("\n")[0]
            print("FILENAME CHANGE: %s has been renamed to %s \n" % (previous_file_name, new_file_name))
            global files_that_have_been_renamed
            files_that_have_been_renamed[previous_file_name] = ""
            return [previous_file_name, new_file_name]
    return []

def renamed_file_has_not_been_deleted(file_in_question):
    global  deleted_files_that_have_been_renamed, files_that_have_been_renamed
    return file_in_question not in deleted_files_that_have_been_renamed.keys() and file_in_question not in files_that_have_been_renamed.keys()

def renamed_file_case_parsing(g, changed_file_for_this_commit, start_commit_id):
    follow_log = g.log("--follow", "--name-status", "--format='%H'", str(os.path.abspath(changed_file_for_this_commit))).split('\n\n')
    changed_filename_tuple = parse_git_log_follow_output(follow_log, start_commit_id)
    return changed_filename_tuple

# This for the case that if a Infer run fails, and there is renamed file with a bug in the repository
def follow_renamed_when_infer_fails(g, start_commit_id, repository, start_commit_msg, start_commit_timestamp):
    with open(BUGS_CSV_LOCATION, 'r') as csvfile:
        reader = csv.reader(csvfile, lineterminator='\n')
        for row in list(reader)[1:]:
            bug_type = row[2]
            file_path_bug_infer = row[3]
            line_number = row[4]
            bug_description = row[5]

            changed_filename_tuple = renamed_file_case_parsing(g, file_path_bug_infer, start_commit_id)
            file_name = changed_filename_tuple[0]
            renamed_file = changed_filename_tuple[1]


            if len(changed_filename_tuple) > 0:
                renamed_file_case_function(file_name, renamed_file, repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp)
                copy_to_old_folder(renamed_file)

def bug_path_exists_in_csv(bug_path):
    print("")
    with open(BUGS_CSV_LOCATION, 'r') as csvfile:
        reader = csv.reader(csvfile, lineterminator='\n')
        for row in reader:
            if str(row[3]) == str(bug_path):
                return True
        return False

def commit_checkout_iterator(g, a_repo, repository_path, author_path, commit_author_date_message_changedfiles):
    commit_index = 1
    x = []
    global bug_tracking_dict
    # FOR LOOP HERE:
    # print('Amount of commits to scan:', len(list(a_repo.iter_commits()))) # prints amount of commits in repository to go through.
    end_commit_id, end_commit_timestamp, end_commit_msg = '', '', ''  # To prevent reference error during analysis of first commit; This is OK because there will never be a removal of a bug in the first commit.
    for commit in reversed(list(a_repo.iter_commits())):  # NOTE: repo subfolder HAS to be empty. Else only last commit will be read.
        g.checkout(commit)    # Checkout the commit of the version of the repo that we analyse.
        print(commit)

        # Read out the git log file:
        for i in range(len(commit_author_date_message_changedfiles)):
            # print(commit_author_date_message_changedfiles[i])
            if str(commit) == commit_author_date_message_changedfiles[i][0]:
                # If the commit equals the commit of the git log
                # print(commit_author_date_message_changedfiles[i])
                author_for_this_commit = commit_author_date_message_changedfiles[i][1]
                start_commit_timestamp = commit_author_date_message_changedfiles[i][2]  # timestamp_for_this_commit
                start_commit_msg = commit_author_date_message_changedfiles[i][3]  # message_for_this_commit
                changed_files_for_this_commit = commit_author_date_message_changedfiles[i][4:]
                # print(changed_files_for_this_commit)

        start_commit_id = commit  # This is just for the naming of write_bugs(), can just be rewritten as commit.
        repository = repository_path.split('repo_subfolder\\')[-1]

        # RUN INFER AND CREATE CSV

        infer_success = InferTool.inferAnalysisIOS(str(commit_index))
        # LHDIFF conditionals can be placed here:

        if infer_success:
            # GET CSV PATH AND READ CSV
            get_commit_csv_name(repository_path, author_path, commit_index)
            bug_list = read_commit_csv(repository_path, author_path, commit_index)
            bug_list_splitted = bug_list_splitter(bug_list)
            # COPY RELEVANT FILES IN OLD-FOLDER
            # print(bug_list_splitted[2])

            file_set_for_files_that_have_not_changed = {file[-1] for file in changed_files_for_this_commit}



            for i in range(len(bug_list_splitted[0])):
                # For i in all bugs found in the csv
                # Might be able to remove newlines and headers from csv with a split or strip.
                # I want to have a list with paths, loc and files. Possible bug when there are more or less bugs in old/new
                file_path_bug_infer = bug_list_splitted[2][i]
                # file_path_list = []
                # file_path_list.append(bug_list_splitted[2][i])
                file_name = bug_list_splitted[2][i].split('/')[-1]
                line_number = bug_list_splitted[3][i]
                bug_type = bug_list_splitted[1][i]
                bug_description = bug_list_splitted[4][i]
                print('Scanning file: %s with bug in loc %s' % (file_name, line_number))
                # print(file_path, file_name, line_number, bug_type, bug_description)

                # This should go down when we have more data. (LHDIFF line tracing for example.) print is for giving examples showing which data is put in the bugs.csv
                # This is the header of bugs.csv: ID,REPO_ID,FILE_PATH,LINE_NUMBER,BUG_DESCRIPTION,LHDIFF_LINE_TRACING,START_COMMIT_ID,START_COMMIT_MSG,START_COMMIT_TIMESTAMP
                # write_bugs(bug_id, repository, bug_type, file_path, line_number, bug_description, lhdiff_line_tracing, start_commit_id, start_commit_msg, start_commit_timestamp)
                # print(bug_id, repository, bug_type, file_path, line_number, bug_description, 'lhdiff_line_tracing', start_commit_id, start_commit_msg, start_commit_timestamp, 'END_COMMIT_MSG', 'END_COMMIT_TIMESTAMP', 'END_COMMIT_ID', 'REMOVAL_COMMIT_ID', 'REMOVAL_COMMIT_MSG', 'REMOVAL_COMMIT_TIMESTAMP')

                # if commit_index == 1:      LEGACY               # Not first commit, LHDiff needs two versions of a file to compare to.
                    # print(file_path) LEGACY
                    # copy_to_new_folder(file_path_bug_infer)         # possible bug: Need to check if this works with the repo_subfolder walk.
                # else: LEGACY
                    # print(len(changed_files_for_this_commit), changed_files_for_this_commit)
                    # print(changed_files_for_this_commit)


                for changed_file_in_git_log in changed_files_for_this_commit:
                    if this_file_is_changed_and_has_a_resource_leak(changed_file_in_git_log, file_path_bug_infer):      # So only files that are found by infer are checked here
                        print('resource leak found in {} that was {} this commit'.format(file_path_bug_infer, changed_file_in_git_log[0]))
                        #print(str(g.log("--follow", "--name-status", "--format='%H'", file_path_bug_infer)))
                        for e in range(len(changed_files_for_this_commit)):     # For every file in the git log that was changed in some way...
                            if relevant_file_is_the_same_as_the_git_file(changed_files_for_this_commit, file_path_bug_infer, e):      # Check if the bug-file Infer returned is the same.
                                this_file_was = changed_files_for_this_commit[e][0][0]
                                # print(str(g.log("--follow", "--name-status", "--format='%H'", file_path_bug_infer)))
                                # if this file was Renamed / Added / Deleted / Modified
                                # print(file_path_bug_infer)
                                if this_file_was == 'R':    # Renamed
                                    # print('RRRRRRRR')
                                    changed_filename_tuple = renamed_file_case_parsing(g, changed_files_for_this_commit,start_commit_id)
                                    # if changed_filename_tuple is empty, it means that no filename change has occured
                                    if len(changed_filename_tuple) > 0:
                                        renamed_file_case_function(changed_filename_tuple[0], changed_filename_tuple[1], repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp)
                                elif this_file_was == 'M':  # Modified
                                    # print('MMMMMMMMM')
                                    modified_file_case_function(changed_files_for_this_commit, e, repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp)
                                elif this_file_was == 'A':  # Added
                                    # print('AAAAAAAAA')
                                    added_file_case_function(g, changed_files_for_this_commit[e][1], repository, bug_type, file_path_bug_infer, line_number, bug_description, start_commit_id, start_commit_msg, start_commit_timestamp)

                if file_path_bug_infer not in file_set_for_files_that_have_not_changed:
                    print('No change found for: {}. This bug is still in the same place from a previous commit and file has not been changed in any way in this commit'.format(file_path_bug_infer))
                    copy_to_new_folder(file_path_bug_infer)
                    if not bug_path_exists_in_csv(file_path_bug_infer):
                        global bug_counter
                        bug_id = repository + '_' + str(bug_counter)
                        bug_counter += 1
                        write_bugs(bug_id, repository, bug_type, file_path_bug_infer, line_number, bug_description, "NULL", start_commit_id, start_commit_msg, start_commit_timestamp, 'END_COMMIT_MSG', 'END_COMMIT_TIMESTAMP', 'END_COMMIT_ID', 'REMOVAL_COMMIT_ID', 'REMOVAL_COMMIT_MSG', 'REMOVAL_COMMIT_TIMESTAMP')
                        bug_tracking_dict[bug_id] = BUG_IS_ACTIVE

                # Check if any bugs are removed


            check_if_bugs_have_been_removed(bug_list_splitted, commit, end_commit_id, end_commit_timestamp, end_commit_msg)


            # PUT DATA IN bugs.csv
            # write_bugs(bug_id, repository, file_path, line_number, bug_description, lhdiff_line_tracing, start_commit_id, start_commit_msg, start_commit_timestamp)
            # CLEAR OLD_FOLDER
            # if commit_index >= 2:
            #     clear_old_files_folder()    # This is needed for storage purposes.
            # PUT NEW_FOLDER CONTENTS IN OLD_FOLDER
            copy_new_files_to_old_files_folder()
            # CLEAR NEW_FOLDER
            clear_new_files_folder()
            # RESTART ON NEXT COMMIT IN FOR-LOOP
            commit_index += 1
            # QUICK AND DIRTY FIX, TO BE CHANGED LATER ###
            # subprocess.call('ls', shell=True)
            # os.chdir(repository_path.split("/")[-1]) # Don't know why this was here..?

        # else:
        #     # Hier commit_index+=1 (in einde van code
        #     follow_renamed_when_infer_fails(g, start_commit_id, repository, start_commit_msg, start_commit_timestamp)

        # A DELETED FILE NEVER HAS A RESOURCE LEAK... SO IT ALSO DOESN'T MATTER IF GRADLE/INFER RUNS OR NOT.
        deleted_file_list_for_this_commit = files_that_were_deleted_this_commit(commit, commit_author_date_message_changedfiles)
        removed_bugs_in_deleted_file = check_if_deleted_file_had_a_bug(deleted_file_list_for_this_commit)
        global solved_bug_archive
        for bug in removed_bugs_in_deleted_file.keys():
            bug_row = removed_bugs_in_deleted_file[bug]
            dt = dateutil.parser.parse(str(commit.committed_datetime))
            unix_date_for_deleted_file = time.mktime(dt.timetuple())
            if not bug_row[0] in solved_bug_archive:
                write_bugs(bug_row[0], bug_row[1], bug_row[2], bug_row[3], bug_row[4], bug_row[5], bug_row[6], bug_row[7], bug_row[8], bug_row[9], end_commit_msg, end_commit_timestamp, end_commit_id, str(commit), str(commit.message).replace("\n", ""), str(unix_date_for_deleted_file))
                solved_bug_archive.append(bug_row[0])
                bug_tracking_dict[bug_row[0]] = BUG_IS_SOLVED


        # This is for the END data in write_bugs(), now specifically for deleted case. Prone to be changed.
        end_commit_msg = str(commit.message).replace("\n", "")
        previous_dt = dateutil.parser.parse(str(commit.committed_datetime))
        unix_date_previous_commit = time.mktime(previous_dt.timetuple())
        end_commit_timestamp = str(unix_date_previous_commit)
        end_commit_id = str(commit)
    clear_old_files_folder()
    clear_new_files_folder()
        
# read_csv_and_clone_github_repositories()             # To read a csv with a list of repositories to clone and then iterate through. (Remove first #) repo_subfolder HAS to be empty.
# write_csv_header_for_bugs_csv()
# search_files()         # For finding all infer-compatible files recursively in the repo_subfolder.
mine_repositories()     # Mining repositories


'''
#APPENDIX (Don't need this code anymore)



                # file_was_renamed():
                #     relevant_file = relevant_files_list[i - 1][0] # DIT KLOPT NIET -> Moet uit git log de renamed file halen
                #     renamed_file = relevant_files_list[i][0]
                #     call_lhdiff_for_renamed_file(relevant_file, renamed_file, line_of_code)
                # elif file_was_removed():
                #
                # # AND DO SOMETHING FOR BUGS.CSV?
                # elif file_was_added():
                #     copy_to_new_folder(file_path)
                #
                # # AND DO SOMETHING FOR BUGS.CSV
                # elif file_was_modified():
                #     copy_to_new_folder(relevant_files_list[i][0])
                #     call_lhdiff(file_name, line_of_code)

                # print(line_of_code)
                # copy_to_new_folder(relevant_files_list[i][0])
                # IF NEW FOLDER IS FILLED OR DIFFERENT RUN LHDIFF
                # if there_are_files_in_new_files_folder():
                #     call_lhdiff(file_name, line_of_code)









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

'''