import discord
import asyncio
import aiofiles
from tailer import follow

# Replace these with your actual values
DISCORD_TOKEN = "BOT_TOKEN_ID"
DISCORD_CHANNEL_ID =   # Replace with the ID of your channel
LOG_FILE_PATH = 

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def tail_and_post():
    """Tail the log file and post relevant lines to Discord asynchronously."""
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        print("Could not find the Discord channel. Check your ID.")
        return

    try:
        # Open the log file asynchronously
        async with aiofiles.open(LOG_FILE_PATH, mode='r') as file:
            # Move to the end of the file
            await file.seek(0, 2)

            while True:
                line = await file.readline()
                if not line:
                    # No new line, wait briefly and retry
                    await asyncio.sleep(0.1)
                    continue

                # Check if the line contains the target string
                if "tells the guild," in line:
                    await channel.send(line.strip())
    except Exception as e:
        print(f"Error while tailing log file: {e}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    # Start the log tailing task
    asyncio.create_task(tail_and_post())

@client.event
async def on_disconnect():
    print("Bot disconnected. Attempting to reconnect...")

# Run the bot
client.run(DISCORD_TOKEN) 
