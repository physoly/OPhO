import csv

from utils import get_connection, run_async


def execute():
    with open("../data/opho_invi20.csv", "r") as csvin:
        for line in csv.reader(csvin):
            print(line)

execute()

"""
CREATE TABLE invi_scores(teamname VARCHAR (35), pr_1 decimal, pr_2 decimal, pr_3 decimal, pr_4 decimal, pr_5 decimal, pr_6 decimal, pr_7 decimal, pr_8 decimal, pr_9 decimal, pr_10 decimal, total_score decimal);
"""
