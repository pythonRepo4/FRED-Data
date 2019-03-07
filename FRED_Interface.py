import csv
import urllib
from bs4 import BeautifulSoup


"""--------------------------------------------------------------------------------------------------


FRED Key - 76a9cc0b26d2fabcf6e75565ca4d3923

For example: US GDP - 
--------------------------------------------------------------------------------------------------"""


def getFRED_data(series_id):
    FRED_key = '76a9cc0b26d2fabcf6e75565ca4d3923'
    
    tempR = urllib.request.urlopen(''.join(['https://api.stlouisfed.org/fred/series/observations?series_id=', series_id,
                                     '&api_key=' , FRED_key]))
    
    rFred = tempR.read()
                                            
    bs = BeautifulSoup(rFred, 'lxml')
    
    FRED_data = []
    obs = bs.find_all('observation')
    for observations in obs:
        tempFred = []
        tempS = str(observations)
        tempSplit = tempS.split('"')
        obsDate = ""
        value = ""
        for i in range(0, len(tempSplit)):
            split = tempSplit[i]
    
            if("observation date" in split):
                obsDate = tempSplit[i+1]
                continue
                
            if("value=" in split):
                value = tempSplit[i+1]
                break
            
        if(value == "."):
            continue
        FRED_data.append([obsDate, value])
        
    return FRED_data

