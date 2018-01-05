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



ID = 0


# Download GitHub repositories from a csv row:
def read_csv():
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
    for i in range(1, 2):
        Repo.clone_from(url[i], path[i])


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
            # because path is object not string
            path_in_str = str(path)
            file_list.append(path_in_str)
        print(file_list)

#    def append_infer_files_list(self, path_in_str):
#        with open('csv/infer_files_list', "wb", encoding="utf8") as infer_files_list:
#            infer_files_list.append(path_in_str)

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

def write_bugs():
    # Write bugs.csv
    with open('csv/bugs.csv', 'w') as csvfile:
        fieldnames = ['ID', 'REPO_ID', 'FILE_PATH', 'LINE_NUMBER', 'BUG_DESCRIPTION', 'LHDIFF_LINE_TRACING', 'START_COMMIT_ID', 'START_COMMIT_MSG', 'START_COMMIT_TIMESTAMP']
        writer = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
        ID = 1
        # Write the fieldnames and then include the data.
        writer.writeheader()
        for repository in repositories[1:]:
            ID += 1
            writer.writerow({'ID': ID, 'REPO_ID': repository, 'FILE_PATH': 'test', 'LINE_NUMBER': 'test',
                         'BUG_DESCRIPTION': 'test', 'LHDIFF_LINE_TRACING': 'test', 'START_COMMIT_ID': 'test',
                         'START_COMMIT_MSG': 'test', 'START_COMMIT_TIMESTAMP': 'test'})


extensions = [
            'java',
            'c',
            'cc',
            'cpp',
            'm',
            'xml'
        ]

def search_files():
    for i in extensions:
        IterateThroughFiles.find_infer_files('repo_subfolder', i) # For finding all java files recursively in the repo_subfolder.

def show_log_files():
    rootdir = 'repo_subfolder'

    for subdir, dirs, files in os.walk(rootdir):
        if subdir.count(os.sep) <= 1 and subdir.count(os.sep) > 0:
            a_repo = git.Repo(str(subdir) + '\\' + str(dirs[0]), odbt=git.GitCmdObjectDB);
            g = git.Git(str(subdir) + '\\' + str(dirs[0]))
            loginfo = g.log()

            for commit in list(a_repo.iter_commits()):
                g.checkout(commit)
                #print(commit)

#read_csv()     # To read a csv with a list of repositories to clone and then iterate through. (Remove first #)
#write_bugs()
#search_files()
show_log_files()

