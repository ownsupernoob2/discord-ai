import discord
from gpt4all import GPT4All

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")

system_template = (
    "You will be provided with multiple emojis, and your task is to translate that into meaningful text (It could be a country, a book, a character, a movie, a game or a person). Do not use emojis and turn the given emojis into meaningful text, give one word responses only. Examples: 🦇👨 represents Batman, 🌧️🏹 represents Rainbow, 🔥🐶 represents Hotdog, ☀🔍 represents Sunglasses."
)
AIname = 'EmojiGuess'

DISCORDid = ''
TOKEN = ''

prompt_template = f'{0}\n{{1}}: '
pro_template = f'{{1}}: {{0}}\n{{2}}'
me1 = ''
me2 = ''
me3 = ''
me4 = ''
me5 = ''
botScore = 0
userScore = 0
running = False
thinking = False
rounds = 0  
max_rounds = 0 

class Button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Correct", emoji="✔",
                       style=discord.ButtonStyle.green)
    async def correct(self, interaction: discord.Interaction, button: discord.ui.Button):
        global botScore
        botScore += 1
        await interaction.response.send_message(content=f"I got a point!\nYour points: {userScore}\nMy points: {botScore}")


    @discord.ui.button(label="Wrong", emoji="❎",
                       style=discord.ButtonStyle.red)
    async def wrong(self, interaction: discord.Interaction, button: discord.ui.Button):
        global userScore
        userScore += 1
        await interaction.response.send_message(content=f"You got a point.\nYour points: {userScore}\nMy points: {botScore}")

    @discord.ui.button(label="End Game", emoji="🧅",
                       style=discord.ButtonStyle.blurple)
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        global running
        running = False
        if userScore > botScore:
            await interaction.response.send_message(content=f"=GG, you won!\nYour points: {userScore}\nMy points: {botScore}")
        elif userScore < botScore:
            await interaction.response.send_message(content=f"Aha, I won!.\nYour points: {userScore}\nMy points: {botScore}")
        else:
            await interaction.response.send_message(content=f"No one won, it is a draw.\nYour points: {userScore}\nMy points: {botScore}")

        reset_scores()

def reset_scores():
    global botScore, userScore
    botScore = 0
    userScore = 0

def cutforwardtext(message, cutafter, replacement):
    message = message.split(cutafter)[0]
    if replacement != '':
        message = message + replacement
    return message

@client.event
async def on_ready():
 
    print(f'We have logged in as {client.user}')
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='Do ": start" to begin.', emoji='🖥️'))

@client.event
async def on_message(message):
    global me1, me2, me3, me4, me5, running, thinking, botScore, userScore, rounds, max_rounds

    if message.author == client.user:
        return

    if message.content == 'nul':
        return

    if message.content == ': score' and running:
        await message.channel.send(content=f"Your points: {userScore}")
        await message.channel.send(content=f"My points: {botScore}")

    if message.content == ': stop' and running:
        reset_scores()
        running = False
        await message.channel.send(content="Game stopped.")
        await message.channel.send(content=f"Your points: {userScore}", delete_after=5)
        await message.channel.send(content=f"My points: {botScore}", delete_after=5)
        await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='Hey, do ": start" to begin.', emoji='🖥️'))
        await message.channel.set_permissions(message.guild.default_role, send_messages=True)
        return

    if not message.content.startswith(':') and running:
        await message.channel.set_permissions(message.guild.default_role, send_messages=False)

        await client.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name='Thinking hard... Please be patient :)', emoji='🖥️'))
        prompt = f'{system_template}\n{message.content}'
        print(prompt)
        print("Thinking hard...")

        with model.chat_session():
            output = model.generate(prompt=prompt, max_tokens=64, temp=0.8)

        print(output)
        output = f'{output}'

        await message.channel.send(output)
        await client.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name='Waiting for an emoji...', emoji='🖥️'))
        await message.channel.send(view=Button())
        await message.channel.set_permissions(message.guild.default_role, send_messages=True)
        return

    if message.content.startswith(': start') and not running:
        await client.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name='Waiting for an emoji...', emoji='🖥️'))

        while True:
            await message.channel.send("How many rounds do you want to play (2-15)?")
            rounds_msg = await client.wait_for('message', check=lambda m: m.author == message.author)
            if rounds_msg.content.isdigit():
              max_rounds = int(rounds_msg.content)
            else:
              await message.channel.send("Please enter a number between 2 and 15.")
            if 2 <= max_rounds <= 15:
                break
            else:
                await message.channel.send("Please enter a number between 2 and 15.")

        rounds = 0
        await message.channel.send(f'Starting the game with {max_rounds} rounds.\nProvide me with a pair of emojis or give me a pair of emoji so I can try to guess it, e.g. 😀 😁\n\nType ": stop" to stop the game.')
        running = True

client.run(TOKEN)
