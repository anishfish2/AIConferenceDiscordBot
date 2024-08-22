import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Retrieve the values from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
ROLE_NAME = os.getenv('ROLE_NAME') 
PASSWORD = os.getenv('PASSWORD')
print(TOKEN)
# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Bot setup
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):  # Check if it's a DM
        if message.content == PASSWORD:
            guild = discord.utils.get(bot.guilds)
            role = discord.utils.get(guild.roles, name=ROLE_NAME)
            if role is None:
                await message.author.send(f'Role "{ROLE_NAME}" not found.')
                return
            member = guild.get_member(message.author.id)
            if member:
                await member.add_roles(role)
                await message.author.send(f'You have been given the "{ROLE_NAME}" role!')
            else:
                await message.author.send('You are not in the server.')
        else:
            await message.author.send('Incorrect password.')
    await bot.process_commands(message)

async def main():
    async with bot:
        await bot.start(TOKEN)

# Check if the event loop is closed and restart if necessary
if __name__ == '__main__':
    if asyncio.get_event_loop().is_closed():
        asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(main())
