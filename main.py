#!/usr/bin/env python3
import csv
import mysql.connector
import redis
import sys
import os
import logging
from converter import convert

logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s', level=logging.INFO)

rawQuery = """select t.idsite, t.idtransaccionsite, t.idestado, group_concat(st.idsite), c.resultadocs, t.intentos, t.idtransaccion
from spstransac t  
left join spstransac_cybersource c on c.idtransaccion = t.idtransaccion
left join spstransac_subtransac tst on tst.idtransaccion = t.idtransaccion 
left join spstransac st on st.idtransaccion = tst.idsubtransaccion 
where (t.distribuida is null or t.distribuida = "F")
group by t.idtransaccion
order by t.idsite, t.idtransaccionsite
limit {0} OFFSET {1}"""

logging.info("Connecting to Mysql")
db = mysql.connector.connect(
  host=os.getenv("MYSQL_HOST","127.0.0.1"),
  port=os.getenv("MYSQL_PORT","3306"),
  user=os.getenv("MYSQL_USER","spsT_usr"),
  passwd=os.getenv("MYSQL_PASSWORD","veef8Eed"),
  db=os.getenv("MYSQL_DB","sps433")
)
logging.info("Connected")

logging.info("Connecting to Redis")
r = redis.Redis(host=os.getenv("REDIS_HOST","127.0.0.1"), port=os.getenv("REDIS_PORT","6379"), db=0)
logging.info("Connected")

page = 0
limit = int(os.getenv("QUERY_LIMIT","100000"))
while True:

  cur=db.cursor()
  logging.info("Executing query with from page {0} limit {1}".format(page,limit))
  dbQuery = rawQuery.format(limit, page * limit)
  cur.execute(dbQuery)
  result = cur.fetchall()
  if len(result) == 0:
    break

  convert(result, r)
  page += 1


