import discord
import datetime
import datetime as dt
import random
from datetime import datetime, timedelta
from datetime import datetime
from discord import Interaction
from discord.ext import commands
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "$", intents = discord.Intents.all())

lore_file = "lore.txt"
birthday_file = "birthdays.txt"
starter_marker = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
ending_marker = "------------------------------------------------------------------------------------------------------------------"

#Extracts a random section from 'lore.txt'
def extract_section():
    section = []
    index = None

    try:    
        #The lore.txt file will be parsed
        with open(lore_file, 'r')as file:
            for line in file:
                line = line.strip()

                #The starting marker will cue to start saving the section
                if line == starter_marker:
                    index = []
                
                #The ending marker will cue to stop saving the section, moving onto the next one
                elif line == ending_marker:
                    if index is not None:
                        section.append(" ".join(index))
                        index = None

                elif index is not None:
                    index.append(line + "\n") 

        if section:
            event = random.choice(section)
            return event.splitlines()
        else:
            return None
        
    except FileNotFoundError:
        print(f"Error:File '{lore_file}' couldn't be found.")
        return None
    
    except Exception as e:
        print(f"An error occurred while using the file: {e}")
        return None

#Embeds the user's memory and presents it to the user for confirmation       
async def create_lore(ctx, header, picture, desc, time):

    embed = discord.Embed(title = header, description = desc)
    embed.set_thumbnail(url = picture)
    embed.add_field(name = "When did this happen?", value = time)
    await ctx.send(embed = embed)

    await ctx.send("Is this how you want to remember this memory?")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel 

    message = await bot.wait_for('message', check = check)

    choice = message.content

    while not(choice == "yes" or choice == "no"):
        if choice == "yes":
            f = open(lore_file, "a")
            with open(lore_file, "a"):
                f.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + "\n")
                f.write(header + "\n")
                f.write(picture + "\n")
                f.write(desc + "\n")
                f.write(time + "\n")
                f.write("------------------------------------------------------------------------------------------------------------------" + "\n")
                f.close()

        elif choice == "no":
            await ctx.send("The memory will be forgotten")
            break

        else:
            await ctx.send("You did not specify what you want to do with this memory. It will be forgotten")

            embed = discord.Embed(title = header, description = desc)
            embed.set_thumbnail(url = picture)
            embed.add_field(name = "When did this happen?", value = time)
            await ctx.send(embed = embed)

            await ctx.send("Is this how you want to remember this memory?")

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel 

            message = await bot.wait_for('message', check = check)

            choice = message.content


#Will print a random memory from the memory vault
@bot.command()
async def remember(ctx):
    section = extract_section()

    if section:
        embed = discord.Embed(title = section[0], description = section[2])
        embed.set_thumbnail(url = section[1])
        embed.add_field(name = "When did this memory happen?", value = section[3])
        await ctx.send(embed = embed)


#Upon running, the bot will send a confirmation text
@bot.event
async def on_ready():
    print("The M.E.M.O.R.Y. Bot is remembering...")

#Will send a private DM to the user wishing them a happy birthday!
@tasks.loop(minutes = 1)
async def wish():
    now = datetime.now()
    print(now)
    tomorrow = now + timedelta(days = 1)
    section = []
    index = None

    f = open(birthday_file, "r")

    try:
        #The lore.txt file will be parsed
        with open(lore_file, 'r')as file:
            for line in file:
                line = line.strip()

                #The starting marker will cue to start saving the section
                if line == starter_marker:
                    index = []
                
                #The ending marker will cue to stop saving the section, moving onto the next one
                elif line == ending_marker:
                    if index is not None:
                        section.append(" ".join(index))
                        index = None

                elif index is not None:
                    index.append(line + "\n") 

        if tomorrow in section:
            print(section)
            userid, birthday = section

            user = await bot.fetch_userinfo(userid)

            if now == birthday:
                try:
                    await user.send(f"Happy Birthday {user}! This is a message from Bryan. I hope you have a great day today.")
                    print(f"Sent DM to {user} for their birthday today at {datetime.datetime.now()}")
                
                except discord.errors.Forbidden:
                    print(f"Unable to send DM to {user} for their birthday. They might have DMs settings that prevent me from sending a message.")

                except Exception as e:
                    print(f"An error occurred while trying to wish {user} a happy birthday.")
            
                else:
                    print("There wasn't anyone in my database that matches that.")

        elif tomorrow in section:
            channel = bot.get_channel(833816365906919428)
            await channel.send(f"{user}'s birthday is tomorrow! Get ready to wish them a happy birthday tomorrow.")
        

        else:
            return None
        
    except FileNotFoundError:
        print(f"Error:File '{lore_file}' couldn't be found.")
        return None
    
    except Exception as e:
        print(f"An error occurred while using the file: {e}")
        return None
        

#Will create an instance to wish a user happy birthday!
@bot.command()
async def add_birthday(ctx):
    f = open(birthday_file, "a")

    choice = ""

    while not(choice.lower() == "yes" or choice.lower() == "y"):
        print("You are about to add a birthday! Get ready to never forget this very special day.")
        await ctx.send("Who do you want to wish a happy birthday? Give me their User ID:")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
            
        message = await bot.wait_for('message', check = check)

        userid = message.content

        userid = int(userid)

        user = bot.get_user(userid)

        await ctx.send(f"When is {user}'s birthday?")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
            
        message = await bot.wait_for('message', check = check)

        birthday = message.content

        dob = datetime.strptime(birthday, "%B %d %Y")

        await ctx.send(f"To confirm, {user}'s birthday is on " + dob.strftime("%B") + " " + dob.strftime("%d") + ", " + dob.strftime("%Y"))

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
            
        message = await bot.wait_for('message', check = check)

        choice = message.content

        if choice.lower() == "yes":
            f.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + "\n")
            f.write(str(userid))
            f.write("\n")
            f.write(dob.strftime("%B %d"))
            f.write("\n")
            f.write("------------------------------------------------------------------------------------------------------------------" + "\n")

            await ctx.send(f"{user}'s birthday has been set to " + dob.strftime("%B") + " " + dob.strftime("%d"))

        else:
            await ctx.send("The birthday has been forgotten.")
        
#Will add a memory to a text file
@bot.command()
async def add_lore(ctx):
    f = open(lore_file, "a")
    print("You have begun to create lore. Get ready to produce some memories.")
    await ctx.send("Give me a title for a memory you don't want to forget:")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel 

    message = await bot.wait_for('message', check = check)

    title = message.content

    await ctx.send("Type the name of the image you want in this memory:")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel 

    message = await bot.wait_for('message', check = check)

    thumbnail = message.content
    
    await ctx.send("Give me a description for the " + title + " memory:")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel 

    message = await bot.wait_for('message', check = check)

    description = message.content

    await ctx.send("Give me a time for when " + title + " happened:")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    message = await bot.wait_for('message', check = check)

    time = message.content

    await create_lore(ctx, title, thumbnail, description, time)

        
    f.close()
    

bot.run('TOKEN')
