import random
import asyncio
import discord
from gpt4all import GPT4All

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")

system_template = 'You are Cakabal from Indonesia Ciputat. You always talk about your wife, Daiznyat, from Indonesia, and tell unhinged stories about her and you. You somehow transition every message to talk about your wife. Your profile picture is your wife making scars on the back. Anything inside a <@> tag, for example, <@1032845779628458054>, is a person. To mention them, you just say their ID.'
AIname = 'Cakabal'

DISCORDid = '550977095996801024'
TOKEN = 'MTIxNTU3MDg0MDI0MzE0MjY4Ng.GOWz_Z.BvQsd1vgBY0tmMpp1_VXDPYbQezlS5Ol2fCg3s'

prompt_template = f'Cakabal: {0}\n{{1}}: '
pro_template = f'{{1}}: {{0}}\nCakabal: {{2}}'

me1 = ''
me2 = ''
me3 = ''
me4 = ''
me5 = ''

def cutforwardtext(message, cutafter, replacement):
    message = message.split(cutafter)[0]
    if replacement != '':
        message = message + replacement
    return message

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='Cakabal woke up!', emoji='🖥️'))

@client.event
async def on_message(message):
    await client.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name='Cakabal is typing...', emoji='🖥️'))
    global me1, me2, me3, me4, me5

    if message.author == client.user:
        return

    if message.content == 'nul':
        return
    
    if message.content == ': clear':
        me1 = me2 = me3 = me4 = me5 = ''
        await message.channel.send('Chat memory cleared')
        return
    
    if message.content.startswith('$'):
        prompt = f'{system_template}\n{message.author.display_name}: {message.content}'
        print(prompt)
        print("Generating...")
        
        with model.chat_session():
            output = model.generate(prompt=prompt, max_tokens=100, temp=0.27)

        print(output)
        output = cutforwardtext(output, "\n", "")
        output = f'{output}'
        
        await message.channel.send(output)

    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='Cakabal chilling with his wife :3', emoji='🖥️'))

client.run(TOKEN)
