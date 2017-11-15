

# fit usage: python plotTextFiles.py fit filename/\areas.txt x1 x2 fit filename/\areas2.txt x1 x2

# python plotTextFiles4.py Idlesweep5_5GSs_0offset_Nov.18_GOOD/txt_files/NDF1_areas.txt Idlesweep5_5GSs_0offset_Nov.18_GOOD/txt_files/NDF1.5_areas.txt fit Idlesweep5_5GSs_0offset_Nov.18_GOOD/txt_files/\NDF2_areas.txt 18000 22000 Idlesweep5_5GSs_0offset_Nov.18_GOOD/txt_files/\NDF2.5_areas.txt 21000 25000 Idlesweep5_5GSs_0offset_Nov.18_GOOD/txt_files/\NDF3_areas.txt 23000 27000

# python plotTextFiles.py Ampsweep_5GSs_Nov18_GOOD/10000_NDF2/dataset/areas.txt Ampsweep_5GSs_Nov18_GOOD/12500_NDF2/dataset/areas.txt Ampsweep_5GSs_Nov18_GOOD/15000_NDF2/dataset/areas.txt Ampsweep_17500_2_Nov28/dataset/areas.txt AmpsweepNEW_Idle20000_NDF2_Nov27/dataset/areas.txt AmpsweepNEW_Idle17500_NDF2_Nov27/dataset/areas.txt

#python plotTextFiles.py Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF1/dataset/areas.txt Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF1.5/dataset/areas.txt Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF2/dataset/areas.txt Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF2.5/dataset/areas.txt Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF3/dataset/areas.txt

# python plotTextFiles.py Ampsweep_15000_2_Nov28/dataset/areas.txt Ampsweep_17500_2_Nov28/dataset/areas.txt Ampsweep_20000_3_Nov28/dataset/areas.txt

# FOR PLOTTING THE SPEC NDF CURVES: python plotTextFiles.py ndfspectxtfiles/NDF05/NDF0.5_spec.txt ndfspectxtfiles/NDF1/NDF1_spec.txt ndfspectxtfiles/NDF15/NDF1.5_spec.txt ndfspectxtfiles/NDF2/NDF2_spec.txt ndfspectxtfiles/NDF25/NDF2.5_spec.txt ndfspectxtfiles/NDF3/NDF3_spec.txt


import matplotlib.pyplot as plt
import csv
import sys
import os
import numpy as np
import ROOT
from scipy.optimize import curve_fit

def linear_func(x, m, c):
    return m*x+copen

fileArray = []
labelArray = []
"""labelArray.append("NDF 1")
labelArray.append("NDF 1.5")
labelArray.append("NDF 2")
labelArray.append("NDF 2.5")
labelArray.append("NDF 3")"""
#labelArray.append("Idle 10000")
#labelArray.append("Idle 12500")
labelArray.append("Idle 15000")
labelArray.append("Idle 17500")
labelArray.append("Idle 20000")

doFit = []
lowFitLimits = []
upFitLimits = []

dataPlot = plt.figure(0)
errorPlot = plt.figure(1)

afterFit = False
afterFitNum  = 999999999 
for i in range(1,len(sys.argv)):
        if sys.argv[i] == "fit":
            afterFit = True
            afterFitNum = i+1
            break
        fileArray.append(sys.argv[i])
        doFit.append(False)

for i in range(afterFitNum,len(sys.argv),3):
        fileArray.append(sys.argv[i])
        doFit.append(True)
        lowFitLimits.append(float(sys.argv[i+1]))
        upFitLimits.append(float(sys.argv[i+2]))
totYVals = []
totXVals = []
totYErr = []
fitCounter = 0
for iteration in range(len(fileArray)):
    inputFile = open(fileArray[iteration],"r")
    print inputFile
    xVals = []
    yVals = []
    yErrs = []
    read = csv.reader(inputFile,delimiter=" ")
    for row in read:
        xVals.append( float(row[0]))
        yVals.append( float(row[1]))
        yErrs.append( float(row[2]))
    totYVals.append(yVals)
    totXVals.append(xVals)
    totYErr.append(yErrs)

for iteration in range(len(fileArray)):
    print fileArray[iteration]
    print os.path.basename(fileArray[iteration])
    plt.figure(0)
    for entryIter in range(len(totYVals[iteration])):
        print str(xVals[entryIter])+" "+str(totYVals[iteration][entryIter])+" "+str(totYErr[iteration][entryIter])+" "+str(totYErr[iteration][entryIter]/totYVals[iteration][entryIter])+"\n"
    plt.errorbar(xVals,np.multiply(totYVals[iteration],-1),yerr=totYErr[iteration],label=str((labelArray[iteration])))
    negyVals = np.multiply(totYVals[iteration],-1.0)
    #print np.divide(yErrs,yVals)
    plt.figure(1)
    plt.plot(xVals,np.divide(totYErr[iteration],negyVals),label=""+str(labelArray[iteration]))
    if doFit[iteration]:
        plt.figure(0)
        fitWeights = []
        for iError in range(len(yErrs)):
            fitWeights.append(1.0/(yErrs[iError]))
        lowIndex = 0
        upIndex = 0
        
        for i in range(len(xVals)):
            if xVals[i] > lowFitLimits[fitCounter]:
                lowIndex = i 
                break
        
        for i in range(len(xVals)-1,0,-1):
            if xVals[i] < upFitLimits[fitCounter]:
                upIndex = i+1
                break
       
        fitCounter += 1
        fitResults = np.polyfit(xVals[lowIndex:upIndex],np.multiply(yVals[lowIndex:upIndex],-1.0),1,w=fitWeights[lowIndex:upIndex],full=True)
        fitValues = fitResults[0]
        chi_squared = fitResults[1]
        poly = np.poly1d(fitValues)
        plt.plot(xVals[lowIndex:upIndex],poly(xVals[lowIndex:upIndex]),label="Fit to: "+(labelArray[iteration]))
        reduced_chi_squared = chi_squared/(len(xVals[lowIndex:upIndex])-len(fitValues))
        print "Parameters for fit to: "+str(os.path.basename(fileArray[iteration]))+"    "+str(fitValues)
        print "Number of Degrees of Freedom is: "+str(len(xVals[lowIndex:upIndex])-len(fitValues))
        print "chi squared is: "+str(chi_squared)
        print "Reduced chi squared is: "+str(reduced_chi_squared)
        print "Likelihood of fit for no aging is is: "+str(ROOT.TMath.Prob(chi_squared,len(xVals[lowIndex:upIndex])-len(fitValues)))

plt.ylabel('SDOM / | Area |')
plt.xlabel('DAC Value')
plt.xlim(120, 255)
plt.ylim(0,0.08)
#plt.xlim(0, 255)
#plt.xlim(0, 30000)
plt.legend(loc="upper right")
plt.figure(0)

# zoom plot
plt.ylabel('| Area | (V.s)')
plt.xlabel('DAC Value')
plt.xlim(0, 110) #0-110 FOR ZOOM
#plt.xlim(0, 255)
#plt.ylim(-0.05e-9,0.05e-9) (with NDF2 still in)
#plt.ylim(-0.5e-7,4.5e-7) # full
plt.ylim(-0.2e-7,0.2e-7) # zoomed in
#plt.xlim(0, 30000)
plt.legend(loc="upper left")
plt.figure(1)


plt.show()

