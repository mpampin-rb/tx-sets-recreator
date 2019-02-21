#!/usr/bin/env python3
import csv
import logging
from converter import convert

logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s', level=logging.INFO)

with open('temp.csv', 'r') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  convert(csvreader)

