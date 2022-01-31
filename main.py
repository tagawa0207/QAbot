import os
import discord  # discord.py
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!",
]

if "responding" not in db.keys():
  db["responding"] = True

# return the quote from API
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

# db operation
def update_encouragements(encouraging_message):
  if "encouragement" in db.keys():
    encouragements = db["encouragement"]
    encouragements.append(encouraging_message)
    db["encouragement"] = encouragements
  else:
    db["encouragement"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragement"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragement"] = encouragements


@client.event
async def on_ready():
  print('we have logged in as {0.user}'
  .format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  # respond to sad words with encouraging words
  if db["responding"]:
    options = starter_encouragements
    if "encouragement" in db.keys():
      options = options + db["encouragement"].value

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  # add a new encouraging word
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  # delete an existing encouraging word
  if msg.startswith("$del"):
    encouragements = []
    if "encouragement" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragement"]
    await message.channel.send(encouragements)

  # show existing encouraging words
  if msg.startswith("$list"):
    encouragements = []
    if "encouragement" in db.keys():
      encouragements = db["encouragement"].value
    await message.channel.send(encouragements)

  # switch if bot respond to sad words with encouragement
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")


keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)

