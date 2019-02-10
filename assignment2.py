#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 2 - Assignment 2"""

import csv
import urllib2
from datetime import datetime
import logging
import argparse
from pprint import pprint


def downloadData(url):
    """
    Takes in a string containing a URL and returns
    the raw data for processing. 

    Args:
        url (str): URL string.

    Returns:
        response: Raw text data from link.
    """

    response = urllib2.urlopen(url)
    return response


def processData(data):
    """
    Accepts raw text data from CSV file and processes
    the data. This function formats the data then checks
    if there are any bad values. Any rows containing an
    invalid data format will not be inserted into the new
    dictionary.

    Args:
        data (str): Raw text passed returned from downloadData().

    Returns:
        new_data (dict): A dictionary with valid data, with IDs mapped
        to tuples of names and datetime objects.
    """

    # Getting a logger with the appropriate name
    error_logger = logging.getLogger('assignment2')

    new_data = {}

    # Counter will track the ID
    counter = 1
    csv_data = csv.DictReader(data)

    for row in csv_data:
        try:
            for key, val in row.iteritems():
                if key == 'birthday':
                    birthday = datetime.strptime(val, '%m/%d/%Y')
                if key == 'id':
                    id_num = int(val)
                if key == 'name':
                    name = val
            new_data[id_num] = (name, birthday)
        except Exception:
            error_logger.error(' Error processing line #{} for ID #{}.'.format(
                csv_data.line_num, counter))
            counter += 1
            continue
        counter += 1

    return new_data


def displayPerson(id_num, personData):
    """[summary]

    Searches the returned dictionary from processData().
    This function then returns the requested user information
    in a formatted string. 

    Args:
        id_num (int): The user ID.
        personData (dict): Dictionary containing user data.
    """

    try:
        user_id = int(id_num)
        name = personData[user_id][0]
        birthday = personData[user_id][1]
        print 'Person #{} is {} with a birthday of {}.'.format(
            user_id, name, str(birthday.date()))
    except LookupError as err:
        print "No user found with that ID."
    except Exception as err:
        print err


def main():
    """
    This program requires a URL string linking to a CSV file to be
    passed as an argument to a single parameter. The data from the 
    file will be downloaded and processed. The data will be parsed 
    and bad data will be discarded whilst being error logged. A user 
    must input a valid ID in order to retrieve the user's data. In 
    order to exit the program, a negative integer or 0 must be input.   
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str,
                        help='Enter a link to a valid CSV file.')
    args = parser.parse_args()

    # Setting logger level and output file
    logging.basicConfig(filename='error.log', level=logging.ERROR)

    try:
        csvData = downloadData(args.url)
    except Exception:
        print 'ERROR: Something went wrong...'
        return

    personData = processData(csvData)

    while True:
        try:
            id_input = int(raw_input('Enter a user ID for lookup: '))

            if id_input <= 0:
                break
            displayPerson(id_input, personData)
        except ValueError:
            print 'Only integer values are accepted.'
        except Exception as err:
            print err


if __name__ == '__main__':
    main()
