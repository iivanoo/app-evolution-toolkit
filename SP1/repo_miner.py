'''
This file will iterate through repositories from GitHub.

Made by:
Bob van den Berg
Vrije Universiteit Amsterdam
'''

import csv

# Opening my example csv file with GitHub repositories.
with open('example_github_repos.csv', "rt", encoding="utf8") as csv_file:
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
