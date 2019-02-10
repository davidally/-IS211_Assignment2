#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import urllib2
from datetime import datetime
import logging
import argparse
from pprint import pprint

URL = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'


def downloadData(url):

    response = urllib2.urlopen(url)
    return response


def processData(data):

    error_logger = logging.getLogger('assignment2')

    new_data = {}

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

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str,
                        help='Please enter a link to a CSV file.')
    args = parser.parse_args()

    logging.basicConfig(filename='error.log', level=logging.ERROR)

    try:
        csvData = downloadData(args.url)
    except Exception:
        print 'ERROR: Something went wrong...'
        return

    personData = processData(csvData)

    while True:
        try:
            id_input = raw_input('Enter a user ID for lookup:')

            if int(id_input) <= 0:
                break

            displayPerson(id_input, personData)
        except ValueError:
            print 'Only integer values are accepted.'
        except Exception as err:
            print err


if __name__ == '__main__':
    main()
