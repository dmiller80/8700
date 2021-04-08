# import random  # just a pun, we don't need a random import
import csv
import os


# This program ingests data from the 2019 CDC BRFSS data file
# Pertinent data is extracted from the file based on the associated codebook
# Data extracted: High Blood Pressure, High Cholesterol,
# Coronary Heart Disease, Diabetes, Smoking, BMI, Heart Attack
#


def read_from_file(file_name, HrtAttckYorN):
    """Reads the file provided as file_name, and returns a list of strings
    Only data for NE will be returned"""
    ne_line = []
    with open(file_name, mode='r') as cdc_file:
        cdc_lines = cdc_file.readlines()
        line_count = 0
        for cdc_line in cdc_lines:
            if line_count > 7770: break
            print(line_count)
            # Note-31 NE state code and  col 116 == 1 is hrt attk
            # read both if '3' passed in
            # Better: if [:2]=='31': if YoN=='3': append() :else [116] == YorN
            if cdc_line[:2] == '31':
                if HrtAttckYorN == '3':
                    ne_line.append(cdc_line)
                elif HrtAttckYorN == cdc_line[116]:
                    ne_line.append(cdc_line)
                line_count += 1

    return ne_line


def write_to_file(the_list, file_name):
    # writes the file with the data from the_list
    #
    with open(file_name, mode='w') as cdc_file:
        for row in the_list:
            str_write = str(row) + "\n"
            cdc_file.write(str_write)
    return

def write_arff_header(file_name):
    # writes ARFF header data
    # else Weka can open csv file if header row
    # has attribute names
    with open(file_name, mode='a') as arff_file:
        header_string = '''@relation HeartATTCK

@attribute Sex numeric
@attribute High_BP numeric
@attribute High_Cholesterol numeric
@attribute Angina numeric
@attribute Diabetes numeric
@attribute Smoking numeric
@attribute Weight numeric
@attribute Heart_Attack {Y,N}

@data'''
        arff_file.write(header_string)
        arff_file.write("\n")
    return

def map_highbp(hbp):
    if hbp == '1':
        out = '0'
    elif hbp == '4':
        out = '.2' # Borderline closer to hbp
    elif hbp == '2':
        out = '.67'
    else:
        out = '1'
    return out


def map_diabetes(dbt):
    if dbt == '1':
        out = '0'
    elif dbt == '4':
        out = '.2'
    elif dbt == '2':
        out = '.67'
    else:
        out = '1'
    return out


def map_smoking(smk):
    if smk == '1':
        out = '0'
    elif smk == '2':
        out = '.3'
    else:
        out = '1'
    return out


def map_bmi(bmi):
    if bmi == '4':
        out = '0'
    elif bmi == '3':
        out = '.33'
    elif bmi == '2':
        out = '.67'
    else:
        out = '1'
    return out

def parse_row(count, row):
    # Parse the rows we are interested in.  Ignore any row where there
    # is a space as that indicates no data (there are other no data cast
    # Note=Could have iterated through a list of cols looking for no data
    data_found = True
    # Here are the key values (field names from code book):
    # Year, Sex, High BP, High Cholesterol, Heart Attk, Heart Disease, Diabetes, Smoking, Weight

    # map high blood pressure
    hbp = map_highbp(row[111])
    dbt = map_diabetes(row[126])
    bmi = map_bmi(row[2001])

    # Want Heart Attack Indicator as Label
    if row[116] == '1':
        ha = 'Y'
    else:
        ha = 'N'
    holding_list = (row[90], hbp, row[114], row[117], dbt, bmi, ha)
    #                 row[117], dbt, smk, row[2001], ha)
    parsed = str(",").join(holding_list)
    for elem in holding_list:
        if elem == " " or elem == '7' or elem == '9':  # Per code book 7, 9 or blank is 'no data'
            data_found = False
            print("skipped ")
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


    myfile = "LLCP2019.ASC"  # Mmoved source file to local dir for ease of use
    print("Retrieving data from: ", myfile)

    try:
        # This will only read rows that in NE AND have Heart Attack True
        # Only read hrt attck data = '1', only no hrt attck, or 3 all
        the_ne_list = read_from_file(myfile, '3')  # returns state=NE and Heart Attack 1(Y), 2(N) or 3(both)
        file_name = input("Enter output filename: ")

        icnt = 1
        list_of_recs = [[]]
        for row in the_ne_list:
            parsed = parse_row(icnt, row)
            if len(parsed) != 0:
                if icnt == 1:
                    list_of_recs[0] = \
                        "Sex,High_BP,High_Cholesterol,Angina,Diabetes,Weight,Heart_Attack"
                        # "Sex,High_BP,High_Cholesterol,Angina,Diabetes,Smoking,Weight,Heart_Attack"
                    icnt += 1
                else:
                    list_of_recs.append(parsed)
                    print(icnt, parsed)
                    icnt += 1
            write_to_file(list_of_recs, file_name)

    except FileNotFoundError:
        print("BRFSS data not read from file - file not found: ", myfile)

    print("Success")

if __name__ == '__main__':
    main()


