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
## Next, run cmd.exe and cd to Python 27 directory, and type "Python get-pip.py" to install
## INSTALL numpy and matplotlib by opening cmd.exe and cd to the root of Python27
## type (without ") "python -m pip install numpy".
## Once numpy is installed, install matplotlib by typing (without ") "python -m pip install matplotlib".
##_____________________________________________________________________
## NOTE: tk FileDialog was changed to "filedialog" in Python 3.x, so replace
## with "import tkinter.filedialog" or "from tkinter import filedialog"

import glob, Tkinter, tkFileDialog, os, sys
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from decimal import Decimal
import numpy as np

print ("\n Please select an appropriate .gg file \n")

root = Tkinter.Tk()         ## These three lines prevent  
root.withdraw()             ## extra TK dialog windows from opening
root.update()

GGfile = tkFileDialog.askopenfilename(initialdir = "N:/04 - IPE Projects Docs", title = "Select file", filetypes = (("gg files","*.gg"),("all files","*.*")))

# For Temp x-axis
index = 1
hys = []

#For Charge FET Control Limits
FET_curr = []
FET_hys_high = []
SOT1 = []
t1 = []
i1 = []

#Boolean for cell derating
neg30 = False


#For degrees celsius symbol
Tfuse = 93              #Temperature at which thermal fuse fails
t = u"\u2103"           #Used to allow degree celsius symbol

## Function uses two-point formula to calculate missing point on logic fuse plot
def thirdpoint(x,y):
    y2 = y[3]

    y10 = y[3]-y[2]

    x10 = x[3]-x[2]

    x32 = x[5]-x[3]
    
    point3 = y2 + (x32*(float(y10)/x10)) # two-point formula
    ## m = y1-y0
    ##     -----
    ##     x1-x0
    return point3

## Function uses two-point formula to calculate missing point on thermal fuse plot
def fourthpoint(x,y):
    y2 = y[3]

    y10 = y[3]-y[2]

    x10 = x[3]-x[2]

    x32 = Tfuse-x[3]
   
    point3 = y2 + (x32*(float(y10)/x10)) # two-point line formula
    ## m = y1-y0
    ##     -----
    ##     x1-x0
    return point3

## Function for prompting user to select which Logic fuse is installed
## in the battery, and draws the logic fuse plot accordingly

def FUSEselect():
    
    global derating         #Need to declare this as global to use outside of this function
    selection = False

    ##Menu prompt for installed logic fuse
    print ("\n Which Logic Fuse is installed? \n")
    menu = {}
    menu['0']="SONY SFH-1212  (750014)" 
    menu['1']="SONY SFH-1415A (750016)"
    menu['2']="SONY SFH-1215B (750017)"
    menu['3']="SONY SFH-1412B (750019)"
    menu['4']="SONY SFH-1415B (750022)" 
    menu['5']="SONY SFH-3030  (750026)"
    menu['6']="SONY SFH-2030  (750027)"
    menu['7']="SONY SFH-2015B (750028)"
    menu['8']="SONY SFK-4030  (750024)"
    menu['9']="PARALLEL FUSE CONFIGURATION"
    menu['10']="Exit"

    ## While there is no selection, or user continues to input invalid selection
    ## we will remain here. We can consolidate these options with "or" statements
    ## since some fuses have the same 25C and 40C current values
    while selection == False: 
        options=menu.keys()
        options.sort(key=int)
        for entry in options: 
            print (entry, menu[entry])

        fuse=int(raw_input("Enter Fuse number 0-10:")) 
        if fuse == 0:
            print ("1212 \n")
            selection = True
            model = 'SFH-1212'
            i25C = 13.5                                         ## Set current at 25C
            i40C = 12                                           ## Set current at 40C
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])      ## x-axis
            i1.extend([i25C,i25C,i40C,10,0])                    ## y-axis
            return model
        elif fuse == 1:
            print ("1415a \n")
            selection = True
            model = 'SFH-1415a'
            i25C = 17
            i40C = 15
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,12.5,0])
            return model
        elif fuse == 2:
            print ("1215b \n")
            selection = True
            model = 'SFH-1215b'
            i25C = 17
            i40C = 15
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,12.5,0])
            return model
        elif fuse == 3:
            print ("1412b \n")
            selection = True
            model = 'SFH-1412b'
            i25C = 13.5
            i40C = 12
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,10,0])
            return model
        elif fuse == 4:
            print ("1415b \n")
            selection = True
            model = 'SFH-1415b'
            i25C = 17
            i40C = 15
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,12.5,0])
            return model
        elif fuse == 5:
            print ("3030 \n")
            selection = True
            model = 'SFH-3030'
            i25C = 34
            i40C = 30
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,25,0])
            return model
        elif fuse == 6:
            print ("2030 \n")
            selection = True
            model = 'SFH-2030'
            i25C = 34
            i40C = 30
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,25,0])
            return model
        elif fuse == 7:
            print ("2015b \n")
            selection = True
            model = 'SFH-1215b'
            i25C = 17
            i40C = 15
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,12.5,0])
            return model
        elif fuse == 8:
            print ("4030 \n")
            selection = True
            model = 'SFK-4030'
            i25C = 34
            i40C = 30
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,25,0])
            return model
        elif fuse == 9:
            print ("Custom Parallel Fuse \n")
            rating25C = float(raw_input("Enter your 25C current rating: "))
            print ("%gA" % (rating25C))
            rating40C = float(raw_input("Enter your 40C current rating: "))
            print ("%gA" % (rating40C))
            rating60C = float(raw_input("Enter your 60C current rating: "))
            print ("%gA" % (rating60C))
            selection = True
            model = 'Custom Parallel Fuse'
            i25C = (rating25C*2)
            print(i25C)
            i40C = (rating40C*2)
            print(i40C)
            i60C = (rating60C*2)
            print(i60C)
            t1.extend([derating,25,40,60,SOT1[0],SOT1[0]])
            i1.extend([i25C,i25C,i40C,i60C,0])
            return model
        else: 
            print ("Exiting... \n")
            sys.exit()
    
##This function parses through selected .gg file and appends the appropriate arrays with related values
def appendCP(filename):
    global neg30               
    page = open(filename,"a+").readlines()      #Opens the selected file, and assigns each line of text to an index in array "page"
    name = os.path.basename(filename)           #Trims path and leaves only file name with its extension
    name = name.rsplit("_")                     #Splits file name by underscore delimiter
    
    for z in range(len(name)):                  #Finding whether cell operates in low temp, i.e -30C
        if (name[z] == '2058') or (name[z] == '2501') or (name[z] == '5271'):   #Hardcoded chem ID# 2058 for the time being
            neg30 = True
       
    for line in page:                           #Parses through each line in the array "page"
        words = line.split(' = ')               #Splits each line by equal sign delimiter to an index in array "words"

        if 'OC (1st Tier) Dsg' in words:        #Checks for this specific phrase, and appends array "FET_curr" with the subsequent value
            FET_curr.append(float(words[index].rstrip('\n'))/1000)
            ##print words[1]    ## Used in debugging to see whether file is read correctly or not
            
        if 'OT1 Dsg Threshold' in words:
            FET_hys_high.append(float(words[index].rstrip('\n')))
            
        if 'OT1 Dsg Recovery' in words:
            FET_hys_high.append(float(words[index].rstrip('\n')))

        if 'SOT1 Dsg Threshold' in words:
            SOT1.append(float(words[index].rstrip('\n')))
            
        if 'Temp Hys' in words:
            hys.append(float(words[index].rstrip('\n')))

    
    open(filename,"a+").close()     #Closes file. Not necessarily needed, by used for completeness



    
#################################
#################################
###      MAIN STARTS HERE     ###
#################################
#################################

appendCP(GGfile)

if neg30 == True:       #Condition statement to set x-axis min based on cell operating range (low temp)
    derating = -30      #Hardcoded -30C for Chem ID#2058
    limit = '0'         #Hardcoded Current delivery limit in derating line annotation
else:
    derating = -20      # Default derating for all other cells
    limit = '10'
    
FUSEselect()

i1.insert(4,thirdpoint(t1,i1))  #Finds, and inserts missing point into 4th index for logic fuse line plot

#Discharge FET control line plot points
t2 = [derating, FET_hys_high[0], FET_hys_high[1],FET_hys_high[1]]   #x-axis
i2 = [FET_curr[0],FET_curr[0],0,FET_curr[0]]                        #y-axis

#Thermal fuse line plot points
t3 = [SOT1[0],Tfuse,Tfuse]                      #x-axis
i3 = [thirdpoint(t1,i1),fourthpoint(t1,i1),0]   #y-axis

#Derating line plot points
t4 = [derating, (derating+20)]                  #x-axis
i4 = [(FET_curr[0]*0.25), FET_curr[0]]          #y-axis


#Plot commands for all four plots
plt.plot(t1,i1,
               color = 'red',                   #Defines color of line
               linewidth=2,                     #Defines width of line
               label = "Logic Fuse Control",    #Defines label of plot in legend
               linestyle ='-')                  #Defines style of line plot

plt.step(t2,i2,
               color = 'blue',
               linewidth=2,
               label = "DISCHARGE FET Control Limits",
               linestyle ='--')
      
plt.plot(t3,i3,
               color = 'red',
               linewidth=2,
               label = "Thermal Fuse Control",
               linestyle ='--')
plt.plot(t4,i4,
               color = 'green',
               linewidth=2,
               label = "Cell Derating",
               linestyle ='--')      

##Condition to set y-axis tick interval according to logic fuse max current
if (max(i1) >= 30):
    ytick = 2
else:
    ytick = 1
    
##Set range for y-axis    
plt.yticks(np.arange(0, max(i1)+2, ytick))
##Set range for x-axis
plt.xticks(np.arange(derating, max(t1)+20, 10))

##Arrows for Discharge FET Control
plt.annotate('', xy=(max(t1)/2, FET_curr[0]), xytext=((max(t1)/2)-10, FET_curr[0]),arrowprops=dict(facecolor='blue',lw=0, width=0.5,headwidth=8),)                  #Arrow in middle of Max current
plt.annotate('', xy=(FET_hys_high[0], FET_curr[0]/2), xytext=(FET_hys_high[0], (FET_curr[0]/2)+0.5),arrowprops=dict(facecolor='blue',lw=0, width=0.5,headwidth=8),)   #Arrow pointing down,       11/21: Changed xytext y-coord constant to 0.5. 
plt.annotate('', xy=(FET_hys_high[1], FET_curr[0]/2), xytext=(FET_hys_high[1], (FET_curr[0]/2)-0.5),arrowprops=dict(facecolor='blue',lw=0, width=0.5,headwidth=8),)   #Arrow pointing up          11/21: Changed xytext y-coord constant to -0.5.
plt.annotate('', xy=(FET_hys_high[1], min(i1)), xytext=(FET_hys_high[1]+5, min(i1)),arrowprops=dict(facecolor='blue',lw=0, width=0.5,headwidth=8),)                 #Arrow pointing left

##Annotation for Cell derating
plt.annotate('Current Delivery May be\nLimited by Cells <'+limit+t, xy=(derating+10, FET_curr[0]/2), xytext=(derating+20, FET_curr[0]*0.25),arrowprops=dict(facecolor='black',lw=0, width=1,headwidth=8),bbox=dict(boxstyle="round", fc="w"))

plt.xlabel('Temp('+t+')')
plt.ylabel('Current(A)')
plt.title('Discharge Operating Limits')
plt.grid(True)
plt.legend(loc='upper right',prop={'size':7})
plt.show()

