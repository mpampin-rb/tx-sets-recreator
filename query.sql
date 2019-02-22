select t.idsite, t.idtransaccionsite, t.idestado, group_concat(st.idsite), c.resultadocs, t.intentos, t.idtransaccion
from spstransac t  
left join spstransac_cybersource c on c.idtransaccion = t.idtransaccion
left join spstransac_subtransac tst on tst.idtransaccion = t.idtransaccion 
left join spstransac st on st.idtransaccion = tst.idsubtransaccion 
where (t.distribuida is null or t.distribuida = "F") 
  and t.idsite in ({2}) and t.fechainicio > "{3}"
group by t.idtransaccion
order by t.idsite, t.idtransaccionsite
INTO OUTFILE '/var/lib/mysql-files/tx2.csv' 
CHARACTER SET utf8 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'