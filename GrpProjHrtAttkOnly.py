# import random  # just a pun, we don't need a random import
import csv
import os


# This program ingests data from the 2019 CDC BRFSS data file
# Pertinent data is extracted from the file based on the associated codebook
# Data extracted: Heart Attack, Coronary Heart Disease, High Blood Pressure,
# High Cholesterol, Diabetes, BMI
# Note: need to add Sex, Smoking and Age (Smoking is complex due to varied questions-did you quit recently, etc)


def store_to_csv(a_list):
    """The function takes a list of strings and stores it as csv data in the 2019_brfss.csv file"""
    with open('2019_brfss_HaOnly.csv', mode='w', newline='') as brfss_file:
        brfss_writer = csv.writer(brfss_file, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # we need to parse--need to extract variables--list passed in should only have data we want
        for row in a_list:
            brfss_writer.writerow(row)
    return


def read_from_file(file_name):
    """Reads the file provided as file_name, and returns a list of strings
    Only data for NE will be returned"""
    ne_line = []
    with open(file_name, mode='r') as cdc_file:
        cdc_lines = cdc_file.readlines()
        line_count = 0
        for cdc_line in cdc_lines:
            # Note-31 NE state code and  col 116 == 1 is hrt attk
            if cdc_line[:2] == '31' and cdc_line[116] == '1':
                ne_line.append(cdc_line)
                line_count += 1
    return ne_line


def write_to_file(the_list):
    # writes the file with the data from the_list
    file_name = "2019_HaOnlyParsed.csv"
    with open(file_name, mode='w') as cdc_file:
        for row in the_list:
            str_write = str(row) + "\n"
            cdc_file.write(str_write)
    return


def parse_row(count, row):
    # Parse the rows we are interested in.  Ignore any row where there
    # is a space as that indicates no data (there are other no data cast
    # Note=Could have iterated through a list of cols looking for no data
    data_found = True
    # Here's the key values (field names from code book):
    # Year, Sex, High BP, High Cholesterol, Heart Attk, Heart Disease, Diabetes, Smoking, Weight
    holding_list = (str(row[22:26]), row[90], row[111], row[114],
                     row[117], row[126], row[207], row[2001], row[116])
    parsed = str(",").join(holding_list)
    for elem in holding_list:
        if elem == " " or elem == '7' or elem == '9':  # Per code book 7, 9 or blank is 'no data'
            data_found = False
            break
    # To Do: Make Easier And Name Each Var Per Code Book-use a Dictionary
    # print(count, "yr\t", row[22:26], "\tSX\t", row[90], "\tBP\t", row[111], "\tCHL\t", row[114], "\tHATTK\t", row[116],
    #       "\tHRDISE\t", row[117], "\tDBTS\t", row[126], "\tBMI\t", row[2001])
    # Check if the survey did not complete and ignore data from this case, too

    if not data_found or row[31:35] == "1200":
        parsed = ""
    return parsed


def main():
    # Program Title
    print("Extract data from 2019 BRFSS")
    print()

    # Prompt user for filename
    # myfile = input("Enter the filename containing the BRFSS data: ")
    # mydir = os.path.join("C:\\", "Users", "Dan", "OneDrive", "8700", "GroupProject", "2019brfss", "LLCP2019ASC")
    # myfile = "LLCP2019.ASC"
    # myfile = os.path.join(mydir, myfile)
    myfile = "LLCP2019.ASC"  # I moved source file to local dir for ease of use
    print("Retrieving data from: ", myfile)

    try:
        # This will only read rows that in NE AND have Heart Attack True
        the_ne_list = read_from_file(myfile)  # returns records from state=NE
        icnt = 1
        list_of_recs = [[]]
        for row in the_ne_list:
            parsed = parse_row(icnt, row)
            if len(parsed) != 0:
                if icnt == 1:
                    list_of_recs[0] = \
                        "Year,Sex,High BP,High Cholesterol,Heart Attk,Heart Disease,Diabetes,Smoking,Weight"
                    icnt += 1
                else:
                    list_of_recs.append(parsed)
                    # write_to_file(parsed)
                    print(icnt, parsed)
                    icnt += 1
            write_to_file(list_of_recs)

    except FileNotFoundError:
        print("BRFSS data not read from file - file not found: ", myfile)
    try:
        store_to_csv(list_of_recs)
    except IOError as e:
        print("Failed to write ", e)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
