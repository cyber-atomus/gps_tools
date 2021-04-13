#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sats=0
used=0
sat_name=[]
sat_pwr=[]
sat_ena=[]

#json from gpspipe
jsonf='/tmp/gps1.json'
#output
gpspng='/tmp/gps-plot.png'

# all happens here
with open(jsonf) as data_file:
    data = json.load(data_file)
    for satelita in data:
        sats+=1
        if(satelita['used']==bool("true")):
            used+=1
            sat_ena.append("1")
            sat_name.append(str(satelita['PRN']))
        else:
            sat_ena.append("0")
            sat_name.append(str(satelita['PRN']))
        sat_pwr.append(satelita['ss'])


print(sats)
print(used)

#print(sat_name)
#print(sat_pwr)
#print(sat_ena)

col = []
col_b = []
for index,val in enumerate(sat_pwr):
    if((10 > val) and (sat_ena[index]=="1")):
        col.append('#D50000')
        col_b.append('#ECEFF1')
    elif(10 <= val <= 20) and (sat_ena[index]=="1"): 
        col.append('#DD2C00')
        col_b.append('#1B5E20')
    elif(20 < val < 27) and (sat_ena[index]=="1"): 
        col.append('#FF6D00')
        col_b.append('#1B5E20')
    elif(27 <= val) and (sat_ena[index]=="1"): 
        col.append('#00C853')
        col_b.append('#1B5E20')
    else:
        col.append('#EDE7F6')
        col_b.append('#ECEFF1')

#        sat_name[index]=sat_name[index]+"\nD"
matplotlib.rc('axes',edgecolor='#E0E0E0')
plt.rcParams['savefig.facecolor']='#263238'

fig, ax = plt.subplots(figsize=(7.5, 3))
#fig = plt.figure()

g = np.arange(sats)

p1 = ax.bar(g, sat_pwr, width=0.9, align='center', color=col, edgecolor = 'black', label="A")
for index,val in enumerate(sat_pwr):
    opis = str(sat_pwr[index])
    if(sat_ena[index]=="0"):
        opis="DI\n"+opis
    else:
        opis="OK\n"+opis
    ax.text(index-0.35, val/sat_pwr[index]+3 ,opis, fontsize=11,fontweight='bold', color='#212121')



ax.patch.set_facecolor('#263238')
fig.set_facecolor('#37474F')

ax.tick_params(axis='x', colors='#E0E0E0')
ax.tick_params(axis='y', colors='#E0E0E0')

ax.set_ylabel('SNR (dB)', color='#E0E0E0')
ax.set_title('Siła sygnału GPS', color='#E0E0E0')

ax.set_xticks(g)
ax.set_xticklabels((sat_name))
#ax.legend()

#ax.bar_label(p1, label_type='center')

plt.savefig(gpspng, dpi=80)
