#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import warnings

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from matplotlib import gridspec

from datetime import datetime


sats=0
used=0
sat_name=[]
sat_pwr=[]
sat_ena=[]
sat_ele=[]
sat_azi=[]
czas=datetime.now().replace(second=0, microsecond=0)

with open('/tmp/gps1.json') as data_file:
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
        sat_ele.append(90-satelita['el'])
        sat_azi.append(satelita['az'])


#print(sats)
#print(used)

#print(sat_name)
#print(sat_ele)
#print(sat_azi)

col = []
col_b = []
font2 = {'color':  '#00796B',
        'size': 12,
        }
matplotlib.rc('axes',edgecolor='#E0E0E0')
plt.rcParams['savefig.facecolor']='#263238'

theta=np.radians(sat_azi)
#theta=np.radians(sat_azi)
zeniths=sat_ele
#plt.ioff()

fig, (ax1, ax2) = plt.subplots(1, 2)

fig = matplotlib.pyplot.figure(figsize=(12, 3.5))
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 4]) 

ax1 = plt.subplot(gs[0], projection='polar',  axisbg='#ECEFF1')  # create figure & 1 axis

ax1.patch.set_facecolor('#263238')
#fig.set_facecolor('#37474F')

ax1.set_xticklabels([])
ax1.set_yticklabels([])
gridX,gridY = 30.0,30.0
parallelGrid = np.arange(-90.0,90.0,gridX)
meridianGrid = np.arange(-180.0,180.0,gridY)

ax1.text(0.5,1.025,'N',transform=ax1.transAxes,horizontalalignment='center',verticalalignment='bottom',size=14)

for para in np.arange(gridY,360,gridY):
    x= (1.1*0.5*np.sin(np.deg2rad(para)))+0.5
    y= (1.1*0.5*np.cos(np.deg2rad(para)))+0.5
    if(para==90.0): ax1.text(x,y,'E',transform=ax1.transAxes,horizontalalignment='center',verticalalignment='center',size=14)
    elif(para==180.0): ax1.text(x,y,'S',transform=ax1.transAxes,horizontalalignment='center',verticalalignment='center',size=14)
    elif(para==270.0): ax1.text(x,y,'W',transform=ax1.transAxes,horizontalalignment='center',verticalalignment='center',size=14)
    else: ax1.text(x,y,u'%i\N{DEGREE SIGN}'%para,transform=ax1.transAxes,horizontalalignment='center',verticalalignment='center',fontdict=font2)

ax1.set_aspect('auto',adjustable='datalim')
ax1.set_autoscale_on(True)
ax1.set_rmax(90)
ax1.set_theta_zero_location("N")
ax1.set_theta_direction(-1)

#ax1.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*90, color='#0d47a1', linestyle='-')
#ax1.plot(theta,zeniths,'-',color='#00695C',lw=2)
for index,val in enumerate(sat_pwr):
    if((10 > val) and (sat_ena[index]=="1")):
        ax1.scatter(theta[index],zeniths[index], color='#D50000', s=int(sat_pwr[index]*15))
        ax1.text(theta[index],zeniths[index],str(sat_name[index]),horizontalalignment='center',verticalalignment='center',size=12,color='white')
        col_b.append('#ECEFF1')
        col.append('#D50000')
    elif(10 <= val <= 20) and (sat_ena[index]=="1"): 
        ax1.scatter(theta[index],zeniths[index], color='#DD2C00', s=int(sat_pwr[index]*15))
        ax1.text(theta[index],zeniths[index],str(sat_name[index]),horizontalalignment='center',verticalalignment='center',size=12,color='#263238')
        col_b.append('#1B5E20')
        col.append('#DD2C00')
    elif(20 < val < 27) and (sat_ena[index]=="1"): 
        ax1.scatter(theta[index],zeniths[index], color='#FF6D00', s=int(sat_pwr[index]*15))
        ax1.text(theta[index],zeniths[index],str(sat_name[index]),horizontalalignment='center',verticalalignment='center',size=12,color='#263238')
        col_b.append('#1B5E20')
        col.append('#FF6D00')
    elif(27 <= val) and (sat_ena[index]=="1"): 
        ax1.scatter(theta[index],zeniths[index], color='#00C853', s=int(sat_pwr[index]*15))
        ax1.text(theta[index],zeniths[index],str(sat_name[index]),horizontalalignment='center',verticalalignment='center',size=12,color='#263238')
        col_b.append('#1B5E20')
        col.append('#00C853')
    else:
        ax1.scatter(theta[index],zeniths[index], color='#EDE7F6', s=int(sat_pwr[index]*15))
        ax1.text(theta[index],zeniths[index],str(sat_name[index]),horizontalalignment='center',verticalalignment='center',size=12,color='#263238')
        col_b.append('#ECEFF1')
        col.append('#EDE7F6')
dc=0.01

## DRUGI
g = np.arange(sats)

ax2 = plt.subplot(gs[1])

p1 = ax2.bar(g, sat_pwr, width=0.9, align='center', color=col, edgecolor="#263238", label="A")
for index,val in enumerate(sat_pwr):
    opis = str(sat_pwr[index])
    if(sat_ena[index]=="0"):
        opis="DI\n"+opis
    else:
        opis="OK\n"+opis
    ax2.text(index-0.35, val/sat_pwr[index]+3 ,opis, fontsize=11,fontweight='bold', color='#212121')



ax2.patch.set_facecolor('#263238')
fig.set_facecolor('#37474F')

ax2.tick_params(axis='x', colors='#E0E0E0')
ax2.tick_params(axis='y', colors='#E0E0E0')

ax2.set_ylabel('SNR (dB)', color='#E0E0E0')
ax2.set_title('widoczne:'+str(sats)+"   |   w użyciu:"+str(used)+"   |  "+str(czas), color='#E0E0E0')

ax2.set_xticks(g)
ax2.set_xticklabels((sat_name))

#gs.tight_layout(fig)
#plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    plt.savefig('/tmp/gps_plot2.png', dpi=80, bbox_inches='tight')

plt.close()    # close the figure
