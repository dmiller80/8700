# import random  # just a pun, we don't need a random import
import csv
import os


# This program ingests raw loan data provided for Chapter 5 HW question number four.
# Note: the data is processed in accordance with the Chapter 5 page 82 data transformation
# rules.


def store_to_csv(a_list):
    """The function takes a list of strings and stores it as csv data
    FOR Homework-only use 2000 rows"""
    with open('wekaLoan.csv', mode='w', newline='') as weka_file:
        weka_writer = csv.writer(weka_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # list passed includes header row
        icnt = 0
        for row in a_list:
            if icnt < 2001: # again-this is due to homework directions (used 2000, 1/2 train, 1/2 test)
                weka_writer.writerow(row)
                icnt += 1
    return


def read_from_csv_file(file_name):
    """Reads the file provided as file_name, and returns a list of strings
    Only data for NE will be returned"""
    ln_2dlist = [[]]
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header_str = ", ".join(row)
                print(f'Column names are {header_str}')
                ln_2dlist[0] = row
                line_count += 1
            else:
               # print(f'\t{row[0]}, \t{row[1]}, \t{row[2]}, \t{row[3]}, \t{row[4]}, \t{row[5]}, \t{row[6]}')
                ln_2dlist.append(row)
                line_count += 1
        print(f'Processed {line_count} lines.')
    return ln_2dlist



def map_age(age):
    if age < 20:
        normalized =0.0
    elif age < 50:
        normalized = (age-20)/30.0
    elif age < 80:
        normalized = 1.0 - (age - 50)/30
    else:
        normalized = 0.0

    return round(normalized, 2)


def map_risk(assets, debt, want):
    assets_to_debt = assets/(debt + want)
    if assets_to_debt > 1:
        normalized = 1
    else:
        normalized = assets_to_debt

    return round(normalized, 2)


def map_income(income):
    if income < 0:
        normalized = 0
    elif income < 100000:
        normalized = income/100000
    else:
        normalized = 1

    return normalized

def map_credit(color):
    print("map_credit-the color is", color)
    if color == "green":
        normalized = 1.0
    elif color == "amber":
        normalized = 0.3
    else:
        normalized = 0.0

    return normalized


def normalize_rows(ln):
    # Use the following functions to normalize data:
    # ln[0] = Age = map_age(ln[0]), ln[1] = Income = int(ln[1]), ln[2] = Asset = int(ln[2])
    # ln[3] = Debt = int(ln[3]), ln[4] = want = int(ln[4]), map_risk(ln[1],ln[2],ln[3]),
    # map_atty(fl[5]), fl[6] = outcome = int(fl[6])
    icnt = 0
    outcnt = 0
    normalized_list = [[]]
    for row in ln:
        if icnt == 0:
            # skip header row
            icnt += 1
        else:
            new_row = []
            print(row)

            row[0] = map_age(int(row[0]))
            row[1] = round(map_income(int(row[1])), 2)
            row[2] = int(row[2])
            row[3] = int(row[3])
            row[6] = map_risk(row[2], row[3], int(row[4]))  # Need to think about this
            row[5] = float(map_credit(row[5]))
            row[7] = int(row[7])
            new_row = [row[0], row[1], row[6], row[5], row[7]]
            if outcnt == 0:
                normalized_list[0] = new_row
                outcnt += 1
            else:
                normalized_list.append(new_row)


    return normalized_list


def main():
    # Program Title
    print("Extract data from raw loan file and transform it for Weka K-means")
    print()

    csv_file = "LoanRaw.csv"  # I moved source file to local dir for ease of use
    print("Retrieving data from: ", csv_file)

    try:

        the_2d_list = read_from_csv_file(csv_file)
        # Normalize the data
        ln = normalize_rows(the_2d_list)
        print(ln)
    except FileNotFoundError:
        print("Fraud data not read from file - file not found: ", csv_file)


# Once normalize columns complete for Weka K Means,
# write csv file-then prepend with attribute labels for weka
    try:
        store_to_csv(ln)
    except IOError as e:
        print("Failed to write ", e)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
