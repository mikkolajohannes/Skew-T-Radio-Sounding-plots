# coding=utf-8
import os,sys,string,requests
import xml.etree.ElementTree as ET
import os,sys,string,requests
import xml.etree.ElementTree as ET
import math
import matplotlib as plt
import numpy as np
import pandas as pd
import arrow
import string
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units

def height2pressure(height):
    t0 = 288
    gamma = 6.5*0.001
    p0 = 1013.25
    g = 9.81
    Rd = 287.00
    return p0 * (1 - (gamma / t0) * height) ** (g / (Rd * gamma))

def getWindComponent(speed,wdir):
    u = -speed * np.sin(2*np.pi*wdir/360)
    v = -speed * np.cos(2*np.pi*wdir/360)
    return u, v

def fmi2skewt(station,time,img_name):

    apikey='e72a2917-1e71-4d6f-8f29-ff4abfb8f290'

    url = 'http://data.fmi.fi/fmi-apikey/' + str(apikey) + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::sounding::multipointcoverage&fmisid=' + str(station) + '&starttime=' + str(time) + '&endtime=' + str(time) + '&'

    req = requests.get(url)
    xmlstring = req.content
    tree=ET.ElementTree(ET.fromstring(xmlstring))
    root = tree.getroot()

    #reading location and time data to "positions" from XML
    positions = ""
    for elem in root.getiterator(tag='{http://www.opengis.net/gmlcov/1.0}positions'):
        positions = elem.text

    #'positions' is string type variable
    #--> split positions into a list by " "
    #then remove empty chars and "\n"
    # from pos_split --> data into positions_data

    try:
	       pos_split = positions.split(' ')
    except NameError:
	       return "Sounding data not found: stationid " + station + " time " + time

    pos_split = positions.split(' ')

    positions_data = []
    for i in range(0,len(pos_split)):
        if not (pos_split[i] == "" or pos_split[i] == "\n"):
            positions_data.append(pos_split[i])

    #index for height: 2,6,10 etc in positions_data
    height = []
    myList = range(2,len(positions_data))
    for i in myList[::4]:
        height.append(positions_data[i])

    p = []
    for i in range(0,len(height)):
        p.append(height2pressure(float(height[i])))

    #reading wind speed, wind direction, air temperature and dew point data to 'values'
    values = ""
    for elem in root.getiterator(tag='{http://www.opengis.net/gml/3.2}doubleOrNilReasonTupleList'):
        values = elem.text

    #split 'values' into a list by " "
    #then remove empty chars and "\n"

    val_split = values.split(' ')
    values_data = []
    for i in range(0,len(val_split)):
        if not(val_split[i] == "" or val_split[i]=="\n"):
            values_data.append(val_split[i])

    #data in values_data: w_speed, w_dir, t_air, t_dew
    wind_speed = []
    wind_dir = []
    T = []
    Td = []
    myList = range(0,len(values_data))
    for i in myList[::4]:
        wind_speed.append(float(values_data[i]))
        wind_dir.append(float(values_data[i+1]))
        T.append(float(values_data[i+2]))
        Td.append(float(values_data[i+3]))

    if stationid == "101104":
        loc_time = "Jokioinen Ilmala " + time
    elif stationid == "101932":
        loc_time = "Sodankyla Tahtela " + time
    else:
        return None

    #calculate wind components u,v:
    u = []
    v = []
    for i in range(0,len(wind_speed)):
        u1, v1 = getWindComponent(wind_speed[i], wind_dir[i])
        u.append(u1)
        v.append(v1)

    #find index for pressure < 100hPa (for number of wind bars)
    if min(p)>100:
        wthin = len(p)/20
        u_plot = u
        v_plot = v
        p_plot = p
    else:
        for i in range(0,len(p)):
            if p[i]-100<=0:
                wthin = i/20
                u_plot = u[0:i]
                v_plot = v[0:i]
                p_plot = p[0:i]
                break;

    #units
    wind_speed = wind_speed*units("m/s")
    wind_dir = wind_dir*units.deg
    T = T*units.degC
    Td = Td*units.degC
    p = p*units("hPa")

    #calculate pwat, lcl, cape, cin and plot cape
    pwat = mpcalc.precipitable_water(Td,p,bottom=None,top=None)
    lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])
    prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')

    try:
        cape,cin = mpcalc.cape_cin(p,T,Td,prof)
    except IndexError:
        cape = 0*units("J/kg")
        cin = 0*units("J/kg")

    #__________________plotting__________________
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig, rotation=45)
    font_par = {'family': 'monospace',
        'color':  'darkred',
        'weight': 'normal',
        'size': 10,
        }
    font_title = {'family': 'monospace',
        'color':  'black',
        'weight': 'normal',
        'size': 20,
        }
    font_axis = {'family': 'monospace',
        'color':  'black',
        'weight': 'normal',
        'size': 10,
        }
    # Plot the data using normal plotting functions, in this case using
    # log scaling in Y, as dictated by the typical meteorological plot
    skew.plot(p, T, 'k')
    skew.plot(p, Td, 'b')
    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(-50, 30)
    skew.plot_barbs(p_plot[0::wthin], u_plot[0::wthin], v_plot[0::wthin])
    skew.plot_dry_adiabats(alpha=0.4)
    skew.plot_moist_adiabats(alpha=0.4)
    skew.plot_mixing_lines(alpha=0.4)
    #skew.shade_cape(p, T, prof,color="orangered")
    plt.title(loc_time,fontdict=font_title)
    plt.xlabel("T (C)",fontdict=font_axis)
    plt.ylabel("P (hPa)",fontdict=font_axis)

    #round and remove units from cape,cin,plcl,tlcl,pwat
    if cape.magnitude > 0:
        capestr = str(np.round(cape.magnitude))
    else:
        capestr = "NaN"

    if cin.magnitude > 0:
        cinstr = str(np.round(cin.magnitude))
    else:
        cinstr = "NaN"

    lclpstr = str(np.round(lcl_pressure.magnitude))
    lclTstr = str(np.round(lcl_temperature.magnitude))
    pwatstr = str(np.round(pwat.magnitude))

#    str_par = "CAPE[J/kg]=" + capestr + " CIN[J/kg]=" + cinstr + " Plcl[hPa]=" + lclpstr + " Tlcl[C]=" + lclTstr + " pwat[mm]=" + pwatstr
#    font = {'family': 'monospace',
#        'color':  'darkred',
#        'weight': 'normal',
#        'size': 10,
#        }
#    plt.text(-20,1250,str_par,fontdict=font_par)
    save_file = img_name
    plt.savefig(save_file)

#Johannes Mikkola, 8/2018
#FMI open radiosounding data to Skew-T diagram

#python fmi2skewt_metpy.py 101104 2018-08-27T12:00:00Z pdf


stationid = sys.argv[1] #Jokioinen=101104 Sodankylä=101932
time = sys.argv[2] #Jokioinen 00, 06, 12 and 18, Sodankylä 00 and 12
fileformat = "." + sys.argv[3] #png or pdf

time_for_imgname = time.replace(":","_").replace(".","_").replace("-","_").replace(":00:00:00","")

if stationid == "101104":
    station = "Jokioinen"
elif stationid == "101932":
    station = "sodankyla"

img_name = station + "_" + time_for_imgname + fileformat

try:
    fmi2skewt(stationid,time,img_name)
except ValueError:
    print
    print "----------------------------------------------"
    print "Data not found: " + station + " " + time
    print "----------------------------------------------"
    print
