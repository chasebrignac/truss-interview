"""
Author: Chase J. Brignac
Email:  cjbrignac000@gmail.com
Created: November 19, 2018
Edited: November 19,2018
"""

#==========================================================================
# This program goes through a csv file and creates a normalized version
# in addition it closely follows the instructions outlined in the README.md
#==========================================================================

import sys
import csv
import argparse
import datetime

def read_csv(input_file):
    """
    #==========================================================================
    # read_csv takes a csv file formatted with commas always between quotes
    #
    # input_file - a string specifying the file to read in
    #
    # returns - list of rows from the file where each row is a different list
    # O(abc) time complexity where a is number of rows, b is number of columns
    # c is the number of characters in each row-column item, if two of a, b, or
    # c are kept constant then it simplifies to O(a), O(b), or O(c)
    #==========================================================================
    """
    csv.register_dialect('my_dialect',
    delimiter = ',',
    skipinitialspace=True)

    csv_list_of_rows = []
    with open(input_file, 'r', encoding='utf-8', errors='replace') as csv_file:
        reader = csv.reader(csv_file, dialect='my_dialect')
        for row in reader:
            item_count = 0
            for item in row:
                if ',' in item:
                    row[item_count] = '"' + item + '"'
                item_count += 1
            csv_list_of_rows += [row]
    return csv_list_of_rows

def output_csv_list_of_rows(csv_list_of_rows, output_file):
    """
    #==========================================================================
    # output_csv_list_of_rows takes a list of rows, where each row is a list
    # and writes this list to a file
    #
    # csv_list_of_rows - list of rows where each row is a different list
    # output_file - a string specifying the file to read in
    #
    # O(ab) time complexity where a is number of rows, b is number of columns
    # if either a or b are kept constant then it simplifies to O(a) or O(b)
    #==========================================================================
    """
    sys.stdout = open(output_file, 'w')
    row_count = 0
    for row in csv_list_of_rows:
        item_count = 0
        for item in row:
            if item_count != 0:
                sys.stdout.write(',')
            sys.stdout.write(str(item))
            item_count += 1
        row_count += 1
        if row_count != len(csv_list_of_rows):
            sys.stdout.write('\n')

def find_item_positions(csv_list_of_rows, item_value, row_position):
    """
    #==========================================================================
    # find_item_positions takes in a list of rows, where each row is a list
    # and the string value of an item, and the row position to look, and finds
    # column number this value is found in the specified row
    #
    # csv_list_of_rows - list of rows where each row is a different list
    # item_value - a string specifying the name of the item you're looking for
    # row_position - an int specifying which row to look in
    #
    # returns - column positions where the item was found in the specified row
    # O(b) time complexity where b is number of columns, if b is kept contant
    # this is O(1)
    #==========================================================================
    """
    item_indices = []
    item_count = 0
    found_column_title = False
    for item in csv_list_of_rows[row_position]:
        if item == item_value:
            # we found the column title!
            found_column_title = True
            item_indices += [item_count]
        item_count += 1
    if found_column_title == True:
        return item_indices
    else:
        return []

def change_date(csv_list_of_rows, time_column_name, date_format, seconds_forward):
    """
    #==========================================================================
    # change_date takes a list of rows, where each row is a list and the name
    # of the column that has dates of format date_format and an int of seconds
    # that you would like to move time forward (use negative to go backwards)
    #
    # csv_list_of_rows - list of rows where each row is a different list
    # time_column_name - a string specifying the name of the column with times
    # date_format - a string specifying time format, ex: %m/%d/%y %I:%M:%S %p
    # seconds_forward - number of seconds in time (use negative to go backwards)
    #
    # returns - list of rows from the file where each row is a different list
    # O(ab) time complexity where a is number of rows, b is number of columns
    # if either a or b are kept constant then it simplifies to O(a) or O(b)
    #==========================================================================
    """
    time_column_indices = find_item_positions(csv_list_of_rows, time_column_name, 0)
    if time_column_indices == []:
        sys.stderr.write('The following column of data was not found: ' + time_column_name + '\n')
    row_count = 0
    for time_column_index in time_column_indices:
        while row_count < len(csv_list_of_rows):
            if row_count > 0:
                try:
                    if '�' not in csv_list_of_rows[row_count][time_column_index]:
                        csv_date = datetime.datetime.strptime(csv_list_of_rows[row_count][time_column_index], date_format)
                        eastern_time = csv_date + datetime.timedelta(seconds = seconds_forward)
                        csv_list_of_rows[row_count][time_column_index] = eastern_time.strftime(date_format)
                    else:
                        sys.stderr.write('The URC turned a date field for row ' + str(row_count) + ' into something unparseable: ' + str(csv_list_of_rows[row_count][time_column_index]) + ' so we are dropping the row\n')
                        del csv_list_of_rows[row_count]
                        row_count -= 1
                except Exception as ex:
                    sys.stderr.write('Row ' + str(row_count) + ' causes an exception so we will leave this date alone: ' + str(ex) + '\n')
            row_count += 1
    return csv_list_of_rows

def format_zips(csv_list_of_rows, zip_column_name):
    """
    #==========================================================================
    # format_zips takes a list of rows, where each row is a list and the name
    # of the column that has zip codes with a five digit format and fills in
    # zeros at the beginning of the zip code if there are fewer than five digits
    # and leaves the zip code alone if there are five or more digits
    #
    # csv_list_of_rows - list of rows where each row is a different list
    # zip_column_name - a string specifying the name of the column with zip codes
    #
    # returns - list of rows from the file where each row is a different list
    # O(ab) time complexity where a is number of rows, b is number of columns
    # if either a or b are kept constant then it simplifies to O(a) or O(b)
    #==========================================================================
    """
    zip_column_indices = find_item_positions(csv_list_of_rows, zip_column_name, 0)
    if zip_column_indices == []:
        sys.stderr.write('The following column of data was not found: ' + zip_column_name + '\n')
    row_count = 0
    for zip_column_index in zip_column_indices:
        while row_count < len(csv_list_of_rows):
            if row_count > 0:
                try:
                    while len(csv_list_of_rows[row_count][zip_column_index]) < 5:
                        csv_list_of_rows[row_count][zip_column_index] = '0' + csv_list_of_rows[row_count][zip_column_index]
                except Exception as ex:
                    sys.stderr.write('Row ' + str(row_count) + ' causes an exception so we will leave this ZIP alone: ' + str(ex) + '\n')
            row_count += 1
    return csv_list_of_rows

def names_to_uppercase(csv_list_of_rows, name_column_name):
    """
    #==========================================================================
    # names_to_uppercase takes a list of rows, where each row is a list and the
    # name of the column that has names in it that will be converted to
    # uppercase
    #
    # csv_list_of_rows - list of rows where each row is a different list
    # name_column_name - a string specifying the name of the column with names
    #
    # returns - list of rows from the file where each row is a different list
    # O(ab) time complexity where a is number of rows, b is number of columns
    # if either a or b are kept constant then it simplifies to O(a) or O(b)
    #==========================================================================
    """
    name_column_indices = find_item_positions(csv_list_of_rows, name_column_name, 0)
    if name_column_indices == []:
        sys.stderr.write('The following column of data was not found: ' + name_column_name + '\n')
    row_count = 0
    for name_column_index in name_column_indices:
        while row_count < len(csv_list_of_rows):
            if row_count > 0:
                try:
                    csv_list_of_rows[row_count][name_column_index] = csv_list_of_rows[row_count][name_column_index].upper()
                except Exception as ex:
                    sys.stderr.write('Row ' + str(row_count) + ' causes an exception so we will leave this name alone: ' + str(ex) + '\n')
            row_count += 1
    return csv_list_of_rows

def sum_times(csv_list_of_rows, first_element_name, second_element_name, sum_result_column_name):
    """
    #==========================================================================
    # sum_times takes a list of rows, where each row is a list and the
    # name of the columns that has the first element to add as well as the
    # name of the columns that have the second element to add and the name of
    # the column where the sum of the elements should replace the current value
    # and adds all elements, storing the results in the sum result column
    #
    # csv_list_of_rows - list of rows where each row is a different list
    # first_element_name - the name of the column that has the first elements to
    # be added in the sum of times, this can only be of format %I:%M:%S.%f
    # second_element_name - the name of the column that has the second elements
    # to be added in the sum of times, this can only be of format %I:%M:%S.%f
    # sum_result_column_name - the name of the column that will have the results
    # of the sum of elements stored by replacing the current data of this column
    #
    # returns - list of rows from the file where each row is a different list
    # O(ab) time complexity where a is number of rows, b is number of columns
    # if either a or b are kept constant then it simplifies to O(a) or O(b)
    #==========================================================================
    """
    first_element_indices = find_item_positions(csv_list_of_rows, first_element_name, 0)
    second_element_indices = find_item_positions(csv_list_of_rows, second_element_name, 0)
    sum_result_column_indices = find_item_positions(csv_list_of_rows, sum_result_column_name, 0)
    row_count = 0
    if first_element_indices == [] or first_element_indices == [] or sum_result_column_indices == []:
        sys.stderr.write('At least one of the following columns of data were not found: ' + first_element_name + ' and/or ' + second_element_name + ' and/or ' + sum_result_column_name + '\n')
    element_indices_to_sum = first_element_indices + second_element_indices
    while row_count < len(csv_list_of_rows):
        if row_count > 0:
            total_seconds = 0.0
            try:
                for element_index in element_indices_to_sum:
                    if '�' not in csv_list_of_rows[row_count][element_index]:
                        absolute_seconds = datetime.timedelta(hours=int(csv_list_of_rows[row_count][element_index].split(':')[0]), minutes=int(csv_list_of_rows[row_count][element_index].split(':')[1]), seconds=int(csv_list_of_rows[row_count][element_index].split(':')[2].split('.')[0]), milliseconds=int(csv_list_of_rows[row_count][element_index].split(':')[2].split('.')[1])).total_seconds()
                        csv_list_of_rows[row_count][element_index] = absolute_seconds
                        total_seconds += absolute_seconds
                    else:
                        sys.stderr.write('The URC turned a date field for row ' + str(row_count) + ' into something unparseable: ' + str(csv_list_of_rows[row_count][element_index]) + ' so we are dropping the row\n')
                        del csv_list_of_rows[row_count]
                        row_count -= 1
                for sum_result_column_index in sum_result_column_indices:
                    csv_list_of_rows[row_count][sum_result_column_index] = str(total_seconds)
            except Exception as ex:
                sys.stderr.write('Row ' + str(row_count) + ' causes an exception so we will leave this time alone: ' + str(ex) + '\n')
        row_count += 1
    return csv_list_of_rows

def main():
    parser = argparse.ArgumentParser(description='This program takes in a csv file and normalizes it.')
    parser.add_argument("input_file", help="this is the csv file you want the program to use as csv format input")
    parser.add_argument("output_file", help="this is the csv file you want the program to use as csv format output")
    args = parser.parse_args()

    # Add O(n) time complexity assuming the number of columns and characters per field in the csv are constant
    parsed_csv_list = read_csv(args.input_file)

    # debug statement to print out how the csv was parsed
    #print(str(parsed_csv_list))

    # Add O(n) time complexity assuming the number of columns in the database are constant
    parsed_csv_list = change_date(parsed_csv_list, 'Timestamp', '%m/%d/%y %I:%M:%S %p', 7200)

    # Add O(n) time complexity assuming the number of columns in the database are constant
    parsed_csv_list = format_zips(parsed_csv_list, 'ZIP')

    # Add O(n) time complexity assuming the number of columns in the database are constant
    parsed_csv_list = names_to_uppercase(parsed_csv_list, 'FullName')

    # Add O(n) time complexity assuming the number of columns in the database are constant
    parsed_csv_list = sum_times(parsed_csv_list, 'FooDuration', 'BarDuration', 'TotalDuration')

    # Add O(n) time complexity assuming the number of columns in the database are constant
    output_csv_list_of_rows(parsed_csv_list, args.output_file)

if __name__ == '__main__':
    main()
