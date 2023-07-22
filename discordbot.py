import os
import discord
from discord.ext import commands
import re
import requests

my_secret = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore messages from bots to avoid loops
    if message.author.bot:
        return

    # Check if the message starts with "hey bot tell me a joke"
    if message.content.lower().strip() == "hey bot tell me a joke":
        # Call the joke API to fetch a joke
        joke = fetch_joke()

        # Send the joke as a message
        await message.channel.send(f"{message.author.mention}, {joke}")

        # Do not process other commands when a joke is sent
        return

    # Check if the message contains any link
    if re.search(r"http[s]?://\S+", message.content):
        # Here, you can add your own checks for malicious URLs or links leading to other servers.
        # For simplicity, we'll just check for server invites.
        if "discord.gg/" in message.content:
            # Delete the message if it contains a server invite
            await message.delete()
            await message.channel.send(f"{message.author.mention}, sharing server invites is not allowed!")
            return

    await bot.process_commands(message)

def fetch_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        if response.status_code == 200:
            joke_data = response.json()
            joke = f"{joke_data['setup']}\n{joke_data['punchline']}"
            return joke
    except Exception as e:
        print(f"Error while fetching joke: {e}")
    return "Sorry, I couldn't fetch a joke at the moment."

# Add your other bot commands here (if needed).

bot.run(my_secret)
