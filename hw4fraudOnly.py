# import random  # just a pun, we don't need a random import
import csv
import os


# This program ingests raw fraud data provided for Chapter 5 HW question number one.
#
# Note: the data is processed in accordance with the Chapter 5 Table 1 data transformation
# The data is split into OK and Fraud instances evenly after the Chapter 5 transformations.
# rules.


def store_to_csv(a_list):
    """The function takes a list of strings and stores it as csv data
    FOR Homework-only use 2000 rows"""
    with open('wekaFraudOnly.csv', mode='w', newline='') as weka_file:
        weka_writer = csv.writer(weka_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # list passed includes header row
        icnt = 0
        for row in a_list:
            if icnt < 2001:
                weka_writer.writerow(row)
                icnt += 1
    return


def read_from_csv_file(file_name):
    """Reads the file provided as file_name, and returns a list of strings
    Only data for NE will be returned"""
    fraud_2dlist = [[]]
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header_str = ", ".join(row)
                print(f'Column names are {header_str}')
                fraud_2dlist[0] = row
                line_count += 1
            else:
               #  print(f'\t{row[0]}, \t{row[1]}, \t{row[2]}, \t{row[3]}, \t{row[4]}, \t{row[5]}, \t{row[6]}')
                if row[6] == '1':
                    fraud_2dlist.append(row)
                    line_count += 1
                else:
                    line_count += 1
        print(f'Processed {line_count} lines.')
    return fraud_2dlist



def map_age(age):
    if age < 20:
        normalized =0.0
    elif age < 40:
        normalized = (age-20)/20.0
    elif age < 60:
        normalized = 1.0
    elif age < 70:
        normalized = 1.0 - (age - 60)/10.0
    else:
        normalized = 0.0
    return normalized


def map_claim(claim):
    normalized = max(1-claim/5000.0, 0)

    return round(normalized, 2)


def map_tickets(tickets):
    if tickets == 0:
        normalized = 1.0
    elif tickets == 1:
        normalized = 0.6
    else:
        normalized = 0.0

    return normalized

def map_prior(prior):
    if prior == 0:
        normalized = 1.0
    elif prior == 1:
        normalized = 0.5
    else:
        normalized = 0.0

    return normalized


def map_atty(atty):
    if atty == 'none':
        normalized = 1
    else:
        normalized = 0

    return normalized


def normalize_rows(fl):
    # Use the following functions to normalize data:
    # fl[0] = Age = map_age(fl[0]), fl[1] = Gender = int(fl[1]), fl[2] = Claim = map_claim(fl[2])
    # fl[3] = tickets = map_tickets(fl[3]), fl[4] = prior = map_prior[fl4], fl[5] = atty =
    # map_atty(fl[5]), fl[6] = outcome = int(fl[6])
    icnt = 0
    for row in fl:
        if icnt == 0:
            # skip header row
            icnt +=1
        else:
            icnt += 1
            row[0] = map_age(int(row[0]))
            row[1] = int(row[1])
            row[2] = map_claim(int(row[2]))
            row[3] = map_tickets(int(row[3]))
            row[4] = map_prior(int(row[4]))
            row[5] = map_atty(row[5])

            if row[6] == "1":
                row[6] = "Fraud"
                fl[icnt] = row
    return fl


def main():
    # Program Title
    print("Extract data from raw fraud file and transform it for Weka K-means")
    print()

    csv_file = "FraudRaw.csv"  # I moved source file to local dir for ease of use
    print("Retrieving data from: ", csv_file)
    # fl = [[]]
    try:

        the_2d_list = read_from_csv_file(csv_file)  # returns records from state=NE
        # Normalize the data
        fl = normalize_rows(the_2d_list)
        print(fl)
    except FileNotFoundError:
        print("Fraud data not read from file - file not found: ", csv_file)


# Once normalize columns complete for Weka K Means,
# write csv file-then prepend with attribute labels for weka
    try:
        store_to_csv(fl)
    except IOError as e:
        print("Failed to write ", e)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
