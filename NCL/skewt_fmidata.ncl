;skewt FMI Open data,
;Johannes Mikkola, 6/18

;you may have to change these directions
load "/usr/share/ncarg/nclscripts/csm/gsn_code.ncl"
load "/usr/share/ncarg/nclscripts/csm/skewt_func.ncl"
load "/usr/share/ncarg/nclscripts/csm/contributed.ncl"

;color tables (eg. for color of filled area):
;https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml
;gsn_define_colormap(wks,"ColorTableName")

;named colors(temperature curve, wind bars):
;https://www.ncl.ucar.edu/Document/Graphics/named_colors.shtml

;more information about customising ncl plot:
;https://www.ncl.ucar.edu/Applications/skewt.shtml
;http://www.ncl.ucar.edu/Document/Functions/

begin

;___read data in___

Data = asciiread ("./data_fmi.txt", (/nlvl,ncol/), "float")

wspd = Data(:,0)	;wind speed [m/s]
wdir = Data(:,1)	;wind dir [deg]
tc = Data(:,2) 	    ;temperature [C]
tdc = Data(:,3)	    ;dew point temp [C]
z = Data(:,4)		;height [m]

;height to pressure, based on 1976 US standard atmosphere
;(while waiting for pressure data from FMI)
apu = stdatmus_z2tdp(Data(:,4))
p = apu(2,:)

;plot same amount of wind bars for every data set
numb_of_wbars = 25
i_100 = closest_val(100.,p)
wthin = i_100/numb_of_wbars

;output file name

outfile = str_sub_str(title," ","_");
outfile = str_sub_str(outfile,":", "_");
outfile = str_sub_str(outfile,"-", "_");

;___create plot___

wks  = gsn_open_wks ("png", outfile)  ;send graphics to png/pdf file

gsn_define_colormap(wks,"WhiteBlueGreenYellowRed")

; --- Create background skew-T and plot sounding----------------

skewtOpts                    = True
skewtOpts@DrawColAreaFill    = True         ;default is False
skewtOpts@tiMainString       = title
skewtOpts@DrawFahrenheit     = False        ;default is True
;skewtOpts@DrawHeightScale   = True         ;uncomment if you want heihgt scale
;skewtOpts@DrawHeightScaleFt = False
skewtOpts@DrawFahrenheit     = False         ;default is True
skewtOpts@DrawColAreaColor   = 10            ;(see line 9-11)
dataOpts                     = True          ;options describing data and ploting
;dataOpts@colTemperature      = "green"       ;default "black"
dataOpts@Wthin               = wthin         ;plot every n-th wind bar
dataOpts@colDewPt            = "blue"        ;default "RoyalBlue"
;dataOpts@colCape             = "purple"      ;default "red"

skewt_bkgd = skewT_BackGround (wks, skewtOpts)
skewt_data = skewT_PlotData   (wks, skewt_bkgd, p,tc,tdc,z \
                                    , wspd,wdir, dataOpts)
draw (skewt_bkgd)
draw (skewt_data)
frame(wks)

end
