from github3api.ratelimit_github import RateLimitedGitHub
import os
import csv


from github3api.get_repo_data import RepoChecker

input_file_path = '../3_plist_checked.csv'
output_file_path = '../4_activity_check.csv'
removed_file_path = '../4_failed_activity_check.csv'
error_file_path = '../4_error.csv'

# Determine initial headers for csv.
CSV_COLUMNS = [
    'id', 'name', 'full_name', 'language', 'commit_count', 'active_days'
    ]

# initiate RateLimitedGitHub instance to avoid abuse detection
class PerilAvoidance(RateLimitedGitHub):

# get repo date from get_repo_data.py and
    def check_activity(self, repo):
        if repo.count_commits() > 6 and repo.count_active_days() > 56:
            return True
        else:
            return False


    # iterate over all lines and for each line request repo data from "get_repo_data.py"
    def iter_over_repos(self):
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'a', newline='') as output_file, open(removed_file_path, 'a', newline='') as removed_repos, open(error_file_path, 'a', newline='') as error_file:
            output_writer = csv.DictWriter(output_file, fieldnames=CSV_COLUMNS)
            removed_writer = csv.DictWriter(removed_repos, fieldnames=CSV_COLUMNS)
            error_writer = csv.DictWriter(error_file, fieldnames=['repo', 'error'])
            output_writer.writeheader(), removed_writer.writeheader(), error_writer.writeheader()
            repo_verifier = RepoChecker(token=os.getenv('GITHUB_AUTH_TOKEN'))

            for line in input_file:
                while line:
                    print(github.rate_limit())
                    try:
                        repo = repo_verifier.get_repo(line)

                        if repo:
                            # collect data from Repository object
                            repo_data = repo.repo_data
                            repo_data['commit_count'] = repo.count_commits()
                            repo_data['active_days'] = repo.count_active_days()

                            if self.check_activity(repo):
                                print("Writing to Output: " + repo.full_name)
                                output_writer.writerow(repo_data)
                            else:
                                print("Writing to Removed: " + repo.full_name)
                                removed_writer.writerow(repo_data)
                        break
                    except Exception as error:
                        error_writer.writerow({'repo': line.split()[0], 'error': error})
                        break

github = PerilAvoidance(token=os.getenv('GITHUB_AUTH_TOKEN'))

github.iter_over_repos()
