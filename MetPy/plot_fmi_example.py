# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units
from metpy.calc import wind_components

######################################################
######################################################
######################################################
#Python script for plotting radiosounding as Skew-T
#Meteorological Observation Systems, University of Helsinki
#Johannes Mikkola, Nov 2021
#All you (should) need is MetPy-package (pip install metpy)
#https://unidata.github.io/MetPy/latest/api/generated/metpy.plots.SkewT.html
######################################################
######################################################
######################################################

#data in order:
#t(s), pscl, T(K), RH(%), u(m/s), v(m/s), z(m), p(hPa), TD(K), MR (g/kg), DD(dgr), FF (m/s), AZ(dgr), EI(dgr), range, lon, lat

# #read data in
# infile = "2021_soundings/kumpula_2021_11_11.dat"
# data = np.loadtxt(infile)
#
# pres = data[:,7]
# temp = data[:,2]-273.15 #K to C
# dew_point = data[:,8]-273.15 #K to C
# uu = 1.94*data[:,5] #m/s to knots
# vv = 1.94*data[:,4] #m/s to knots
#
# #apply metpy units for the variables
# uu = uu*units.knots
# vv = vv*units.knots
# temp = temp*units.degC
# dew_point = dew_point*units.degC
# pres = pres*units("hPa")

infile = "Sodankyla_Tahtela_2017_07_03T12_00_00Z.txt"
data = np.loadtxt(infile)

hgt = data[:,0]*units.m
pres = data[:,1]*units.hPa
wspd = data[:,2]*units.mps
wdir = data[:,3]*units.degrees
uu, vv = wind_components(wspd,wdir)
uu, vv = 1.94*uu*units.knots, vv*1.94*units.knots
temp = data[:,4]*units.degC
dew_point = data[:,5]*units.degC

#plotting
fig = plt.figure(figsize=(9,9))
skew = SkewT(fig, rotation=45)
skew.plot(pres, dew_point, 'g',label="Td")
skew.plot(pres, temp, 'k',label="T")

#average winds over the plotting "density"
uu_mean = uu.copy()
vv_mean = vv.copy()
every_ith = 70
ptop = 580
for ii in range(every_ith,uu.shape[0]-every_ith):
    uu_mean[ii] = np.nanmean(uu[ii-every_ith:ii+every_ith])
    vv_mean[ii] = np.nanmean(vv[ii-every_ith:ii+every_ith])
skew.plot_barbs(pres[pres>ptop*units("hPa")][::every_ith],
                uu_mean[pres>ptop*units("hPa")][::every_ith],
                vv_mean[pres>ptop*units("hPa")][::every_ith])

skew.plot_dry_adiabats(np.arange(-10,70,5.0)*units.degC,alpha=0.4,label="$\\Gamma _d$")
skew.plot_moist_adiabats(np.arange(-10,70,5.0)*units.degC,alpha=0.4,label="$\\Gamma _m$")
#skew.plot_mixing_lines(alpha=0.4)

plt.ylabel("Pressure (hPa)")
plt.xlabel("Temperature ($^\\circ$C)")
title = infile.replace(".txt","").replace("_"," ")
plt.title(title)

yticks = np.arange(200,1021)[::20]
yticklabels = yticks.copy().astype(str)
yticklabels[yticks%100!=0] = ""

xticks = np.arange(-80,51)[::2]
xticklabels = xticks.copy().astype(str)
xticklabels[xticks%10!=0] = ""

skew.ax.set_yticks(yticks)
skew.ax.set_yticklabels(yticklabels)
skew.ax.set_xticks(xticks)
skew.ax.set_xticklabels(xticklabels)

for T in np.arange(-80,51)[::10]:
    skew.ax.plot([T,T],[1020,200],'k',alpha=.5,zorder=1)

for p in np.arange(200,1001)[::100]:
    skew.ax.plot([-80,51],[p,p],'k',alpha=.5,zorder=1)

plt.ylim(1020,ptop)
plt.xlim(0,22)

skew.ax.legend(fontsize=18)

figname = "teht4_lask.pdf"
plt.savefig(figname,bbox_inches = 'tight',dpi=300)
