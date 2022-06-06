#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 07:57:35 2020

@author: JacobsMac
"""

import csv
import time
import matplotlib.pyplot as mpp
delay = 0

DataFile = "WolinJacob.csv"
with open(DataFile, "r") as csvfile: #opening my csv file to read it
    MySpotify = csv.reader(csvfile)
    myrows = [r for r in MySpotify] #converts each line in the csv file into a list that can be called later
    #for row in myrows:
    #   print(row)
    #   print(", ".join(row))

def createcolumn(index, integer=None): #this function generates a column with a given index
    column = []
    for row in myrows:
        column.append(row[index])
    if integer == "yes": #converts the numbers into integers if in parameters
        column.pop(0)
        column = [int(i) for i in column] 
    return column #returns the constructed column

def MMAM(index): #this function takes a given column and finds the max, min, average and median
    column = createcolumn(index, "yes")
    total = len(column)
    initmax = 0 
    initmin = 10000 #none of my variables exceed 10,000 so the initial min is set as it to ensure that the program functions effectively 
    initavg = 0
    x = 1
    for value in column:
        #MAX
        if value >= initmax: #if the most recent value is larger than the previous max, it becomes the new max
            initmax = value
            maxindex = x
        #MIN
        if value <= initmin: #if the most recent value is smaller than the previous min, it becomes the new min
            initmin = value
            minindex = x
        #AVG
        initavg += value #adds every value to the total average
        x += 1
    average = initavg / total #divides total values by the amount of items in column
    #MED
    column.sort() #this function sorts the column in numerical order
    if total % 2 == 0: #if there are an even amount of items, it takes the average of the two middle terms
        highmed = int(column[total//2])
        lowmed = int(column[(total//2) - 1])
        median = (highmed + lowmed)/2
    else: #if there are an odd amount of items, it takes the middle item
        median = int(column[total//2])
    maxsong = myrows[maxindex][1] #the program then finds the corresponding song and artist for the values of max and min that were found
    minsong = myrows[minindex][1]
    maxartist = myrows[maxindex][2]
    minartist = myrows[minindex][2]
    fullmax = maxsong + " by " + maxartist #creates a string with the song and artist
    fullmin = minsong + " by " + minartist
    return str(initmax), fullmax, str(initmin), fullmin, str(average), str(median) #converts all of the returned variables into strings so that they can be concatenated

def AppendFunction(textfile, dataframe): #this function takes the .txt file and the .csv file
    characters = []
    with open(textfile, "a") as txtfile:
        txtfile.write("\n")
        txtfile.write("\n")
        with open(dataframe, "r") as csvfile: #it adds the dataframe into the .txt file
            MySpotify = csv.reader(csvfile)
            myrows = [r for r in MySpotify]
            for row in myrows: #for each row of the .csv file, it converts the list into a string, then appends it to the .txt file along with a newline character
                newline = ", ".join(row)
                txtfile.write(newline) 
                txtfile.write("\n")
            csvfile.close() 
        txtfile.close() #both files get closed because the .txt file is no longer being appended to
    with open(textfile, "r") as txtfile: #the textfile is reopened so that it'll be read from the beginning
        for line in txtfile: #for each line in the file, the program counts how many characters there are and appends it to a growing list (characters) with all of the numbers
            count = len(line)
            characters.append(count)
        txtfile.close()
    listtotal = 0
    for item in characters: #for every number in characters, it is added to the total number of characters
        listtotal += item
    characters.append(listtotal) #the total number of characters is added to the list
    return characters #the list of all characters is returned

def MakeGraphs(dataframe): #this function creates 4 graphs out of data from the .csv file
    firstcol = createcolumn(0, "yes") #using the createcolumn function, all the columns with numerica data are created
    energycol = createcolumn(5, "yes")
    dancecol = createcolumn(6, "yes")
    valcol = createcolumn(8, "yes")
    acccol = createcolumn(10, "yes")
    popcol = createcolumn(11, "yes")
    datecol = createcolumn(3)
    datecol.pop(0)
    #SCATTER PLOT
    mpp.figure(1) #creates figure
    mpp.axis([0,100,0,100]) #sets axis on a scale of 100
    mpp.grid() #adds gridlines
    mpp.scatter(dancecol, popcol) #creates a scatter plot with the two columns being compared
    mpp.title("Relationship between Danceability and Popularity") #title of the graph
    mpp.xlabel("Danceability") #label on the x axis
    mpp.ylabel("Popularity") #label on the y axis
    mpp.savefig("Scatter.jpg") #saves the figure to folder
    mpp.show() #shows the plot
    #BOXPLOT
    mpp.figure(2) #creates figure
    fullset = [energycol, dancecol, valcol, acccol, popcol] #the columns being compared
    setlabel = ["Energy", "Danceability", "Valence", "Acousticness", "Popularity"] #the title of each of the box plots
    mpp.boxplot(fullset) #plots the columns
    mpp.xticks([1,2,3,4,5], setlabel) #for each of the 5 plots, it matches it w the corresponding label
    mpp.title("Values of Different Musical Elements") #title of the plot
    mpp.savefig("BoxPlot.jpg") #saves the figure to folder
    mpp.show() #shows the plot
    #LINEPLOT
    mpp.figure(3) #creates figure
    mpp.plot(firstcol,dancecol) #creates a line plot with the columns given
    mpp.xlabel("Ranking (out of 100)") #sets x axis label
    mpp.ylabel("Danceability Score") #sets the y label
    mpp.title("Personal Preference in Terms of Danceability") #sets the title
    mpp.savefig("LinePlot.jpg") #saves the figure to folder
    mpp.show() #shows the plot
    #PIECHART
    uniqueyear = [] #list of all unique years
    yearcount = [] #frequency of unique years
    percent = [] #ratio of unique years to total
    for date in sorted(datecol): #sorts the date column so it is in chronological order
        year = int(date[:4]) #only takes the year released and not month or day
        if year not in uniqueyear: 
            uniqueyear.append(year) #if the year is unique, it appends to list of all unique years
            yearcount.append(1)
        else:
            position = uniqueyear.index(year) #if it is a repeated year, it finds where the year is on the uniqueyear list
            yearcount[position] += 1 #and it adds one to the frequency
    for num in yearcount:
        decimal = (num / len(datecol)) #for every frequency, it creates a decimal percentage of its frequency
        percent.append(decimal)
    mpp.figure(4) #creates figure
    mpp.pie(percent, labels=uniqueyear, autopct='%1.1f%%') #creates pie chart with percentages, labels, and displays percentage
    mpp.title("Frequency of Year Song Was Released On Playlist") #title of the chart
    mpp.savefig("PieChart.jpg") #saves figure to the folder
    mpp.show() #shows the figure
        
def main(): #the main function
    global column0
    time.sleep(delay)
    print("The third row is:")
    time.sleep(delay)
    print(myrows[2]) #displays the third row, but 2nd index in python
    time.sleep(delay)
    print("")
    
    column0 = createcolumn(0) 
    print("The first column is:")
    time.sleep(delay)
    print(column0) #prints the first column, but 0 index in python
    time.sleep(delay)
    print("")
    
    print("The first row, fifth column is:")
    time.sleep(delay)
    print(myrows[0][4]) #prints the first row, fifth column but 0 and 4th indexes in python respectively
    print("")
    time.sleep(delay)
    
    for row in myrows: #this for loop turns ever M:SS time stamp into seconds so it can numerically calculated
        if row[9] == "LENGTH":
            continue
        else:
            row[9] = (int(row[9][:1])*60) + int(row[9][2:])
    maxlen, maxlensong, minlen, minlensong, avglen, medlen = MMAM(9) #the columns of times are put into the MMAM function
    len1 = "The longest song is " +  maxlen + " seconds. It is " + maxlensong + "."
    print(len1)
    time.sleep(delay)
    len2 = "The shortest is " + minlen + " seconds. It is " + minlensong + "."
    print(len2)
    time.sleep(delay)
    len3 = "The average song is " + avglen + " seconds. The median is " + medlen + " seconds."
    print(len3)
    time.sleep(delay)
    print("") #stats are printed
    
    maxbpm, maxbpmsong, minbpm, minbpmsong, avgbpm, medbpm = MMAM(4) #the column of BPM is put into the MMAM function
    bpm1 = "The song with highest beats per minute is " + maxbpm + " BPM. It is " + maxbpmsong + "."
    print(bpm1)
    time.sleep(delay)
    bpm2 = "The lowest is " + minbpm + " BPM. It is " + minbpmsong + "."
    print(bpm2)
    time.sleep(delay)
    bpm3 = "The average is " + avgbpm + " BPM. The median is " + medbpm + " BPM."
    print(bpm3)
    time.sleep(delay)
    print("") #stats are printed
    
    maxpop, maxpopsong, minpop, minpopsong, avgpop, medpop = MMAM(11) #the popularity column is put into the MMAM function
    pop1 = "The most popular song is " + maxpopsong + ". It has a popularity score of " + maxpop + "."
    print(pop1)
    time.sleep(delay)
    pop2 = "The least is " + minpopsong + ". It has a popularity score of " + minpop + "."
    print(pop2)
    time.sleep(delay)
    pop3 = "The average popularity is a score of " + avgpop + ". The median popularity is " + medpop
    print(pop3)
    time.sleep(delay)
    print("") #the stats are printed


    NewFile = "output.txt" #a new textfile is created
    with open(NewFile, "w") as txtfile: #it is opened so it can be written in
        txtfile.write(len1)
        txtfile.write("\n")
        txtfile.write(len2)
        txtfile.write("\n")
        txtfile.write(len3)
        txtfile.write("\n")
        txtfile.write("\n")
        txtfile.write(bpm1)
        txtfile.write("\n")
        txtfile.write(bpm2)
        txtfile.write("\n")
        txtfile.write(bpm3)
        txtfile.write("\n")
        txtfile.write("\n")
        txtfile.write(pop1)
        txtfile.write("\n")
        txtfile.write(pop2)
        txtfile.write("\n")
        txtfile.write(pop3) #one by one it adds each of the lines from above with a newline character separating them
        txtfile.close() #the file is closed so it stops getting edited
        
    finallist = AppendFunction(NewFile, DataFile) #AppendFunction is called to generate the amount of characters per line
    time.sleep(delay)
    print("These are the amount of characters per line:", finallist) #that number is printed
    time.sleep(delay)
    print("There are", finallist[-1], "characters total in the textfile", NewFile) #the total amount of characters are printed
    print("")
    
    
    MakeGraphs(DataFile) #the MakeGraphs function is called
main()

