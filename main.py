from keep_alive import keep_alive
import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_option

import asyncio
import os
import time
from fuzzywuzzy import process

import requests
from bs4 import BeautifulSoup as BS

#creating bot
client = commands.Bot(command_prefix='/', help_command=None)
slash = SlashCommand(client, sync_commands=True)

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
@client.event
async def on_ready():

	await client.change_presence(
		activity=discord.Activity(
        type=discord.ActivityType.listening,
		name='на утроI /help')
	)
	print('Bot alive {0.user}'.format(client))


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
@slash.slash(name="est",
             description="Показывает точное время в шиндолайф",
             guild_ids=[788033226911645726])
async def _est(ctx: SlashContext):
    update()
    estime = time.strftime("%I:%M:%S",time.localtime(time.time()-18000))
    embed = discord.Embed(title='Время в Shindo Life',
                          description=estime,
                          color=discord.Color.blue())
    await ctx.send(embed=embed)


@slash.slash(name="intm",
             description="Показывает все предметы в текущем времени в шиндолайф",
			 options=[
				create_option(
					name="hour",
					description="item spawn hour",
					option_type=4,
					required=True
               ),
			   create_option(
					name="min",
					description="item spawn minute",
					option_type=4,
					required=True
               )
			 ],
             guild_ids=[788033226911645726])
async def _intm(ctx:SlashContext, hour:int , min:int):
	update()
	a = 2
	text = 'В ' + str(hour) + ':' + str(min)
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

	await ctx.send(embed=embed)


@slash.slash(name="item",
             description="Все предметы в шиндолайф в текущий момент",
             guild_ids=[788033226911645726])
async def _item(ctx: SlashContext):
    update()
    a = 2
    embed = discord.Embed(
        title="Сейчас в Shindo life",
        description=" ",
        color=discord.Color.purple(),
        icon_url=
        'https://pbs.twimg.com/profile_images/1343591571627892736/tfEpLg6R_400x400.jpg'
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
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    ghg = time.time()
    await ctx.send('PONG!')
    text = ('(Выполнено за ' + str(round(
        (time.time() - ghg) * 1000) / 1000) + ' секунд)')
    await ctx.send(text)




@slash.slash(name="info",
			description="Попробуй",
			options=[
			create_option(
				name="item",
				description="item name",
				option_type=3,
				required=True
               )
			],
    		guild_ids=[788033226911645726]
)
async def _info(ctx:SlashContext,item:str):
	input = item
	item = process.extractOne(input,items)
	if item[1]>55:
				i=0
				time_hour = item[i][1]
				time_min = item[i][2]
				interval = 26
				village = item[i][3]
				chance = item[i][4]
				str_chance = round(100 * (1 / chance) * 100) / 100
				tm_end = str(int(time_min) + interval)
				th_end = time_hour
				if int(tm_end) == 13:
					tm_end == '01'
				for i2 in range(int(time_min), int(time_min) + interval + 1):
					if int(time_min) + interval >= 60:
						th_end = str(int(time_hour) + 1)
						tm_end = '00'
					if int(th_end) == 13:
						th_end == '01'
				embed = discord.Embed(
					title=item[i][0],
					description=(
						"`({0}:{1}-{2}:{3}) в {4} шанс {5}%(1/{6})`".format(
							time_hour, time_min, th_end, tm_end, village,
							str_chance, chance)),
					color=discord.Color.orange())
				embed.add_field(name='Описание', value=item[i][5])
				await ctx.send(embed=embed)
	else:
		await ctx.send('Ошибка')

#starting bot
keep_alive()
client.run(os.getenv('TOKEN'))
