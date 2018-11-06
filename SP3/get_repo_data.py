from github3.repos.repo import Repository
from github3api.ratelimit_github import RateLimitedGitHub
from typing import Tuple
from datetime import datetime
import re


class Repo(Repository):


    @property
    def repo_data(self):
        repo = self
        repo_json = self.to_json()
        return {
            'id': repo.id,
            'name': repo.name,
            'full_name': repo.full_name,
            # 'description': repo.description,
            # 'size': repo.size,
            # 'private': repo.private,
            'language': repo.language,
            # 'default_branch': repo.default_branch,
            # 'owner_id': repo.owner,
        }

    # count number of commits
    def count_commits(self):
        number_of_commits = 0
        for result in self.iter_commits():
            number_of_commits += 1
        return number_of_commits

    # count number of days between date of first commit and date of last commit
    def count_active_days(self):
        list_of_commit_date = []
        for result in self.iter_commits():
            list_of_commit_date.append(result.commit.author['date'].split('T')[0])
            first_commit = datetime.strptime(str(list_of_commit_date[-1]), '%Y-%m-%d')
            last_commit = datetime.strptime(str(list_of_commit_date[0]), '%Y-%m-%d')
            active_days = (last_commit - first_commit).days
        return active_days


class RepoChecker(RateLimitedGitHub):

    PATT = re.compile(r'^([a-z0-9-]+)\/([a-z0-9_\.-]+)$', re.I)

    def get_repo(self, full_name: str) -> Repo:
        owner, name = self.full_name_parts(full_name)
        repo = self.repository(owner, name)
        return Repo(repo.to_json(), repo._session)

    @staticmethod
    def full_name_parts(full_name: str) -> Tuple[str, str]:
        match = RepoChecker.PATT.match(full_name)
        # print(match)
        if match:
            return match.groups()

    # Count the number of times a file with certain extension is in repository.
    def file_counter(self, repo, extension):
        counter = 0
        for result in self.search_code('repo:{} in:path *.{}'.format(repo, extension)):
            counter += 1
        return counter
