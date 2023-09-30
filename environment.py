APP_ID = "qwerty" # OpenWeather_API_Key
CITY = "HomeTown" # Bulb_Location
COORD = "lat=YY.YY&lon=XX.XX" # Bulb_Location coordenates
OPEN_WEATHER_ADDRESS = f"https://api.openweathermap.org/data/3.0/onecall?{COORD}&exclude=daily,minutely,hourly&appid={APP_ID}"
TAPO_BULD_IP = "192.168.X.X" # smart bulb IP address
TAPO_EMAIL = "yourEmail at mail.com" # Tapo account email (it is needed to handshake the bulb)
TAPO_PWD = "pwd" # Tapo account password
EXEC_EVERY = 3600 # how often to fetch new forecast and update bulb (seconds)