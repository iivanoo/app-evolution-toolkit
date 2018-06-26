import os
import csv
from pathlib import Path
import dateutil.relativedelta
import datetime
import statistics

BUGS_CSV_LOCATION = str(Path(os.path.abspath("csv/bugs.csv")))
START_COMMIT_TIMESTAMP = "START_COMMIT_TIMESTAMP"
END_COMMIT_TIMESTAMP = "REMOVAL_COMMIT_TIMESTAMP"

bugs = {}

with open(BUGS_CSV_LOCATION, 'r') as csvfile:
    reader = csv.reader(csvfile, lineterminator='\n')
    for row in reader:
        id = str(row[0])
        if id != "BUG_ID":
            bugs[id] = {}
            bugs[id][START_COMMIT_TIMESTAMP] = str(row[9])
            bugs[id][END_COMMIT_TIMESTAMP] = str(row[15])

# Code for date parsing adapted from: https://stackoverflow.com/questions/6574329/how-can-i-produce-a-human-readable-difference-when-subtracting-two-unix-timestam/6574789

diff_time_stamps = []
for bug in bugs.keys():
    if bugs[bug][END_COMMIT_TIMESTAMP] != END_COMMIT_TIMESTAMP:
        dt1 = datetime.datetime.fromtimestamp(float(bugs[bug][START_COMMIT_TIMESTAMP]))
        dt2 = datetime.datetime.fromtimestamp(float(bugs[bug][END_COMMIT_TIMESTAMP]))
        rd = dateutil.relativedelta.relativedelta (dt2, dt1)
        diff_time_stamps.append(float(bugs[bug][END_COMMIT_TIMESTAMP]) - float(bugs[bug][START_COMMIT_TIMESTAMP]))
        print("Solving time: \n")
        print (
        "%d years, %d months, %d days, %d hours, %d minutes and %d seconds" % (
        rd.years, rd.months, rd.days, rd.hours, rd.minutes, rd.seconds))

# Remove outlier
# diff_time_stamps = diff_time_stamps[:-1]
# print(sum(diff_time_stamps)/len(diff_time_stamps))
print("Mean time spent is: " + str(statistics.mean(diff_time_stamps)))
print("Median solving time is: " + str(statistics.median(diff_time_stamps)))
print("Standard deviation is: " + str(statistics.stdev(diff_time_stamps)))