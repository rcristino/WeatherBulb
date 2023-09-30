import json
import urllib3
import logging
import time
from logging.handlers import RotatingFileHandler
import datetime
import environment
import asyncio
from plugp100.common.credentials import AuthCredential
from plugp100.new.device_factory import connect, DeviceConnectConfiguration
from plugp100.api.tapo_client import TapoClient, TapoRequest
from plugp100.api.light_effect import LightEffect


logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = RotatingFileHandler("WeatherBulb.log", maxBytes=10000)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.INFO)

def GetWeather():
    http = urllib3.PoolManager()

    rootLogger.info("Sending request to get weather details")
   
    response = http.request("GET",
                            environment.OPEN_WEATHER_ADDRESS,
                            body = json.dumps("{}"),
                            headers = {"Content-Type": "application/json"},
                            retries = False)

    rootLogger.debug("response = {}".format(type(response)))

    dataStr = response.data.decode('utf-8')
    dataDict = json.loads(dataStr)

    currentWeather = dataDict["current"]["weather"]
    icon = currentWeather[0]["icon"]
    
    rootLogger.info(currentWeather)

    return icon

def GetColor(icon): # HSV color
    if str(icon).startswith("01"): # clear sky
        return (60, 100, 100, 5)
    if str(icon).startswith("02"): # few clouds
        return (212, 20, 100, 5)
    if str(icon).startswith("03"): # scattered clouds
        return (212, 0, 88, 5)
    if str(icon).startswith("04"): # broken clouds
        return (212, 0, 75, 5)
    if str(icon).startswith("09"): # shower rain
        return (210, 60, 100, 5)
    if str(icon).startswith("10"): # rain
        return (240, 100, 100, 5)
    if str(icon).startswith("11"): # thunderstorm
        return (0, 100, 100, 5)
    if str(icon).startswith("13"): # snow
        return (0, 0, 100, 5)
    if str(icon).startswith("50"): # mist
        return (180, 60, 100, 5)
    return (0, 0, 0, 0)
    
async def SetBulb(hue, saturation, temperature, brightness):
    credentials = AuthCredential(environment.TAPO_EMAIL, environment.TAPO_PWD)
    device_configuration = DeviceConnectConfiguration(
        host=environment.TAPO_BULD_IP,
        credentials=credentials,
        device_type="SMART.TAPOBULB",
        encryption_type="klap",
        encryption_version=2
    )
    bulbDevice = await connect(device_configuration)
    await bulbDevice.update()
    print({
        'type': type(bulbDevice),
        'protocol': bulbDevice.protocol_version,
        'raw_state': bulbDevice.raw_state,
        'components': bulbDevice.get_device_components
    })
    if(bulbDevice.device_info):
        isBulbOn = bulbDevice.raw_state["device_on"]
        if isBulbOn:
            rootLogger.info("Sending request to update bulb state")
            await bulbDevice.set_brightness(brightness)
            await bulbDevice.set_color_temperature(temperature)
            await bulbDevice.set_hue_saturation(hue, saturation)
            await bulbDevice.update()
            rootLogger.info(bulbDevice.device_info)
    await bulbDevice.client.close()

async def main():
    while True:
        icon = GetWeather()
        hue, saturation, temperature, brightness = GetColor(icon)
        await SetBulb(hue, saturation, temperature, brightness)
        time.sleep(environment.EXEC_EVERY)

if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(0.1))
        loop.close()
    except KeyboardInterrupt:
        print("Bye bye...")


       