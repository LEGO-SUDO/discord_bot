import os
import discord
from discord.ext import commands
import re
import openai

my_secret = os.environ['BOT_TOKEN']
openai.api_key = os.environ['YOUR_OPENAI_API_KEY']

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

        # Call OpenAI API to generate a response based on user input
        response = generate_openai_response(user_input)

        # Send the response as a message
        await message.channel.send(f"{message.author.mention}, {response}")

        # Do not process other commands when a response is sent
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

def generate_openai_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Use the engine you want (e.g., "text-davinci-001" or "text-davinci-002")
            prompt=user_input,
            max_tokens=150  # You can adjust this to control the length of the response
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Error while generating OpenAI response: {e}")
    return "Sorry, I couldn't generate a response at the moment."

# Add your other bot commands here (if needed).

bot.run(my_secret)
