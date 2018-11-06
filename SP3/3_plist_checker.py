from github3api.ratelimit_github import RateLimitedGitHub
from github3.models import GitHubError
import os
import csv


input_file_path = '../2_all_repos.csv'
output_file_path = '../3_plist_checked.csv'
removed_file_path = '../3_plist_not_present.csv'
error_file_path = '../csv/3_error.csv'


# initiate RateLimitedGitHub instance to avoid abuse detection
class PlistSearcher(RateLimitedGitHub):

    # search in repository "repo" for "key" to be present in file "info.plist"
    def searchcode(self, repo, key):
        return self.search_code(
            'repo:{} filename:info.plist {} in:file '.format(repo, key))

    # provide usable arguments for searchcode
    def find_keys(self, repo_name):
        for result in self.searchcode(repo_name.split()[0], 'UIRequiredDeviceCapabilities OR LSRequiresIPhoneOS'):
            if result:
                return True

    # read all lines of csv and if find_keys = True, write to new csv.
    def iter_over_repos(self):
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'a') as output_file, open(removed_file_path, 'a') as removed_repos, open(error_file_path, 'a') as error_file:
            for line in input_file:
                while line:
                    try:
                        print("Checking repo: " + line)
                        if self.find_keys(line):
                            wr = csv.writer(output_file)
                            wr.writerow(line.split())
                        else:
                            w2r = csv.writer(removed_repos)
                            w2r.writerow(line.split())
                        break
                    except GitHubError as error:
                        if error.code == 422:  # Validation Failed
                            w3r = csv.writer(error_file)
                            w3r.writerow(line.split())
                            break


github = PlistSearcher(token=os.getenv('GITHUB_AUTH_TOKEN'))

github.iter_over_repos()
