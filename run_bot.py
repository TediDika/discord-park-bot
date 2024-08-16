import discord
import requests
import os
from bs4 import BeautifulSoup


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
TOKEN = 'TOKEN GOES HERE'


def get_parking():
    url = 'https://services.utdallas.edu/transit/garages/_code.php'
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    date = soup.p.text
    emoji_key = (
            "🟩 - Green Permit\n"
            "🟨 - Gold Permit\n"
            "🟧 - Orange Permit\n"
            "🟪 - Purple Permit\n"
            "💰 - Pay-By-Space\n"
    )
    embed = discord.Embed(title="UTD Available Parking", color=0xFFA500, description=emoji_key)
    embed.set_footer(text=date)

    garages = soup.findAll("table")
    for garage in garages:
        garage_name = garage.find("caption").text
        spaces = garage.findAll("td", class_='rightalign')

        output = (
                "🟩 Level 5: " + spaces[0].text + "\n"
                "🟨 Level 4: " + spaces[1].text + "\n"
                "🟨 Level 3: " + spaces[2].text + "\n"
                "🟧 Level 3: " + spaces[3].text + "\n"
                "🟧 Level 2: " + spaces[4].text + "\n"
                "🟪 Level 2: " + spaces[5].text + "\n"
                "💰 Level 1: " + spaces[6].text + "\n"
        )

        embed.add_field(name=garage_name, value=output, inline=True)

    return embed


@client.event
async def on_ready():
    print(f'{client.user} is now running!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    duck = """```ansi
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟[0;37m⣉⡥⠶⢶⣿⣿⣿⣿⣷⣆[0m⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿[0;37m⢡⡞⠁⠀⠀⠤⠈⠿⠿⠿⠿⣿[0m[0;31m⠀⢻⣦⡈[0m⠻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⠘⡁⠀[0;37m⢀⣀⣀⣀⣈⣁⣐⡒[0m[0;31m⠢⢤⡈⠛⢿⡄[0m⠻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⠀[0;37m⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄[0m[0;31m⠉⠐⠄⡈⢀[0m⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠇[0;37m⢠⣿⣿⣿⣿⡿⢿⣿⣿⣿⠁⢈⣿⡄[0m⠀[0;36m⢀⣀[0m⠸⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠟[0;33m⣡⣶⣶⣬⣭⣥⣴[0m[0;37m⠀⣾⣿⣿⣿⣶⣾⣿⣧[0m[0;36m⠀⣼⣿⣷⣌[0m⡻⢿⣿
⣿⣿⠟[0;33m⣋⣴⣾⣿⣿⣿⣿⣿⣿⣿⡇[0m[0;37m⢿⣿⣿⣿⣿⣿⣿⡿[0m[0;36m⢸⣿⣿⣿⣿⣷[0m⠄⢻
⡏[0;33m⠰⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢂[0m[0;37m⣭⣿⣿⣿⣿⣿⠇[0m[0;36m⠘⠛⠛⢉⣉[0m⣠⣴⣾
⣿⣷⣦[0;33m⣬⣍⣉⣉⣛⣛⣉⠉[0m[0;37m⣤⣶⣾⣿⣿⣿⣿⣿⣿⡿[0m⢰⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧[0;37m⡘⣿⣿⣿⣿⣿⣿⣿⣿⡇[0m⣼⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇[0;37m⢸⣿⣿⣿⣿⣿⣿⣿⠁[0m⣿⣿⣿⣿⣿⣿⣿⣿⣿
```"""

    if message.content.startswith('!hello'):
        await message.channel.send("Hey there!")

    if message.content.startswith('!duck'):
        await message.channel.send(duck)

    if message.content.startswith('!park'):
        parking_embed = get_parking()
        await message.channel.send(embed=parking_embed)


client.run(TOKEN)
