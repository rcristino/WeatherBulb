# WeatherBulb

## What is this about?
The idea is to have a smart bulb changing colour accordingly to the weather forcast. 
This is great because it can give a great enviromment mood at your office or living room by not having the natural window's light but also by a humble smart bulb. 

## How it works? 
We have a smart bulb connected to the wifi by using the manufacturing procedure.
Then, running on your PC or RaspberryPi, there is this python based program. It will get the current weather forecast, map it to the specific colour schema (HSV) and then send it to the bulb. The cycle is repeated every hour.

## Dependencies and prerequisites
- Acquire a smart bulb, this example is based on TP-Link Tapo L530E 
- Create an account on https://openweathermap.org and get an API key.

## Configuration

### Step 1
If first time with fresh checkout create virtual environment first by doing
```
sudo apt install python3 python3-pip python3-venv
python -m venv ./venv
```

Activating the virtual environment run
```
source venv/bin/activate
```

Installing the required depencies aka libraries in the virtual environment
```
pip install -r requirements.txt
```

### Step 2
All basic configuration should be done in envrionment.py file
```
APP_ID = "qwerty" # OpenWeather_API_Key
CITY = "HomeTown" # Bulb_Location
COORD = "lat=YY.YY&lon=XX.XX" # Bulb_Location coordenates
OPEN_WEATHER_ADDRESS = f"https://api.openweathermap.org/data/3.0/onecall?{COORD}&exclude=daily,minutely,hourly&appid={APP_ID}"
TAPO_BULD_IP = "192.168.X.X" # smart bulb IP address
TAPO_EMAIL = "yourEmail at mail.com" # Tapo account email (it is needed to handshake the bulb)
TAPO_PWD = "pwd" # Tapo account password
EXEC_EVERY = 3600 # how often to fetch new forecast and update bulb (seconds)
```

## Running it
```
cd WeatherBulb
python WeatherBulb.py
```

## Logging
It is possible to monitoring the requests across OpenWeather and the bulb by looking into the logs in WeatherBulb.log file
