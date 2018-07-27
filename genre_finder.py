# Currently, this takes a folder of jsons and prints a list of genres from
# each show. It stores the genres in a dictionary with the show date as a key -
# the genres for each night are in a list accessed by that key.
# Things to add:
#   Have this write the list to a PDF
#       Get it to work not in IDLE
#   Add in analysis - count each type of genre, etc.

import os
import glob
import json
import csv_dict_writer as csv


# json_reader - takes open file and extracts and returns the data.
def json_reader(filename):
    return json.load(filename)


# genre_finder - takes in json data from json_reader and parses through the
#   show data to create a dictionary genre_dict. This dictionary uses the
#   show date as a key to access a list containing the titles & genres of the
#   shows performed that night.
def genre_finder(genre_dict, json_data):
    record = json_data["ephemeralRecord"]
    shows = record["shows"]
    for show in shows:
        date = show["date"]
        genre_dict[date] = []
        performances = show["performances"]
        for performance in performances:
            genre_dict[date].append(
                [performance["title"], performance["genreClaim"]])
    return genre_dict


def genre_csv_list(genre_dict):
    master = []
    for date in genre_dict:
        for show in range(len(genre_dict[date])):
            lst = []
            lst.append(date)
            lst.append(genre_dict[date][show][0])
            lst.append(genre_dict[date][show][1])
            master.append(lst)
    return master


def run_genre_csv(master, directory):
    data = ["Date,Title,Genre".split(",")]
    for i in master:
        str = "{} ,{} ,{}".format(i[0], i[1], i[2])
        data.append(str.split(" ,"))
    file = "{}/{}".format(directory, "results.csv")
    csv.run_csv_writer(data, file)


def run_genre_finder(directory):
    paths = glob.glob(os.path.join(directory, "*.json"))
    paths.sort()
    genre_dict = {}
    for filename in paths:
        with open(filename, "r") as my_file:
            json_data = json_reader(my_file)
            genre_dict = genre_finder(genre_dict, json_data)
    return genre_dict


def main():
    directory = input("Genre Finder: Please input the folder path: ")
    directory = os.path.expanduser(directory)
    genre_dict = run_genre_finder(directory)
    master = genre_csv_list(genre_dict)
    run_genre_csv(master, directory)


if __name__ == "__main__":
    main()
