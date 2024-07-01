import discord
from discord.ext import commands
from discord import Intents
from config import settings
intents = Intents.default()
intents.members = True  # Listen to member join/leave events
intents.message_content = True # Listen to message content
bot = commands.Bot(command_prefix = settings['prefix'], intents=intents)
# Define the on_member_join event
@bot.event
async def on_member_join(member):
    # Get the welcome channel (replace with the actual channel ID)
    welcome_channel_id = 1256070843495223297  # Replace with your channel ID
    welcome_channel = bot.get_channel(welcome_channel_id)

    # Send the welcome message to the specific channel
    await welcome_channel.send(
        f'{member.mention}, присоединился к проекту')

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined a specific voice channel
    if after.channel and after.channel.id == 1256068142854307864:
        # Create a new voice channel in the same category
        new_channel = await member.guild.create_voice_channel(f"{member.name}'s Channel", category=bot.get_channel(1256068142854307862))
        # Move the user to the new channel
        await member.move_to(new_channel)
        # Grant the user all permissions in the new channel
        await new_channel.set_permissions(member, manage_channels=True, manage_permissions=True)
        # Store the channel ID for later use
        channel_ids[new_channel.id] = member.id
    # Check if the user left a voice channel
    if before.channel and before.channel.id in channel_ids:
        # Check if all users have left the channel
        if len(before.channel.members) == 0:
            # Delete the channel
            await before.channel.delete()
            # Remove the channel ID from the dictionary
            del channel_ids[before.channel.id]
channel_ids = {}
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.top_role.name == "Тех. Админ🛠️" and message.content.startswith("send"):
        await message.channel.send(message.content[5:])
        await message.delete()
        print ("сообщение отправленно")
    elif message.author.top_role.name == "Админ⭐" and message.content.startswith("send"):
        await message.channel.send(message.content[5:])
        await message.delete()
        print ("сообщение отправленно")

try:
    bot.run(settings['token']) 
except Exception as e:
    print(f"An error occurred: {e}")