import discord
import requests
import json
import time
from datetime import datetime
import os
import asyncio
import threading

intents = discord.Intents.default()
intents.message_content = True
active = True
client = discord.Client(intents=intents)
channel = client.get_channel(1329327570478698547)
bot_ready = asyncio.Event()
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    channel = client.get_channel(1329327570478698547)
    bot_ready.set()
   



async def main_script():
    await bot_ready.wait()
    channel = client.get_channel(1329327570478698547)
    pinged = False
    EventUpdated = False
    print(channel)
    while active:


            if EventUpdated == False:
                CurrentDwarvenEvent, CurrentDwarvenTimeStamp, EndingDwarvenTimeStamp = check_event()
                EventUpdated = True
                #Send message in discord with data
                print("Event Updated")
                print("Current Event: " + CurrentDwarvenEvent)
            if datetime.now().timestamp() >= EndingDwarvenTimeStamp:
                EventUpdated = False
                pinged = False

            if CurrentDwarvenEvent == "DOUBLE_POWDER" and pinged == False:
                
                pinged = True
                print("2x Powder")
                time_diff = EndingDwarvenTimeStamp - datetime.now().timestamp()
                await channel.send("2x Powder" + " ends at" +"<t:" + str(EndingDwarvenTimeStamp) + ":F>")
                await channel.send("<@&" + str(1329338766938341428) +">")
              
             
            else:
                print("Event not changed, waiting 60 seconds")
                await asyncio.sleep(60)
                
            
                

async def main():
    await asyncio.gather(main_script(), client.start(os.getenv('TOKEN')))



    



def check_event():
    rq = requests.get("https://api.soopy.dev/skyblock/chevents/get")
    data = rq.json()
    formatted_data = json.dumps(data, indent=2)
    DwarvenData = data["data"]["event_datas"]["DWARVEN_MINES"]
    CurrentDwarvenEvent = next(iter(DwarvenData))
    CurrentDwarvenTimeStamp = round(int(DwarvenData[CurrentDwarvenEvent]["starts_at_min"]) / 1000)
    EndingDwarvenTimeStamp = round(int(DwarvenData[CurrentDwarvenEvent]["ends_at_max"]) / 1000) # convert to seconds
    
    
    
    #CHData = data["data"]["event_datas"]["CRYSTALL_HOLLOWS"]

    
    return CurrentDwarvenEvent, CurrentDwarvenTimeStamp, EndingDwarvenTimeStamp

asyncio.run(main())