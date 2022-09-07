import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import find


intents = discord.Intents.default()
intents.members = True

defaultPrefix = '$'

#Have a different prefix for each server
def prefix(ctx, message):
  #Get the server Id
  ServerId = message.guild.id

  #Find if prefix file exists in the folder of the server id
  #If not return default
  if not os.path.exists("Servers/"+str(ServerId)+"/Prefix.txt"):
    return defaultPrefix
  else:
    #If it exists open it
    with open("Servers/"+str(ServerId)+"/Prefix.txt", 'r') as file:
      
      #return the text In the prefix folder
      return file.readline(),str(defaultPrefix)

#Client
client = commands.Bot(command_prefix=prefix, intents=intents)



#Setup Command
@client.command(pass_context=True, aliases=['setup'])
#Make it Admin only
@has_permissions(administrator=True)
async def Setup(ctx):
  #Get current server
  ServerId = ctx.message.guild.id

  #Make path
  dirName = "Servers/"+str(ServerId)

  #check if path exists
  if not os.path.exists(dirName):
      #Make all the directions needed
      os.mkdir(dirName)
      os.mkdir(dirName+"/Quotes")  

      #Make Prefix file with default prefix written
      with open('Servers/'+ str(ServerId) +'/Prefix.txt', 'w') as file:
        file.write(str(defaultPrefix))

      #Make a file used to download
      with open('Servers/'+ str(ServerId) +'/QuotesFile.txt', 'w') as file:

        #Say that the server is setup
        await ctx.send("Setup for server completed.")
      await ctx.send("Use $Prefix (prefix) to change it.")
    
  #If the path already exists say so
  else:    
      await ctx.send("This server is already set up.")


    
#On Guild join
@client.event
async def on_guild_join(guild):
  #Get server id
  ServerId = guild.id

  #Make path
  dirName = "Servers/"+str(ServerId)

  #Check if path does not exist
  if not os.path.exists(dirName):
      #Make all the directions
      os.mkdir(dirName)
      os.mkdir(dirName+"/Quotes")  

      #Make Prefix file with default prefix written
      with open('Servers/'+ str(ServerId) +'/Prefix.txt', 'w') as file:
        file.write("$")

      #Make a file used to download
      with open('Servers/'+ str(ServerId) +'/QuotesFile.txt', 'w') as file:

        #Find the general text chat and type hello
        general = find(lambda x: x.name == 'general',  guild.text_channels)
      if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))
        await general.send("Make sure to use $Help and $prefix")
      

        
#Make Quote
@client.command(pass_context=True, aliases=['Quote', 'quote', 'makequote', 'MQ' , 'mq'])
async def MakeQuote(ctx,user: discord.Member, *, Quote=None):
  #Get server id
  ServerId = ctx.message.guild.id

  #Make path for the user
  dirName = "Servers/"+str(ServerId)+"/Quotes/"+str(user.id)

  #If the path does not exist yet, make it
  if not os.path.exists(dirName):
    os.mkdir(dirName)

  #Recieve all the files in the direction
  #Count the ammount of files
  _, _, files = next(os.walk(dirName))
  file_count = len(files)

  #Open a file called the ammount of files + 1
  with open(dirName+'/#' + str(file_count + 1) + '.txt', 'w') as file:
    #Write all info of the quote
    file.write(str(Quote)+ '\n')
    file.write("Quote by " + str(user)+ '\n')
    file.write("Quote Submitted by " + str(ctx.author)+ '\n')
    file.write(str(ctx.message.created_at))

  #Say that the quote was made
  await ctx.send("Added Quote #" +str(file_count + 1) + ' to ' + str(user))


  
#See All Quotes
@client.command(pass_context=True, aliases=['AllQuotes', 'AQ' , 'aq'])
async def allquotes(ctx):
  #Get the server ID
  ServerId = ctx.message.guild.id

  #Make the path of the Quotes of the server
  dirName = "Servers/"+str(ServerId)+"/Quotes"

  #Create a variable used to keep track of loop
  totalDirections = 0;

  #Create a bool To fix issue later
  firstTime = True

  #Open the file to download 
  with open('Servers/'+ str(ServerId) +'/QuotesFile.txt', 'w') as AllQuotesFile:
    #Clear the file
    AllQuotesFile.truncate(1)

    #For each direction(USER) in the path loop
    for dirs in os.walk(dirName):
      #Check if its the first time looping
      #(Was problem with index out of range otherwise)
      if not firstTime:

        #Get all the files in the user folder
        _, _, files = next(os.walk(dirName+"/"+os.listdir(dirName)[totalDirections]))

        #Get the name of the user from direction user id
        user = await client.fetch_user(str(os.listdir(dirName)[totalDirections]))

        #Write the user in the download file
        AllQuotesFile.write('\n'+str(user)+" : "+ '\n')

        #Loop through every file and write the quote in the download file
        for x in files:
          with open(dirName+"/"+os.listdir(dirName)[totalDirections]+'/' + str(x), 'r') as file:
            AllQuotesFile.write(str(x.split(".")[0])+" : "+str(file.readline()))

        #Make the Total directions one higher
        totalDirections += 1

      #If first time make First Time False
      else:
        firstTime = False

  #Say that y
  await ctx.send("Here is the file with all the Quotes in the server.")
  await ctx.send(file=discord.File(r'Servers/'+ str(ServerId) +'/QuotesFile.txt'))
  
    
#See Quotes of one person
@client.command(pass_context=True, aliases=['quotes', 'Q' , 'q'])
async def Quotes(ctx,user: discord.Member):
  ServerId = ctx.message.guild.id
  dirName = "Servers/"+str(ServerId)+"/Quotes/"+str(user.id)
  
  if not os.path.exists(dirName):
    await ctx.send("This person does not have any quotes yet")
  else:
    with open('Servers/'+ str(ServerId) +'/QuotesFile.txt', 'w') as PersonQuotesFile:
      PersonQuotesFile.truncate(1)
    
      _, _, files = next(os.walk(dirName))

      PersonQuotesFile.write('\n'+str(user)+" : "+ '\n')

      for x in files:
        with open(dirName+'/' + str(x), 'r') as file:
          PersonQuotesFile.write(str(x.split(".")[0])+" : "+str(file.readline()))

    await ctx.send("Here is the file with all the Quotes of "+ str(user))
    await ctx.send(file=discord.File(r'Servers/'+ str(ServerId) +'/QuotesFile.txt'))
  
#See My quotes
@client.command(pass_context=True, aliases=['myquotes', 'MyQ' , 'myq'])
async def MyQuotes(ctx):
  ServerId = ctx.message.guild.id
  dirName = "Servers/"+str(ServerId)+"/Quotes/"+str(ctx.author.id)
  
  if not os.path.exists(dirName):
    await ctx.send("You do not have any Quotes yet.")
  else:
    with open('Servers/'+ str(ServerId) +'/QuotesFile.txt', 'w') as PersonQuotesFile:
      PersonQuotesFile.truncate(1)
    
      _, _, files = next(os.walk(dirName))

      PersonQuotesFile.write('\n'+str(ctx.author)+" : "+ '\n')

      for x in files:
        with open(dirName+'/' + str(x), 'r') as file:
          PersonQuotesFile.write(str(x.split(".")[0])+" : "+str(file.readline()))

    await ctx.send("Here is the file with your Quotes")
    await ctx.send(file=discord.File(r'Servers/'+ str(ServerId) +'/QuotesFile.txt'))


    
#Info of a quote
@client.command(pass_context=True, aliases=['quoteinfo', 'QI' , 'qi'])
async def QuoteInfo(ctx,user: discord.Member,number):
  ServerId = ctx.message.guild.id
  dirName = "Servers/"+str(ServerId)+"/Quotes/"+str(user.id)

  await ctx.send("Here is the file with the Quote info of "+ str(user))
  await ctx.send(file=discord.File(r''+dirName+"/#"+str(number)+'.txt'))


#Help command
@client.command(pass_context=True, aliases=['QHelp', 'quoteshelp', 'QH'])
async def QuotesHelp(ctx):

  text = """             
-----=====--------Commands--------=====-----
$MakeQuote (MQ) Makes a Quote about a person
    $MQ 'User Mention' 'Quote'

$Quotes (Q) Shows the Quotes of a specific person
    $Q 'User Mention'
  
$AllQuotes (AQ) Shows all Quotes in the server

$MyQuotes (MyQ) Shows all of your Quotes
            
$QuoteInfo (QI) Shows info of a Quote
    $QI 'User Mention' 'Quote Number'
  
-----=====----ADMIN Commands----=====-----
$Prefix (Pref) Changes the prefix
    $Pref 'New Prefix'
  
$ResetPrefix Resets the prefix to $

$ServerId (SID) Shows the server ID 
  
$PlayerId (PID) Shows A player's ID 
    $PID 'User Mention'
  
$Setup is used to setup bot if it is broken
  """
  
  await ctx.send(text)




  
  
#Prefix Command
@client.command(pass_context=True, aliases=['prefix', 'Pref', 'pref'])
@has_permissions(administrator=True)
async def Prefix(ctx, Prefix):
  ServerId = ctx.message.guild.id
  dirName = "Servers/"+str(ServerId)

  with open(str(dirName)+"/Prefix.txt", 'w') as file:
    file.truncate(1)
    file.write(str(Prefix))

    await ctx.send("The prefix is now "+str(Prefix))


    
#Server ID Command
@client.command(pass_context=True, aliases=['Sid', 'SID', 'sid' , 'serverid'])
@has_permissions(administrator=True)
async def ServerId(ctx):
  ServerId = ctx.message.guild.id
  
  await ctx.send("This server's ID is "+ str(ServerId))


  
#Player ID Command
@client.command(pass_context=True, aliases=['Pid', 'PID', 'pid' , 'playerid'])
@has_permissions(administrator=True)
async def PlayerId(ctx,user: discord.Member):
  
  await ctx.send("This player's ID is "+ str(user.id))


  
#Test Command
@client.command(pass_context=True, aliases=['test', 't', 'T'])
@has_permissions(administrator=True)
async def Test(ctx):
  await ctx.send("This is a test.")

#reset Prefix command
@client.command(pass_context=True)
@has_permissions(administrator=True)
async def ResetPrefix(ctx):
  ServerId = ctx.message.guild.id
  dirName = "Servers/"+str(ServerId)

  with open(str(dirName)+"/Prefix.txt", 'w') as file:
    file.truncate(1)
    file.write("$")

    await ctx.send("The Prefix has been reset to '$'")
  
client.run(os.environ['Token'])