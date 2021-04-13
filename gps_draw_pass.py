#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import warnings
#import datetime
from time import gmtime, strftime
import subprocess
import os
import os, shutil
import re
import signal
import json
import MySQLdb

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from matplotlib import gridspec

from datetime import datetime


dbase_user=''
dbase_pass=''
dbase_host=''
dbase_base=''

outfile='/tmp/gps_plot_a.png'

data_teraz=datetime.now()

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



def getprnlist(data):
    try:
        prn=[]
        db=MySQLdb.connect(dbase_host, dbase_user, dbase_pass, dbase_base)
        cur=db.cursor()
        query="select distinct prn from gps where timestamp like '"+str(data)+"%'"
        cur.execute(query)
        rekordy = cur.fetchall()
        for sats in rekordy:
            prn.append(int(sats[0]))
        return(prn)
    except Exception as exc:
        print("Something wrong: "+str(exc)+"!")

def getfromdb(prn, date):
#    now = time.time()
    prn=prn
    az=[]
    el=[]
    ss=[]
    ts=[]
    us=[]
    try:
        db=MySQLdb.connect(dbase_host, dbase_user, dbase_pass, dbase_base)
        cur=db.cursor()
        query="select unix_timestamp(timestamp), prn, az, el, ss, used from gps where prn='"+str(prn)+"' AND timestamp like '"+str(data)+"%'"
        cur.execute(query)
        rekordy = cur.fetchall()
#        print(len(rekordy))
        for row in rekordy:
            sat_ts=int(row[0])
            ts.append(sat_ts)
            sat_az=int(row[2])
            az.append(sat_az)
            sat_el=int(row[3])
            el.append(sat_el)
            sat_ss=int(row[4])
            ss.append(sat_ss)
            sat_us=int(row[5])
            us.append(sat_us)
        cur.close()
        return(ts, az, el, ss, us)
    except Exception as exc:
        print("Something wrong: "+str(exc)+"!")

def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)
# Generate random colormap
def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np

    if type not in ('bright', 'soft'):
        print ('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in xrange(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in xrange(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')

    return random_colormap

#def plot(PRN, sat_azi, sat_ele, sat_pwr, sat_ena):
def plot(satki):
    font2 = {'color':  '#00796B', 'size': 12,}
    matplotlib.rc('axes',edgecolor='#E0E0E0')
    plt.rcParams['savefig.facecolor']='#263238'
    plt.ioff()


    fig, ax1 = plt.subplots()
    fig = matplotlib.pyplot.figure(figsize=(9, 6))
    ax1 = plt.subplot(111, projection='polar',  axisbg='#ECEFF1')  # create figure & 1 axis
    ax1.patch.set_facecolor('#263238')

    ax1.set_xticklabels([])
    ax1.set_yticklabels([])

    gridX,gridY = 45.0,45.0

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
    ax1.set_autoscale_on(False)
    ax1.set_rmax(90)
    ax1.set_theta_zero_location("N")
    ax1.set_theta_direction(-1)

    try:
        satkil=satki.keys()
        a=0.01
        c=1
        band_cnt=3*(len(satki))
        rnd_cmap = rand_cmap(band_cnt, type='bright', first_color_black=False, last_color_black=False, verbose=False)
        for key,val in satki.items():
            sat_azi=satki[key]['az']
            sat_ele=satki[key]['el']
            md = []
            for mx in sat_ele:
                if(mx<=0):
                    mx=mx*(-1)
                    if(mx>=90): mx=90
                md.append(90-mx)
            sat_max_str=max(satki[key]['ss'])
            theta=np.radians(sat_azi)
            zeniths=sat_ele
            items=len(sat_ele)
            kolor=rnd_cmap(c)
            ax1.scatter(theta, md, color=rnd_cmap(c), s=2)
            plt.figtext(0,0+a, "PRN: "+str(key).rjust(3,'0')+" | max: "+str(sat_max_str)+"dbHz | cnt:"+str(items).rjust(4,'0'), fontsize=11, color=rnd_cmap(c) ,ha="left")
            a+=0.03
            c+=2
    except Exception as ko:
            print("S:"+str(ko))
    dc=0.01

    fig.tight_layout()
    fig.subplots_adjust(left=.35)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.savefig(outfile, dpi=80, bbox_inches='tight')

    plt.close()    # close the figure



try:
    if((len(sys.argv)-1)>=1):
        kiedy=sys.argv[1]
    else:
        kiedy=raw_input("Podaj datę w formacie YYYY-mm-dd lub 'dzis': ")
    if(kiedy in ['dzis', 'dziś','dzisiaj','today', 'now', 'teraz']):
        data=data_teraz.strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(kiedy, "%Y-%m-%d")
            data=kiedy
        except Exception as err:
            print("Bledna data! Stosuje dzisiaj. "+str(err))
            data=data_teraz.strftime("%Y-%m-%d")

    listPRN=getprnlist(data)
    if(len(listPRN)>0):
        zk={}
        for d in listPRN:
            lista=getfromdb(d,data)
            zk[d] = {
            "ts" : lista[0],
            "az" : lista[1],
            "el" : lista[2],
            "ss" : lista[3],
            "us" : lista[4]
            }
        satki=zk.keys()

        print("Drawing for: "+str(satki))
        try:
            plot(zk)
        except Exception as ko:
            print("PLOT ERR:"+str(ko))
    else:
        print("Empty set")
        exit(0)

except Exception as exc:
    print("GENERAL ERR: "+str(exc))
