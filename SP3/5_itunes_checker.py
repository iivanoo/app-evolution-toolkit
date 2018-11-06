from github3api.ratelimit_github import RateLimitedGitHub
import csv
import json
import os
import re
import requests
import time
from github3 import GitHubError

input_file_path = '../4_activity_check.csv'
output_file_path = '../5_itunes_check.csv'
removed_file_path = '../5_failed_itunes_check.csv'
error_file_path = '../5_error.csv'



class FindAppInItunesStore(RateLimitedGitHub):

    def init(self):
        print("geinit")

    def search_identifier(self, repo):
        return self.search_code(
            'repo:{} in:path .pbxproj'.format(repo))

    def search_identifier_plist(self, repo):
        return self.search_code(
            'repo:{} in:path info.plist'.format(repo))

    def search_apple_store(self, identifier):
        url = "https://itunes.apple.com/lookup?bundleId=" + identifier
        appstore_json = requests.get(url).json()
        time.sleep(1)
        store_identifiers = []
        for result in appstore_json['results']:
            store_identifiers.append(result['bundleId'])
        return store_identifiers

    def get_raw_data(self, repo):
        url = requests.get(repo.to_json()['html_url'])
        return url.text.split('\n')

    def filter_common_words(self, identifiers_list):
        common_words = ['--ID--', 'yourcompany', '.wordpress', 'com.Parse']
        matching = [x for x in identifiers_list if any(xs in x for xs in common_words)]
        for id in matching:
            identifiers_list.remove(id)
        return identifiers_list

    def identifier_in_plist(self, repo):
        potential_identifiers = []
        real_identifiers = []
        try:
            for result in self.search_identifier_plist(repo):
                raw_data = self.get_raw_data(result)
                for index, line in enumerate(raw_data):
                    try:
                        if "&gt;CFBundleIdentifier" in line:
                            line = raw_data[index + 4].split('&gt;')[1].split('&lt')[0]
                            potential_identifiers.append(line)
                    except Exception:
                        pass
                for id in potential_identifiers:
                    if "PRODUCT_BUNDLE_IDENTIFIER" not in id and "PRODUCT_NAME" not in id:
                        if id not in real_identifiers:
                            real_identifiers.append(id)
        except GitHubError as error:
            if error.code == 422 or error.code == 403:  # Validation Failed
                return real_identifiers
        print("Identifiers in plist:" + str(self.filter_common_words(real_identifiers)))
        return self.filter_common_words(real_identifiers)
        print(self.filter_common_words(real_identifiers))

    def identifier_in_pbxproj(self, repo):
        potential_identifiers_pbxproj = []
        product_name_list = []
        real_identifiers_pbxproj = []
        try:
            for result in github.search_identifier(repo):
                raw_data = self.get_raw_data(result)
                for index, line in enumerate(raw_data):
                    line = re.sub('&quot', '', line)
                    if "PRODUCT_NAME =" in line:
                        product_name = (re.sub('["$(); ]', '', line).split("=")[-1].split("<")[0])
                        if "TARGET_NAME" not in product_name and "PROJECT_NAME" not in product_name:
                            if product_name not in product_name_list:
                                product_name_list.append(product_name)

                    elif "PRODUCT_BUNDLE_IDENTIFIER" in line:
                        first_sub = (re.sub('["$(); ]', '', line).split("=")[-1].split('<')[0])
                        if "&quot" in first_sub:
                            print(re.sub('&quot', '', first_sub) + "lol")

                        elif "PRODUCT_NAME" in first_sub:
                            if "{P" in first_sub:
                                for product_name in product_name_list:
                                    if (first_sub.split("{P")[0] + product_name) not in potential_identifiers_pbxproj:
                                        potential_identifiers_pbxproj.append((first_sub.split("{P")[0] + product_name))

                            elif "PRODUCT_" in first_sub:
                                for product_name in product_name_list:
                                    if (first_sub.split("PRODUCT_")[0] + product_name) not in potential_identifiers_pbxproj:
                                        potential_identifiers_pbxproj.append((first_sub.split("PRODUCT_")[0] + product_name))
                        else:
                            if first_sub not in potential_identifiers_pbxproj:
                                potential_identifiers_pbxproj.append(first_sub)
        except GitHubError as error:
            if error.code == 422 or error.code == 403:  # Validation Failed
                print("Found error while checking for the pbxproj " + str(error))
                return potential_identifiers_pbxproj
        print("Identifiers in pbxproj:" + str(self.filter_common_words(potential_identifiers_pbxproj)))
        return(self.filter_common_words(potential_identifiers_pbxproj))



    def iter_over_repos(self):
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'a', newline='') as output_file, open(removed_file_path, 'a', newline='') as removed_repos, open(error_file_path, 'a', newline='') as error_file:

            csv_reader = csv.DictReader(input_file)
            fieldnames = csv_reader.fieldnames + ['apple_store']
            output_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            removed_writer = csv.DictWriter(removed_repos, fieldnames=fieldnames)
            error_writer = csv.DictWriter(error_file, fieldnames=['repo', 'error'])
            output_writer.writeheader(), removed_writer.writeheader(), error_writer.writeheader()

            for line in csv_reader:
                while line:
                    print(github.rate_limit())
                    try:
                        print("Checking for repo: " + line['full_name'])
                        plists = self.identifier_in_plist(line['full_name'])
                        # print("Dit is de plist:", plists)
                        pbxproj_list = self.identifier_in_pbxproj(line['full_name'])
                        # print("Dit is pbxproj:", pbxproj_list)
                        has_identifier = False
                        if pbxproj_list or plists:
                            for id in plists+pbxproj_list:
                                if id in self.search_apple_store(id):
                                    print("found match in plist on: " + id)
                                    line['apple_store'] = id
                                    has_identifier = True
                                    break
                        if has_identifier:
                            output_writer.writerow(line)
                        else:
                            line['apple_store'] = "No identifier"
                            removed_writer.writerow(line)
                        break
                    except Exception as error:
                        error_writer.writerow(line)
                        break


github = FindAppInItunesStore(token=os.getenv('GITHUB_AUTH_TOKEN'))
print(github.rate_limit())

github.iter_over_repos()

