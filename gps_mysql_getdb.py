#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import datetime
from time import gmtime, strftime
import subprocess
import os
import os, shutil
import re
import sys
import signal
import json
import MySQLdb

dbase_user=''
dbase_pass=''
dbase_host=''
dbase_base=''

## create table gps
#  id int not null auto_increment primary key
#  timestamp timestamp
#  prn int(5)
#   az int(5)
#   el int(5)
#   ss int(5)
# used tinyint(1));
####

sat_name=[]
sat_pwr=[]
sat_ena=[]


#        print(satelita['ss'])

def getprnlist():
    try:
        prn=[]
        db=MySQLdb.connect(dbase_host, dbase_user, dbase_pass, dbase_base)
        cur=db.cursor()
        query="select distinct prn from gps"
        cur.execute(query)
        rekordy = cur.fetchall()
        for sats in rekordy:
            prn.append(int(sats[0]))
        return(prn)
    except Exception as exc:
        print("Something wrong: "+str(exc)+"!")

def getfromdb(prn, date):
    now = time.time()
    prn=prn
    az=[]
    el=[]
    ss=[]
    ts=[]
    try:
        db=MySQLdb.connect(dbase_host, dbase_user, dbase_pass, dbase_base)
        cur=db.cursor()
        query="select unix_timestamp(timestamp), prn, az, el, ss, used from gps where prn='"+str(prn)+"'"
        cur.execute(query)
        rekordy = cur.fetchall()
        for row in rekordy:
            sat_ts=int(row[0])
            ts.append(sat_ts)
            sat_az=int(row[2])
            az.append(sat_az)
            sat_el=int(row[3])
            el.append(sat_el)
            sat_ss=int(row[4])
            ss.append(sat_ss)
        cur.close()
#        print(el)
#        print(az)
#        print(ss)
        return(ts, az, el, ss)
    except Exception as exc:
        print("Something wrong: "+str(exc)+"!")


try:
    listPRN=getprnlist()
    print("Satki w bazie: "+str(listPRN))
    ktory = input("która satelita? ->> ")
    PRN=ktory
    lista=getfromdb(PRN,"2021-04-13")
    ts=lista[0]
    az=lista[1]
    el=lista[2]
    ss=lista[3]
    for g in enumerate(lista[0]):
        numer=g[0]
#        print(count(numer))
#        print lista[1][numer]
#        print lista[2][numer]
        print("Sat PRN:"+str(PRN)+" | ts: "+str(ts[numer])+" | azi: "+str(az[numer])+"° | ele: "+str(el[numer])+"° | moc: "+str(ss[numer])+"dBHz")
except Exception as exc:
    print("ERR: "+str(exc))
