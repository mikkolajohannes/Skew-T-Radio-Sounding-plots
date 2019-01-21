Johannes Mikkola, 6/18

Firstly you need Python and NCL (NCAR Command Language, http://www.ncl.ucar.edu/) on your computer.
Download getfmidata.py and skewt_fmidata.ncl into same folder.

This program plots FMI radiosonde sounding data into a skew-T diagram.
Data is read and parsed by getfmidata.py and transfered to skewt_fmidata.ncl via data_fmi.txt.

Python script requires few command line arguments: (script name), fmi-apikey, station id, time
For example:
python3 getfmidata.py e72a2917-1e71-4d6f-8f29-ff4abfb8f290 101104 2018-05-30T12:00:00Z

(e72a2917-1e71-4d6f-8f29-ff4abfb8f290 = Johannes's api-key from 5/18)

FMI Open data gives sounding data from two stations:
     *Jokioinen(station id = 101104) 00:00:00 and 12:00:00 since 02/2015, 06:00:00 and 18:00:00 since 12/2016
     *Sodankylä(station id = 101932) 00:00:00 and 12:00:00 since 01/2015

Python script runs the NCL script so there's no need to run NCL separately.
NCL script requires some command line arguments too so it's easier to run getfmidata.py.

There's a few options how you can customise the output file (from skewt_fmidata.ncl):
    *print either png of pdf file
    *change colors in figure, eg. temperature and cape curves, filled area colors, see lines 9-14
    *number of wind bars

More information: https://www.ncl.ucar.edu/Applications/skewt.shtml/
                  http://www.ncl.ucar.edu/Document/Functions/
