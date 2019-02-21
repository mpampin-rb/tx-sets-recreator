#!/usr/bin/env python3
import csv
from converter import convert

with open('temp.csv', 'r') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  convert(csvreader)

