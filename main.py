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
  and t.idsite in ({2}) and t.fechainicio > "{3}"
group by t.idtransaccion
order by t.idsite, t.idtransaccionsite
limit {0} OFFSET {1}"""

safeMode=os.getenv("SAFE_MODE","true") == "true"
deleteOld=os.getenv("DELETE_OLD","true") == "true"
logging.info(
  "Running in safe mode. This means that I'll create keys with different names and then replace old ones." if safeMode
  else "WARNING: running in not safe mode. This means that I'll delete keys and create new ones with the same name."
)

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
fechainicio = os.getenv("START_DATE","2019-01-01")
sites = os.getenv("SITE_LIST","99999990,28464383,00120418").split(",")
sitesStr = ",".join(list(map(lambda site: "\"{0}\"".format(site), sites)))

if not safeMode and deleteOld:
  logging.info("Deleting sites sets")
  for site in sites:
    logging.info("Deleting sites:{0}:tx".format(site))
    r.delete("sites:{0}:tx".format(site))
    
while True:
  
  cur=db.cursor()
  logging.info("Executing query with from page {0} limit {1}".format(page,limit))
  dbQuery = rawQuery.format(limit, page * limit,sitesStr,fechainicio)
  cur.execute(dbQuery)
  result = cur.fetchall()
  convert(result, safeMode, r)

  if len(result) < limit:
    break
    
  page += 1

if safeMode:
  logging.info("Deleting old sets and renaming new ones")
  for site in sites:
    logging.info("Deleting and renaming {0}".format(site))
    r.delete("sites:{0}:tx".format(site))
    r.rename("sites:{0}:tx:new".format(site), "sites:{0}:tx".format(site))

