import os
import discord
from discord.ext import commands
import re

my_secret = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
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

    # Check if the message contains any link
    if re.search(r"http[s]?://\S+", message.content):
        # Here, you can add your own checks for malicious URLs or links leading to other servers.
        # For simplicity, we'll just check for server invites.
        if "discord.gg/" in message.content:
            # Delete the message if it contains a server invite
            await message.delete()
            await message.channel.send(f"{message.author.mention}, sharing server invites is not allowed!")
            return

    # Check for custom replies
    if "hello bot" in message.content.lower():
        # Send a cool reply when someone says "hello bot"
        await message.channel.send(f"Hello there, {message.author.mention}! How can I assist you today?")

    await bot.process_commands(message)

# Add your other bot commands here (if needed).

bot.run(my_secret)
