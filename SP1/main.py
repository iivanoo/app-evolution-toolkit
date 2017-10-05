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
        repositories.append('www.github.com/' + repo)

# Example print on 5 repositories.
print(repositories[1:5])



'''
#path for the analyser
analyzer = "../SP2/analyzer"
'''

# Write bugs.csv
with open('csv/bugs.csv', 'w') as csvfile:
    fieldnames = ['ID', 'REPO_ID', 'FILE_PATH', 'LINE_NUMBER', 'BUG_DESCRIPTION', 'LHDIFF_LINE_TRACING', 'START_COMMIT_ID', 'START_COMMIT_MSG', 'START_COMMIT_TIMESTAMP']
    writer = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')

    # Write the fieldnames and then include the data.
    writer.writeheader()
    for row in repositories[1:]:
        ID += 1
        writer.writerow({'ID': ID, 'REPO_ID': row, 'FILE_PATH': 'test', 'LINE_NUMBER': 'test',
                     'BUG_DESCRIPTION': 'test', 'LHDIFF_LINE_TRACING': 'test', 'START_COMMIT_ID': 'test',
                     'START_COMMIT_MSG': 'test', 'START_COMMIT_TIMESTAMP': 'test'})

