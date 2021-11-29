import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
token = os.environ['TOKEN']
client = discord.Client()



sad_words = ["sad","depressed","cry","lonely","unhappy","angry","depressing","miserable"]

starter_encouragements = ["Cheer up","Hang in there","You are a great person / bot!"]\

if "responding" not in db.keys():
  db["responding"] = True

def get_inspire():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote_translate = json_data[0]['q']
  quote = quote_translate + ' - ' + json_data[0]['a']
  return quote

def update_encouragements(enc_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(enc_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enc_msg]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def get_joke():
  url = "https://dad-jokes.p.rapidapi.com/random/joke"

  headers = {
    'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
    'x-rapidapi-key': "d0e06b0924msh4bba56ebd4c47c0p1b53e1jsn56d14013d35e"
    }

  response = requests.request("GET", url, headers=headers)
  json_data = json.loads(response.text)
  json_data = json_data['body']
  setup = json_data[0]['setup']
  punchline = json_data[0]['punchline']
  return setup + "\n" + punchline


  
  
def get_quote():
  url = "https://quotes15.p.rapidapi.com/quotes/random/"

  headers = {
    'x-rapidapi-host': "quotes15.p.rapidapi.com",
    'x-rapidapi-key': "d0e06b0924msh4bba56ebd4c47c0p1b53e1jsn56d14013d35e"
    }

  response = requests.request("GET", url, headers=headers)
  json_data= json.loads(response.text)
  quote = json_data["content"]
  author = json_data["originator"]["name"]
  return quote + '--- by ' + author


def get_covid(country):
  url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
  querystring = {"country":country}
  headers = {
    'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    'x-rapidapi-key': "d0e06b0924msh4bba56ebd4c47c0p1b53e1jsn56d14013d35e"
    }
  response = requests.request("GET", url, headers=headers, params=querystring)
  json_data = json.loads(response.text)
  deaths = json_data["data"]["deaths"]
  confirmed = json_data["data"]["confirmed"]
  location = json_data["data"]["location"]

  return "No of deaths: {}".format(deaths) +"\n"+ " No of confirmed cases: {}".format(confirmed) +"\n"+ "Location: {}".format(location) 
  
 
@client.event

async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event

async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  
  if msg.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if msg.startswith("$covid"):
    country = msg.split("$covid ",1)[1]
    covid = get_covid(country)
    await message.channel.send(covid)

  if msg.startswith("$joke"):
    joke = get_joke()
    await message.channel.send(joke)
  
  if msg.startswith("$inspire"):
    inspire = get_inspire()
    await message.channel.send(inspire)
  
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  
  if msg.startswith("$new"):
    enc_msg = msg.split("$new ",1)[1]
    update_encouragements(enc_msg)
    await message.channel.send("New encouraging msg added vro")
  
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(token)