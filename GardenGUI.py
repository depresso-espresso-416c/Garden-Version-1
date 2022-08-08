import tkinter as tk
from tkinter import *
import tkinter.font as tkFont

from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image

import socket
from datetime import datetime
from datetime import timedelta
import datetime as dt
import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import GardenInterface

lastColor = '#ff09ac'

gardenOne = GardenInterface.Garden()
gardenOne.updateSoilMoisture()

xAir = []
xSoil = []
temps = []
hmds = []
avgMoistures = []
greatestMoistures = []
lowestMoistures = []

update_interval = 15000
max_elements = 60

tempConfigOpen = False
minTempValue = gardenOne.getMinTemp()

currentTemp = 20
maxTempValue = gardenOne.getMaxTemp()
temporaryMinTemp = minTempValue
temporaryMaxTemp = maxTempValue

humConfigOpen = False
minHumValue = gardenOne.getMinHmd()
currentHmd = 50
maxHumValue = gardenOne.getMaxHmd()
temporaryMinHum = minHumValue
temporaryMaxHum = maxHumValue

soilConfigOpen = False
optimalMoisture = gardenOne.getOptimalMoisture()
averageSoilMoisture = 47
greatestSoilMoistureValue = 51
lowestSoilMoistureValue = 45

temporaryOptiSoilMoisture = optimalMoisture

def increaseMaxTemp(entry):
    if maxTempValue < 40:
        updateMaxTemp(maxTempValue + 1)
def increaseMinTemp(entry):
    if minTempValue < 40:
        updateMinTemp(minTempValue + 1)
def decreaseMaxTemp(entry):
    if maxTempValue > 5:
        updateMaxTemp(maxTempValue - 1)
def decreaseMinTemp(entry):
    if minTempValue > 5:
        updateMinTemp(minTempValue - 1)
        
def maxTempEntryCommand(maxTempEntryCommands):
    maxTempEntryStr = maxTempEntry.get()
    maxTempEntryInt = int(maxTempEntryStr)
    if maxTempEntryInt > 40:
        maxTempEntryInt = 40
    elif maxTempEntryInt < 5:
        maxTempEntryInt = 5
    updateMaxTemp(maxTempEntryInt)
    
def minTempEntryCommand(minTempEntryCommands):
    minTempEntryStr = minTempEntry.get()
    minTempEntryInt = int(minTempEntryStr)
    if minTempEntryInt > 40:
        minTempEntryInt = 40
    elif minTempEntryInt < 5:
        minTempEntryInt = 5
    updateMinTemp(minTempEntryInt)

def saveTempConfig():
    global tempConfigOpen
    tempConfigOpen = False
    if maxTempValue != temporaryMaxTemp:
        gardenOne.modMaxTemperature(maxTempValue)
    if minTempValue != temporaryMinTemp:
        gardenOne.modMinTemperature(minTempValue)
    tempConfigWindow.destroy()
    
def cancelTempConfig():
    global tempConfigOpen
    global minTempValue
    global maxTempValue
    tempConfigOpen = False
    updateMinTemp(temporaryMinTemp)
    updateMaxTemp(temporaryMaxTemp)
    tempConfigWindow.destroy()

def updateMinTemp(val):
    global minTempValue
    global maxTempValue
    
    val=int(float(val))
    
    minTempValue = val
    minTempScale.set(val)
    minTempEntry.delete(0, tk.END)
    minTempEntry.insert(0, str(minTempValue))
    minTemperatureLabel.configure(text = "Min temperature \nparameter: " + str(minTempValue))
    if val > maxTempValue and val <= 40:
        updateMaxTemp(val+1)

def updateMaxTemp(val):
    global minTempValue
    global maxTempValue
    
    val = int(float(val))
    maxTempValue = val
    maxTempScale.set(val)
    maxTempEntry.delete(0, tk.END)
    maxTempEntry.insert(0, str(maxTempValue))
    maxTemperatureLabel.configure(text = "Max temperature \nparameter: " + str(maxTempValue))
    if val < minTempValue and val >= 5:
        updateMinTemp(val-1)

def configureTemp():
    global tempConfigOpen
    global maxTempValue
    global minTempValue
    global temporaryMaxTemp
    global temporaryMinTemp
    
    if tempConfigOpen == False:
        tempConfigOpen = True
        temporaryMaxTemp = maxTempValue
        temporaryMinTemp = minTempValue
        
        global tempConfigWindow
        tempConfigWindow = Toplevel()
        tempConfigWindow.title("Temp Config")
        tempConfigWindow.geometry("250x350")
        tempConfigWindow.resizable(False, False)
        tk.Label(tempConfigWindow, text='Configure Temperature',font=("areil", 13)).pack(pady=5)
        tk.Label(tempConfigWindow, text = str(minTempValue))
        
        global maxTempScale
        global minTempScale
        global maxTempEntry
        global minTempEntry
        
        maxTempLabel = tk.Label(tempConfigWindow, text = 'Max Temp')
        minTempLabel = tk.Label(tempConfigWindow, text = 'Min Temp')
        maxTempScale = tk.Scale(tempConfigWindow, from_=40, to=5, tickinterval = 5, digit = 2, command = updateMaxTemp, length = 200, orient=VERTICAL)
        minTempScale = tk.Scale(tempConfigWindow, from_=40, to=5, tickinterval = 5, digit = 2, command = updateMinTemp, length = 200, orient=VERTICAL)
        maxTempEntry = tk.Entry(tempConfigWindow, width = 3)
        minTempEntry = tk.Entry(tempConfigWindow, width = 3)
        maxTempEntry.bind('<KP_Enter>', maxTempEntryCommand)
        minTempEntry.bind('<KP_Enter>', minTempEntryCommand)
        maxTempScale.bind('<Button-4>', increaseMaxTemp)
        maxTempScale.bind('<Button-5>', decreaseMaxTemp)
        minTempScale.bind('<Button-4>', increaseMinTemp)
        minTempScale.bind('<Button-5>', decreaseMinTemp)
        increaseMaxTempBtn = tk.Button(tempConfigWindow, text = '+', command = lambda: increaseMaxTemp(""), height = 1)
        increaseMinTempBtn = tk.Button(tempConfigWindow, text = '+', command = lambda: increaseMinTemp(""), height = 1)
        decreaseMaxTempBtn = tk.Button(tempConfigWindow, text = '-', command = lambda: decreaseMaxTemp(""), height = 1)
        decreaseMinTempBtn = tk.Button(tempConfigWindow, text = '-', command = lambda: decreaseMinTemp(""), height = 1)
        saveTempBtn = tk.Button(tempConfigWindow, text = "Save", command = saveTempConfig, width = 6)
        cancelTempBtn = tk.Button(tempConfigWindow, text = "Cancel", command = cancelTempConfig, width = 6)
        
        
        maxTempScale.set(maxTempValue)
        minTempScale.set(minTempValue)
        maxTempEntry.delete(0, tk.END)
        minTempEntry.delete(0, tk.END)
        maxTempEntry.insert(0, str(maxTempValue))
        minTempEntry.insert(0, str(minTempValue))
        
        maxTempLabel.place(x=40, y=30)
        minTempLabel.place(x=130, y=30)
        maxTempScale.place(x=30, y=50)
        minTempScale.place(x=120, y=50)
        maxTempEntry.place(x=56, y=260)
        minTempEntry.place(x=156, y=260)
        increaseMaxTempBtn.place(x=85, y=255)
        increaseMinTempBtn.place(x=185, y=255)
        decreaseMaxTempBtn.place(x=25, y=255)
        decreaseMinTempBtn.place(x=125, y=255)
        saveTempBtn.place(x=30, y=300)
        cancelTempBtn.place(x=140, y=300)
        
        tempConfigWindow.protocol("WM_DELETE_WINDOW", saveTempConfig)
        
        
def increaseMaxHum(entry):
    if maxHumValue < 100:
        updateMaxHum(maxHumValue + 1)
def increaseMinHum(entry):
    if minHumValue < 100:
        updateMinHum(minHumValue + 1)
def decreaseMaxHum(entry):
    if maxHumValue > 0:
        updateMaxHum(maxHumValue - 1)
def decreaseMinHum(entry):
    if minHumValue > 0:
        updateMinHum(minHumValue - 1)
        
def maxHumEntryCommand(maxHumEntryCommands):
    maxHumEntryStr = maxHumEntry.get()
    maxHumEntryInt = int(maxHumEntryStr)
    if maxHumEntryInt > 100:
        maxHumEntryInt = 100
    elif maxHumEntryInt < 0:
        maxHumEntryInt = 0
    updateMaxHum(maxHumEntryInt)
    
def minHumEntryCommand(minHumEntryCommands):
    minHumEntryStr = minHumEntry.get()
    minHumEntryInt = int(minHumEntryStr)
    if minHumEntryInt > 100:
        minHumEntryInt = 100
    elif minHumEntryInt < 0:
        minHumEntryInt = 0
    updateMinHum(minHumEntryInt)

def saveHumConfig():
    global humConfigOpen
    if maxHumValue != temporaryMaxHum:
        gardenOne.modMaxHumidity(maxHumValue)
    if minHumValue != temporaryMinHum:
        gardenOne.modMinHumidity(minHumValue)
    humConfigOpen = False
    humConfigWindow.destroy()
    
def cancelHumConfig():
    global humConfigOpen
    global minHumValue
    global maxHumValue
    global temporaryMaxHum
    global temporaryMinHum
    humConfigOpen = False
    updateMinHum(temporaryMinHum)
    updateMaxHum(temporaryMaxHum)
    humConfigWindow.destroy()

def updateMinHum(val):
    global minHumValue
    global maxHumValue
    
    val=int(float(val))
    
    minHumValue = val
    minHumScale.set(val)
    minHumEntry.delete(0, tk.END)
    minHumEntry.insert(0, str(minHumValue))
    minHumidityLabel.configure(text = "Min humidity \nparameter: " + str(minHumValue))
    if val > maxHumValue and val <= 100:
        updateMaxHum(val+1)

def updateMaxHum(val):
    global minHumValue
    global maxHumValue
    
    val = int(float(val))
    maxHumValue = val
    maxHumScale.set(val)
    maxHumEntry.delete(0, tk.END)
    maxHumEntry.insert(0, str(maxHumValue))
    maxHumidityLabel.configure(text = "Max humidity \nparameter: " + str(maxHumValue))
    if val < minHumValue and val >= 0:
        updateMinHum(val-1)

def configureHum():
    global humConfigOpen
    global maxHumValue
    global minHumValue
    global temporaryMaxHum
    global temporaryMinHum
    
    if humConfigOpen == False:
        humConfigOpen = True
        temporaryMaxHum = maxHumValue
        temporaryMinHum = minHumValue
        
        global humConfigWindow
        humConfigWindow = Toplevel()
        humConfigWindow.title("Hum Config")
        humConfigWindow.geometry("250x350")
        humConfigWindow.resizable(False, False)
        tk.Label(humConfigWindow, text='Configure Humerature',font=("areil", 13)).pack(pady=5)
        tk.Label(humConfigWindow, text = str(minHumValue))
        
        global maxHumScale
        global minHumScale
        global maxHumEntry
        global minHumEntry
        
        maxHumLabel = tk.Label(humConfigWindow, text = 'Max Hum')
        minHumLabel = tk.Label(humConfigWindow, text = 'Min Hum')
        maxHumScale = tk.Scale(humConfigWindow, from_=100, to=0, tickinterval = 10, digit = 2, command = updateMaxHum, length = 200, orient=VERTICAL)
        minHumScale = tk.Scale(humConfigWindow, from_=100, to=0, tickinterval = 10, digit = 2, command = updateMinHum, length = 200, orient=VERTICAL)
        maxHumEntry = tk.Entry(humConfigWindow, width = 3)
        minHumEntry = tk.Entry(humConfigWindow, width = 3)
        maxHumEntry.bind('<KP_Enter>', maxHumEntryCommand)
        minHumEntry.bind('<KP_Enter>', minHumEntryCommand)
        maxHumScale.bind('<Button-4>', increaseMaxHum)
        maxHumScale.bind('<Button-5>', decreaseMaxHum)
        minHumScale.bind('<Button-4>', increaseMinHum)
        minHumScale.bind('<Button-5>', decreaseMinHum)
        increaseMaxHumBtn = tk.Button(humConfigWindow, text = '+', command = lambda: increaseMaxHum(""), height = 1)
        increaseMinHumBtn = tk.Button(humConfigWindow, text = '+', command = lambda: increaseMinHum(""), height = 1)
        decreaseMaxHumBtn = tk.Button(humConfigWindow, text = '-', command = lambda: decreaseMaxHum(""), height = 1)
        decreaseMinHumBtn = tk.Button(humConfigWindow, text = '-', command = lambda: decreaseMinHum(""), height = 1)
        saveHumBtn = tk.Button(humConfigWindow, text = "Save", command = saveHumConfig, width = 6)
        cancelHumBtn = tk.Button(humConfigWindow, text = "Cancel", command = cancelHumConfig, width = 6)
        
        
        maxHumScale.set(maxHumValue)
        minHumScale.set(minHumValue)
        maxHumEntry.delete(0, tk.END)
        minHumEntry.delete(0, tk.END)
        maxHumEntry.insert(0, str(maxHumValue))
        minHumEntry.insert(0, str(minHumValue))
        
        maxHumLabel.place(x=40, y=30)
        minHumLabel.place(x=130, y=30)
        maxHumScale.place(x=30, y=50)
        minHumScale.place(x=120, y=50)
        maxHumEntry.place(x=56, y=260)
        minHumEntry.place(x=156, y=260)
        increaseMaxHumBtn.place(x=85, y=255)
        increaseMinHumBtn.place(x=185, y=255)
        decreaseMaxHumBtn.place(x=25, y=255)
        decreaseMinHumBtn.place(x=125, y=255)
        saveHumBtn.place(x=30, y=300)
        cancelHumBtn.place(x=140, y=300)
        
        humConfigWindow.protocol("WM_DELETE_WINDOW", saveHumConfig)
        
def increaseOptimalMoisture(entry):
    global optimalMoisture
    if optimalMoisture < 100:
        updateOptimalMoisture(optimalMoisture + 1)
        
def decreaseOptimalMoisture(entry):
    global optimalMoisture
    if optimalMoisture > 0:
        updateOptimalMoisture(optimalMoisture - 1)

    
def optimalMoistureEntryCommand(optimalMoistureEntryCommands):
    optimalMoistureEntryStr = optimalMoistureEntry.get()
    optimalMoistureEntryInt = int(optimalMoistureEntryStr)
    if optimalMoistureEntryInt > 100:
        optimalMoistureEntryInt = 100
    elif optimalMoistureEntryInt < 0:
        optimalMoistureEntryInt = 0
    updateOptimalMoisture(optimalMoistureEntryInt)

def saveOptimalMoistureConfig():
    global soilConfigOpen
    soilConfigOpen = False
    moistureConfigWindow.destroy()
    gardenOne.modOptimalSoil(optimalMoisture)
    
def cancelOptimalMoistureConfig():
    global soilConfigOpen
    global optimalMoistureValue
    global temporaryOptimalMoisture
    soilConfigOpen = False
    updateOptimalMoisture(temporaryOptimalMoisture)
    moistureConfigWindow.destroy()

def updateOptimalMoisture(val):
    global optimalMoisture
    val = int(float(val))
    optimalMoisture = val
    optimalMoistureScale.set(val)
    optimalMoistureEntry.delete(0, tk.END)
    optimalMoistureEntry.insert(0, str(optimalMoisture))
    optimalMoistureLabel.configure(text = "optimalMoisture \nparameter: " + str(optimalMoisture))

def configureSoilMoisture():
    global soilConfigOpen
    global optimalMoisture
    global temporaryOptimalMoisture
    
    if soilConfigOpen == False:
        soilConfigOpen = True
        temporaryOptimalMoisture = optimalMoisture
        
        global moistureConfigWindow
        moistureConfigWindow = Toplevel()
        moistureConfigWindow.title("Moisture Config")
        moistureConfigWindow.geometry("250x350")
        moistureConfigWindow.resizable(False, False)
        tk.Label(moistureConfigWindow, text='Configure Optimal Moisture',font=("areil", 13)).pack(pady=5)
        tk.Label(moistureConfigWindow, text = str(optimalMoisture))
        
        global optimalMoistureScale
        global optimalMoistureEntry
        
        optimalMoistureLabel = tk.Label(moistureConfigWindow, text = 'Optimal Moisture')
        optimalMoistureScale = tk.Scale(moistureConfigWindow, from_=100, to=0, tickinterval = 10, digit = 2, command = updateOptimalMoisture, length = 200, orient=VERTICAL)
        optimalMoistureEntry = tk.Entry(moistureConfigWindow, width = 3)
        optimalMoistureEntry.bind('<KP_Enter>', optimalMoistureEntryCommand)
        optimalMoistureScale.bind('<Button-4>', increaseOptimalMoisture)
        optimalMoistureScale.bind('<Button-5>', decreaseOptimalMoisture)
        increaseOptimalMoistureBtn = tk.Button(moistureConfigWindow, text = '+', command = lambda: increaseOptimalMoisture(""), height = 1)
        decreaseOptimalMoistureBtn = tk.Button(moistureConfigWindow, text = '-', command = lambda: decreaseOptimalMoisture(""), height = 1)
        saveOptimalMoistureBtn = tk.Button(moistureConfigWindow, text = "Save", command = saveOptimalMoistureConfig, width = 6)
        cancelOptimalMoistureBtn = tk.Button(moistureConfigWindow, text = "Cancel", command = cancelOptimalMoistureConfig, width = 6)
        
        
        optimalMoistureScale.set(optimalMoisture)
        optimalMoistureEntry.delete(0, tk.END)
        optimalMoistureEntry.insert(0, str(optimalMoisture))
        optimalMoistureLabel.place(x=75, y=30)
        optimalMoistureScale.place(x=80, y=50)
        optimalMoistureEntry.place(x=115, y=260)
        increaseOptimalMoistureBtn.place(x=145, y=255)
        decreaseOptimalMoistureBtn.place(x=85, y=255)
        saveOptimalMoistureBtn.place(x=30, y=300)
        cancelOptimalMoistureBtn.place(x=140, y=300)
        
        moistureConfigWindow.protocol("WM_DELETE_WINDOW", saveOptimalMoistureConfig)


def animateAir(i, tempGraph, hmdGraph, xAir, temps, hmds):
    gardenOne.updateTemp()
    gardenOne.updateHumidity()
    currentTemp = gardenOne.getTemp()
    currentHmd = gardenOne.getHmd()
    
    currentTempLabel.configure(text = 'Current Temp: ' + str(currentTemp))
    currentHumLabel.configure(text = 'Current Hmd: ' + str(currentHmd))
    
    timestamp = mdates.date2num(dt.datetime.now())
    xAir.append(timestamp)
    
    temps.append(int(currentTemp))
    hmds.append(int(currentHmd))
    
    xAir = xAir[-max_elements:]
    temps = temps[-max_elements:]
    hmds = hmds[-max_elements:]
    
    color = 'tab:red'
    tempGraph.clear()
    tempGraph.set(ylim=(0, 100))
    tempGraph.set_ylabel('Temperature (C)', color=color)
    tempGraph.tick_params(axis='y', labelcolor=color)
    tempGraph.fill_between(xAir, temps, 0, linewidth=2, color=color, alpha=0.3)
    
    color = 'tab:blue'
    hmdGraph.clear()
    hmdGraph.set(ylim=(0, 100))
    hmdGraph.set_ylabel('Humidity (%)', color=color)
    hmdGraph.tick_params(axis='y', labelcolor=color)
    hmdGraph.plot(xAir, hmds, linewidth=2, color=color)
    
    tempGraph.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    airGraphFig.autofmt_xdate()
    
    tempGraph.collections[0].set_visible(True)
    hmdGraph.get_lines()[0].set_visible(True)
    

def animateSoil(i, avgGraph, greatestGraph, lowestGraph, xSoil, avgMoistures, greatestMoistures, lowestMoistures):
    gardenOne.updateSoilMoisture()
    averageSoilMoisture = gardenOne.getAverageMoisture()
    greatestSoilMoisture = gardenOne.getGreatestMoisture()
    lowestSoilMoisture = gardenOne.getLowestMoisture()
    
    currentSoilMoistureLabel.configure(text = 'Average Soil\n Moisture: ' + str(averageSoilMoisture))
    greatestSoilMoistureLabel.configure(text = 'Greatest Soil\n Moisture: ' + str(greatestSoilMoisture))
    lowestSoilMoistureLabel.configure(text = 'Lowest Soil\n Moisture: ' + str(lowestSoilMoisture))
    
    graphYMin = int(lowestSoilMoisture) - 5
    graphYMax = int(greatestSoilMoisture) + 5
    
    
    timestamp = mdates.date2num(dt.datetime.now())
    xSoil.append(timestamp)
    
    avgMoistures.append(int(averageSoilMoisture))
    greatestMoistures.append(int(greatestSoilMoisture))
    lowestMoistures.append(int(lowestSoilMoisture))
    
    xSoil = xSoil[-max_elements:]
    avgMoistures = avgMoistures[-max_elements:]
    greatestMoistures = greatestMoistures[-max_elements:]
    lowestMoistures = lowestMoistures[-max_elements:]
    
    color = 'tab:red'
    avgGraph.clear()
    avgGraph.set(ylim=(graphYMin, graphYMax))
    avgGraph.set_ylabel('Average Moisture (%)', color=color)
    avgGraph.tick_params(axis='y', labelcolor=color)
    avgGraph.fill_between(xSoil, avgMoistures, 0, linewidth=2, color=color, alpha=0.3)
    
    color = 'tab:blue'
    greatestGraph.clear()
    greatestGraph.set(ylim=(graphYMin, graphYMax))
    greatestGraph.set_ylabel('Greatest Moisture (%)', color=color)
    greatestGraph.tick_params(axis='y', labelcolor=color)
    greatestGraph.plot(xSoil, greatestMoistures, linewidth=2, color=color, solid_capstyle='round')
    
    color = 'tab:green'
    lowestGraph.clear()
    lowestGraph.set(ylim=(graphYMin, graphYMax))
    lowestGraph.spines['right'].set_position(("axes", 1.2))
    lowestGraph.set_ylabel('Lowest Moisture (%)', color=color)
    lowestGraph.tick_params(axis='y', labelcolor=color)
    
    lowestGraph.plot(xSoil, lowestMoistures, linewidth=2, color=color)
    
    avgGraph.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    airGraphFig.autofmt_xdate()
    
    avgGraph.collections[0].set_visible(True)
    greatestGraph.get_lines()[0].set_visible(True)
    lowestGraph.get_lines()[0].set_visible(True)
    

def callBack():
    global lastColor
    result = askcolor(title = "Tkinter Color Chooser", color = lastColor)
    if str(result[1]) != 'None':
        lastColor = result[1]
        gardenOne.modLights(result[0])
    colorBox.configure(bg=lastColor)
    
     
root = tk.Tk()
root.geometry('1100x700')

root.resizable(False, False)
root.title("Garden Control Panel")

rootLabel = tk.Label(root, text = 'Garden Control Panel', font = ('Aerial', 20))
colorFrame = tk.LabelFrame(root, text = 'Light Color', labelanchor = 'n', relief='sunken', width = 150, height = 205)
colorBox = tk.Button(colorFrame, text='', command=callBack, bg=lastColor, height = 5, width = 10)
tk.Button(colorFrame, text='Choose Color',command=callBack, width = 10).place(x = 17, y = 115)

temperatureFrame = tk.LabelFrame(root, text = 'Temperature', labelanchor = 'n', relief='sunken', width = 150, height = 205)
btnConfigTemp = tk.Button(temperatureFrame, text = 'Configure', command = configureTemp)
maxTemperatureLabel = tk.Label(temperatureFrame, text = "Max temperature \nparameter: " + str(maxTempValue), justify = "left")
minTemperatureLabel = tk.Label(temperatureFrame, text = "Min temperature \nparameter: " + str(minTempValue), justify = "left")
currentTempLabel = tk.Label(temperatureFrame, text = "Current Temp: ", font = ("aerial", 10))

humidityFrame = tk.LabelFrame(root, text = 'Humidity', labelanchor = 'n', relief='sunken', width = 150, height = 205)
maxHumidityLabel = tk.Label(humidityFrame, text = "Max humidity \nparameter: " + str(maxHumValue), justify = "left")
minHumidityLabel = tk.Label(humidityFrame, text = "Min humidity \nparameter: " + str(minHumValue), justify = "left")
btnConfigHum = tk.Button(humidityFrame, text = 'Configure', command = configureHum)
currentHumLabel = tk.Label(humidityFrame, text = 'Current Hmd: ', font = ('aerial', 10))

soilMoistureFrame = tk.LabelFrame(root, text = 'Soil Moisture', labelanchor = 'n', relief='sunken', width = 150, height = 215)
currentSoilMoistureLabel = tk.Label(soilMoistureFrame,  text = 'Average Soil \n Moisture: ' + str(averageSoilMoisture), justify = "left", font = ('aerial', 10))
greatestSoilMoistureLabel = tk.Label(soilMoistureFrame, text = 'Greatest Soil \n Moisture Value: ' + str(greatestSoilMoistureValue), justify = "left")
lowestSoilMoistureLabel = tk.Label(soilMoistureFrame, text = 'Lowest Soil \n Moisture Value: ' + str(lowestSoilMoistureValue), justify = "left")
optimalMoistureLabel = tk.Label(soilMoistureFrame, text = 'Optimal Soil \nMoisture Level: ' + str(optimalMoisture), justify = "left")
btnConfigureOptiSoilMoisture = tk.Button(soilMoistureFrame, text = 'Configure', command = configureSoilMoisture)

img = ImageTk.PhotoImage(Image.open("icons/icon.jpeg"))
icon1 = tk.Label(root, image = img)

airGraphFrame = tk.Frame(root, width = 550, height = 320)
airGraphFig = figure.Figure(figsize=(5, 3))
airGraphFig.subplots_adjust(right=0.85)
tempGraph = airGraphFig.add_subplot(1, 1, 1)
tempGraph.set(ylim=(0, 100))

hmdGraph = tempGraph.twinx()
hmdGraph.set(ylim=(0, 100))

airCanvas = FigureCanvasTkAgg(airGraphFig, master=airGraphFrame)
airCanvasPlot = airCanvas.get_tk_widget()

soilGraphFrame = tk.Frame(root, width = 550, height = 320)
soilGraphFig = figure.Figure(figsize=(5, 3))
soilGraphFig.subplots_adjust(right=0.75)
avgGraph = soilGraphFig.add_subplot(1, 1, 1)
avgGraph.set(ylim=(0, 100)) 

greatestGraph = avgGraph.twinx()
greatestGraph.set(ylim=(0, 100))
lowestGraph = avgGraph.twinx()
lowestGraph.set(ylim=(0, 100))


soilCanvas = FigureCanvasTkAgg(soilGraphFig, master=soilGraphFrame)
soilCanvasPlot = soilCanvas.get_tk_widget()


rootLabel.pack(pady=5)
colorFrame.place(x=10, y=50)
colorBox.place(x=17, y=27)

temperatureFrame.place(x=175, y=50)
btnConfigTemp.place(x=30, y=150)
maxTemperatureLabel.place(x=10, y=45)
minTemperatureLabel.place(x=10, y=80)
currentTempLabel.place(x=10, y=10)

humidityFrame.place(x=340, y=50)
maxHumidityLabel.place(x=10, y=45)
minHumidityLabel.place(x=10, y=80)
currentHumLabel.place(x=10, y=10)
btnConfigHum.place(x=30, y=150)

soilMoistureFrame.place(x=10, y=265)
currentSoilMoistureLabel.place(x=10, y=10)
optimalMoistureLabel.place(x=10, y=115)
lowestSoilMoistureLabel.place(x=10, y=45)
greatestSoilMoistureLabel.place(x=10, y=80)
btnConfigureOptiSoilMoisture.place(x=30, y=155)

airGraphFrame.place(x=500, y=50)
airCanvasPlot.place(x=0, y=0)

soilGraphFrame.place(x=500, y=380)
soilCanvasPlot.place(x=0, y=0)

fargsAir = (tempGraph, hmdGraph, xAir, temps, hmds)
aniAir = animation.FuncAnimation(airGraphFig, animateAir, fargs=fargsAir, interval=update_interval)
fargsSoil = (avgGraph, greatestGraph, lowestGraph, xSoil, avgMoistures, greatestMoistures, lowestMoistures)
aniSoil = animation.FuncAnimation(soilGraphFig, animateSoil, fargs=fargsSoil, interval=update_interval)

tk.mainloop()