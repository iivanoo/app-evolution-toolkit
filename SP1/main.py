'''
This file will iterate through repositories from GitHub.

Made by:
Bob van den Berg
Vrije Universiteit Amsterdam
'''

import csv

ID = 0

# Opening my example csv file with GitHub repositories.
with open('csv/example_github_repos.csv', "rt", encoding="utf8") as csv_file:
    # Csv file rows are cut into pieces using ';'. Change if needed.
    csv_file_data = csv.reader(csv_file, delimiter=";")
    repositories = []
    for rows in csv_file_data:
        # In example file the repositories are stored in the 0 position in a row. Change if needed.
        repo = rows[0]
        # Append GitHub with the repository extension.
        #repositories.append('www.github.com/' + repo)
        repositories.append('git://github.com/' + repo + '.git')

# Example print on 5 repositories.
print(repositories[1:5])

'''
repo: GitHub repo in the form <username>/<repo_id>
Example: “duckduckgo/Android”
DONE
repo_subfolder: path within the repo to focus on (and recursively on all its subfolders). For example, in the DuckDuckGo GitHub repo, we want to focus on the “app/src/main” folder because the source code of the Android app is there, all the other folders contain other resources that we do not care about

keep_temp_data: boolean, if true, all the intermediate files and data produced by the static analyzer will be kept in a dedicated folder

output_path: the path in the file system where the output bugs.csv file will be created

output_folder_path: the folder in the file system where to put all the other generated files which may be useful

analyzer: the path in the file system where to find the main Python script for running the static analyzer (Infer in the case of SP2, but it can be any)

'''

'''
#path for the analyser
analyzer = "../SP2/analyzer.py"
'''


# Write bugs.csv
with open('csv/bugs.csv', 'w') as csvfile:
    fieldnames = ['ID', 'REPO_ID', 'FILE_PATH', 'LINE_NUMBER', 'BUG_DESCRIPTION', 'LHDIFF_LINE_TRACING', 'START_COMMIT_ID', 'START_COMMIT_MSG', 'START_COMMIT_TIMESTAMP']
    writer = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')

    # Write the fieldnames and then include the data.
    writer.writeheader()
    for repo in repositories[1:]:
        ID += 1
        writer.writerow({'ID': ID, 'REPO_ID': repo, 'FILE_PATH': 'test', 'LINE_NUMBER': 'test',
                     'BUG_DESCRIPTION': 'test', 'LHDIFF_LINE_TRACING': 'test', 'START_COMMIT_ID': 'test',
                     'START_COMMIT_MSG': 'test', 'START_COMMIT_TIMESTAMP': 'test'})



