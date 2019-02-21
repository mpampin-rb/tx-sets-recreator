select t.idsite, t.idtransaccionsite, t.idestado, group_concat(st.idsite), c.resultadocs, t.intentos
from spstransac t  
left join spstransac_cybersource c on c.idtransaccion = t.idtransaccion
left join spstransac_subtransac tst on tst.idtransaccion = t.idtransaccion 
left join spstransac st on st.idtransaccion = tst.idsubtransaccion 
group by t.idtransaccion
order by 1
INTO OUTFILE '/var/lib/mysql-files/tx2.csv' 
CHARACTER SET utf8 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'