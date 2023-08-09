from keep_alive import keep_alive
import discord
from discord.ext import commands

import asyncio
import os
import time
from fuzzywuzzy import process

import requests
from bs4 import BeautifulSoup as BS

#creating bot
intents = discord.Intents.default()
bot = commands.Bot(
	command_prefix='!',
	help_command=None ,
	intents=intents
)

#get list of items
items=[]
if True:
	if True:
		r=requests.get("https://shindo-life-rell.fandom.com/wiki/Shindo_Life_Item_Spawn_List")
		html = BS(r.content,'html.parser')
		for el in html.select(".article-table > tbody > tr"):
			item=el.select("td")
			if item!=[]:
				try:
					items.append([
					#name
					item[0].text[0:-1],
					#time
					int(item[1].text.split(":")[0]),
					int(item[1].text.split(":")[1].split()[0]),
					#place
					item[2].text[0:-1],
					#chance
					int(item[3].text.split("/")[1][0:-1]),
					#description
					"yes"
					])
				except:
					pass

	


#commands on bot start
@bot.event
async def on_ready():
	await bot.change_presence(
		activity=discord.Activity(
        type=discord.ActivityType.listening,
		name='на утроI /help')
	)
	print('Bot alive {0.user}'.format(bot))


#updates shindo time
def update():
    global now_hour
    global now_min
    global int_hour
    global int_min
    if time.gmtime()[3] < 6:
        now_hour = time.gmtime()[3] + 7
    else:
        now_hour = time.gmtime()[3] - 5
    now_min = time.gmtime()[4]
    if now_hour > 12:
        now_hour = now_hour - 12

    if now_hour < 10:
        now_hour = '0' + str(now_hour)
    else:
        now_hour = str(now_hour)
    int_hour = int(now_hour)
    now_min = time.gmtime()[4]
    int_min = int(now_min)
    if now_min < 10:
        now_min = '0' + str(now_min)
    else:
        now_min = str(now_min)

#Shindo life time command
@bot.tree.command(name="est",
             description="Показывает точное время в шиндолайф",
             )
async def _est(interaction: discord.Interaction):
    update()
    estime = time.strftime("%I:%M:%S",time.localtime(time.time()-18000))
    embed = discord.Embed(title='Время в Shindo Life',
                          description=estime,
                          color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)
#shows current shindo life items
@bot.tree.command(name="item",
             description="Все предметы в шиндолайф в текущий момент",
             )
async def _item(interaction: discord.Interaction):
    update()
    a = 2
    embed = discord.Embed(
        title="Сейчас в Shindo life",
        description=" ",
        color=discord.Color.purple(),
    )
    for i in range(0, len(items)):

        item_name = items[i][0]
        time_hour = items[i][1]
        time_min = items[i][2]
        interval = 26
        village = items[i][3]
        chance = items[i][4]
        str_chance = round(100 * (1 / chance * 100) / 100)
        tm_end = str(int(time_min) + interval)
        th_end = str(time_hour)
        for i2 in range(int(time_min), int(time_min) + interval + 1):
            if int(time_min) + interval >= 60:
                th_end = str(int(time_hour) + 1)
                tm_end = '00'
            if int(th_end) == 13:
                th_end == '01'
            if int(time_hour) == int_hour and i2 == int_min:
                a = 1
                embed.add_field(
                    name=item_name,
                    value=("`({0}:{1}-{2}:{3}) в {4} шанс {5}%(1/{6})`".format(
                        time_hour, time_min, th_end, tm_end, village,
                        str_chance, chance)),
                    inline=False)
    if a == 2:
        embed.add_field(name='ничего нет отдыхай',
                        value=("но будет через 5-10 минут..."))
    await interaction.response.send_message(embed=embed)


#starting bot
keep_alive()
bot.run(os.getenv('TOKEN'))
