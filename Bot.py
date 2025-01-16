import discord
import requests
from datetime import datetime
import os
import asyncio


intents = discord.Intents.default()
intents.message_content = True
active = True
client = discord.Client(intents=intents)
channel = client.get_channel(1329327570478698547)
bot_ready = asyncio.Event()
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    bot_ready.set()
   

embedded_format = discord.Embed(
    title = "Dwarven Mines Event",
    description = "Current Event: ",
    color = discord.Color.green()
)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$event"):
        CurrentDwarvenEvent, CurrentDwarvenTimeStamp, EndingDwarvenTimeStamp, is_double = check_event()
        embedded_format.description = "Current Event: " + str(prettier_event_name(CurrentDwarvenEvent)) + " ends at " + "<t:" + str(EndingDwarvenTimeStamp) + ":F>"
        channel = message.channel
        await channel.send(embed=embedded_format)
        print("Event Command Used")

async def main_script():
    await bot_ready.wait()
    channel = client.get_channel(1329327570478698547)
    pinged = False
    EventUpdated = False
    while active:


            if not EventUpdated:
                CurrentDwarvenEvent, CurrentDwarvenTimeStamp, EndingDwarvenTimeStamp, is_double = check_event()
                EventUpdated = True
                #Send message in discord with data
               
                print("Current Event: " + str(CurrentDwarvenEvent))
            if datetime.now().timestamp() >= EndingDwarvenTimeStamp:
                EventUpdated = False
                pinged = False
                print("======================Event Ended======================")

            if CurrentDwarvenEvent == "DOUBLE_POWDER" and not pinged:
                embedded_format.description = "Current Event: " + str(prettier_event_name(CurrentDwarvenEvent)) + " ends at " + "<t:" + str(EndingDwarvenTimeStamp) + ":F>"
                embedded_format.color = discord.Color.teal()
                pinged = True
                await channel.send(embed=embedded_format)
                print("2x Powder")
                await channel.send("<@&" + str(1329338766938341428) +">")
            print("Checking Event in 60 seconds")
            await asyncio.sleep(60)
                
            
                

async def main():
    await asyncio.gather(main_script(), client.start(os.getenv('TOKEN')))



def prettier_event_name(event):
    match event:
        case "DOUBLE_POWDER":
            return "Double Powder"
        case "BETTER_TOGETHER":
            return "Better Together"
        case "MITHRIL_GOURMAD":
            return "Mithril Gourmad"
        case "GONE_WITH_THE_WIND":
            return "Gone with the Wind"
        case "RAFFLE":
            return "Raffle"
        case "GOBLIN_RAID":
            return "Goblin Raid"



def check_event():
    print("Checking Event")
    rq = requests.get("https://api.soopy.dev/skyblock/chevents/get")
    data = rq.json()
    DwarvenData = data["data"]["event_datas"]["DWARVEN_MINES"]
    CurrentDwarvenEvent = next(iter(DwarvenData))
    CurrentDwarvenTimeStamp = round(int(DwarvenData[CurrentDwarvenEvent]["starts_at_min"]) / 1000)
    EndingDwarvenTimeStamp = round(int(DwarvenData[CurrentDwarvenEvent]["ends_at_max"]) / 1000) # convert to seconds
    
    for event in DwarvenData:
        if event == "DOUBLE_POWDER":
            CurrentDwarvenEvent = next(iter(DwarvenData))
            EndingDwarvenTimeStamp = round(int(DwarvenData[event]["ends_at_max"]) / 1000) # convert to seconds
            is_double = True
        else:
            CurrentDwarvenEvent = next(iter(DwarvenData))
            EndingDwarvenTimeStamp = round(int(DwarvenData[event]["ends_at_max"]) / 1000)
            print(event + "Ends at " + datetime.fromtimestamp(EndingDwarvenTimeStamp).strftime('%Y-%m-%d %H:%M:%S'))
            is_double = False
            
    
    
    #CHData = data["data"]["event_datas"]["CRYSTALL_HOLLOWS"]

    
    return CurrentDwarvenEvent, CurrentDwarvenTimeStamp, EndingDwarvenTimeStamp, is_double

asyncio.run(main())