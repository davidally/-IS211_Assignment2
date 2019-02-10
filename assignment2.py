#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import urllib2
import datetime
import logging
import argparse
from pprint import pprint

URL = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'


def downloadData(url):

    response = urllib2.urlopen(url)
    return response


def processData(data=downloadData(URL)):

    new_data = {}
    counter = 1

    csv_data = csv.DictReader(data)
    for row in csv_data:
        try:
            for key, val in row.iteritems():
                if key == 'birthday':
                    birthday = datetime.datetime.strptime(val, '%m/%d/%Y')
                if key == 'id':
                    id_num = int(val)
                if key == 'name':
                    name = val
            new_data[id_num] = (name, birthday)
        except Exception:
            print 'ERROR: Date format issue with ID#: {}.'.format(counter)
            counter += 1
            continue
        counter += 1

    pprint(new_data)


processData()
