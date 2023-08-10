from keep_alive import keep_alive

import discord
from discord.ext import commands, tasks
from discord import app_commands

import asyncio
import os
from fuzzywuzzy import process

import requests
from bs4 import BeautifulSoup as BS

from datetime import datetime
import pytz

import random

loc_dt = datetime.now(pytz.timezone('US/Eastern'))

#get list of items
#item format
#[item_name,item time,item place,item chance,item description]
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
					])
				except:
					pass

#updates shindo time
def update():
    global now_hour
    global now_min
    global int_hour
    global int_min
    now_hour= loc_dt.strftime("%I")
    now_min = loc_dt.strftime("%M")
    int_hour = int(now_hour)
    int_min = int(now_min)
	


#creating bot
intents = discord.Intents.all()
bot = commands.Bot(
	command_prefix='/',
	help_command=None ,
	intents=intents
)

#commands on bot start
@bot.event
async def on_ready():
	await bot.change_presence(
		activity=discord.Activity(
        type=discord.ActivityType.listening,
		name='на утроI /help')
	)
	print('Bot alive {0.user}'.format(bot))
	test.start()

#jokes
#generator of jokes
def get_joke():
	f = open('анекдоты.txt','r')
	jokes=f.read().split("* * *")
	f.close()
	return jokes[random.randint(0,len(jokes))]
#jokes sender
@tasks.loop(hours=24)
async def test():
    channel = bot.get_channel(980380538315612160)
    await channel.send(get_joke())

#Member changing actions
#when somebody leaves
@bot.event
async def on_member_remove(member):
	guild=member.guild
	channel=guild.get_channel(980380538315612160)
	await channel.send(member.name+' покинул кладбище')
#when somebody joins
@bot.event
async def on_member_join(member):
	guild=member.guild
	channel=guild.get_channel(980380538315612160)
	await channel.send(member.name+' зашел в кладбище(и увидел там только трупы)')

#Commands
#Shindo life time command
@bot.tree.command(name="est",
             description="Показывает точное время в шиндолайф",
             )
async def _est(interaction: discord.Interaction):
    update()
    estime = loc_dt.strftime("%I:%M:%S")
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
        interval = 25
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
	
#Custom time items shindo life command
@bot.tree.command(name="intm",
             description="Предметы в шиндо лайф в заданный момент",
             )
@discord.app_commands.describe(hour="hour")
@discord.app_commands.describe(min="min")
async def _intm(interaction: discord.Interaction,hour:int,min:int):
	if hour>13 or hour<0 or min>60 or min<0:
		await interaction.response.send_message("Ошибка попробуйте написать корректное время")
	text = 'В ' + str(hour) + ':' + str(min)
	if min<10:
		text = 'В ' + str(hour) + ':0' + str(min)
	update()
	a = 2
	
	embed = discord.Embed(title=str(text),
                          description=" ",
                          color=discord.Color.purple())
	for i in range(0, len(items)):
		item_name = items[i][0]
		time_hour = items[i][1]
		time_min = items[i][2]
		interval = 26
		village = items[i][3]
		chance = items[i][4]
		str_chance = round(100 * (1 / chance) * 100) / 100
		if time_min < 10:
			tm_start = '0' + str(time_min)
		else:
			tm_start = str(time_min)
		tm_end = str(time_min + interval)
		th_end = str(time_hour)
		for i2 in range(time_min, time_min + interval + 1):
			if time_min + interval >= 60:
				th_end = str(time_hour + 1)
				tm_end = '00'
				if th_end == '13':
					th_end == '01'
			if time_hour == hour and i2 == min:
				a = 1
				embed.add_field(
                    name=item_name,
                    value=("`({0}:{1}-{2}:{3}) в {4} шанс {5}%(1/{6})`".format(
                        time_hour, tm_start, th_end, tm_end, village,
                        str_chance, chance)),
                    inline=False)
	if a == 2:
		embed.add_field(name='ничего нет отдыхай',
                        value=("но будет через 5-10 минут..."))

	await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info",
             description="Предметы в шиндо лайф в заданный момент",
             )
async def _info(interaction: discord.Interaction):
	await interaction.response.send_message("Используйте !wiki <нужный предмет>")

#starting bot
keep_alive()
bot.run(os.getenv('TOKEN'))
