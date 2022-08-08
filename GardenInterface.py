"""
This is the class for connecting to gardens with sockets
All gardens must be on the same network for this to work
I have no idea what im doing
"""

import socket
import random
import time
from datetime import datetime

class Garden:
    
    def __init__(self):
        global temperature
        global humidity
        global averageSoilMoisture
        global greatestSoilMoisture
        global lowestSoilMoisture
        global optimalMoisture
        global fanState
        global clientSocket
        global moistureList
        optimalMoisture = 45
        temperature = 20
        humidity = 50
        averageSoilMoisture = 47
        greatestSoilMoisture = 51
        lowestSoilMoisture = 45
        fanState = False
        moistureList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    
    
    def updateTemp(self):
        global temperature
        global clientSocket
        
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send('request.temp'.encode())
            response = clientSocket.recv(1024).decode()
            temperature = (response.split("."))[2]
            clientSocket.close()
            
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
        
        
    def updateHumidity(self):
        global humidity
        global clientSocket
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send('request.hmd'.encode())
            response = clientSocket.recv(1024).decode()
            humidity = (response.split("."))[2]
            clientSocket.close()
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
        
    def updateSoilMoisture(self):
        global moistureList
        global averageSoilMoisture
        global greatestSoilMoisture
        global lowestSoilMoisture
        global clientSocket
        
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send('request.soil'.encode())
            response = clientSocket.recv(1024).decode()
            soilMoistureValuesStr = (response.split("."))[2]
            soilMoistureValuesStr = soilMoistureValuesStr.replace("[", "")
            soilMoistureValuesStr = soilMoistureValuesStr.replace(":]", "")
            strMoistureValuesArr = soilMoistureValuesStr.split(":")
            
            highestValue = -1
            lowestValue = 101
            sumValues = 0
                
            for i in range(len(strMoistureValuesArr)):
                moistureList[i] = int(strMoistureValuesArr[i])
                sumValues = sumValues + moistureList[i]
                if moistureList[i] > highestValue:
                    highestValue = moistureList[i]
                if moistureList[i] < lowestValue:
                    lowestValue = moistureList[i]
                
            lowestSoilMoisture = lowestValue
            greatestSoilMoisture = highestValue
            averageSoilMoisture = int(sumValues / len(moistureList))
            clientSocket.close()
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
    
        
    
    def getTemp(self):
        return(temperature)
    
    def getHmd(self):
        return(humidity)
    
    def getAverageMoisture(self):
        return(averageSoilMoisture)
    
    def getGreatestMoisture(self):
        return(greatestSoilMoisture)
    
    def getLowestMoisture(self):
        return(lowestSoilMoisture)
    
    def modLights(self, rgb):
        print(rgb)
        
    def modMaxTemperature(self, newMaxTemp):
        maxTemperature = newMaxTemp
        
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send(('mod.temp.max.' + str(newMaxTemp)).encode())
            clientSocket.close()
            
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
        
    def modMinTemperature(self, newMinTemp):
        minTemperature = newMinTemp
        
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send(('mod.temp.min.' + str(newMinTemp)).encode())
            clientSocket.close()
            
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
        
        
    def modMaxHumidity(self, newMaxHmd):
        maxHumidity = int(newMaxHmd)
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send(('mod.hmd.max.' + str(newMaxHmd)).encode())
            clientSocket.close()
            
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
        
        
    def modMinHumidity(self, newMinHmd):
        minHumidity = newMinHmd
        
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send(('mod.hmd.min.' + str(newMinHmd)).encode())
            clientSocket.close()
            
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
            
    def modOptimalSoil(self, newOptimalSoil):
        optimalMoiture = newOptimalSoil
        
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send(('mod.soil.' + str(newOptimalSoil)).encode())
            clientSocket.close()
            
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
            
    def getMaxTemp(self):
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send('get.temp.max'.encode())
            response = clientSocket.recv(1024).decode()
            maxTemp = (response.split("."))[1]
            clientSocket.close()
            return(int(maxTemp))
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
            return(-1)
        
    def getMinTemp(self):
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send('get.temp.min'.encode())
            response = clientSocket.recv(1024).decode()
            minTemp = (response.split("."))[1]
            clientSocket.close()
            return(int(minTemp))
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
            return(-1)
    
    def getMaxHmd(self):
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send('get.hmd.max'.encode())
            response = clientSocket.recv(1024).decode()
            maxHmd = (response.split("."))[1]
            clientSocket.close()
            return(int(maxHmd))
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
            return(-1)
    
    def getMinHmd(self):
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send('get.hmd.min'.encode())
            response = clientSocket.recv(1024).decode()
            minHmd = int((response.split("."))[1])
            clientSocket.close()
            return(int(minHmd))
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
            return(-1)
    
    def getOptimalMoisture(self):
        try:
            clientSocket = socket.socket()
            clientSocket.connect(('127.0.0.1', 8080))
            clientSocket.send('get.soil'.encode())
            response = clientSocket.recv(1024).decode()
            optimalMoisture = (response.split("."))[1]
            clientSocket.close()
            return(int(optimalMoisture))
        except:
            print("Error contacting Garden")
            print("or something, i don't really know")
            return(-1)