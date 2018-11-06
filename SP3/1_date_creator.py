from github3api.ratelimit_github import RateLimitedGitHub
from github3 import GitHubError
import csv
import os
import datetime
import sys

# change name as desired
output_file_path = "../1_dateranges.csv"


# initiate RateLimitedGitHub instance to avoid abuse detection
class DateCreator(RateLimitedGitHub):

    # search for repositories that are created between [daterange] + containing "ios"
    def search_repos(self, datum):
        return self.search_repositories(
            'created:{} ios'.format(datum))

    # if count is > 1000 some results are excluded.
    # return "false" as long as results > 1000 so daterange gets adjusted
    def check_count_per_date(self, datum: str):
        results = self.search_repos(datum)
        # result = next(results)
        next(results)
        # print(results.total_count)
        if results.total_count < 1000:
            return True
        else:
            return False

    # write dat range to csv in a format so that GitHub understands it: "2001-01-01..2010-01-01
    def create_dates(self, date_from, date_to):
        date = str(date_from) + ".." + str(date_to)
        if date_from.split('-')[0] == '2018':
            print("Done")
            sys.exit()
        while self.check_count_per_date(date) == False:
            try:
                date_to = subtract_day(date_to)
                date = str(date_from) + ".." + str(date_to)
                print(date)
            except GitHubError as error:
                if error.code == 422:
                    date_to = subtract_day(date_to)
                    date = str(date_from) + ".." + str(date_to)
        else:
            write_dates_csv(date)
            print(date + " Added to the list.")
            date_from = date_to
            date_to = add_week(date_to)
            date = str(date_from) + ".." + str(date_to)
            self.create_dates(date_from,date_to)

# return new date with 1 day subtracted of it
def subtract_day(date_to):
    date_as_datetime = datetime.datetime.strptime(str(date_to), "%Y-%m-%d").date()
    new_datetime = date_as_datetime - datetime.timedelta(days=1)
    return new_datetime.strftime("%Y-%m-%d")


# return new date with 7 days added to it
def add_week(date_to):
    date_as_datetime = datetime.datetime.strptime(str(date_to), "%Y-%m-%d").date()
    new_datetime = date_as_datetime + datetime.timedelta(days=7)
    return new_datetime.strftime("%Y-%m-%d")


# write every newly created daterange to csv_output
def write_dates_csv(dates):
    with open(output_file_path, 'a', newline='') as csv_output:
        wr = csv.writer(csv_output)
        wr.writerow(dates.split())

# initiate RateLimitedGitHub to avoid abuse detection
github = DateCreator(token=os.getenv('GITHUB_AUTH_TOKEN'))

# initiate date creating
github.create_dates("2001-01-01","2010-01-01")