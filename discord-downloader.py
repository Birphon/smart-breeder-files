import discord
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.name == 'bot-testing':
        for attachment in message.attachments:
            folder_path = './downloads'
            file_path = os.path.join(folder_path, attachment.filename)
            if os.path.exists(file_path):
                print(f"'{attachment.filename}' skipped.")
            else:
                await attachment.save(file_path)
                print(f"Downloaded: {attachment.filename}")

client.run('MTE4MjYxMDExOTQ1NzAwMTQ3NA.GXXuSL.XOLcjwGOZ9carNwGTtTQRj1IVrJTUOU98E-ubk')
