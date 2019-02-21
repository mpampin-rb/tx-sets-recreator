#!/usr/bin/env python3
import redis
import os
import logging

def convert(rows): 

  logging.info("Connecting to Redis")
  r = redis.Redis(host=os.getenv("REDIS_HOST","127.0.0.1"), port=os.getenv("REDIS_PORT","6379"), db=0)
  csConverter = {
    "AMARILLO": "yellow",
    "AZUL": "blue",
    "NEGRO": "black",
    "ROJO": "red",
    "VERDE": "green"
  }
  logging.info("Connected")

  opDictionary = {}
  lastSite = None
  lastIdOp = None

  for row in rows:
    idSite = row[0].decode("utf-8")
    idOp = row[1].decode("utf-8")
    txState = row[2]
    subTx = row[3]
    fraudDetection = row[4]
    retries = int(row[5])

    if lastSite is not None and (idSite != lastSite or len(opDictionary) > 100000):
      logging.info("Saving site {0} with {1} items".format(lastSite, len(opDictionary)))
      r.hmset("sites:"+lastSite+":tx", opDictionary)
      opDictionary = {}
    
    lastSite = idSite
    lastIdOp = idOp
    
    opDictionary[idOp + ":status"] = txState
    if txState != 4:
      opDictionary[idOp + ":reps"] = retries + 1
      opDictionary[idOp + ":paymentType"] = "N" if subTx is None else "S"
      
      if fraudDetection is not None:
        opDictionary[idOp + ":fraudDetectionDecision"] = csConverter[fraudDetection]
      
      if subTx is not None:
        opDictionary[idOp + ":countSubpayments"] = subTx
  
  r.hmset("sites:"+lastSite+":tx", opDictionary)

  return (lastSite, lastIdOp)