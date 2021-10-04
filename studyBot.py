import discord
import datetime as dt
import json
from datetime import timedelta


client = discord.Client()

DADES_ESTUDIANTS = {}
CONFIG = {}

#change before using it it raspi
STUDENTS_JSON_PATH = "students.json"
CONFIG_JSON_PATH = "config.json"
SECRET_CONFIG = "secret.json"

DEMANAR_AJUDA = 888148895002132540
TEACHER_LOUNGE_ID = 888487793515434034

DELETE_MESAGES = "!delete"
SET_CD = "!setcd"
TOGGLE_CD = "!togglecd"
GIVE_XP = "!givexp"
SIMPLE_GIVE_XP = 2
COMPLEX_GIVE_XP = 3
HELP_CD = timedelta
TOGGLE_HELP_CD = bool
ADMIN = "Admin"

AJUDA_MATES = ['ajuda mates','ajuda matematiques','ajuda matemàtiques', 'ajuda mat', 'ayuda mates', 'ayuda matematicas', 'ayuda matemáticas', 'ayuda mat']
AJUDA_NATUS = ['ajuda natus','ajuda naturals', 'ajuda nat', 'ayuda natus', 'ayuda naturales', 'ayuda nat']
AJUDA_FISICA = ['ajuda física', 'ajuda fisica', 'ajuda fis', 'ayuda física', 'ayuda fisica', 'ayuda fis']
AJUDA_QUIMICA = ['ajuda química', 'ajuda quimica', 'ajuda qui', 'ayuda química', 'ayuda quimica', 'ayuda qui']
AJUDA_CAT = ['ajuda catala', 'ajuda català', 'ajuda catala', 'ajuda cat', 'ayuda catalan', 'ayuda catalán', 'ayuda cat']
AJUDA_CAST = ['ajuda castella', 'ajuda castellà', 'ajuda caste', 'ayuda castellano', 'ayuda caste', 'ayuda español']
AJUDA_ANG = ['ajuda angles', 'ajuda anglès', 'ajuda ang', 'ajuda eng', 'ayuda ingles', 'ayuda inglés', 'ayuda ing', 'ayuda eng', 'help english', 'help eng']
AJUDA_HIST = ['ajuda historia', 'ajuda hist', 'ajuda història', 'ayuda historia', 'ayuda hist']
AJUDA_SOCIALS = ['ajuda socials', 'ajuda socis', 'ayuda sociales', 'ayuda socis']

PROFE_MATES = "Professor/a Mates"
PROFE_NATUS = "Professor/a Naturals"
PROFE_FISICA = "Professor/a Física"
PROFE_QUIMICA = "Professor/a Química"
PROFE_CAT = "Professor/a Català"
PROFE_CAST = "Professor/a Castellà"
PROFE_ANG = "Professor/a Anglès"
PROFE_HIST = "Professor/a Història"
PROFE_SOCIALS = "Professor/a Socials"

#set teacher role to mention deppending on the help
def set_role_to_mention (message):
  global roleToMention
  if message.content.lower() in AJUDA_MATES: 
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_MATES)
  elif message.content.lower() in AJUDA_NATUS:
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_NATUS)
  elif message.content.lower() in AJUDA_FISICA:
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_FISICA)
  elif message.content.lower() in AJUDA_QUIMICA:
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_QUIMICA)
  elif message.content.lower() in AJUDA_CAT:
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_CAT)
  elif message.content.lower() in AJUDA_CAST:
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_CAST)
  elif message.content.lower() in AJUDA_ANG:
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_ANG)
  elif message.content.lower() in AJUDA_HIST:
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_HIST)
  elif message.content.lower() in AJUDA_SOCIALS:
    roleToMention = discord.utils.get(message.channel.guild.roles, name = PROFE_SOCIALS)
  else:
    return False 


def readJSON(filepath):
  with open(filepath, "r", encoding="utf8") as f:
    data = json.load(f)
  return data

def writeJSON (filepath, data):
  with open(filepath, 'w', encoding='utf8') as f:
    json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))

def fromBoolToOnOff (boolValue):
  if boolValue:
    return "off"
  else:
    return "on"

def fromOnOffToBool (stringValue):
  if stringValue == "true":
    return "off"
  else:
    return "on"

  

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  global DADES_ESTUDIANTS
  global CONFIG
  global HELP_CD
  global TOGGLE_HELP_CD #true means off and false means on
  global TOGGLE_CD
  DADES_ESTUDIANTS = readJSON(STUDENTS_JSON_PATH)
  CONFIG = readJSON(CONFIG_JSON_PATH)
  HELP_CD = timedelta(minutes = int(CONFIG.get("HELP_CD")))
  TOGGLE_HELP_CD = fromOnOffToBool(bool(CONFIG.get("TOGGLE_HELP_CD")))
  



@client.event
async def on_message(message):
  global DEMANAR_AJUDA
  global DADES_ESTUDIANTS
  global HELP_CD
  global TOGGLE_HELP_CD
  global CONFIG
  global SET_CD
  

  

  if message.author == client.user:
    return

  #save data from user
  if str(message.author.id) not in DADES_ESTUDIANTS :
    DADES_ESTUDIANTS[str(message.author.id)] = { "name" : message.author.name,"dateLastMessage" : str(message.created_at), "nick":str(message.author.nick), "dateLastHelpMessage":str(message.created_at), "workXp":0, "lvl":0 }
  else:
    DADES_ESTUDIANTS[str(message.author.id)]["dateLastMessage"] = str(message.created_at)
    DADES_ESTUDIANTS[str(message.author.id)]["name"] = str(message.author.name)
    DADES_ESTUDIANTS[str(message.author.id)]["nick"] = str(message.author.nick)



  
  #si un admin utilitza:
  
  if message.author.roles[-1] == message.channel.guild.roles[-1]:
    print ("entra un admin")
    if message.content.lower().startswith(DELETE_MESAGES):
      #!delete <seconds>
      #Takes the number from the message plus the actual message, that will be also deleted
      messagesToDelete = int(message.content.lower().split()[-1]) + 1
      await message.channel.purge(limit = messagesToDelete)    

    # !setCD X
    elif message.content.lower().startswith(SET_CD):
      cdToSet = message.content.lower().split()[-1]
      HELP_CD = timedelta(minutes = int(cdToSet))
      CONFIG["HELP_CD"] = cdToSet
      writeJSON(CONFIG_JSON_PATH, CONFIG)

    #si un admin utilitza !togglecd
    elif message.content.lower().startswith(TOGGLE_CD):
      TOGGLE_HELP_CD = not TOGGLE_HELP_CD
      CONFIG["TOGGLE_HELP_CD"] = fromBoolToOnOff(TOGGLE_HELP_CD)
      writeJSON(CONFIG_JSON_PATH, CONFIG)
      await message.delete()
      await message.channel.send(content = f'Help cd turned {CONFIG["TOGGLE_HELP_CD"]}!', delete_after = 10)

    elif message.content.lower().startswith(GIVE_XP) :
      xpMessage = message.content.lower().split()
      if len(xpMessage) == SIMPLE_GIVE_XP:
        for id in DADES_ESTUDIANTS:
          if id in xpMessage[1]:
            DADES_ESTUDIANTS[id]["workXp"] = DADES_ESTUDIANTS[id]["workXp"] + 10
            writeJSON(STUDENTS_JSON_PATH, DADES_ESTUDIANTS)
      elif len(xpMessage) == COMPLEX_GIVE_XP:
        xpMessage = message.content.lower().split()
        for id in DADES_ESTUDIANTS:
          if id in xpMessage[1]:
            DADES_ESTUDIANTS[id]["workXp"] = DADES_ESTUDIANTS[id]["workXp"] + int(xpMessage[2])
            writeJSON(STUDENTS_JSON_PATH, DADES_ESTUDIANTS)
      else:
        await message.delete()
        await message.channel.send(content = f'Wrong command, use !giveXP <name> or !giveXP <name> <amount>', delete_after = 10)

    else :
      return

  #si s'utilitza "ajuda <assignatura>"
  elif int(message.channel.id) == DEMANAR_AJUDA and message.content.lower().startswith("ajuda"):
    if set_role_to_mention(message) == False:
      await message.delete()
      await message.channel.send('Missatge erroni.\nAquest canal només s\'utilitza per demanar ajuda mitjançant la comanda "ajuda <assignatura>".', delete_after = 10)
      return

    #mirar si pot demanar ajuda: Si fa més de 5min o no ha demanat mai ajuda pot
    actualTime = message.created_at

    lastHelpMessageTime = dt.datetime.strptime(DADES_ESTUDIANTS[str(message.author.id)]["dateLastHelpMessage"], "%Y-%m-%d %H:%M:%S.%f")
    differenceBetweenHelpsInTime = actualTime - lastHelpMessageTime
    
    if (DADES_ESTUDIANTS[str(message.author.id)]["dateLastHelpMessage"] == str(message.created_at) or differenceBetweenHelpsInTime >= HELP_CD) or TOGGLE_HELP_CD: 
      #post message to channel ES_DEMANA_AJUDA
      await client.get_channel(TEACHER_LOUNGE_ID).send(f'{message.author.mention} demana ajuda de mates {roleToMention.mention}' )

      #send message sent and delete helpl message from DEMANAR_AJUDA
      await message.delete()
      await message.channel.send(content = f'Message sent, wait for the teacher to answer {message.author.mention}!', delete_after = 10)
      #update lastHelpMessage
      DADES_ESTUDIANTS[str(message.author.id)]["dateLastHelpMessage"] = str(message.created_at)
       
    
    else:
    #Si no pot demanar ajuda s'ha de calcular quant de temps falta perquè pugui tornar a demanar ajuda i avisar
      timeLeft = HELP_CD - differenceBetweenHelpsInTime 
      timeLeftMinutesSeconds = divmod(timeLeft.seconds, 60) 
      await message.delete()
      await message.channel.send(content = f'You need to wait {timeLeftMinutesSeconds[0]} minutes and {timeLeftMinutesSeconds[1]} seconds to ask for help again {message.author.mention}!', delete_after = 10)


      
  else:
    if  int(message.channel.id) == DEMANAR_AJUDA:
      await message.delete()
      await message.channel.send('Missatge erroni.\nAquest canal només s\'utilitza per demanar ajuda mitjançant la comanda "ajuda <assignatura>".', delete_after = 10)

  #actualitem DB
  writeJSON(STUDENTS_JSON_PATH, DADES_ESTUDIANTS)

SECRET = readJSON(SECRET_CONFIG)
client.run(SECRET["STUDYBOT_TOKEN"])
