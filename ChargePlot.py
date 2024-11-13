# -*- coding: cp1252 -*-
## Download and Install Python 2.7 from: https://www.python.org/downloads/release/python-2713/
## Already installed with Python 2.7: glob, Tkinter, os, tkFileDialog, pip (for Python > 2.7.9
## Need to install: Visual C++ compiler for Python 2.7, numpy, and matplotlib.

## INSTALL Microsoft Visual C++ Compiler for Python 2.7 or your current verison
## From here: https://www.microsoft.com/en-us/download/details.aspx?id=44266
## Download numpy and matplotlib (amd64 versions) from here: https://www.lfd.uci.edu/~gohlke/pythonlibs/
## Upgrade pip opening cmd.exe and cd to the root of Python 27 (usually "cd C:\Python27"). After you cd, enter (without ") "python -m pip install -U pip"
## If pip is not already installed, download from: https://bootstrap.pypa.io/get-pip.py
## to Python 27 directory, and change extension to .py
## Next, run cmd.exe and cd to Python 27 directory, and type "python get-pip.py" to install
## INSTALL numpy and matplotlib by opening cmd.exe and cd to the root of Python27
## type (without ") "python -m pip install numpy".
## Once numpy is installed, install matplotlib by typing (without ") "python -m pip install matplotlib".
##_____________________________________________________________________
## NOTE: tk FileDialog was changed to "filedialog" in Python 3.x, so replace
## with "import tkinter.filedialog" or "from tkinter import filedialog"
import glob, Tkinter, tkFileDialog, os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from decimal import Decimal
import numpy as np

print "\n Please select an appropriate .gg file \n"

root = Tkinter.Tk()         ## These three lines prevent  
root.withdraw()             ## extra TK dialog windows from opening
root.update()

##Sets initial directory to N drive folder 4, allows user to select binary data file, and assign its contents to "GGfile"
GGfile = tkFileDialog.askopenfilename(initialdir = "N:/04 - IPE Projects Docs", title = "Select file", filetypes = (("gg files","*.gg"),("all files","*.*")))

# For Temp x-axis
Temperature = []        #Temperature array for SMBus
Temperature2 = []       #Temperature array for FET control
index = 1
hys = []                #Temperature hysteresis, usually 1 degree C

#For Charge FET Control Limits
FET_curr = []           #FET Current amplitude
FET_hys = []            #FET hysteresis current

#For ChargeCurrent SMBus Request
SMBus_curr = []         #SMBus current request
SMBus_hys = []          #SMBus hysteresis current

D = []
t = u"\u2103"   #Used to allow degree celsius symbol

##This function parses through selected .gg file and appends the appropriate arrays with related values
def appendCP(filename):

    page = open(filename,"a+").readlines()              #Opens the selected file, and assigns each line of text to an index in array "page"

    for line in page:                                   #Parses through each line in the array "page"
        words = line.split(' = ')                       #Splits each line by equal sign delimiter to an index in array "words"

        if 'JT1' in words:                              #Checks for this specific phrase, and appends array "FET_curr" with the subsequent value
            Temperature.append(float(words[index].rstrip('\n')))           ## THIS WORKS!
            ##print "JT1: " + words[1]                    ## Used in debugging to see whether file is read correctly or not

        if 'JT2' in words:
            Temperature.append(float(words[index].rstrip('\n')))


        if 'JT2a' in words:
            Temperature.append(float(words[index].rstrip('\n')))


        if 'JT3' in words:
            Temperature.append(float(words[index].rstrip('\n'))) 

            
        if 'JT4' in words:
            Temperature.append(float(words[index].rstrip('\n')))


        if 'OC (1st Tier) Chg' in words:
            FET_curr.append(float(words[index].rstrip('\n'))/1000)

            
        if ('OT1 Chg Threshold' or 'Over Temp Chg') in words:
            FET_hys.append(float(words[index].rstrip('\n')))

            
        if ('OT1 Chg Recovery' or 'OT Chg Recovery') in words:
            FET_hys.append(float(words[index].rstrip('\n')))

            
        if 'LT Chg Current1' in words:
            SMBus_curr.append(float(words[index].rstrip('\n'))/1000)

            
        if 'ST1 Chg Current1' in words:
            SMBus_curr.append(float(words[index].rstrip('\n'))/1000)

            
        if 'ST2 Chg Current1' in words:
            SMBus_curr.append(float(words[index].rstrip('\n'))/1000)

            
        if 'HT Chg Current1' in words:
            SMBus_curr.append(float(words[index].rstrip('\n'))/1000)

            
        if 'Temp Hys' in words:
            hys.append(float(words[index].rstrip('\n')))

    open(filename,"a+").close()         #Closes file. Not necessarily needed, by used for completeness


    
#################################
#################################
###      MAIN STARTS HERE     ###
#################################
#################################

count = 0

appendCP(GGfile)

SMBus_hys = [(Temperature[3]-hys[0]), (Temperature[4]-hys[0])]      ##Replace the last two elements in Temperature array with hysteresis temperature values
j=0                                                                 ##Else leave everything else alone
for j in range (len(Temperature)):
    if (j == 3):
        Temperature[j] = SMBus_hys[0]
        Temperature2.append(FET_hys[1])
    elif(j == 4):
        Temperature[j] = SMBus_hys[1]
        Temperature2.append(FET_hys[1])
    else:
        Temperature2.append(Temperature[j])


Temperature = sorted(Temperature)

original_templength = len(Temperature)

l=0
for l in range (len(Temperature)):
    if (l==0):
        Temperature.append(Temperature[l])
        Temperature2.append(Temperature2[l])
        Temperature = sorted(Temperature)
        ## ex. Now Temperature is [-10, -10, 0, 30, 44, 54]
        Temperature2 = sorted(Temperature2)
        SMBus_curr.insert(0,0)

        FET_curr.insert(0,0)

        p=1
        for p in range (3):
            FET_curr.append(FET_curr[1])
    elif (l==2):
        Temperature.append(Temperature[l])
        Temperature = sorted(Temperature)

        ## ex. Now Temperature is [-10, -10, 0, 0, 30, 44, 54]
    elif (l==3):
        Temperature.append(Temperature[l])
        Temperature = sorted(Temperature)
        Temperature.insert(l,Temperature[0])

        ## ex. Now Temperature is [-10, -10, 0, -10, 0, 0, 30, 44, 54]
    elif (l == original_templength-1): #4

        Temperature.append(Temperature[len(Temperature)-2])
        SMBus_curr.insert(l+1,SMBus_curr[0])
        SMBus_curr.insert(l+2,SMBus_curr[l])
        SMBus_curr.insert(l-2,SMBus_curr[0])
        SMBus_curr.insert(l-2,SMBus_curr[0])
        SMBus_curr.insert(l,SMBus_curr[l])
        FET_curr.append(FET_curr[0])

##### This works for all other fuel gauges #####
##h1 =    [-10,   -10,    0,  -10, 0, 0,  30, 45, 55, 45]         # X-axis
##i =     [0,     0.75,   0,  0,   3, 3,  3,  2,  0,  2]          # Y-axis
##h2 =    [-10,-10,0,30,55,55]             
##n =     [0,4,4,4,4,0]
################################################


###OLD w/o initial hysteresis
####### Format works for all other fuel gauges #####
##h1 = [-10,-10,0,30,45,55,45]
##i = [0,0.75,3,3,2,0,2]
##h2 = [-10,-10,0,30,55,55]             
##n = [0,4,4,4,4,0]
##################################################

############ Format Works for 40z80 hysteresis ###############
##h2 = [-10,-10,-8,-10,0,30,45,55,56,58,56]             #
##n = [4.25,0,4.25,4.25,4.25,4.25,4.25,4.25,4.25,0,4.25]#
#######################################################

##Assign labels l1 and l2 for legend
l1, = plt.step(Temperature,SMBus_curr,
               color = 'green',
               linewidth=2,
               label = "CHARGECURRENT SMBus Request",
               where = 'post')

l2, = plt.step(Temperature2,FET_curr,
               color = 'blue',
               linewidth=2,
               label = "CHARGE FET Control Limits",
               linestyle ='--',
               where = 'post')


#plt.ylim(0, max(FET_curr)+0.5)
plt.yticks(np.arange(0, max(FET_curr)+0.5, 0.5))
plt.xticks(np.arange(min(Temperature), max(Temperature2)+5, 5))
##Arrows for SMBus Current
plt.annotate('', xy=(Temperature[0], SMBus_curr[1]/2), xytext=(Temperature[0], (SMBus_curr[1]/2)+0.5),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7,shrink=5))  #1st loop at 12 and 9 oclock
plt.annotate('', xy=(Temperature[0]/2, SMBus_curr[1]), xytext=((Temperature[0]/2)+5, SMBus_curr[1]),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)

plt.annotate('', xy=(Temperature[0]/2, SMBus_curr[0]), xytext=((Temperature[0]/2)-5, SMBus_curr[0]),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)    #1st loop at 6 and 3 oclock
plt.annotate('', xy=(Temperature[2], SMBus_curr[1]/2), xytext=(Temperature[2], (SMBus_curr[1]/2)-0.5),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)

plt.annotate('', xy=(Temperature[5], SMBus_curr[6]/2), xytext=(Temperature[5], (SMBus_curr[5]/2)-0.5),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)  #opposing arrows at 0C
plt.annotate('', xy=(Temperature[5], SMBus_curr[6]/2), xytext=(Temperature[5], (SMBus_curr[5]/2)+0.5),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)

plt.annotate('', xy=(Temperature[6], max(SMBus_curr)), xytext=(Temperature[6]+5, max(SMBus_curr)),arrowprops=dict(facecolor='g', lw=0, width=0.5,headwidth=7),)     #opposing arrows at max SMBus current
plt.annotate('', xy=(Temperature[6]/2, max(SMBus_curr)), xytext=((Temperature[6]/2-5), max(SMBus_curr)),arrowprops=dict(facecolor='g', lw=0, width=0.5,headwidth=7),)

plt.annotate('', xy=(Temperature[7], SMBus_curr[7]), xytext=(Temperature[7], SMBus_curr[7]+0.5),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)        #End hysteresis loop, left arrow pointing down
plt.annotate('', xy=(Temperature[7], SMBus_curr[7]), xytext=(Temperature[7], SMBus_curr[7]-0.5),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)        #End hysteresis loop, left arrow pointing up
plt.annotate('', xy=(Temperature[8]-5, SMBus_curr[7]), xytext=(Temperature[8]-10, SMBus_curr[7]),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)       #End hysteresis loop, top arrow
plt.annotate('', xy=(Temperature[8], SMBus_curr[7]/2), xytext=(Temperature[8], SMBus_curr[1]+0.5),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)      #End hysterssis loop, right arrow
plt.annotate('', xy=(Temperature[7]+5, SMBus_curr[0]), xytext=(Temperature[7]+5+5, SMBus_curr[0]),arrowprops=dict(facecolor='g',lw=0, width=0.5,headwidth=7),)      #End hysteresis loop, bottom arrow

##Arrows for FET Current
plt.annotate('', xy=(Temperature2[0], max(FET_curr)/2+0.5), xytext=(Temperature[0], (max(FET_curr)/2)-0.5),arrowprops=dict(facecolor='b',lw=0, width=0.5,headwidth=7),)                 #Left blue arrow up
plt.annotate('', xy=(Temperature2[0], max(FET_curr)/2-0.5), xytext=(Temperature[0], (max(FET_curr)/2)+0.5),arrowprops=dict(facecolor='b',lw=0, width=0.5,headwidth=7),)                 #Left blue arrow down
plt.annotate('', xy=(Temperature2[3], max(FET_curr)), xytext=(Temperature2[3]-5, max(FET_curr)),arrowprops=dict(facecolor='b',lw=0, width=0.5,headwidth=7),)                        #Top blue arrow
plt.annotate('', xy=(max(Temperature2), (max(FET_curr)/2)-0.5), xytext=(max(Temperature2), (max(FET_curr)/2)+0.5+0.5),arrowprops=dict(facecolor='b',lw=0, width=0.5,headwidth=7),)  #Right blue arrow pointing down
plt.annotate('', xy=(max(Temperature2), (max(FET_curr)/2)+0.5), xytext=(max(Temperature2), (max(FET_curr)/2)-0.5-0.5),arrowprops=dict(facecolor='b',lw=0, width=0.5,headwidth=7),)  #Right blue arrow pointing up

plt.xlabel('Temp('+t+')')   ## "t" prints degrees celsius symbol
plt.ylabel('Current(A)')
plt.title('Charge Operating Limits')
plt.grid(True)
plt.legend([l1,l2], ["CHARGECURRENT SMBus Request","CHARGE FET Control Limits"],prop={'size':8})
plt.show()

