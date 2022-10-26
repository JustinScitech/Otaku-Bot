from replit import db
import random, math, json, os, requests, discord, nacl, time
from keep_alive import keep_alive
from discord.ext import commands, tasks
from dotenv import load_dotenv


db["bacon_count"] = db["bacon_count"]
db["sadge_count"] = db["sadge_count"]

intents = discord.Intents().all()

def mixedCase(*args):
  total = []
  import itertools
  for string in args:
    a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in string)))
    for x in list(a): total.append(x)

  return list(total)

client = commands.Bot(command_prefix = mixedCase("rui "), case_insensitive=True)

api_key = os.environ['weatherkey']
base_url = "http://api.openweathermap.org/data/2.5/weather?"

sad_words = ['depressed', 'kms','depress']
encouragement = ["don't be sad, I'll always be here for you", "don't be sad, just play Valorant <3", "I believe in you, you got this :)"]
bot_help = ["I don't know how to help you", "Aid comes at a cost sometimes", "Im a bot, I cannot help you", "Sometimes you must face challenges on your own"]
compliments = ["You're amazing :)", "You're a great person", "I believe in you :)", "You are awesome"]




characters = {
  'mikasa':{'img':'https://cdn.discordapp.com/avatars/877227425048723486/aebc34ba7facad7ea215d2a707953231.webp?size=100','commands':{'hello':'hello there!'}},
  
  'komi':{'img':'https://cdn.discordapp.com/avatars/929905896371396619/e544319fa418eada522f6a6764ad8ed8.webp?size=100','commands':{'laugh': 'h h he-', 'talk': 'i i- i- i-'}},
  
  }

def get_character(character,*commands):
  """with open("characters.json","r") as f:
    characters = json.load(f) """
  if character in characters:
    messages = []
    for command in commands:
      if command in characters[character]['commands']:
        messages.append(characters[character]['commands'][command])
    return (character,characters[character]['img'],messages)
  return 

@client.event
async def on_message(message):
  await client.process_commands(message)
  if message.author == client.user: return
  msg = message.content
  if 'sadge' in msg.lower():
    db["sadge_count"] += 1
  name,image,messages = get_character(*message.content.split(" ")) or (None,None,None)
  if image is None: return 
  webhook = await message.channel.create_webhook(name=message.author.name)
  for msg in messages:
    msg = msg.replace('user:mention',str(message.author.mention))
    await webhook.send(msg, username=name, avatar_url=image)
  await webhook.delete()



@client.event
async def on_ready():
  print('ready to use {0.user}'.format(client))

@client.command(name = 'play', brief='This plays music.', description='This starts playing music upon request by the user.')
async def play(ctx):
  await ctx.send("I am not able to play music at the moment. Check again soon!")  
  
@client.command(name = 'probability', brief='This gives a probability.', description='This gives a random probability from 0-100%.')
async def probability(ctx):
  probability = random.randint(0,100)
  await ctx.send(f'{probability}%')  

@client.command(name = 'blink', brief='This gives a nice gif.', description='This sends a blink from Rui.')
async def blink(ctx):
  link = 'https://c.tenor.com/HqbXBonGFPMAAAAC/rui-domekano.gif'
  await ctx.send(f'{link}')  
@client.command(name = 'bruh', brief='Rui sends a bruh face.', description='Rui will send her bruh face.')
async def bruh(ctx):
  link = 'https://c.tenor.com/IGpnCm48MPoAAAAC/eye-twitch-anger.gif'
  await ctx.send(f'{link}')

@client.command(name = 'dance', brief='Rui dances.', description='Rui will show off her dance moves.')
async def dance(ctx):
  link = 'https://i.imgur.com/yFE0A4z.gif?noredirect'
  await ctx.send(f'{link}')


@client.command(name = 'eat', brief='Rui will delete your specified message count.', description='To delete messages, format is: Rui eat number_of_messages')
async def eat(ctx):
  channel = ctx.message.channel
  max = 1 + int(ctx.message.content.split("eat")[1])
  if max > 11: return
  await channel.purge(limit = max)
  await ctx.send(f'{max-1} messages deleted')

@client.command(name = 'rec', brief='Rui will recommend an anime or manga.', description='Rui will recommend an anime or manga')
async def rec(ctx):
  with open("recommendations.json","r") as f:
    users = json.load(f) 
  await ctx.send(f"You should watch {str(random.choice(list(users))).title()}")

@client.command(name = 'sadgecount', brief='Count sadges.', description='Rui will count the number of sadges.')
async def sadgecount(ctx):
  db["sadge_count"] -= 1
  await ctx.send(db["sadge_count"])

@client.command(name = 'recadd')
async def recadd(ctx):
  if ctx.author.id == int("263903363740073984"):
    title = str(ctx.message.content.split(" recadd ")[1]).lower()
    with open("recommendations.json","r") as f:
      recommendations = json.load(f) 
    if str(title) in recommendations: 
      await ctx.send(f"{str(title).title()} already in recommendations!")
    else:
      await ctx.send(f"Added {str(title).title()} to the recommendations list")
      recommendations[str(title)] = {}
      with open("recommendations.json","w") as f:
        json.dump(recommendations,f) 

@client.command(name = 'recdel')
async def recdel(ctx):
  if ctx.author.id == int("263903363740073984"):
    title = str(ctx.message.content.split(" recdel ")[1]).lower()
    with open("recommendations.json","r") as f:
      recommendations = json.load(f) 
    if str(title) in recommendations: 
      await ctx.send(f"Removed {str(title).title()} from the recommendations list")
      recommendations.pop(title, None)
      with open("recommendations.json","w") as f:
        json.dump(recommendations,f) 
    else:
      await ctx.send(f"{str(title).title()} not in recommendations!")

@client.command(name = 'fax', brief='Rui will agree.', description='No cap')
async def fax(ctx):
  await ctx.send("no cap")

@client.command(name = 'copy', brief='Rui will copy your message.', description='Copy messages')
async def copy(ctx):
    bot_msg = ctx.message.content.split("copy")[1]
    await ctx.message.channel.send(bot_msg)

@client.command(name = 'reverse', brief='Rui will reverse messages.', description='To reverse messages, do: Rui reverse your_message_here')
async def reverse(ctx):
    bot_msg = ctx.message.content.split("reverse")[1]
    await ctx.message.channel.send(bot_msg[::-1])

@client.command(name = 'funny', brief='Rui will laugh.', description='hahahahaha okay')
async def funny(ctx):
  await ctx.message.channel.send("Here is a fun joke...")
  await ctx.message.channel.send("https://youtu.be/1ro2weu-vug")

@client.command(name = 'weather', brief='Rui will send a weather update.', description='Get your weather by doing: Rui weather city_name_here')
async def weather(ctx, *, city: str):
  city_name = city
  complete_url = base_url + "appid=" + api_key + "&q=" + city_name
  response = requests.get(complete_url)
  x = response.json()
  channel = ctx.message.channel
  if x["cod"] != "404":
    async with channel.typing():
      y = x["main"]
      current_temperature = y["temp"]
      current_temperature_celsiuis = str(round(current_temperature - 273.15))
      z = x["weather"]
      weather_description = z[0]["description"]
      embed = discord.Embed()
      embed.description = f"The temperature in {city_name} is {current_temperature_celsiuis} degrees celsius. \n \n Weather description: {weather_description}."
      await ctx.send (embed = embed)
  else:
    await ctx.send ("Sorry I couldn't find the city you were looking for")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please use me properly!") 

@client.command(pass_context = True)
async def join(ctx):
  if (ctx.message.author.voice):
    channel = ctx.message.author.voice.channel
    await channel.connect()
  else:
    await ctx.send("Please join a channel")

@client.command(pass_context=True)
async def leave(ctx):
    if ctx.message.author.voice:
        server = ctx.message.guild.voice_client
        await server.disconnect()

@client.command(name = 'advertise', brief='Rui will advertise.', description='Advertises master Arctic')
async def advertise(ctx):  
  embed = discord.Embed()
  embed.description = "You should subscribe to master ArcticZombie [Please support him](https://www.youtube.com/c/arcticzombie)."
  await ctx.send (embed = embed)

@client.command(name = 'die', aliases = ['selfdestruct', 'kys', 'killyourself','suicide','explode'])
async def die(ctx):
  await ctx.send("I am now dead :(")

@client.command(name='laugh', aliases=['joke', 'comedy', 'entertain'])
async def laugh(ctx):
  await ctx.send(random.choice(["hahaha you make me laugh", "hahaha you're such a funny person ;) ", "lol stop ittt you're so funny", "omggg stop it hahaha you're hilarious"]))

@client.command(name='compliment', aliases=['happy', 'positivity'])
async def compliment(ctx):
  await ctx.send(random.choice(compliments) + ctx.message.author.mention)

@client.command(name='support', aliases=['aid'])
async def support(ctx):
  await ctx.send(random.choice(bot_help) + ctx.message.author.mention)

@client.command(name='sad', aliases=[word for word in sad_words])
async def sad(ctx):
  await ctx.send(random.choice(encouragement) + ctx.message.author.mention)

#CURRENCY TOOLS

@client.command(name = 'balance', brief='Rui will show your Otaku Coin balance.', description='Show balance of your Otaku coins')
async def balance(ctx):
  await check_bal(ctx.author)
  users = await get_bank_data()
  user = ctx.author
  wallet_bal = users[str(user.id)]["balance"]
  bank_bal = users[str(user.id)]["bank"]
  em = discord.Embed(title = f"{ctx.author.name}'s Otaku balance", color = discord.Color.green())
  em.add_field(name = "Otaku Coin Balance", value = wallet_bal)
  em.add_field(name = "Bank Balance", value = bank_bal)
  
  await ctx.send(embed = em)

@client.command(name = 'collection', brief='Rui will show a user character collection.', description='Shows character collection by doing: Rui collection @username')
async def collection(ctx):
  a = ctx.message.content.split(" collection ")[1]
  a = str(a)
  a = a.replace("<","")
  a = a.replace(">","")
  a = a.replace("@","")
  a = a.replace("!","")
  await direct_collection_check(a)
  with open("collection.json","r") as f:
    users = json.load(f)
  collection = users[a]
  em = discord.Embed(title = f"Character collection", color = discord.Color.green())
  for character in collection:
    em.add_field(name = str(character).title(), value = collection[str(character)])
  await ctx.send(embed = em)

@client.command(name = "store", aliases = ['shop'], brief='Rui will show the store.', description='Shows Otaku store')
async def store(ctx):
  with open("store.json","r") as f:
    store = json.load(f)
  em = discord.Embed(title = "Rui Character Store")
  for character in store:
    em.add_field(name = "Name", value = str(character).title(), inline=True)
    em.add_field(name='Cost', value=store[str(character)]["Cost"], inline=True)
    em.add_field(name='Supply', value=store[str(character)]["Supply"], inline=True)

  await ctx.send(embed = em)

@client.command(name = 'buy', brief='You can buy a character.', description='Buy a character by doing: Rui buy character_name_here')
async def buy(ctx):
  await check_bal(ctx.author)
  await check_collection(ctx.author)
  users = await get_bank_data()
  with open("store.json","r") as f:
    store = json.load(f) 
  with open("collection.json","r") as f:
    collection = json.load(f) 
  character = str(ctx.message.content.split(" buy ")[1]).lower()
  if character not in store:
    await ctx.send(f"There are no more supplies of {str(character).title()}")
    return
  user = ctx.author
  cost = store[character]["Cost"]
  supply = store[character]["Supply"]
  if users[str(user.id)]["balance"] - cost < 0: 
    await ctx.send(f"You do not have enough to purchase {str(character).title()}")
  else:   
    users[str(user.id)]["balance"] -= cost
    with open("economy.json","w") as f:
      json.dump(users,f) 
    supply -= 1
    store[character]["Supply"] -= 1
    if store[character]["Supply"] == 0:
      store.pop(character, None)
    with open("store.json","w") as f:
      json.dump(store,f)
    if str(character) in collection[str(user.id)]:
      collection[str(user.id)][str(character)] += 1
    else: 
      collection[str(user.id)][str(character)] = 1
    with open("collection.json","w") as f:
      json.dump(collection,f)
    await ctx.send(f"{user.name} just purchased a {character} for {cost} Otaku coins. There are now {supply} {str(character).title()}'s remaining.")

@client.command(name = 'donate', brief='Donate money.', description='Donate by doing Rui donate amount @user')
async def donate(ctx):
  await check_bal(ctx.author)
  users = await get_bank_data()
  message = ctx.message.content.split(" donate ")[1]
  donation, a = message.split(" ")
  donation = int(donation)  
  a = str(a)
  a = a.replace("<","")
  a = a.replace(">","")
  a = a.replace("@","")
  user = ctx.author
  if users[str(user.id)]["balance"] - donation < 0: 
    await ctx.send(f"You do not have enough to donate")
  else:   
    users[str(user.id)]["balance"] -= donation
    with open("economy.json","w") as f:
      json.dump(users,f) 
    await ctx.send(f"{user.name} just wasted {donation} Otaku coins trying to donate lol.")

@client.command(name = 'create')
async def create(ctx):
  if ctx.author.id == int("263903363740073984") or ctx.author.id == int("675487166310121475"):
    message = str(ctx.message.content.split(" create ")[1]).lower()
    character, cost, supply = message.split(' ')
    with open("store.json","r") as f:
      store = json.load(f) 
    if str(character) in store: 
      await ctx.send(f"{character} is already in the store!")
      return
    elif int(supply) <= 0: 
      await ctx.send(f"supply must be greater than 0!")
      return
    else:
      store[str(character)] = {}
      store[str(character)]["Cost"] = int(cost)
      store[str(character)]["Supply"] = int(supply)
    with open("store.json","w") as f:
      json.dump(store,f) 
    await ctx.send(f"Successfully added {str(character).title()} for {str(cost).title()} Otaku coins with a supply of {str(supply).title()}.")

@client.command()
async def remove(ctx):
  if ctx.author.id == int("263903363740073984"):
    character = str(ctx.message.content.split(" remove ")[1]).lower()
    with open("store.json","r") as f:
      store = json.load(f) 
    if str(character) not in store: 
      await ctx.send(f"{character} is not in the store!")
      return
    else:
      store.pop(str(character), None)
    with open("store.json","w") as f:
      json.dump(store,f) 
    await ctx.send(f"Successfully removed {str(character).title()}.")

@client.command(name = 'use', brief='Uses a character from your collection.', description='To use a character, do Rui use character_name')
async def use(ctx):
  user = ctx.author
  await check_collection(user)
  with open("collection.json","r") as f:
    collection = json.load(f)
  character = str(ctx.message.content.split(" use ")[1]).lower()
  if character not in collection[str(user.id)]:
    await ctx.send(f"You do not have {str(character).title()}")
  else:   
    character = str(character).title()
    em = discord.Embed(title = f"{user.name} just used {character}", color = discord.Color.green())
    em.description = f"{character} Says hi."
    await ctx.send(embed = em)
    #Do something here, possibly search image on google and send it
    """with open("collection.json","w") as f:
      json.dump(collection,f)"""

async def direct_collection_check(a):
  with open("collection.json","r") as f:
    users = json.load(f) 
  if a in users:
    return False
  else: 
    users[a] = {}    
  with open("collection.json","w") as f:
    json.dump(users,f) 
  return True

async def check_bal(user):
  with open("economy.json","r") as f:
    users = json.load(f) 
  if str(user.id) in users: 
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["balance"] = 0
    users[str(user.id)]["bank"] = 0

  with open("economy.json","w") as f:
    json.dump(users,f) 
  return True

async def check_collection(user):
  with open("collection.json","r") as f:
    users = json.load(f) 
  if str(user.id) in users:
    return False
  else: 
    users[str(user.id)] = {}
    
  with open("collection.json","w") as f:
    json.dump(users,f) 
  return True

async def get_bank_data():
  with open("economy.json","r") as f:
    users = json.load(f) 
  return users

#GAMES FOR OTAKU BOT

@client.command(name='cointoss')
async def cointoss(ctx):
  coin = ["heads", "tails"]
  await check_bal(ctx.author)
  users = await get_bank_data()
  user = ctx.author
  earnings = random.randint(2,3)
  users[str(user.id)]["balance"] += earnings
  with open("economy.json","w") as f:
    json.dump(users,f) 
  await ctx.send(f"I flipped a {random.choice(coin)}. You just earned {earnings} Otaku coins!")

@client.command(name='leetcode')
async def leetcode(ctx):
  difficulty = random.randint(1,1000)
  await check_bal(ctx.author)
  users = await get_bank_data()
  user = ctx.author
  level = ""
  if difficulty >= 950:
    level = "hard"
    earnings = 100
  elif difficulty >= 600:
    earnings = 25
    level = "medium"
  else:
    earnings = 10
    level = "easy"
  users[str(user.id)]["balance"] += earnings
  with open("economy.json","w") as f:
    json.dump(users,f) 
  await ctx.send(f"You just solved a {level} level leetcode problem! You just earned {earnings} Otaku coins!")


@client.command(name='valorant')
async def valorant(ctx):
  difficulty = random.randint(1,500)
  await check_bal(ctx.author)
  users = await get_bank_data()
  user = ctx.author
  outcome = ""
  if difficulty >= 400:
    outcome = "ranked up"
    earnings = 500
  else:
    earnings = -50
    outcome = "deranked"
  users[str(user.id)]["balance"] += earnings
  with open("economy.json","w") as f:
    json.dump(users,f) 
  await ctx.send(f"Congratulations! You just {outcome}. You just got {earnings} Otaku coins.")
  if outcome == "deranked": 
    await ctx.send(f"Probably shoulda gotten a carry instead lol")

@client.command()
async def roll(ctx):
  await check_bal(ctx.author)
  users = await get_bank_data()
  user = ctx.author
  earnings = random.randint(0,10)
  users[str(user.id)]["balance"] += earnings
  with open("economy.json","w") as f:
    json.dump(users,f) 
  em = discord.Embed(title = f"{user.name}'s Otaku Roll", color = discord.Color.green())
  em.add_field(name = "SHEESH YOU JUST ROLLED", value = f"{earnings} OTAKU COINS")
  await ctx.send(embed = em)

keep_alive()
client.run(os.getenv('TOKEN'))