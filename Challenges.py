# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 14:55:50 2015

@author: ItelinaMa
"""
import os
os.getcwd()
os.chdir('/Users/ItelinaMa/Documents/Metis/Benson')
import csv
from collections import defaultdict
import dateutil.parser
from datetime import datetime
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

def Challenge_1():
    f = open('turnstile_150404.txt')
    csv_f = csv.reader(f)
    keys = []
    values = []
    
    for row in csv_f:
        keys.append(row[0:4])
        values.append(row[4:10])
    del keys[0]  
    del values[0]

    subwaydict = {}
    dummylist = []
    for i, key in enumerate(keys):
        if tuple(key) in dummylist:
            subwaydict[tuple(key)].append(values[i])
        else:
            subwaydict[tuple(key)] = [values[i]]
            dummylist.append(tuple(key))
    
    return subwaydict

def Challenge_2():
    f = open('turnstile_150404.txt')
    csv_f = csv.reader(f)
    keys = []
    values = []

    for row in csv_f:
        keys.append(row[0:4])
        values.append([row[6], row[7], row[9]])
    del keys[0]  
    del values[0]
    
    values2 = []
    for i in range(len(values)):
        values2.append([values[i][0] + ' ' + values[i][1]])
        values2[i].extend([values[i][2]])
        values2[i][0] = dateutil.parser.parse(values2[i][0])
    
    subwaydict = {}
    dummylist = []
    for i, key in enumerate(keys):
        if tuple(key) in dummylist:
            subwaydict[tuple(key)].append(values2[i])
        else:
            subwaydict[tuple(key)] = [values2[i]]
            dummylist.append(tuple(key))
    
    return subwaydict

'''
def Challenge_3():
    x = Challenge_2()
    subwaydict = {}
    for key in x.keys():
        dates ={}
        dummydates = []
        for datelist in x[key]:
            datevalue = datelist[0].date()
            if datevalue in dummydates:
                dates[datevalue] += int(datelist[1])
            else:
                dates[datevalue] = int(datelist[1])
                dummydates.append(datevalue)
        subwaydict[key] = dates
    return subwaydict
'''

def Challenge_3(data=None):
    if not data:
        data = Challenge_2()
    for turnstiles in data.keys():
        i = 0
        while i < len(data[turnstiles]):
            timegaps = [datetime.time(0, 0), datetime.time(1, 0), datetime.time(2, 0), datetime.time(3, 0)]
            if data[turnstiles][i][0].time() not in timegaps:
                del data[turnstiles][i]
            else:
                i += 1
        dates = {}
        for i, values in enumerate(data[turnstiles]):
            if i == len(data[turnstiles]) -1:
                break
            dates[values[0]] = int(data[turnstiles][i+1][1]) - int(values[1])
        data[turnstiles] = dates
    return data
            
#%matplotlib inline
import matplotlib.pyplot as plt
def Challenge_4(data=None):
    if not data:
        data = Challenge_3()
    turnID = data.keys()[0]
    turnTimeS = data[turnID]
    dates = turnTimeS.keys()
    counts = turnTimeS.values()
    dates, counts = zip(*sorted(zip(dates, counts)))
    plt.figure(figsize=(10,3))
    plt.plot(dates,counts)

'''    
 def Challenge_5():
    f = open('turnstile_150404.txt')
    csv_f = csv.reader(f)
    keys = []
    values = []

    for row in csv_f:
        keys.append([row[0], row[1], row[3]])
        values.append([row[6], row[7], row[9]])
    del keys[0]  
    del values[0]
    
    values2 = []
    for i in range(len(values)):
        values2.append([values[i][0] + ' ' + values[i][1]])
        values2[i].extend([values[i][2]])
        values2[i][0] = dateutil.parser.parse(values2[i][0])
    
    subwaydict = {}
    dummylist = []
    for i, key in enumerate(keys):
        if tuple(key) in dummylist:
            subwaydict[tuple(key)].append(values2[i])
        else:
            subwaydict[tuple(key)] = [values2[i]]
            dummylist.append(tuple(key))
    
    for turnstiles in subwaydict.keys():
        i = 0
        while i < len(subwaydict[turnstiles]):
            timegaps = [datetime.time(0, 0), datetime.time(1, 0), datetime.time(2, 0), datetime.time(3, 0)]
            if subwaydict[turnstiles][i][0].time() not in timegaps:
                del subwaydict[turnstiles][i]
            else:
                i += 1
        dates = {}
        for i, values in enumerate(subwaydict[turnstiles]):
            if i == len(subwaydict[turnstiles]) -1:
                break
            subwaydict[values[0]] = int(subwaydict[turnstiles][i+1][1]) - int(values[1])
        subwaydict[turnstiles] = dates
        
    return subwaydict
'''

def ReadData(file='turnstile_150404.txt'):
    with open(file) as f:
        reader = csv.reader(f)
        rows = [[cell.strip() for cell in row] for row in reader]
    
    rows[0].extend(['DateTime', 'Weekday','Week','TurnstileID', 'SubwayID', 'TRAFFIC'])
    
    i = 1
    while i < len(rows):
        # Makes Additional Data Points        
        date = datetime.strptime(rows[i][6] + rows[i][7], '%m/%d/%Y%X')
        
        rows[i].append(date)
        rows[i].append(rows[i][-1].isoweekday())
        rows[i].append(rows[i][-2].isocalendar()[1]) #this accesses the week element in the isocalendar tuple
        
        turnstileID = rows[i][0] + rows[i][1] + rows[i][2] + rows[i][3]
        subwayID = rows[i][0] + rows[i][1] + rows[i][3]
        
        rows[i].append(turnstileID)
        rows[i].append(subwayID)

        # Reshapes the cumulative data
        if rows[i-1][-2] == rows[i][-2]:
            
            # Calculates Entries Traffic
            rows[i-1][9] = int(rows[i][9]) - int(rows[i-1][9])
            
            # Calculates Exit Traffic
            rows[i-1][10] = int(rows[i][10]) - int(rows[i-1][10])
            
            # Calculate Sum of Traffic
            rows[i-1].append(rows[i-1][9] + rows[i-1][10])
        elif i>1:
            rows[i-1][9]  = 0
            rows[i-1][10] = 0
            rows[i-1].append(0)

        i += 1
    
    rows.pop(-1)
    return rows

def CombineData(dlist=['turnstile_150404.txt', 'turnstile_150411.txt', 'turnstile_150418.txt', 'turnstile_150425.txt']):
    output = []
    for i, item in enumerate(dlist):
        if i>0:
            readin = ReadData(item)
            readin.pop(0)
            output.extend(readin)
        else:
            readin = ReadData(item)
            output.extend(readin)
    return output
    
def CleanData():
    data = CombineData()
    col = data[0]
    data = pd.DataFrame(data, columns = col)
    data = data.ix[1:, :]
    #Get rid of data that has negative entry values
    data = data[data.ENTRIES > 0]
    #Get rid of data with entries that are really high
    data = data[data.ENTRIES < 400000]
    return data
    
def aggregateF(group1='DATE', group2=None, output='ENTRIES', data=None):
    try:
        clean_data = not data
    except ValueError:
        clean_data = data.empty
        
    if clean_data:
        data = CleanData()
    if not group2:
        values= data.groupby([group1])[output].agg('sum').order(ascending=False)
    else:
        values= data.groupby([group1,group2])[output].agg('sum')
        values = values.reset_index()
    #values = values.groupby(level=0).apply(lambda x: x.order(ascending=False))
    return values

#Challenge 7
def stationPlot(station='34 ST-PENN STA', x='TIME', y='ENTRIES', data=None):
    series = aggregateF('STATION', x, y, data=data) 
    print(station)
    series[station].plot()
 
#Challenge 8
def Challenge_8(station='34 ST-PENN STA'):
    print station
    data = CleanData()
    d1 = data.groupby(['STATION', 'Weekday', 'Week'])['TRAFFIC'].agg('sum')
    d1 = d1.reset_index()
    
    output = d1[d1['STATION'] == station]
    output = output.pivot('Weekday', 'Week', 'TRAFFIC')
    
    plt.figure(); output.plot(); plt.legend(loc='best')

#Challenge 10
def Challenge_10():
    a = CleanData()
    a = a[a.TRAFFIC > 0]
    data = aggregateF('STATION', output='TRAFFIC', data=a)
    data.hist(bins=20)

'''
ts = Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
df = DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
df = df.cumsum()
plt.figure(); df.plot(); plt.legend(loc='best')
'''

    

    
    
    
    
       
        
            
    
        
    
    




            
            
                
            
    
        
        
        
    


