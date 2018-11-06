from github3api.ratelimit_github import RateLimitedGitHub
from github3.models import GitHubError
import csv
import os
import requests
import time
from github3api.get_repo_data import RepoChecker

# input_file_path = '../5_itunes_check.csv'
input_file_path = '../csv/appstore/appstore_checked.csv'
output_file_path = '../6_additional_info.csv'
error_file_path = '../6_error.csv'


class AppInformation(RateLimitedGitHub):

    # check if iTunes API returns results for identifier
    def app_information(self, identifier):
        app_information = []
        url = "https://itunes.apple.com/lookup?bundleId=" + identifier
        appstore_json = requests.get(url).json()
        time.sleep(1)

        # if non-empty json extract artistName and primaryGenreName
        for result in appstore_json['results']:
            app_information.append(result['artistName'])
            app_information.append(result['primaryGenreName'])
        return app_information

    # read all lines of csv add additional repository data to line
    def iter_over_repos(self):
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'a', newline='') as output_file, \
                open(error_file_path, 'a', newline='') as error_file:

            csv_reader = csv.DictReader(input_file)

            # add headers for additional data to existing headers
            fieldnames = csv_reader.fieldnames + ['category'] + ['artist'] + ['java_files'] + \
            ['c_files'] + ['obj_c_files'] + ['h_files'] + ['html_files'] + ['css_files'] + ['js_files']

            # set fieldnames per file
            output_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            error_writer = csv.DictWriter(error_file, fieldnames=['repo', 'error'])
            output_writer.writeheader(), error_writer.writeheader()

            repo_verifier = RepoChecker(token=os.getenv('GITHUB_AUTH_TOKEN'))

            # write repository parameters
            for line in csv_reader:
                try:
                    if self.app_information(line['apple_store']):
                        app_info = self.app_information(line['apple_store'])
                        line['category'] = app_info[1]
                        line['artist'] = app_info[0]
                        line['java_files'] = repo_verifier.file_counter(line['full_name'], 'java')
                        line['c_files'] = repo_verifier.file_counter(line['full_name'], 'c')
                        line['obj_c_files'] = repo_verifier.file_counter(line['full_name'], 'm')
                        line['h_files'] = repo_verifier.file_counter(line['full_name'], 'h')
                        line['html_files'] = repo_verifier.file_counter(line['full_name'], 'html')
                        line['css_files'] = repo_verifier.file_counter(line['full_name'], 'css')
                        line['js_files'] = repo_verifier.file_counter(line['full_name'], 'js')
                        output_writer.writerow(line)
                    else:
                        pass
                except:
                    print("There has been an error")
                    pass

github = AppInformation(token=os.getenv('GITHUB_AUTH_TOKEN'))
print(github.rate_limit())

github.iter_over_repos()

