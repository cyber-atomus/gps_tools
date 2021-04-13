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

def addtodb(prn, az, el, ss, used):
    now = time.time()
    prn=int(prn)
    az=int(az)
    el=int(el)
    ss=int(ss)
    if (used == bool("true")):
        used=int(1)
    elif (used == bool("false")):
        used=int(0)
    else:
        used=int(0)
    try:
        db=MySQLdb.connect(dbase_host, dbase_user, dbase_pass, dbase_base)
        cur=db.cursor()
#        print(str(now))
        cur.execute("""INSERT INTO gps(timestamp,prn,az,el,ss,used) VALUES (from_unixtime(%s),%s,%s,%s,%s,%s)""",(now,prn,az,el,ss,used))
        db.commit()
#        print("Added to DB")
    except Exception as exc:
        print("Something wrong: "+str(exc)+"!")

def getgps():
    sats=0
    used=0
    with open('/tmp/gps1.json') as data_file:
        data = json.load(data_file)
        for satelita in data:
            sats+=1
            if(satelita['used']==bool("true")):
                sat_ena.append("0")
                used+=1
            else:
                sat_ena.append("0")
#            print(str(satelita['PRN'])+" "+str(satelita['az']))
            addtodb(satelita['PRN'], satelita['az'], satelita['el'], satelita['ss'], satelita['used'])
try:
    getgps()
except Exception as exc:
    print("ERR: "+str(exc))
