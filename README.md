# Tx sets replicator
Replicador de sets con solo los últimos ids usados (limpia los ids anteriores a una fecha). Lo que hace es levantar de la base del sac todos los datos de las transacciones de los id sites indicados posteriores a la fecha indicada y recrear los sets de redis con la key "sites:*siteid*:tx"

## Cómo usar
Hay que bajar la imagen registry-desa.prismamediosdepago.com/decidir2/tx-sets-replicator:latest y ejecutarla con las variables de entorno necesarias

```
docker pull docker run registry-desa.prismamediosdepago.com/decidir2/tx-sets-replicator:0.0.1
docker run -it -e SITE_LIST=11111111,22222222,33333333 -e START_DATE=2019-01-01 registry-desa.prismamediosdepago.com/decidir2/tx-sets-replicator:0.0.1
```

## Variables de configuración
Se pueden cambiar las siguientes variables de entorno:
- **MYSQL_HOST:** IP o host del mysql *(default 127.0.0.1)*
- **MYSQL_PORT:** puerto del mysql *(default 3306)*
- **MYSQL_USER:** Usuario del mysql *(default spsT_usr)*
- **MYSQL_PASSWORD:** Password del mysql
- **MYSQL_DB:** Database del mysql *(default sps433)*
- **REDIS_HOST:** Host de redis *(default 127.0.0.1)*
- **REDIS_PORT:** Port de redis *(default 6379)*
- **QUERY_LIMIT:** Cantidad de TX que trae de la base en cada ciclo *(default 100000)*
- **START_DATE:** Fecha desde la que toma las transacciones, usando la fechainicio de la tabla spstransac *(default sps433)*
- **SITE_LIST:** Listado de sitios a volver a generar los sets en redis, separados por coma (por ejemplo, "11111111,22222222,33333333")
- **SAFE_MODE:** Si usa el modo seguro, arma un nuevo set para cada sitio y al final elimina el viejo y renombra el nuevo. Caso contrario, primero borra el set y luego lo sobreescribe. Valores True o False *(default True)*
- **DELETE_OLD:** Solo se usa si SAFE_MODE es False. Si DELETE_OLD es True, va a borrar el viejo set y crear uno nuevo. Si es False, va a escribir los campos sobre el set ya existente. *(default True)*


