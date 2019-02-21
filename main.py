#!/usr/bin/env python3
import csv
import mysql.connector
import sys
import os
from converter import convert

dbQuery = """select t.idsite, t.idtransaccionsite, t.idestado, group_concat(st.idsite), c.resultadocs, t.intentos
from spstransac t  
left join spstransac_cybersource c on c.idtransaccion = t.idtransaccion
left join spstransac_subtransac tst on tst.idtransaccion = t.idtransaccion 
left join spstransac st on st.idtransaccion = tst.idsubtransaccion 
where t.distribuida is null or t.distribuida = "F"
group by t.idtransaccion
order by t.idsite, t.idtransaccionsite"""

print("Connecting to Mysql")
db = mysql.connector.connect(
  host=os.getenv("MYSQL_HOST","127.0.0.1"),
  port=os.getenv("MYSQL_PORT","3306"),
  user=os.getenv("MYSQL_USER","spsT_usr"),
  passwd=os.getenv("MYSQL_PASSWORD","veef8Eed"),
  db=os.getenv("MYSQL_DB","sps433")
)
cur=db.cursor()
print("Executing query")
cur.execute(dbQuery)

convert(cur)