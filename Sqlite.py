import sqlite3
import os
from Variables import *

def execute(commands, input = None):
    directory = Variables.preDirectory + '\\MacroData\\MacroData.db'
    conn = sqlite3.connect(directory)
    c = conn.cursor()
    returnArray = []
    
    
    if(input == None or input == False):
        cursor = c.execute(commands)
    else:
        cursor = c.execute(commands,input)

    for i in cursor:
        returnArray.append(i)
    
    conn.commit()
    conn.close()
    
    return returnArray
