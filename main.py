# import random  # just a pun, we don't need a random import
import csv
import os

# This program ingests data from the 2019 (only at this point) CDC BRFSS data file
# Pertinent data is extracted from the file based on the associated codebook
# Data extracted: Heart Attack, Coronary Heart Disease, High Blood Pressure,
# High Cholesterol, Diabetes, BMI
# Note: need to add Sex, Smoking and Age (Smoking is complex due to varied questions-did you quit recently, etc)


def store_to_csv(a_list):
    """The function takes a list of strings and stores it as csv data in the 2019_brfss.csv file"""
    with open('2019_brfss.csv', mode='w', newline='') as brfss_file:
        brfss_writer = csv.writer(brfss_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
# we need to parse--need to extract variables--list passed in should only have data we want
        for row in a_list:
            brfss_writer.writerow(row)

    return


def read_from_file(file_name, lines_to_read):
    """Reads the file provided as file_name, and returns a list of strings
    Only data for NE will be returned"""
    ne_line = []
    with open(file_name, mode='r') as cdc_file:
        cdc_lines = cdc_file.readlines()
        line_count = 0
        for cdc_line in cdc_lines:
            if cdc_line[:2] == '31':      # Note-31 NE state code
                ne_line.append(cdc_line)
                line_count += 1
                if line_count >= lines_to_read:    # There are over 15,800 records-cut off early for ease of use
                    break
    return ne_line


def get_yes_no(user_prompt):
    """The function receives a prompt string and displays the request prompt
    to the user and then returns True if input not equal to 'n' """
    result = input(user_prompt + ': ')
    if result.lower() == 'n':
        return False

    else:
        return True


def parse_row(count, row):
    no_data = 0
    if row[111] == " " or row[114] == " " or row[116] == " " or row[117] == " " \
            or row[126] == " "\
            or row[2001] == " ": no_data = 1
# print(count, "yr\t", row[22:26], "\tSX\t", row[68], row[81], "\tBP\t", row[111], "\tCHL\t", row[114], "\tHATTK\t", row[116],
#       "\tHRDISE\t", row[117], "\tDBTS\t", row[126], "\tBMI\t", row[2001])
    holding = (str(row[22:26]), str(row[111]), str(row[114]),
                   str(row[116]), str(row[117]), str(row[126]), str(row[2001]))
    parsed = str(",").join(holding)
    if no_data == 1: parsed = ""
    return parsed

def main():

    # display a title
    print("Extract data from 2019 BRFSS")
    print()

    #
    # Prompt user for filename
    # mydir = str(r"C/:Users/Dan/OneDrive/8700/GroupProject/2019brfss/LLCP2019ASC")
    myfile = "LLCP2019.ASC"
    # file_name = 'test.txt'
    # input("Enter the filename containing the BRFSS data: ")
    try:
        the_ne_list = read_from_file(myfile, 100)
        icnt = 1
        list_of_recs = [[]]
        for row in the_ne_list:
            parsed = parse_row(icnt, row)
            if len(parsed) != 0:
                list_of_recs.append(parsed)
                print(icnt, parsed)
                icnt += 1

    except FileNotFoundError:
        print("BRFSS data not read from file - file not found: ", myfile)
    # if not get_yes_no("Would you like to continue (y/n)"):
    #     try:
    #         store_to_csv(the_trips)
    #         print("Trips saved to file trips.csv")
    #     except IOError as e:
            # If there is error on attempt to open/write file
            # alert the user that file was not saved
    #         print("Could not save the trips file ", e)
    #    break

# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/