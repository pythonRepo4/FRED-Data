from MacroData import Interface
from Analyze import StatisticsFunctions
from astropy.units import day
import Utility
import matplotlib.pyplot as plt

def performRegression(series1, series2):
    reg1, reg2 = [], []
    for j in range(0, len(series1)):
        reg1.append(series1[j][1])
        reg2.append(series2[j][1])
             
    return StatisticsFunctions.linearReg(reg1, reg2)

def makeSeriesSame(series1, series2):
    daysMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    flip = False
    if(len(series1) < len(series2)):
        shorter = series1
        longer = series2
    else:
        shorter = series2
        longer = series1
        flip = True
    secondArray = []

    """Make start years the same """
    yearL = int(longer[-1][0].split("-")[0])
    year = int(shorter[-1][0].split("-")[0])
    while(abs(yearL - year) > 0):
        if(yearL > year):
            del longer[-1]
        if(yearL < year):
            del shorter[-1]
        yearL = int(longer[-1][0].split("-")[0])
        year = int(shorter[-1][0].split("-")[0])
    

    """Try best to match dates. One series may have much more data than another. 
    For regression purposes, match the data by dates.
    
    Start at latest date, and work way back. For easier comparison of dates,
    dates are calculated as Year*365 + Month*days + Days. Ex. 2019/1/25 = 2019*365 + 1 * 0 + 25"""
    for i in range(len(shorter) - 1, -1, -1):
        date = shorter[i][0]
        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)
        shorterDay = sum(daysMonth[0:month-1]) + day + year*365
#         print("SHORT" + date + " : " + str(shorterDay))

        dayDifference = 1000000
        """Try to find closest counterpart in longer. Start at end (latest date) """
        for j in range(len(longer) - 1, -1 , -1):
            longer_date = longer[j][0]
            yearL, monthL, dayL = longer_date.split("-")
            yearL, monthL, dayL = int(yearL), int(monthL), int(dayL)
            longerDay = sum(daysMonth[0:monthL-1]) + dayL + yearL*365
#             print("LONG" + longer_date + " : " + str(longerDay))

            """If same exact date, add immediately"""
            if((shorterDay - longerDay) == 0):
                secondArray.insert(0, longer[j])
                dayDifference = 100000
                 
                """Delete all others"""
#                 for k in range(len(longer) - 1, j - 1, -1):
#                     del longer[k]
                break
            """If shorter date keeps getting closer to longer date, keep iterating.
            Otherwise, stop.  """
            if(abs(shorterDay - longerDay) < dayDifference):
                dayDifference = abs(shorterDay - longerDay)
                continue
            else:
                dayDifference = 1000000
                try:
                    secondArray.insert(0, longer[j+1])
                except:
                    secondArray.insert(0, longer[j])
                """Delete """
#                 for k in range(len(longer) - 1, j - 1, -1):
#                     del longer[k]
                break
            
#         if(abs(year - yearL) > 1):
#             break

#     try:
#         for i in range(0, len(shorter)):
#             print(str(shorter[i]) + " : " +  str(secondArray[i]))
#     except:
#         pass
    
    """Sometimes, shorter date goes back further, at smaller intervals. Cut rest out """
    if(len(shorter) > len(secondArray)):
        difference = len(shorter) - len(secondArray)
        for i in range(0, difference):
            del shorter[0]
    
    """Remove redundant entries on longer """
    while(secondArray[0][0] == secondArray[1][0]):
        del secondArray[0]
        del shorter[0]

    
#     if(len(secondArray) < len(shorter)):
#         for i in range(0, len(secondArray)):
#             del shorter[0]
#     print(len(secondArray))
# #     print(len(shorter))
#     for i in range(0, len(shorter)):
#         print(str(shorter[i]) + " : " +  str(secondArray[i]))
 
    if(flip == True):
        return secondArray, shorter
    else:
        return shorter, secondArray
    
"""-----------------------------------------------------------------------------------
Simple plot function 
-----------------------------------------------------------------------------------"""   
def plot(tickerName, x, y, x_axis , y_axis):
    plt.title(tickerName)
    plt.plot(x, y)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.show()
    
"""-------------------------------------------------------------------------------------
Stagger series 2 at 6 months. Ex. Compare 10-yr (series 2) at 01/2015 v GDP (series 1) at 06/2015
------------------------------------------------------------------------------------"""
def regressStaggered(name1, name2, stagger):
    series1, series2 = makeSeriesSame(Interface.getData(name1), Interface.getData(name2)) 
    daysMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    date = series2[-1][0]
    year, month, day = date.split("-")
    year, month, day = int(year), int(month), int(day)
    days = sum(daysMonth[0:month-1]) + day + year*365

    truncate = 0
    staggerDate = days - stagger
    """Stagger""" 
    for i in range(len(series2) - 2, -1, -1):
        date = series2[i][0]
        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)
        nextDate = sum(daysMonth[0:month-1]) + day + year*365
        
        if(nextDate < staggerDate):
            break
        
        truncate += 1
    
    regressionSeries2 = series2[-1][1]
    for i in range(0, truncate):
        del series2[-1]
        del series1[0]
        
#     for i in range(0, len(series1)):
#         print(str(series1[i]) + " : " +  str(series2[i]))
        
    m, b, r2 = performRegression(series1, series2)
#     if(r2 > .70):
    name = Interface.getSeriesName(name1) + " VS. " + Interface.getSeriesName(name2)
    print(name + " : r2 = " + str(r2))
    print("Possible GDP Value = " + str(float(m) * float(regressionSeries2) + float(b)))
#         plot1, plot2 = [], []
#         for i in series1:
#             plot1.append(i[1])
#         for i in series2:
#             plot2.append(i[1])
#         plot(name, plot1, plot2, "Y", "X")

def runRegression():
    seriesList = Interface.getAllSeries()
     
    """Regress to GDP """
    for i in seriesList:
        print(i)
        if(i == "GDP"):
            continue
        try:
            regressStaggered("GDP", i, 183)
            regressStaggered("GDP", i, 365)
        except:
            print("error" + i)

# runRegression()
# regressStaggered("GDP", "DFII5", 183)
# series1, series2 = makeSeriesSame(Interface.getData("GDP"), Interface.getData("FKKYGTA"))

    
    
