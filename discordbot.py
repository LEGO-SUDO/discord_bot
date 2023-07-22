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

    # Check if the message starts with "hey bot"
    if message.content.lower().startswith("hey bot"):
        # Get the user's input (remove "hey bot" from the message)
        user_input = message.content[len("hey bot"):].strip()

        # Call RapidAPI to generate a response based on user input
        response = generate_rapidapi_response(user_input)

        # Send the response as a message
        await message.channel.send(f"{message.author.mention}, {response}")


        return

    # Check if the message contains any link
    if re.search(r"http[s]?://\S+", message.content):
        # TODO checks for malicious URLs or links leading to other servers.
        # check for server invites.
        if "discord.gg/" in message.content:
            # Delete the message if it contains a server invite
            await message.delete()
            await message.channel.send(f"{message.author.mention}, sharing server invites is not allowed!")
            return

    await bot.process_commands(message)

def generate_rapidapi_response(user_input):
    try:
        url = "https://aeona3.p.rapidapi.com/"
        querystring = {"text": user_input, "userId": "12312312312"}  # Update the userId as needed
        headers = {
            "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
            "X-RapidAPI-Host": "aeona3.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json().get('response', 'No response from API')
    except Exception as e:
        print(f"Error while generating RapidAPI response: {e}")
    return "Sorry, I couldn't generate a response at the moment."



bot.run(my_secret)
