"""
This is the class for connecting to gardens with sockets
All gardens must be on the same network for this to work
I haveno idea what im doing
"""

import socket
import random
import time

class Garden:
    
    def __init__(self):
        global temperature
        global humidity
        global averageSoilMoisture
        global greatestSoilMoisture
        global lowestSoilMoisture
        global maxTemperature
        global minTemperature
        global maxHumidity
        global minHumidity
        global optimalMoisture
        global fanState
        maxTemperature = 22
        minTemperature = 17
        maxHumidity = 55
        minHumidity = 45
        optimalMoisture = 45
        temperature = 20
        humidity = 50
        averageSoilMoisture = 47
        greatestSoilMoisture = 51
        lowestSoilMoisture = 45
        fanState = False
    
    
    def updateTemp(self):
        global temperature
        toAdd = random.randrange(-1, 1)
        temperature = temperature + toAdd
        
        if temperature > maxTemperature:
            temperature = temperature - 3
        elif temperature < minTemperature:
            temperature = temperature + 3
    
    def updateHumidity(self):
        global humidity
        toAdd = random.randrange(-1, 1)
        humidity = humidity + toAdd
        
        if humidity > maxHumidity:
            humidity = humidiy - 3
        elif humidity < minHumidity:
            humidity = humidity + 3
    
    def updateSoilMoisture(self):
        global lowestSoilMoisture
        global greatestSoilMoisture
        global averageSoilMoisture
        moistureValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(moistureValues)):
            toAdd = random.randrange(-(random.randrange(3, 5)), random.randrange(3, 5))
            moistureValues[i] = averageSoilMoisture + toAdd
            
            if moistureValues[i] < optimalMoisture:
                moistureValues[i] = moistureValues[i] + 3
                
            if moistureValues[i] > optimalMoisture + 10:
                moistureValues[i] = moistureValues[i] - 3
            
        highestValue = -1
        lowestValue = 101
        sumValues = 0
            
        for i in range(len(moistureValues)):
            sumValues = sumValues + moistureValues[i]
            if moistureValues[i] > highestValue:
                highestValue = moistureValues[i]
            if moistureValues[i] < lowestValue:
                lowestValue = moistureValues[i]
            
        lowestSoilMoisture = int(lowestValue)
        greatestSoilMoisture = int(highestValue)
        averageSoilMoisture = int(sumValues / len(moistureValues))

    def getTemp(self):
        return(temperature)
    
    def getHmd(self):
        return(humidity)
    
    def getAverageMoisture(self):
        return(averageSoilMoisture)
    
    def getGreatestMoisture(self):
        global greatestSoilMoisture
        return(greatestSoilMoisture)
    
    def getLowestMoisture(self):
        return(lowestSoilMoisture)
    
    def modOptimalMoisture(self, newMoisture):
        global optimalMoisture
        optimalMoisture = int(newMoisture)
        
    def modMaxTemperature(self, newMaxTemp):
        global maxTemperature
        maxTemperature = newMaxTemp
        
    def modMinTemperature(self, newMinTemp):
        global minTemperature
        minTemperature = newMinTemp
        
    def modMaxHumidity(self, newMaxHmd):
        global maxHumidity
        maxHumidity = newMaxHmd
        
    def modMinHumidity(self, newMinHmd):
        global minHumidity
        minHumidity = newMinHmd
        
    def getMaxTemp(self):
        return(maxTemperature)
    
    def getMinTemp(self):
        return(minTemperature)
    
    def getMaxHmd(self):
        return(maxHumidity)
    
    def getMinHmd(self):
        return(minHumidity)
    
    def getOptimalMoisture(self):
        return(optimalMoisture)
