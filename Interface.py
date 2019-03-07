from MacroData import FRED_Interface as FRED
from MacroData import Sqlite as sql


"""-----------------------------------------------------------------------------------
SQL table has indexKey which has

(series ex. GDP, name "US FY GDP") 

and then 
tableName with data
ex. 
GDP 
(1972, 50,000)
(1973, 48,800)
.......
-----------------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------------
Inserts FRED data which is simply [date, value] with tableName 

tableName is in the form : Gross Domestic Product_GDP  (Name_SeriesName).
-----------------------------------------------------------------------------------"""
def insertMechanism(tableName, data):
    sql.execute('DROP TABLE IF EXISTS ' + tableName, None)
    sql.execute('CREATE TABLE ' + tableName + '(date TEXT, value TEXT)', None)
    
    totalText = ''
    for i in data:
        totalText += '('
        for j in i:
            totalText += "'" + str(j) + "',"
        totalText = totalText[0:len(totalText) -1 ]
        totalText += '),'
    #             tempArray.append(j)
    #         totalText += valuesText + ','
        
    totalText = totalText[0:len(totalText)-1]
    sql.execute('INSERT INTO ' + tableName + ' VALUES ' + totalText, None)
        
"""-----------------------------------------------------------------------------------
Retrieve data by tableName. EX. GDPFY
-----------------------------------------------------------------------------------"""
def getData(tableName):
    tempData = sql.execute('SELECT * FROM ' + tableName)
    data = []
     
    for i in tempData:
        data.append([i[0], float(i[1])])
     
    return data
"""-----------------------------------------------------------------------------------
Get Data Series by getting all tables.
-----------------------------------------------------------------------------------"""
def getAllSeries():
#     temp = sql.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    temp = sql.execute("SELECT * FROM indexKey")

    allTables = []
    for i in temp:
        print(i)
        allTables.append(i[0])
    return allTables
# sql.execute("UPDATE indexKey SET name = 'Real Gross Domestic Product % Change Not Seasonally Adjusted' where series = 'A191RL1A225NBEA' ")
# getAllSeries()
"""-----------------------------------------------------------------------------------
Get Data Series by getting all tables.
-----------------------------------------------------------------------------------"""
def getSeriesName(series):
    return sql.execute("SELECT name FROM indexKey WHERE series = ?", [series])[0][0]

"""-----------------------------------------------------------------------------------
Delete Table
-----------------------------------------------------------------------------------"""
def deleteTable(tableName):
    sql.execute("DROP TABLE IF EXISTS " + tableName, None)

"""-----------------------------------------------------------------------------------
Update All Data Series
-----------------------------------------------------------------------------------"""
def updateAll():
    allSeries = getAllSeries()
    print("Start Update")
    for i in allSeries:
        try:
            print(i)
            """Get update series from FRED"""
            newData = FRED.getFRED_data(i)
            oldData = getData(i)
            
            """No update"""
            if(oldData[-1][0] == newData[-1][0]):
                print("No Update")
                continue
            
            """If new data is missing some earlier data"""
            """Find where oldData matches 0 index of newData. Everything from 0 - difference 
            must later be added to newData."""
            if(oldData[0][0] != newData[0][0]):
                difference = 0
                for j in range(0, len(oldData)):
                    if(oldData[j][0] != newData[0][0]):
                        continue
                    else:
                        difference = j - 1
                        break

                for j in range(0, difference):
                    newData.insert(0, oldData[difference-j])
            
            insertMechanism(i, newData)
            print("Updated Series : " + i)
        except:
            print("Error Failed Update - " + str(i))
    



"""-----------------------------------------------------------------------------------
Search for Duplicates
-----------------------------------------------------------------------------------"""
def duplicates():  
    temp = sql.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    print(len(temp))
      
    allTables = sql.execute("SELECT * FROM indexKey")
    delete = []
    for i in range(0, len(allTables)):
        for j in range(i + 1, len(allTables)):
            if(allTables[i][0] == allTables[j][0]):
                if(j not in delete):
                    print(allTables[i])
                    print(allTables[j])
                    delete.append(j)
    print(delete)           
    newArray = []
    for i in range(0, len(allTables)):
        if(i not in delete):
            newArray.append(allTables[i])
            
    print(len(newArray))
    

newFile = open("FRED_ADD.txt", "r")
for i in newFile.readlines():
    temp = i.split("(")
    series = temp[0].strip()
    name = temp[1]
    name = name[0:len(name) - 2]
    print(series)
    print(name)
    
    
    
    
    
    