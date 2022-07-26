#server:

# first of all import the socket library
import socket
import random

# next create a socket object
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print ("Socket successfully created")

# reserve a port on your computer in our
port = 8080

temperature = 20
maxTemperature = 22
minTemperature = 17

humidity = 50
maxHumidity = 55
minHumidity = 45

averageMoisture = 45

moistureValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
optimalMoisture = 45

climateControlState = 'off'
fanState = False

def soilMoistureString():
    global moistureValues
    returnString = ".["
    
    for i in range(len(moistureValues)):
        returnString = returnString + str(moistureValues[i]) + ":"
        
    returnString.strip(":")
    returnString = returnString + "]"
    return(returnString)

def updateSoilMoisture():
    global averageMoisture
    global optimalMoisture
    sumAll = 0.0
    for i in range(len(moistureValues)):
        toAdd = random.randrange(-(random.randrange(1, 2)), random.randrange(3, 5))
        newVal = int(averageMoisture + toAdd)
        
        if newVal < optimalMoisture:
            newVal = newVal + 6
        if newVal > optimalMoisture + 10:
            newVal = newVal - 6    
            
        moistureValues[i] = newVal
        sumAll = sumAll + newVal
    averageMoisture = sumAll / len(moistureValues)
    
def updateTemp():
    global temperature
    global climateControlState

    if temperature > maxTemperature:
        climateControlState = 'cool'
        temperature = temperature - 3
        print("Cooling on")
    elif temperature < minTemperature:
        climateControlState = 'heat'
        temperature = temperature + 3
        print("heat on")
    else:
        climateControlState = 'off'
        temperature = temperature + random.randrange(-1, 1)

def updateHmd():
    global humidity
       
    if humidity > maxHumidity:
        humidity = humidiy - 3
        fanState = True
    elif humidity < minHumidity:
        humidity = humidity + 3
        fanState = True
    else:
        humidity = humidity + random.randrange(-1, 1)
        fanState = False
        

s.bind(('', port))
print ("socket binded to %s" %(port))


updateSoilMoisture()

# put the socket into listening mode
s.listen(5)
print ("socket is listening")



while True:
    c, addr = s.accept()
    print(addr)
    try:
        message = c.recv(1024).decode()
        print (message)
        messageArr = message.split(".")
        
        
        if message == 'request.temp':
            updateTemp()
            try:
                c.send(('response.temp.'+str(temperature)).encode())
            except:
                print("error sending response")
        elif message == 'request.hmd':
            updateHmd()
            try:
                c.send(('response.hmd.'+str(humidity)).encode())
            except:
                print("error sending response")
        elif message == 'request.soil':
            updateSoilMoisture()
            strAdd = soilMoistureString()
            try:
                c.send(('response.soil' + strAdd).encode())
            except:
                print("error sending response")
        elif messageArr[0] == 'get':
            if messageArr[1] == 'temp':
                if messageArr[2] == 'max':
                    c.send(('request.' + str(maxTemperature)).encode())
                else:
                    c.send(('request.' + str(minTemperature)).encode())
            elif messageArr[1] == 'hmd':
                if messageArr[2] == 'max':
                    c.send(('request.' + str(maxHumidity)).encode())
                else:
                    c.send(('request.' + str(minHumidity)).encode())
            elif messageArr[1] == 'soil':
                c.send(('request.' + str(optimalMoisture)).encode())
            elif messageArr[1] == 'climate':
                print(climateControlState)
                c.send(('request.' + climateControlState).encode())
            elif messageArr[1] == 'fan':
                if fanState == True:
                    c.send(('request.on').encode())
                else:
                    c.send(('request.off').encode())
            else:
                c.send(('error.error').encode())
                print('unknown command' + messageArr)
            
            
        else:
            if messageArr[0] == 'mod':
                if messageArr[1] == 'temp':
                    if messageArr[2] == 'max':
                        maxTemperature = int(messageArr[3])
                    elif messageArr[2] == 'min':
                        minTemperature = int(messageArr[3])
                    else:
                        print("unknown mod temp command: " + message + "---"  + str(messageArr))
                
                elif messageArr[1] == 'hmd':
                    if messageArr[2] == 'max':
                        maxHumidity = int(messageArr[3])
                    elif messageArr[2] == 'min':
                        minHumidity = int(messageArr[3])
                    else:
                        print("unknown mod hmd command: " + message + "---"  + str(messageArr))
                elif messageArr[1] == 'soil':
                    optimalMoisture = int(messageArr[2])
                else:
                    print("Unknown mod command " + message + "---" + str(messageArr))
            else:
                print('unknown command')
                
            
            
    except:
        print("AHHHHHHHH" + str(messageArr))

