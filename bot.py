#------------------imports-----------------------
import sys
import discord
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from discord.ext import commands

#------------------OS get------------------------
def os_get(os):
	common = {
		'linux': 'driver/linux64/chromedriver',
		'win32': 'driver/win32/chromedriver.exe',
		'cygwin': 'driver/win32/chromedriver.exe',
		'darwin': 'driver/mac64/chromedriver'
	}
	global path
	path = common.get(os, 'OS not found')
os_get(sys.platform)

#------------------bot setup---------------------
bot = commands.Bot(command_prefix = 'val.')

@bot.event
async def on_ready():
    print('Bot is ready.')
    game = discord.Game('Im watching you...')
    await bot.change_presence(status = discord.Status.online, activity = game)

#------------------WEB SCRAPER-------------------
def leaderboard_get(page):
    #sets up chrome driver
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(executable_path = path, options = options)
    
    #opens the valorant page using custom page number
    #closes after 3 seconds
    driver.get(f'https://playvalorant.com/en-us/leaderboards/?page={page}&act=ab57ef51-4e59-da91-cc8d-51a5a2b9b8ff')
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    page_source = driver.page_source
    driver.close()

    #converts selenium to a soup object
    output_string = '\n'
    soup = BeautifulSoup(page_source, features = 'html5lib')
    top_players = soup.find_all('li', class_ = 'LeaderboardsItem-module--leaderboardsItem--1gN45')
    #finds top players using class and adds onto the output
    for top_player in top_players:
        rank = top_player.find('h3', class_ = 'LeaderboardsItem-module--leaderboardRank--3DHty')
        name = top_player.find('h2', class_ = 'LeaderboardsItem-module--playerName--2BYaw')
        #tag = top_player.find('span', class_='LeaderboardsItem-module--tagline--24Wgn') -- unnessary
        rating = top_player.find('p', class_ = 'LeaderboardsItem-module--rating--1zqAY')

        output_string += f'Rank: {rank.text}, {name.text} ({rating.text} elo)\n'
    
    print(output_string)
    return output_string

#------------------Find player using webscraper--
def find_player(player_name):
    #chrome setup
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(executable_path = path, options = options)

    #opens up valorant leaderboards
    #searches for player name with argument player_name
    driver.get('https://playvalorant.com/en-us/leaderboards/?page=1&act=ab57ef51-4e59-da91-cc8d-51a5a2b9b8ff')
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)
    #print(driver.page_source)

    searchBox = driver.find_element_by_id('search')
    searchBox.send_keys(player_name)
    searchBox.submit()

    time.sleep(2)
    page_source = driver.page_source
    #print(page_source)
    driver.close()

    #compares the name of all names in leaderboard and returns the match
    #returns an excepting string if can't find anything
    output_string = '\n'
    soup = BeautifulSoup(page_source, features = 'html5lib')
    top_players = soup.find_all('li', class_ = 'leaderboards-module--highlight--jUhwl')
    for top_player in top_players:
        rank = top_player.find('h3', class_ = 'LeaderboardsItem-module--leaderboardRank--3DHty')
        name = top_player.find('h2', class_ = 'LeaderboardsItem-module--playerName--2BYaw')
        #tag = top_player.find('span', class_='LeaderboardsItem-module--tagline--24Wgn') -- unnessary
        rating = top_player.find('p', class_ = 'LeaderboardsItem-module--rating--1zqAY')

        output_string += f'Rank: {rank.text}, {name.text} ({rating.text} elo)\n'
    
    print(output_string)
    return output_string
    
    #rank = top_player.find('h3', class_='LeaderboardsItem-module--leaderboardRank--3DHty')
    #name = top_player.find('h2', class_='LeaderboardsItem-module--playerName--2BYaw')
    #tag = top_player.find('span', class_='LeaderboardsItem-module--tagline--24Wgn') -- unnessary
    #rating = top_player.find('p', class_='LeaderboardsItem-module--rating--1zqAY')

    #print(name.text)
        #print(player_name)
        #print(str(name.text == player_name))
    print('\n')

        #if name.text == player_name:
            #output_string = f'{player_name} is {rank}th on the leaderboard with {rating}elo'
            #return output_string

    return 'player is not in immortal+ or does not exist'

#command for above two functions, finds if input is a number or a string(person)
@bot.command()
async def topval(ctx, input = '1'):
    if input.isnumeric() == True:
        #Find leaderboard with input as page
        await ctx.send(leaderboard_get(int(input)))
        
    else:
        #Find player in leaderboard and rank
        await ctx.send(find_player(input))

#command for ping
@bot.command()
async def myping(ctx):
    await ctx.send(f'my ping: {round(bot.latency*1000)}ms')

#command to clear text, default value is 5
@bot.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount + 1)

#------------------bot-run-----------------------
bot.run('ODMyNjk4MzUxNzM2NzE3Mzcx.YHnkxQ.mZRc0rnWd3i9isFWN22zMJBUogQ')