# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units

def dewpoint(e):
    a = 243.5*np.log(e/6.112)
    b = 17.67-np.log(e/6.122)
    return a/b

#script to compare NOAA IGRA monthly means on standard pressure levels
#jokioinen=FIM00002963 sodankyla=FIM00002836
#jokioinen 00UTC May 2018 compared to May 1988-2018:

#python noaa_comparison_skewt.py FIM00002963 00 5 2018 1988 2018

#get files temp_00z-mly.txt and vapr_00z-mly.txt (or 12utc) from NOAA IGRA


stationid = sys.argv[1]
time = sys.argv[2]
month = sys.argv[3]
year1 = sys.argv[4]
year2 = sys.argv[5]
year3 = sys.argv[6]

if stationid=="FIM00002963":
    station = "Jokioinen"
elif stationid=="FIM00002836":
    station = "Sodankyla"

print station + " " + time + "UTC month " + month + " year " + year1 + " compared to years from " + year2 + " to " + year3


#---------------------calculate mean temperatures from year2 to year3
#---------------------and read year1 temperatures in----------------
#-------------------------------------------------------------------

p = [9999, 1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20]
T_9999 = []
T_1000 = []
T_925 = []
T_850 = []
T_700 = []
T_500 = []
T_400 = []
T_300 = []
T_250 = []
T_200 = []
T_140 = []
T_100 = []
T_70 = []
T_50 = []
T_30 = []
T_20 = []

p_year1 = []
T_year1 = []

infile = "./temp_" + time + "z-mly.txt"
with open(infile) as data_file:
    for line in data_file:
        parts = line.split() # split line into parts
        if parts[0] == stationid and parts[1]==year1 and parts[2]==month:
            T_year1.append(0.1*float(parts[4]))
            p_year1.append(float(parts[3]))

        if parts[0] == stationid and int(parts[1])+1>int(year2) and int(parts[1])-1<int(year3) and parts[2]==month:
            if int(parts[3])==9999:
                T_9999.append(0.1*float(parts[4]))
            if int(parts[3])==1000:
                T_1000.append(0.1*float(parts[4]))
            if int(parts[3])==925:
                T_925.append(0.1*float(parts[4]))
            if int(parts[3])==850:
                T_850.append(0.1*float(parts[4]))
            if int(parts[3])==700:
                T_700.append(0.1*float(parts[4]))
            if int(parts[3])==500:
                T_500.append(0.1*float(parts[4]))
            if int(parts[3])==400:
                T_400.append(0.1*float(parts[4]))
            if int(parts[3])==300:
                T_300.append(0.1*float(parts[4]))
            if int(parts[3])==250:
                T_250.append(0.1*float(parts[4]))
            if int(parts[3])==200:
                T_200.append(0.1*float(parts[4]))
            if int(parts[3])==150:
                T_140.append(0.1*float(parts[4]))
            if int(parts[3])==100:
                T_100.append(0.1*float(parts[4]))
            if int(parts[3])==70:
                T_70.append(0.1*float(parts[4]))
            if int(parts[3])==50:
                T_50.append(0.1*float(parts[4]))
            if int(parts[3])==30:
                T_30.append(0.1*float(parts[4]))
            if int(parts[3])==20:
                T_20.append(0.1*float(parts[4]))

Temp_y1_to_y2 = []
Temp_y1_to_y2.append(np.mean(T_9999))
Temp_y1_to_y2.append(np.mean(T_1000))
Temp_y1_to_y2.append(np.mean(T_925))
Temp_y1_to_y2.append(np.mean(T_850))
Temp_y1_to_y2.append(np.mean(T_700))
Temp_y1_to_y2.append(np.mean(T_500))
Temp_y1_to_y2.append(np.mean(T_400))
Temp_y1_to_y2.append(np.mean(T_300))
Temp_y1_to_y2.append(np.mean(T_250))
Temp_y1_to_y2.append(np.mean(T_200))
Temp_y1_to_y2.append(np.mean(T_140))
Temp_y1_to_y2.append(np.mean(T_100))
Temp_y1_to_y2.append(np.mean(T_70))
Temp_y1_to_y2.append(np.mean(T_50))
Temp_y1_to_y2.append(np.mean(T_30))
Temp_y1_to_y2.append(np.mean(T_20))

Ty1y2_sd = []
Ty1y2_sd.append(np.std(T_9999))
Ty1y2_sd.append(np.std(T_1000))
Ty1y2_sd.append(np.std(T_925))
Ty1y2_sd.append(np.std(T_850))
Ty1y2_sd.append(np.std(T_700))
Ty1y2_sd.append(np.std(T_500))
Ty1y2_sd.append(np.std(T_400))
Ty1y2_sd.append(np.std(T_300))
Ty1y2_sd.append(np.std(T_250))
Ty1y2_sd.append(np.std(T_200))
Ty1y2_sd.append(np.std(T_140))
Ty1y2_sd.append(np.std(T_100))
Ty1y2_sd.append(np.std(T_70))
Ty1y2_sd.append(np.std(T_50))
Ty1y2_sd.append(np.std(T_30))
Ty1y2_sd.append(np.std(T_20))

T_min = []
T_max = []
for i in range(0,len(Temp_y1_to_y2)):
    T_min.append(Temp_y1_to_y2[i]-Ty1y2_sd[i])
    T_max.append(Temp_y1_to_y2[i]+Ty1y2_sd[i])

#-------------same operation to read vapor pressure and calculate dew point
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

Td_9999 = []
Td_1000 = []
Td_925 = []
Td_850 = []
Td_700 = []
Td_500 = []
Td_400 = []
Td_300 = []
Td_250 = []
Td_200 = []
Td_140 = []
Td_100 = []
Td_70 = []
Td_50 = []
Td_30 = []
Td_20 = []

pd_year1 = []
Td_year1 = []

infile = "./vapr_" + time + "z-mly.txt"
with open(infile) as data_file:
    for line in data_file:
        parts = line.split() # split line into parts
        if parts[0] == stationid and parts[1]==year1 and parts[2]==month:
            Td_year1.append(dewpoint(0.001*float(parts[4])))
            pd_year1.append(float(parts[3]))

        if parts[0] == stationid and int(parts[1])+1>int(year2) and int(parts[1])-1<int(year3) and parts[2]==month:
            if int(parts[3])==9999:
                Td_9999.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==1000:
                Td_1000.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==925:
                Td_925.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==850:
                Td_850.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==700:
                Td_700.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==500:
                Td_500.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==400:
                Td_400.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==300:
                Td_300.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==250:
                Td_250.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==200:
                Td_200.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==150:
                Td_140.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==100:
                Td_100.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==70:
                Td_70.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==50:
                Td_50.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==30:
                Td_30.append(dewpoint(0.001*float(parts[4])))
            if int(parts[3])==20:
                Td_20.append(dewpoint(0.001*float(parts[4])))

Td_y1_to_y2 = []
Td_y1_to_y2.append(np.mean(Td_9999))
Td_y1_to_y2.append(np.mean(Td_1000))
Td_y1_to_y2.append(np.mean(Td_925))
Td_y1_to_y2.append(np.mean(Td_850))
Td_y1_to_y2.append(np.mean(Td_700))
Td_y1_to_y2.append(np.mean(Td_500))
Td_y1_to_y2.append(np.mean(Td_400))
Td_y1_to_y2.append(np.mean(Td_300))
Td_y1_to_y2.append(np.mean(Td_250))
Td_y1_to_y2.append(np.mean(Td_200))
Td_y1_to_y2.append(np.mean(Td_140))
Td_y1_to_y2.append(np.mean(Td_100))
Td_y1_to_y2.append(np.mean(Td_70))
Td_y1_to_y2.append(np.mean(Td_50))
Td_y1_to_y2.append(np.mean(Td_30))
Td_y1_to_y2.append(np.mean(Td_20))

#----------------------------------print dT
#-----------------------------------------
#-----------------------------------------




#-------------------------------------UNITS
#------------------------------------------
#------------------------------------------

p = p*units("hPa")
p_year1 = p_year1*units("hPa")
pd_year1 = pd_year1*units("hPa")
T_min = T_min*units.degC
T_max = T_max*units.degC
Temp_y1_to_y2 = Temp_y1_to_y2*units.degC
Td_y1_to_y2 = Td_y1_to_y2*units.degC
T_year1 = T_year1*units.degC
Td_year1 = Td_year1*units.degC

#-------------------------------plotting
#--------------------------------------
#--------------------------------------

fig = plt.figure(figsize=(9,9))
skew = SkewT(fig,rotation=45)

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

skew.plot(p_year1, T_year1, 'k',linewidth=2)
skew.plot(pd_year1, Td_year1, 'k-.',alpha=0.8)
skew.plot(p, Temp_y1_to_y2, 'r',linewidth=2)
skew.plot(p, Td_y1_to_y2, 'r-.',alpha=0.8)
skew.plot(p, T_min, 'r:',alpha=0.8)
skew.plot(p, T_max, 'r:',alpha=0.8)

skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-30, 60)

if stationid=="FIM00002963" or stationid =="FIM00002836":
    title = station + " " + time + "UTC month=" + month + " (NOAA)"
else:
    title = stationid + " " +  time + "UTC month=" + month + " (NOAA)"
plt.title(title,fontdict=font_title)
plt.xlabel("T (C)",fontdict=font_axis)
plt.ylabel("P (hPa)",fontdict=font_axis)

skew.plot_dry_adiabats(alpha=0.3)
skew.plot_moist_adiabats(alpha=0.3)
skew.plot_mixing_lines(alpha=0.3)
skew.ax.set_ylim(1000, 100)
label1 = year1 + ' air temperature'
label2 = year1 + ' dew point temperature'
label3 = year2 + "-" + year3 + " air temperature"
label4 = year2 + "-" + year3 + " dew point temperature"
label5 = year2 + "-" + year3 + " air temperature $\pm$ SD"
line1, = plt.plot([1,2,3], label=label1, color="black", linestyle="-")
line2, = plt.plot([3,2,1], label=label2, color="black", linestyle="-.")
line3, = plt.plot([3,2,1], label=label3, color="red")
line4, = plt.plot([3,2,1], label=label4, color="red",linestyle="-.")
line5, = plt.plot([3,2,1], label=label5, color="red",linestyle=":")
plt.legend(handles=[line1, line2, line3, line4, line5],loc=5)
outfile_name = "./graphs/" + station + "_" + time + "utc.png"
plt.savefig(outfile_name)
plt.savefig("skewt.pdf")
