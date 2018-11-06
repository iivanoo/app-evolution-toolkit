from github3api.ratelimit_github import RateLimitedGitHub
import os
import csv

input_file_path = '../1_dateranges.csv'
output_file_path = '../2_all_repos.csv'


# initiate RateLimitedGitHub instance to avoid abuse detection
class RepoSearcher(RateLimitedGitHub):

    # search for repositories that are created between [daterange] + containing "ios"
    def search_repos(self, datum):
        return self.search_repositories(
            'created:{} ios'.format(datum))

    # write every result found by search_repos to a new csv.file
    def iterate(self):
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
            for line in input_file:
                results = self.search_repos(line.split()[0])
                next(results)

                for result in results:
                    print(result.repository.full_name)
                    wr = csv.writer(output_file)
                    wr.writerow([result.repository.full_name])


github = RepoSearcher(token=os.getenv('GITHUB_AUTH_TOKEN'))

github.iterate()
