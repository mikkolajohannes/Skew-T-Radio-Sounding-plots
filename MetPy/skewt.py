# coding=utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units


#__________________plotting__________________
fig = plt.figure(figsize=(11,16.5))
skew = SkewT(fig, rotation=30, aspect='auto')
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

skew.ax.set_ylim(1021, 200)
skew.ax.set_xlim(-30, 50)

w = np.array([0.040,0.030,0.020,0.015,0.010,0.007,0.005,0.004,0.003,0.002,0.0015,0.001,0.0005,0.0002])[:, None] * units('g/g')
p = units.hPa * np.linspace(1020, 400, 7)
skew.plot_mixing_lines(w=w, p=p,alpha=0.4, label="Kyllästyssekoitussuhde",zorder=2)

for val in w.flatten()[3:-4]:
    top_p = p[-1]
    dewpt = mpcalc.dewpoint(mpcalc.vapor_pressure(top_p, val))
    skew.ax.text(dewpt, top_p, str(int(val.to('g/kg').m)),horizontalalignment='center',zorder=3)

skew.ax.text(mpcalc.dewpoint(mpcalc.vapor_pressure(400*units.hPa, 0.0002)), 400*units.hPa, "0.2",horizontalalignment='center',zorder=3)
skew.ax.text(mpcalc.dewpoint(mpcalc.vapor_pressure(400*units.hPa, 0.0005)), 400*units.hPa, "0.5",horizontalalignment='center',zorder=3)
skew.ax.text(mpcalc.dewpoint(mpcalc.vapor_pressure(400*units.hPa, 0.001)), 400*units.hPa, "1",horizontalalignment='center',zorder=3)
skew.ax.text(mpcalc.dewpoint(mpcalc.vapor_pressure(400*units.hPa, 0.0015)), 400*units.hPa, "1.5",horizontalalignment='center',zorder=3)
skew.ax.text(mpcalc.dewpoint(mpcalc.vapor_pressure(400*units.hPa, 0.015)), 400*units.hPa, "15",horizontalalignment='center',zorder=3)
skew.ax.text(mpcalc.dewpoint(mpcalc.vapor_pressure(420*units.hPa, 0.020)), 420*units.hPa, "20",horizontalalignment='center',zorder=3)
skew.ax.text(mpcalc.dewpoint(mpcalc.vapor_pressure(520*units.hPa, 0.030)), 520*units.hPa, "30",horizontalalignment='center',zorder=3)
skew.ax.text(mpcalc.dewpoint(mpcalc.vapor_pressure(620*units.hPa, 0.040)), 620*units.hPa, "40",horizontalalignment='center',zorder=3)


skew.plot_dry_adiabats(t0=np.arange(-70,120,5)*units.degC,alpha=0.4, label="Kuiva-adiabaatti",zorder=2)
skew.plot_moist_adiabats(t0=np.arange(-70,70,5)*units.degC,alpha=0.4, label="Pseudokostea-adiabaatti",zorder=2)

for T in np.arange(-80,51)[::10]:
    skew.ax.plot([T,T],[1020,200],'k',alpha=.5,zorder=1)

for p in np.arange(200,1001)[::100]:
    skew.ax.plot([-80,51],[p,p],'k',alpha=.5,zorder=1)

#plt.xlabel("T [$^o$C]",fontdict=font_axis)
#plt.ylabel("p [hPa]",fontdict=font_axis)

font = {'family': 'monospace',
   'color':  'darkred',
   'weight': 'normal',
   'size': 10,
   }

skew.ax.legend(loc="upper right")
plt.savefig("SkewT.pdf",bbox_inches = 'tight')
