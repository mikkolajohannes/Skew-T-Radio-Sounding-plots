# coding=utf-8

#parsing FMI open data for NCL
#Johannes Mikkola, 6/18


import os,sys,string,requests
import xml.etree.ElementTree as ET
import numpy as np

#command line arguments:
#(scriptname) your-fmi-api-key, station id, time
#e.g.
#python getfmidata.py e72a2917-1e71-4d6f-8f29-ff4abfb8f290 101932 2018-05-23T00:00:00Z

apikey=sys.argv[1]      #apikey = 'e72a2917-1e71-4d6f-8f29-ff4abfb8f290' (Johannes's api-key from 5/18)
station=sys.argv[2]     #Jokioinen - 101104, Sodankylä - 101932
time=sys.argv[3]        #YYYY-MM-DDTHH:MM:SSZ      ~2015-->
	                    #Jokioinen 12am, 12pm, 6am and 6pm / Sodankyla 12am and 12pm

url = 'http://data.fmi.fi/fmi-apikey/' + apikey + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::sounding::multipointcoverage&fmisid=' + station + '&starttime=' + time + '&endtime=' + time + '&'
#url = 'http://data.fmi.fi/fmi-apikey/your-api-key/wfs?request=getFeature&storedquery_id=fmi::observations::weather::sounding::multipointcoverage&fmisid=101932&latest=true&'
print(url)

#url->XML->tree->root
req = requests.get(url)
xmlstring = req.content
tree=ET.ElementTree(ET.fromstring(xmlstring))
root = tree.getroot()

#reading location and time data to "positions" from XML
for elem in root.getiterator(tag='{http://www.opengis.net/gmlcov/1.0}positions'):
    positions = elem.text

#'positions' is string type variable
#--> split positions into a list by " "
#then remove empty chars and "\n"
# from pos_split --> data into positions_data

try:
	pos_split = positions.split(' ')
except NameError:
	print("------------")
	print("Sounding data not found: stationid " + station + " time " + time)
	print("------------")
	sys.exit()

positions_data = []
for i in range(0,len(pos_split)):
    if not (pos_split[i] == "" or pos_split[i] == "\n"):
        positions_data.append(pos_split[i])

#index for height: 2,6,10 etc in positions_data
height = []
myList = range(2,len(positions_data))
for i in myList[::4]:
    height.append(positions_data[i])

#reading wind speed, wind direction, air temperature and dew point data to 'values'
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
w_speed = []
w_dir = []
t_air = []
t_dew = []
myList = range(0,len(values_data))
for i in myList[::4]:
    w_speed.append(values_data[i])
    w_dir.append(values_data[i+1])
    t_air.append(values_data[i+2])
    t_dew.append(values_data[i+3])

#read location and time from XML
for elem in root.getiterator(tag='{http://www.opengis.net/gml/3.2}timePosition'):
    time = elem.text

for elem in root.getiterator(tag='{http://www.opengis.net/gml/3.2}name'):
    location = elem.text

locationstr=location.replace(u'ä','a').replace(u'ö','o')

#create text file to transfer data for NCL
outfile = open("data_fmi.txt","w")

#writing data to text file (timestep = 2sec)
#w_speed(m/s) w_dir(deg) t_air(C) t_dew(C) height(m)

myList = range(0,len(height))

for i in myList[::1]:
    str2 = str(w_speed[i]) + " " + str(w_dir[i] + " " + str(t_air[i]) + " " + str(t_dew[i]) + " " + str(height[i]) + '\n')
    outfile.write(str2)

#give text file's number of lines(nlvl) and columns(ncol), title
#for NCL as command line arguments and run NCL script

str_cmline = "ncl skewt_fmidata.ncl nlvl=" + str(len(height)) + " ncol=" + str(5)
#'title="This is a title"'
str_cmline += " 'title=" + '"' + locationstr + " " + str(time) + '"' + "'"

os.system(str_cmline)
