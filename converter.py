#!/usr/bin/env python3
import os
import logging

def convert(rows, safeMode, r): 
  
  csConverter = {
    "AMARILLO": "yellow",
    "AZUL": "blue",
    "NEGRO": "black",
    "ROJO": "red",
    "VERDE": "green"
  }

  opDictionary = {}
  lastSite = None
  lastIdTx = None
  keySuffix = ":new" if safeMode else ""

  for row in rows:
    idSite = row[0].decode("utf-8")
    idOp = row[1].decode("utf-8")
    txState = row[2]
    subTx = row[3]
    fraudDetection = row[4]
    retries = int(row[5])
    idTx = int(row[6])

    if lastSite is not None and (idSite != lastSite or len(opDictionary) > 100000):
      logging.info("Saving site {0} with {1} items".format(lastSite, len(opDictionary)))
      r.hmset("sites:"+lastSite+":tx"+keySuffix, opDictionary)
      opDictionary = {}
    
    lastSite = idSite
    lastIdTx = idTx
    
    opDictionary[idOp + ":status"] = txState
    if txState != 4:
      opDictionary[idOp + ":reps"] = retries + 1
      opDictionary[idOp + ":paymentType"] = "N" if subTx is None else "S"
      
      if fraudDetection is not None:
        opDictionary[idOp + ":fraudDetectionDecision"] = csConverter[fraudDetection]
      
      if subTx is not None:
        opDictionary[idOp + ":countSubpayments"] = subTx
  
  logging.info("Saving site {0} with {1} items".format(lastSite, len(opDictionary)))
  r.hmset("sites:"+lastSite+":tx"+keySuffix, opDictionary)

  return lastIdTx