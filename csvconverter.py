#!/usr/bin/env python3
import csv
import logging
import redis
from converter import convert

logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s', level=logging.INFO)

logging.info("Connecting to Redis")
r = redis.Redis(host=os.getenv("REDIS_HOST","127.0.0.1"), port=os.getenv("REDIS_PORT","6379"), db=0)
logging.info("Connected")

with open('temp.csv', 'r') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  convert(csvreader, False, r)

