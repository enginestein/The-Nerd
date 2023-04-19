from urllib.request import urlopen
from arrays import hug_links
import os
import random
import json
import aiohttp
import asyncio
from colorama import Fore, Style
import datetime
import traceback
from easy_pil import Editor, load_image_async, Font
from disnake.ext import commands, tasks
import disnake
import cryptocompare

import config

token = config.DISCORD_TOKEN


# https://medium.com/techie-delight/top-algorithms-data-structures-concepts-every-computer-science-student-should-know-e0549c67b4ac#:~:text=Depth%20First%20Search%20(DFS)%20Algorithm,Kruskal's%20Algorithm


#https://discord.com/api/oauth2/authorize?client_id=977203203147980881&permissions=1644971949559&scope=bot
dictionary_check = True
timer_check = True 
content_check = True 
history_check = True
lev = ["Level-5+", "Level-10+", "Level-15+"]
level_num = [5, 10, 15]
intents = disnake.Intents.default()
intents.members = True
_bot = commands.Bot(command_prefix="nerd", intents=intents)
_bot.remove_command('help')
amount_del = 0
rand = 0
chvc=[]
time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}
sent_color = 0xE3E5E8
changed_color = 0xFAA61A
deleted_color = 0xF04747
colors = [1752220, 1146986, 3066993, 2067276, 3447003, 2123412, 10181046, 7419530, 15277667, 15844367, 11342935, 12745742, 15105570, 11027200, 15158332, 10038562, 9807270, 9936031, 8359053, 12370112, 3426654, 2899536, 16776960]

@_bot.slash_command()
async def fun(ctx):
    pass

@_bot.slash_command()
async def mod(ctx):
    pass

async def send_first_time_message(ctx: disnake.ApplicationCommandInteraction, command_name: str, embed: disnake.Embed) -> bool:
    user_id = str(ctx.author.id)
    with open('command_history.json', 'r') as f:
        command_history = json.load(f)

    if user_id not in command_history:
        command_history[user_id] = []
        await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
        with open('command_history.json', 'w') as f:
            json.dump(command_history, f)
        return True

    if command_name not in command_history[user_id]:
        command_history[user_id].append(command_name)
        with open('command_history.json', 'w') as f:
            json.dump(command_history, f)
        await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
        return True

    return False

async def send_to_log(bot, embed, channel_id):
    channel = _bot.get_channel(int(channel_id))
    await channel.send(embed=embed)

async def log_reaction(reaction, user, type):

    with open('setup.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  
    
    if data[str(reaction.message.guild.id)]['msg_id'][0] is not None:
        message_log_id = data[str(reaction.message.guild.id)]['msg_id'][0]
    else:
        pass

    if user.id == _bot.user.id:
        return 0
    if reaction.message.guild is None:
        return 0

    bot_user = ""
    if user.bot:
        bot_user = " (bot)"

    if type == 'Deleted':
        color = deleted_color
    elif type == 'Sent':
        color = sent_color

    embed = disnake.Embed(title=f"{user}{bot_user}",description=f"{reaction.emoji}\n"f"[jump to message]({reaction.message.jump_url})",color=color)
    embed.set_footer(text=f"Author ID: {user.id}\nMessage ID: {reaction.message.id}")
    embed.set_thumbnail(url=user.avatar.url)
    embed.set_author(name=f"Reaction {type} in #{reaction.message.channel}",icon_url=_bot.user.avatar.url)

    try:
        embed.set_image(url=reaction.emoji.url)
    except AttributeError:
        unicodes = []
        for emoji in reaction.emoji:
            unicodes.append(f"{ord(emoji):x}")

        filename = '-'.join(unicodes)
        embed.set_image(url=f"https://twemoji.maxcdn.com/v/latest/72x72/{filename}.png")

    await send_to_log(_bot, embed, channel_id=message_log_id)

@_bot.event
async def on_reaction_add(reaction, user):
    await log_reaction(reaction, user, type='Sent')

@_bot.event
async def on_reaction_remove(reaction, user):
    await log_reaction(reaction, user, type='Deleted')

async def setups(user):
    with open('setup.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.guild.id) in data:
        return False
    else:
        data[str(user.guild.id)] = {}
        data[str(user.guild.id)]['msg_id'] = []
        data[str(user.guild.id)]['hello_byebye'] = []
        data[str(user.guild.id)]['level'] = []
        data[str(user.guild.id)]['hbm'] = []
        data[str(user.guild.id)]['hbm2'] = []
        data[str(user.guild.id)]['levelm'] = []        
    
    with open('setup.json', 'w') as file:
        json.dump(data, file)  

@mod.sub_command(description="Set the channel for welcome and leaving messages")
@commands.has_permissions(administrator=True)
async def weleave(ctx, channel_id, welcome_message, leaving_message):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Server welcoming logs command", value="This command requires administrator permissions. It can be used to set logs for welcoming messages and leaving messages. Messages are not editable. Provide the channel ID you want messages in. The new channel ID can be set when the command is ran again with a new channel ID.")
    await send_first_time_message(ctx, "weleave", embed) 

    await setups(ctx)
    with open('setup.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  
    
    if len(data[str(ctx.guild.id)]['hello_byebye']) == 0:
        if len(data[str(ctx.guild.id)]['hbm']) == 0 and len(data[str(ctx.guild.id)]['hbm2']) == 0:
            data[str(ctx.guild.id)]['hello_byebye'].append(channel_id)
            data[str(ctx.guild.id)]['hbm'].append(welcome_message)
            data[str(ctx.guild.id)]['hbm2'].append(leaving_message)
            with open('setup.json', 'w') as file:
                json.dump(data, file)  
        
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="You have set up welcome and leave messages in", value=_bot.get_channel(int(channel_id)))
            await ctx.send(embed=embed)
        
        else:
            data[str(ctx.guild.id)]['hbm'].clear()
            data[str(ctx.guild.id)]['hbm2'].clear()
            with open('setup.json', 'w') as file:
                json.dump(data, file)  
        
            data[str(ctx.guild.id)]['hello_byebye'].append(channel_id)
            data[str(ctx.guild.id)]['hbm'].append(welcome_message)
            data[str(ctx.guild.id)]['hbm2'].append(leaving_message)

            with open('setup.json', 'w') as file:
                json.dump(data, file)
        
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="You have set up welcome and leave messages in", value=_bot.get_channel(int(channel_id)))
            await ctx.send(embed=embed)
            

    else:
        data[str(ctx.guild.id)]['hello_byebye'].clear()
        with open('setup.json', 'w') as file:
            json.dump(data, file)  
        
        data[str(ctx.guild.id)]['hello_byebye'].append(channel_id)
        data[str(ctx.guild.id)]['hbm'].append(welcome_message)
        data[str(ctx.guild.id)]['hbm2'].append(leaving_message)
        with open('setup.json', 'w') as file:
            json.dump(data, file)
        
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name="You have set up welcome and leave messages in", value=_bot.get_channel(int(channel_id)))
        await ctx.send(embed=embed)

@_bot.event
async def on_member_join(member: disnake.Member):
    with open('setup.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    channel = _bot.get_channel(int(data[str(member.guild.id)]['hello_byebye'][0]))
    message = data[str(member.guild.id)]['hbm'][0]
    
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name=message, value=member.mention)
    await channel.send(embed=embed)

@_bot.event
async def on_member_remove(member: disnake.Member):
    with open('setup.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    channel = _bot.get_channel(int(data[str(member.guild.id)]['hello_byebye'][0]))
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="One of our members have left", value=member.mention)
    await channel.send(embed=embed)

@mod.sub_command(description="Set up the logs")
@commands.has_permissions(administrator=True)
async def logs(ctx, logging_channel):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Server logs command", value="This command requires administrator permissions. This is a very useful command which logs server activities to an specific channel, just provide the channel ID. This command logs every reaction, message deletion and also if messages are edited by someone. You can directly jump to that messages as well. To change the logging channel you can run the command again with a new channel ID.")
    await send_first_time_message(ctx, "logs", embed) 

    
    await setups(ctx)
    with open('setup.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  
    
    if len(data[str(ctx.guild.id)]['msg_id']) == 0:
    
        data[str(ctx.guild.id)]['msg_id'].append(logging_channel)

        with open('setup.json', 'w') as file:
            json.dump(data, file)  

        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name='You have set up message and reaction logs in', value=_bot.get_channel(int(logging_channel)))
        await ctx.send(embed=embed)
    
    else:
        data[str(ctx.guild.id)]['msg_id'].clear()
        with open('setup.json', 'w') as file:
            json.dump(data, file)  
        
        data[str(ctx.guild.id)]['msg_id'].append(logging_channel)

        with open('setup.json', 'w') as file:
            json.dump(data, file)
        
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name='You have set up message and reaction logs in', value=_bot.get_channel(int(logging_channel)))
        await ctx.send(embed=embed)

@_bot.event
async def log_message(message, type, before=None, attachments_old=None):

    with open('setup.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if data[str(message.guild.id)]['msg_id'][0] is not None:
        message_log_id = data[str(message.guild.id)]['msg_id'][0]
    else:
        pass

    if message.author.id == _bot.user.id:
        return 0

    if message.guild is None:
        return 0

    bot_user = ""
    if message.author.bot:
        bot_user = " (bot)"

    try:
        attachments = ""
        count = 1
        for a in message.attachments:
            attachments += f"\n[attachment{count}]({a.url})"
            count += 1
    except Exception:
        attachments = ""

    description = ""
    if type == 'Edited':
        color = changed_color
        description = f"Before:\n{before.content}{attachments_old}\n\nAfter:\n"
    elif type == 'Deleted':
        color = deleted_color
    elif type == 'Sent':
        color = sent_color

    embed = disnake.Embed(title=f"{message.author}{bot_user}",description=f"{description}{message.content}{attachments}\n"f"[jump to message]({message.jump_url})",color=color)
    embed.set_footer(text=f"Author ID: {message.author.id}\nMessage ID: {message.id}")
    embed.set_thumbnail(url=message.author.avatar.url)
    embed.set_author(name=f"Message {type} in #{message.channel}", icon_url=_bot.user.avatar.url)
    await send_to_log(_bot, embed, channel_id=message_log_id)

@_bot.event
async def on_message_edit(before, message):
        if before.content == message.content:
            return 0
        try:
            attachments_old = ""
            count = 1
            for a in before.attachments:
                attachments_old += f"\n[attachment{count}]({a.url})"
                count += 1
        except Exception:
            attachments_old = ""

        await log_message(message, type='Edited', before=before,attachments_old=attachments_old)

@_bot.event
async def on_message_delete(message):
        await log_message(message, type='Deleted')

@_bot.event
async def on_ready(): 
    print(f"Bot logged in as {_bot.user}")
    print("--------------------------------------------------------")


class Help(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Fun commands", style=disnake.ButtonStyle.green)
    async def fun(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        embed = disnake.Embed(color=random.choice(colors))
        embed.set_author(name="Games an fun commands")

        commands = [("/hug <user>", "`Hug someone`", False),
              ("/meme", "`Get an meme`", False),
              ("/pmeme", "`Get an programming meme`", False),
              ("/fact", "`Get an fact`", False),
              ("/serverinfo", "`Get server info`", False),
              ("/magic8ball <context>", "`Ask an magic8ball question`", False),
              ("/userinfo <user>", "`Get some information about an user`", False),
              ("/pic", "`Get an cool picture`", False),
              ("/truth", "`Get an random truth question`", False),
              ("/compliment", "`Get an compliment`", False),
              ("/dadjokes", "`Get an dad joke`", False),
              ("/topic", "`Get an topic to chat on`", False),
              ("/coinflip", "`Flip a coin`", False),
              ("/rolldice <num_dice> <num_side>", "`Rolls a specified number of dice with a specified number of sides.`", False),
              ("/avatar <user>", "`Get someone's avatar.`", False),
              ("/image <query>", "`Searches for and displays images based on user input.`", False),
              ("/poll <question> <options>", "`Create and vote on polls.`", False),
              ("/cat", "`Get an random cat image`", False),
              ("/dog", "`Get an random dog image`", False),
              ("/quote", "`Get a quote`", False),
              ("/ping", "`Get bot's latency`", False),
              ("/joke", "`Get a joke`", False),
              ("/trivia", "`Get trivia question`", False),
              ("/fortune", "`Get your fortune`", False),
              ("/report", "`Report a bug or give any suggestion.`", False),
              ("/verify", "`Verify yourself to get verified role.`", False)]

        for name, value, inline in commands:
            embed.add_field(name=name, value=value, inline=inline)
    
        await interaction.response.send_message(embed=embed)
    
    @disnake.ui.button(label="Economy commands", style=disnake.ButtonStyle.green)
    async def eco(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        embed = disnake.Embed(color=random.choice(colors))
        embed.set_author(name="Economy commands")

        commands = [("/bal", "`Get your account balance`", False),
              ("/inv", "`Check your inventory`", False),
              ("/shop", "`Open shop`", False),
              ("/buy <item code>", "`Buy some items`", False),
              ("/geek_coins", "`Mine some geek_coins currency if you have an laptop`", False),
              ("/redeem <amount>", "`Redeem all of your geek_coins currency`", False),
              ("/jobs", "`See the job board`", False),
              ("/job <job code>", "`Get an job`", False),
              ("/subjects", "`Subjects to study`", False),
              ("/learn <subject>", "`Learn any subject`", False),
              ("/learnpoints", "`Get your points in every subject`", False),
              ("/top", "`Get global leaderboard of richest person`", False),
              ("/level", "`See your level`", False),
              ("/software", "`Make softwares if you have software engineer job`", False),
              ("/assemble", "`Assemble an computer if you have enough requirements`", False),
              ("/computer", "`Open your computer, see your programs and os`", False),
              ("/attack <member>", "`Use your spyware, malware or ransomware to earn money and items`", False),
              ("/run", "`Run your Discord bot, app or website`", False),
              ("/daily", "`Get your daily coins`", False),
              ("/retire", "`Retire from your current job`", False),
              ("/delete <program name>", "`Delete an program from your computer`", False),
              ("/loan <amount>", "`Get a loan`", False),
              ("/pay <amount>", "`Pay for loan`", False),
              ("/laboratory", "`Start and navigate your laboratory`", False),
              ("/lend", "`Check how much loan is left`", False)]
        
        for name, value, inline in commands:
            embed.add_field(name=name, value=value, inline=inline)
    
        await interaction.response.send_message(embed=embed)
    
    @disnake.ui.button(label="Economy commands part 2", style=disnake.ButtonStyle.green)
    async def eco2(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        embed = disnake.Embed(color=random.choice(colors))
        embed.set_author(name="Economy commands part 2")

        commands = [("/send <member> <amount>", "`Send money to someone`", False),
              ("/input_item <item> <price>", "`Put item on market`", False),
              ("/remove_item <item>", "`Remove an item from market`", False),
              ("/stream", "`Do a livestream to earn money.`", False),
              ("/sell_all", "`Sell your whole inventory.`", False),
              ("/delete_account", "`Delete your account`", False),
              ("/call", "`Get a random tip if you have a phone.`", False),
              ("/find", "`find an item in an random place`", False),
              ("/market", "`Get global market of items`", False),
              ("/buy_from_market <seller_id> <item_num>", "`Buy any item from global market, just input the seller ID and item number.`", False),
              ("/gift <item_code> <member>", "`Gift an item to someone`", False),
              ("/weekly", "`Get weekly coins`", False),
              ("/monthly", "`Get monthly coins`", False),
              ("/rates", "`Get crypto rates`", False),
              ("/buy_crypto <crypto_code>", "`Buy an crypto coin`", False),
              ("/redeem_crypto <crypto_code> <amount>", "`Redeem an crypto coin`", False),
              ("/crypto_bal", "`Get crypto balance`", False),
              ("/disassemble", "`disassemble an computer, take out it's parts and sell them.`", False),
              ("/sell <item_code>", "`Sell an item`", False),
              ("/start_mine", "`Start the mining career`", False),
              ("/explore", "`Explore new places for mining`", False),
              ("/explored", "`List all explored places`", False),
              ("/mine <place_name>", "`Mine in an place`", False),
              ("/elements", "`Get all found elements`", False),
              ("/sell_element", "`Sell an element`", False),
              ("/robot", "`Build your robot`", False),
              ("/upgrade", "`Upgrade your robot`", False),
              ("/fight <opponent> <money>", "`Fight with someone if you have a robot and they have a robot`", False)]
        
        for name, value, inline in commands:
            embed.add_field(name=name, value=value, inline=inline)
    
        await interaction.response.send_message(embed=embed)
    
    @disnake.ui.button(label="Moderator commands", style=disnake.ButtonStyle.green)
    async def mod(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        embed = disnake.Embed(color=random.choice(colors))
        embed.set_author(name="Moderating commands")

        commands = [("/ban <user>", "`Ban someone`", False),
              ("/mute <user> <mutetime (optional)>", "`Mute someone`", False),
              ("/unmute <user>", "`Unmute someone`", False),
              ("/kick <user>", "`Kick someone`", False),
              ("/warn <user> <context>", "`Give a warning`", False),
              ("/purge <amount>", "`Clear messages`", False),
              ("/dm <user>", "`Dm someone`", False),
              ("/spam", "`Enable or disable spam protection`", False),
              ("/logs <channel id>", "`Set message and reaction logging in an channel`", False),
              ("/weleave <channel id>", "`Set the channel for welcome and leave messages`", False),
              ("/purge <number>", "`Clear messages`", False),
              ("/levlog <channel id>", "`Set level up logs`", False)]
        
        for name, value, inline in commands:
            embed.add_field(name=name, value=value, inline=inline)
    
        await interaction.response.send_message(embed=embed)

@fun.sub_command(descripton="Get your fortune")
async def fortune(ctx):
        fortunes = [
            "A bird in the hand is worth two in the bush.",
            "A good time to finish up old tasks is just before the end of the day.",
            "All the effort you are making will ultimately pay off.",
            "Don't be afraid to take that big step.",
            "Happiness is not the absence of conflict, but the ability to cope with it.",
            "Life is a tragedy for those who feel, and a comedy for those who think.",
            "The greatest risk is not taking one."
        ]
        fortune = random.choice(fortunes)
        await ctx.send(fortune)

async def rep(ctx):
    with open('report.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(ctx.author.id) in data:
        return False
    else:
        data[str(ctx.author.id)] = {}
        data[str(ctx.author.id)]['message'] = []
    
    with open('report.json', 'w') as f:
        json.dump(data, f)
    
    return True

@_bot.slash_command(description="Report any error or any bug")
async def report(ctx, message):
    await rep(ctx)
    embed = disnake.Embed(color = random.choice(colors))
    embed.set_footer(text="Do not give any offensive message, on getting an message like that we may ban you from our bot.")
    with open('report.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    data[str(ctx.author.id)]['message'].append(message)

    with open('report.json', 'w') as file:
        json.dump(data, file)

    await ctx.send("Your report has been stored in our database.")

@fun.sub_command(description="Get trivia questions")
async def trivia(ctx, category: int = 0, difficulty: str = 'easy'):
    url = f'https://opentdb.com/api.php?amount=1&category={category}&difficulty={difficulty}&type=multiple'
    response = requests.get(url).json()
    question = response['results'][0]['question']
    correct_answer = response['results'][0]['correct_answer']
    incorrect_answers = response['results'][0]['incorrect_answers']
    options = [correct_answer] + incorrect_answers
    random.shuffle(options)

    embed = disnake.Embed(title="Trivia Question", description=question, color=0x00ff00)
    for i, option in enumerate(options):
        embed.add_field(name=f"Option {i+1}", value=option, inline=False)

    await ctx.send(embed=embed)

@_bot.slash_command(description="Display items in market")
async def market(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Market command", value="This command is used to display global market, global market is a place where users from all the server around discord who use this bot are selling their items at their own price. You can buy items from here too. To put your own items you can use /input_item, to buy an item you can use /buy_from_market.")
    await send_first_time_message(ctx, "market", embed)   
    
    with open("market.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    items = []
    for seller in data:
        for i in range(1, 5):
            item = data[seller]["Item{}".format(i)]
            price = data[seller]["Item{}p".format(i)]
            if item:
                items.append(f"Item: {item}, Price: {price}, Seller ID: {seller}")

    if items:
        await ctx.send("Here are the items currently available in the market:\n" + "\n".join(items))
    else:
        await ctx.send("There are currently no items available in the market.")

@_bot.slash_command(description="Buy an item from the market")
async def buy_from_market(ctx, seller_id: str, item_num: int):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Buying item from market command", value="You can use this command to buy an item from global market. You need to copy the seller ID from the /market and also type the item number. The items are displayed inside [], and the first item is item number 1. Only four items per seller can be sold.")
    await send_first_time_message(ctx, "buy_from_market", embed)   

    with open("market.json", "r", encoding="utf-8") as file:
        market_data = json.load(file)
    
    with open("account.json", "r", encoding="utf-8") as file:
        account_data = json.load(file)

    if item_num not in range(1, 5):
        return await ctx.send("Invalid item number. Please enter a number between 1 and 4.")
    
    if seller_id not in market_data:
        return await ctx.send("Seller not found in the market.")
    
    item_key = f"Item{item_num}"
    item_price_key = f"Item{item_num}p"
    item_name = market_data[seller_id][item_key]
    item_price = market_data[seller_id][item_price_key]
    print(item_price)

    for i in item_name:
        item = i

    if item in item_name:
        account_data[str(ctx.author.id)]["Inventory"].append(item)
        market_data[seller_id][item_key].clear()
        market_data[seller_id][item_price_key] *= 0
        account_data[str(ctx.author.id)]["Bank"] -= item_price
        account_data[str(seller_id)]["Bank"] += item_price

        with open("market.json", "w", encoding="utf-8") as file:
            json.dump(market_data, file)
            
        with open("account.json", "w", encoding="utf-8") as file:
            json.dump(account_data, file)

        embed = disnake.Embed(color = random.choice(colors))
        embed.add_field(name="Transaction successful", value=f"You have successfuly bought {item} from @<{seller_id}>")

        await ctx.send(embed=embed)
        
    else:
        await ctx.send("That item is not available")
    

class GiftConfirmView(disnake.ui.View):
    def __init__(self, ctx: commands.Context, item_name: str, sender: disnake.Member, receiver: disnake.Member):
        super().__init__(timeout=30.0)
        self.ctx = ctx
        self.item_name = item_name
        self.sender = sender
        self.receiver = receiver

    async def interaction_check(self, interaction: disnake.Interaction):
        return interaction.user.id == self.receiver.id

    @disnake.ui.button(label="Confirm Gift", style=disnake.ButtonStyle.green)
    async def confirm_gift(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        with open("account.json", 'r', encoding='utf-8') as file:
            data = json.load(file)

        data[str(self.receiver.id)]["Inventory"].append(self.item_name)
        with open("account.json", 'w') as file:
            json.dump(data, file)

        color = random.choice(colors)
        embed = disnake.Embed(color=color)
        embed.add_field(name="Success", value=f"{self.receiver.mention} has accepted your gift of {self.item_name.title()}!")
        await self.ctx.send(embed=embed, view=None)

    @disnake.ui.button(label="Decline Gift", style=disnake.ButtonStyle.red)
    async def decline_gift(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        color = random.choice(colors)
        embed = disnake.Embed(color=color)
        embed.add_field(name="Gift Declined", value=f"{self.receiver.mention} has declined your gift of {self.item_name.title()}.")
        await self.ctx.send(embed=embed, view=None)

@_bot.slash_command(description="Gift someone an item")
async def gift(ctx, item_code, member: disnake.User):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Gifting command", value="Gift an item to any user. If you do not have that item in your inventory or the provided item code is wrong, the command won't run. The reciever must accept the gift. After they accept the gift, the item would not be in your inventory anymore.")
    await send_first_time_message(ctx, "gift", embed) 

    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open("shop.json", 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    for item in data2:
        if item in data[str(ctx.user.id)]["Inventory"]:
            if item_code == data2[item]['code']:
                data[str(ctx.user.id)]["Inventory"].remove(item)
                with open("account.json", 'w') as file:
                    json.dump(data, file)

                item_name = item.title()
                sender = ctx.author
                receiver = member

                view = GiftConfirmView(ctx, item_name, sender, receiver)
                await ctx.send(f"{member.mention}, Listen up! {sender.mention} is gifting you {item_name}, would you like to accept?.", view=view)
            else:
                pass
        else:
            pass

@_bot.slash_command(description="Display items in market")
async def input_item(ctx, item: str, price: int):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Inputting item into market command", value="You can use the exact item name to input an item into market. The item should be in your inventory. You can put any price you want. You can access market using /market")
    await send_first_time_message(ctx, "input_item", embed)   

    await markett(ctx)
    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open("shop.json", 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    with open("market.json", 'r', encoding='utf-8') as file3:
        data3 = json.load(file3)
    
    if item in data[str(ctx.user.id)]["Inventory"]:
                if data3[str(ctx.author.id)]['Item1'] == []:
                    data3[str(ctx.author.id)]['Item1'].append(item)
                    data[str(ctx.user.id)]["Inventory"].remove(item)
                    data3[str(ctx.author.id)]['Item1p'] += price

                    with open("market.json", 'w', encoding='utf-8') as file3:
                        json.dump(data3, file3)
                    
                    with open("account.json", 'w', encoding='utf-8') as file:
                        json.dump(data, file)

                    await ctx.send("Item is successfuly displayed in global shop")    
                else:
                    if data3[str(ctx.author.id)]['Item2'] == []:
                        data3[str(ctx.author.id)]['Item2'].append(item)
                        data[str(ctx.user.id)]["Inventory"].remove(item)
                        data3[str(ctx.author.id)]['Item2p'] += price

                        with open("market.json", 'w', encoding='utf-8') as file3:
                            json.dump(data3, file3)    
                        
                        with open("account.json", 'w', encoding='utf-8') as file:
                            json.dump(data, file)    
                        
                        await ctx.send("Item is successfuly displayed in global shop")    

                    else:
                        if data3[str(ctx.author.id)]['Item3'] == []:
                            data3[str(ctx.author.id)]['Item3'].append(item)
                            data[str(ctx.user.id)]["Inventory"].remove(item)
                            data3[str(ctx.author.id)]['Item3p'] += price

                            with open("market.json", 'w', encoding='utf-8') as file3:
                                json.dump(data3, file3)   

                            with open("account.json", 'w', encoding='utf-8') as file:
                                json.dump(data, file)

                            await ctx.send("Item is successfuly displayed in global shop")    
                        else:
                            if data3[str(ctx.author.id)]['Item4'] == []:
                                data3[str(ctx.author.id)]['Item4'].append(item)
                                data[str(ctx.user.id)]["Inventory"].remove(item)
                                data3[str(ctx.author.id)]['Item4p'] += price

                                with open("market.json", 'w', encoding='utf-8') as file3:
                                    json.dump(data3, file3)   
                                
                                with open("account.json", 'w', encoding='utf-8') as file2:
                                    json.dump(data, file)

                                await ctx.send("Item is successfuly displayed in global shop")    

                            else:
                                await ctx.send("You have filed all the slots, can't input more than 4 items")    
    else:
        await ctx.send("You don't have that item")

@_bot.slash_command(descripton="Remove an item from market")
async def remove_item(ctx, item):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Removing item from market command", value="You can use this command to remove any item from market.")
    await send_first_time_message(ctx, "remove_item", embed)   

    await markett(ctx)
    with open("market.json", 'r', encoding='utf-8') as file3:
        data3 = json.load(file3)

    if item in data3[str(ctx.author.id)]['Item1']:
        data3[str(ctx.author.id)]['Item1'].clear()
        data3[str(ctx.author.id)]['Item1p'] * 0

        await ctx.send(f"You have remove {item} from market")
    
    elif item in data3[str(ctx.author.id)]['Item2']:
        data3[str(ctx.author.id)]['Item2'].clear()
        data3[str(ctx.author.id)]['Item2p'] * 0    
        await ctx.send(f"You have remove {item} from market")      
    
    elif item in data3[str(ctx.author.id)]['Item3']:
        data3[str(ctx.author.id)]['Item3'].clear()
        data3[str(ctx.author.id)]['Item3p'] * 0      
        await ctx.send(f"You have remove {item} from market")
    elif item in data3[str(ctx.author.id)]['Item4']:
        data3[str(ctx.author.id)]['Item4'].clear()
        data3[str(ctx.author.id)]['Item4p'] * 0    
        await ctx.send(f"You have remove {item} from market")
    
    with open('market.json', 'w') as data3:
        json.dump(data3, file3)
           
async def markett(user):
    with open('market.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Item1'] = []
        data[str(user.id)]['Item2'] = []
        data[str(user.id)]['Item3'] = []
        data[str(user.id)]['Item4'] = []
        data[str(user.id)]['Item1p'] = 0
        data[str(user.id)]['Item2p'] = 0
        data[str(user.id)]['Item3p'] = 0
        data[str(user.id)]['Item4p'] = 0

    with open('market.json', 'w') as f:
        json.dump(data, f)
    
    return True


component_list = ['Screws', 'Fighter exoskeleton', 'Wires', 'Mech gun', 'Exoskeleton armour plate', 'Titanium fighter system', 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190]

@_bot.slash_command(description="Find items to create robot")
async def find(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Item finding command", value="This command can be used to find items to build a /robot. Some times you get nerd coins instead of items used for robot. you can also /upgrade your robot after collecting necessary items.")
    await send_first_time_message(ctx, "find", embed)   
    places = ["Laboratory", "Factory", "Garbage", "Construction site", "Power plant", "Fields", "Abondened house", "Library", "Electronics workshop", "Cyber cafe", "Engineer's desk", "Scrapyard"]
    place = random.choice(places)
    weights = [1]*6 + [10]*20
    thing = random.choices(component_list, weights=weights, k=1)[0]

    with open('account.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

    if type(thing) == int:
        await ctx.send(f"You found {thing} <:nerd_coin:992265892756979735> in {place}")
        data[str(ctx.author.id)]["Bank"] += thing

    else:
        await ctx.send(f"You found {thing} in {place}")
        data[str(ctx.author.id)]["Inventory"].append(thing)

    with open('account.json', 'w') as file:
        json.dump(data, file)


async def robo(user):
    with open('robot.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Health'] = 100
        data[str(user.id)]['Armour'] = 0
        data[str(user.id)]['Gun'] = 0

    
    with open('robot.json', 'w') as f:
        json.dump(data, f)
    
    return True

@_bot.slash_command(description="Do a livestream to earn money if you have necessary items")
@commands.cooldown(1, 1800, commands.BucketType.user)
async def stream(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Streaming command", value="If you have an computer, microphone, headphone, you can stream to earn money. The cooldown is of 30 minutes.")
    await send_first_time_message(ctx, "stream", embed)   
    
    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
    money = random.choice(5000)

    if any(computer in data[str(ctx.user.id)]['Inventory'] for computer in computers):
        if "Headphones 🎧" in data[str(ctx.user.id)]['Inventory']:
            if "Microphone 🎙️" in data[str(ctx.user.id)]['Inventory']:
                embed = disnake.Embed(color = random.choice(colors))
                embed.add_field(name="Livestream", value=f"You have done an livestream and have earned {money} <:nerd_coin:992265892756979735>")
                data[str(ctx.user.id)]['Bank'] += money

                with open("account.json", 'w', encoding='utf-8') as file:
                    json.dump(data, file)

                await ctx.send(embed)
            
            else:
                await ctx.send("You need microphone for livestream.")
        else:
            await ctx.send("You need headphones for livestream.")
    else:
        await ctx.send("You need a computer to do livestream.")

@stream.error
async def stream_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tim = datetime.timedelta(seconds = error.retry_after)
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name='Command on cooldown', value=f"Wait for **{tim}** before running this command again")
        await ctx.send(embed=embed) 

@_bot.slash_command(description="Sell all items in your inventory")
async def sell_all(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Sell inventory command", value="With this command you can sell all items in your inventory.")
    await send_first_time_message(ctx, "sell_all", embed)  

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Selling all items command", value="Yuu can use this command to sell everything in your inventory.")
    await send_first_time_message(ctx, "sell_all", embed) 

    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open("shop.json", 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)


    inventory = data[str(ctx.user.id)]["Inventory"]
    total_price = 0
    
    if inventory is not None:
        for item in inventory:
            item_price = data2[item]['price'] - 5000  
            total_price += item_price
            inventory.remove(item)

        data[str(ctx.user.id)]["Bank"] += total_price

        with open("account.json", 'w') as file:
            json.dump(data, file)

        await ctx.send(f"Successfully sold all items in your inventory for {total_price} <:nerd_coin:992265892756979735>.")
    
    else:
        await ctx.send("Your inventory is empty")

@_bot.slash_command(description="Remove your account, clear your balance, job, inventory, geek coins.")
async def delete_account(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Account deletion command", value="With this command you can delete your balance, job, inventory and geek coins. Remember, after deleting it you can retrieve your progress back.")
    await send_first_time_message(ctx, "delete_account", embed)   
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    data[str(ctx.author.id)]["Balance"] *= 0
    data[str(ctx.author.id)]["Inventory"].clear()
    data[str(ctx.author.id)]["Job"].clear()
    data[str(ctx.author.id)]["Crypto"] *= 0

    with open('account.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)

    await ctx.send("You have removed your account")

@_bot.slash_command(description="Use your phone to call, this gives you a random tip.")
async def call(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Tip command", value="You can use this command to get a random tip of using this bot, only if you have a phone.")
    await send_first_time_message(ctx, "call", embed)   
    with open("account.json" , 'r', encoding='utf-8') as file:
        data = json.load(file)

    tips = ["Use AI software to double your XP earnings.", "Use antivirus to protect yourself from malware, spyware and ransomware attacks.", "Try running /find command in an interval of one hour to get better items.", "Keep tracking /rates for the best amount of crypto currecy and the best time to sell them and earn money.", "Spamming won't help in increasing your level.", "Never put all your money in /fight.", "Keep monitoring your /computer.", "Sometimes /attack can backfire on you and you can lose your money.", "/explore in an interval of approximately two hours to find great places to /mine.", "/pay your /loan in three days or else it may result in losing everything, if you cant pay your loan in three days and you know that, then try getting a smaller amount of loan.", "Never forget to collect your /monthly, /daily, /weekly nerd coins.", "/computer has many ways to earn money, you can make apps, websites and even discord bot to earn money. you can stream as well.", "A laptop is used to collect geek coins, you can redeem them to nerd coins.", "Never think of inputting something offensive in /report.", "The items you have in your inventory, and you /assemble your computer with them, those items are in your /computer.", "buy windows 10 to protect your pc better.", "Buy kali linux to create awesome softwares that have less chances of failing."]
    tip = random.choice(tips)
    if "Iphone X <:IphoneX:987624956353462312>" or "Smartphone 📱" in data[str(ctx.author.id)]["Inventory"]:
        embed = disnake.Embed(color = random.choice(colors))
        embed.add_field(name = "tip", value=tip)
        await ctx.send(embed=embed)
    else:
        await ctx.send("You need a phone to call.")


@_bot.slash_command(description="Build your robot")
async def robot(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Robot building command", value="You can use this command to build your own robot and then /fight with other user's robot. To build a robot you need three necessary items, which are wires, screws, fighter exoskeleton. These items appear in the server randomly. You need to keep track in order to obtain them. To fight other users, they need to have a robot too. To upgrade your robot you need to use /upgrade.")
    await send_first_time_message(ctx, "robot", embed)   

    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    if "Fighter Robot 🤖" not in data[str(ctx.author.id)]["Inventory"]:
        if "Wires" in data[str(ctx.author.id)]["Inventory"]:
            if "Screws" in data[str(ctx.author.id)]["Inventory"]:
                if "Fighter exoskeleton" in data[str(ctx.author.id)]["Inventory"]:
                    embed = disnake.Embed(color = random.choice(colors))
                    data[str(ctx.author.id)]["Inventory"].append("Fighter Robot 🤖")
                    await robo(ctx)
                    with open('account.json', 'w') as file:
                        json.dump(data, file)


                    embed.add_field(name="Congrats! you have created a robot now you can /fight with someone who also has robot.")
                    await ctx.send(embed = embed)
                else:
                    await ctx.send("You need fighter exoskeleton")
            
            else:
                await ctx.send("You need screws")

        else:
            await ctx.send("You need wires")

    else:
        await ctx.send("You already have a robot")
    
class Upgrade(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__(timeout=None)

        self.member = member

    @disnake.ui.button(label="Upgrade health", style=disnake.ButtonStyle.green)
    async def h(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        with open('robot.json', 'r', encoding='utf-8') as f2:
            file2 = json.load(f2)
        

        if "Titanium fighter system" not in file[str(interaction.user.id)]['Inventory']:
            file2[str(interaction.user.id)]['Health'] += 50
            file[str(interaction.user.id)]['Inventory'].remove('Titanium fighter system')
            with open('robot.json', 'w') as f:
                json.dump(f2, file2)

            with open('account.json', 'w') as f:
                json.dump(file, f)
            
            await interaction.response.send_message("Congrats! you have upgraded your robot and have gained 50+ health")
        else:
            await interaction.response.send_message("You need an Titanium fighter system for this upgrade")
    

    @disnake.ui.button(label="Upgrade armour", style=disnake.ButtonStyle.green)
    async def h(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        with open('robot.json', 'r', encoding='utf-8') as f2:
            file2 = json.load(f2)
        

        if "Exoskeleton armour plate" not in file[str(interaction.user.id)]['Inventory']:
            file2[str(interaction.user.id)]['Armour'] += 50
            file[str(interaction.user.id)]['Inventory'].remove('Exoskeleton armour plate')
            with open('robot.json', 'w') as f:
                json.dump(f2, file2)

            with open('account.json', 'w') as f:
                json.dump(file, f)

            await interaction.response.send_message("Congrats! you have upgraded your robot and have gained 50+ armour")
        else:
            await interaction.response.send_message("You need an Exoskeleton armour plate for this upgrade")

    @disnake.ui.button(label="Add gun", style=disnake.ButtonStyle.green)
    async def h(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        with open('robot.json', 'r', encoding='utf-8') as f2:
            file2 = json.load(f2)
        

        if "Mech gun" not in file[str(interaction.user.id)]['Inventory']:
            file2[str(interaction.user.id)]['Gun'] += 1
            file[str(interaction.user.id)]['Inventory'].remove('Mech gun')
            with open('robot.json', 'w') as f:
                json.dump(f2, file2)

            with open('account.json', 'w') as f:
                json.dump(file, f)

            await interaction.response.send_message("Congrats! you have upgraded your robot and have added a gun to your robot")
        else:
            await interaction.response.send_message("You need an Mech gun for this upgrade")



@_bot.slash_command(description="Upgrade your robot")
async def upgrade(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Upgrade robot command", value="You can use this command to add an upgrade to your robot. There are three types of upgrades, health upgrade, armour upgrade and gun upgrade. You need an titanium fighter system in order to upgrade health, for armour you need exoskeleton armour, for gun you need mech gun. All these items randomly appear in the server.")
    await send_first_time_message(ctx, "upgrade", embed)   
    
    await ctx.send(view=Upgrade())
    

class Fighter:
    def __init__(self, name, hp, armor):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.armor = armor
        self.moves = {
            "Punch": 10,
            "Kick": 20,
            "Shoot": 30
        }

    def take_damage(self, damage):
        damage -= self.armor
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

@_bot.slash_command(description="Fight against another user's robot")
async def fight(ctx, opponent: disnake.Member, money: int):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Fight command", value="This command is used to fight with someone if you have a robot and your opponent has a robot too. According to upgrades your robot's health, armour, attack is effected. Robots fight automatically after starting the fight. You need to put some money on fight and whoever wins the fight gets that money.")
    await send_first_time_message(ctx, "fight", embed)  
    
    with open('account.json', 'r', encoding='utf-8') as f1:
        data = json.load(f1)

    with open('robot.json', 'r', encoding='utf-8') as f:
        robots = json.load(f)

    if str(opponent.id) not in robots:
        await ctx.send(f"{opponent.mention} does not have a robot.")
        return
    
    with open('robot.json', 'r', encoding='utf-8') as f:
        robots = json.load(f)

    if str(ctx.author.id) not in robots:
        await ctx.send("You need to create a robot first with /robot.")
        return

    user_robot = robots[str(ctx.author.id)]
    opponent_robot = robots[str(opponent.id)]

    user_attack = random.choice(["slash", "punch", "kick"])
    opponent_attack = random.choice(["slash", "punch", "kick"])

    if "Exoskeleton armour plate" in user_robot["Upgrades"]:
        user_robot["Armour"] += 50
    if "Mech gun" in user_robot["Upgrades"]:
        user_attack = "shoot"
    if "Titanium fighter system" in user_robot["Upgrades"]:
        user_robot["Health"] += 50

    if "Exoskeleton armour plate" in opponent_robot["Upgrades"]:
        opponent_robot["Armour"] += 50
    if "Mech gun" in opponent_robot["Upgrades"]:
        opponent_attack = "shoot"
    if "Titanium fighter system" in opponent_robot["Upgrades"]:
        opponent_robot["Health"] += 50

    user_damage = random.randint(10, 20)
    opponent_damage = random.randint(10, 20)

    if user_attack == "slash":
        opponent_robot["Health"] -= user_damage
    elif user_attack == "punch":
        opponent_robot["Health"] -= user_damage // 2
        opponent_robot["Armour"] -= user_damage // 2
    elif user_attack == "kick":
        opponent_robot["Health"] -= user_damage // 3
        opponent_robot["Armour"] -= user_damage // 3 * 2
    elif user_attack == "shoot":
        opponent_robot["Health"] -= user_damage // 2

    if opponent_attack == "slash":
        user_robot["Health"] -= opponent_damage
    elif opponent_attack == "punch":
        user_robot["Health"] -= opponent_damage // 2
        user_robot["Armour"] -= opponent_damage // 2
    elif opponent_attack == "kick":
        user_robot["Health"] -= opponent_damage // 3
        user_robot["Armour"] -= opponent_damage // 3 * 2
    elif opponent_attack == "shoot":
        user_robot["Health"] -= opponent_damage // 2

    winner = None
    if user_robot["Health"] <= 0 and opponent_robot["Health"] <= 0:
        winner = "tie"
    elif user_robot["Health"] <= 0:
        winner = opponent
        data[str(opponent.id)]["Bank"] += money
        data[str(ctx.author.id)]["Bank"] -= money
    elif opponent_robot["Health"] <= 0:
        winner = ctx.author
        data[str(opponent.id)]["Bank"] -= money
        data[str(ctx.author.id)]["Bank"] += money


    with open('robot.json', 'w', encoding='utf-8') as f:
        json.dump(robots, f)
    
    with open('account.json', 'w', encoding='utf-8') as f1:
        json.dump(data, f1)


    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(value=f"{winner} is the winner of this match!")
    await ctx.send(embed=embed)

api_key = "AIzaSyDH3KqiosNsnrBzklMHcJSH_C7l6IfBOow"
search_engine_id = "244919d5786ae46f0"

import requests

@fun.sub_command(description="Get a joke")
async def joke(ctx):
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        joke = response.json()
        setup = joke['setup']
        punchline = joke['punchline']
        await ctx.send(f'{setup}\n\n{punchline}')


@fun.sub_command(description="Get bot's current latency")
async def ping(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Ping command", value="When the bot is running slow you can use this command to monitor latency of the bot and use it at the right time.")
    await send_first_time_message(ctx, "ping", embed)    

    latency = _bot.latency * 1000  
    await ctx.send(f'Pong! Latency: {latency:.2f}ms')

@fun.sub_command(description="Get a cat image")
async def cat(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Cat image command", value="A fine command can be used to get an random cat image from an huge cat image database")
    await send_first_time_message(ctx, "cat", embed)    
    
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as response:
            data = await response.json()
            await ctx.send(data[0]['url'])

@fun.sub_command(description="Get a dog image")
async def dog(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Dog image command", value="A fine command can be used to get an random dog image from an huge dog image database")
    await send_first_time_message(ctx, "topic", embed)    

    async with aiohttp.ClientSession() as session:
        async with session.get("https://dog.ceo/api/breeds/image/random") as response:
            data = await response.json()
            await ctx.send(data['message'])

@fun.sub_command(description="Get a quote")
async def quote(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Quote command", value="This command can be used to get a quote and also the person who said that quote")
    await send_first_time_message(ctx, "quote", embed)    

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.quotable.io/random") as response:
            data = await response.json()
            await ctx.send(f"{data['content']} - {data['author']}")

@fun.sub_command(description="Searches for and displays images based on user input.")
async def image(ctx, query: str):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Image search command", value="This command can search an image from the text you type, it uses google search API to search images related to that query.")
    await send_first_time_message(ctx, "image", embed)    

    async with aiohttp.ClientSession() as session:
        params = {'key': api_key, 'cx': search_engine_id, 'q': query, 'searchType': 'image'}
        async with session.get('https://www.googleapis.com/customsearch/v1', params=params) as response:
            data = await response.json()

    if 'items' in data:
        image_url = data['items'][0]['link']
        await ctx.send(f"Here's an image of {query}: {image_url}")
    else:
        await ctx.send(f"Sorry, I couldn't find any images for {query}")


@fun.sub_command(description="Create and vote on polls.")
async def poll(ctx, question: str, option1: str, option2: str, option3=None,
               option4=None, option5=None, option6=None, option7=None, option8=None, option9=None, option10=None):
    
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Voting poll command", value="This command can be used to create a voting poll, you must pass two necessary voting options and 8 optional options.")
    await send_first_time_message(ctx, "poll", embed)    

    options = [option1, option2]
    optional_options = [option3, option4, option5, option6, option7, option8, option9, option10]
    for option in optional_options:
        if option is not None:
            options.append(option)

    # Create the poll message
    poll_message = f"**{question}**\n\n"
    for i, option in enumerate(options):
        poll_message += f"{i+1}. {option}\n"

    # Send the poll message
    message = await ctx.send(poll_message)

    # Add reaction choices to the poll message
    for i in range(len(options)):
        await message.add_reaction(f"{i+1}\u20e3")

    # Define a check to filter out reactions from the bot and only count user reactions
    def check_reaction(reaction, user):
        return not user.bot and reaction.message == message

    # Wait for reactions and count the votes for each option
    votes = [0] * len(options)
    while True:
        reaction, user = await ctx.bot.wait_for('reaction_add', check=check_reaction)

        # If the user removed their reaction, subtract their vote
        if reaction.emoji in [f"{i+1}\u20e3" for i in range(len(options))]:
            option_index = int(reaction.emoji[:-1]) - 1
            votes[option_index] += 1
        elif reaction.emoji == '❌':
            break

    # Create the results message
    results_message = f"**Poll results for '{question}':**\n\n"
    for i, option in enumerate(options):
        results_message += f"{option}: {votes[i]} vote(s)\n"

    # Send the results message
    await ctx.send(results_message)

@fun.sub_command(description="Show avatar of a user")
async def avatar(ctx, user: disnake.User = None):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Avatar command", value="This command can be used to get avatars as an image file, if any user name is not passed then your avatar would be output.")
    await send_first_time_message(ctx, "avatar", embed)    
    
    if user is None:
        user = ctx.author
    avatar_url = user.avatar.url
    await ctx.send(f'{user.display_name}\'s avatar: {avatar_url}')


@fun.sub_command(description='Rolls a specified number of dice with a specified number of sides.')
async def rolldice(ctx, num_dice: int, num_sides: int):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Dog image command", value="This is a non-profit command to roll multiple dices with multiple number of sides, the more you increase the value the harder the game would be.")
    await send_first_time_message(ctx, "topic", embed)    
    
    if num_dice <= 0 or num_dice > 100 or num_sides <= 0 or num_sides > 100:
        await ctx.send('Please enter valid numbers between 1 and 100.')
        return
    rolls = []
    for _ in range(num_dice):
        roll = random.randint(1, num_sides)
        rolls.append(roll)
    total = sum(rolls)
    result = ', '.join(str(r) for r in rolls)
    await ctx.send(f"You rolled {result}. Total: {total}")

async def mining(ctx):
    with open('mining.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(ctx.user.id) in data:
        return False
    else:
        data[str(ctx.user.id)] = {}
        data[str(ctx.user.id)]['explored'] = []
        data[str(ctx.user.id)]['elements'] = []
        
    
    with open('mining.json', 'w') as f:
        json.dump(data, f)
    
    return True    
        
@_bot.slash_command(description="Start the mining career")
async def start_mine(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Start mining command", value="You can start mining career using this command. You just need to have 20 million nerd coins in order to start your minging career, and then your mining account will be opened. Mining is profitable business and can be used in building rockets to get into space adventure and also sell the mined elements to earn a large amount of money. After starting your mining career you need to use /explore command in order to explore places to mine. The next step is to use /explore.")
    await send_first_time_message(ctx, "start_mine", embed) 

    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data[str(ctx.user.id)]["Bank"] >= 20000000:
        await mining(ctx)
        await ctx.send("You have started your mining career!")
    else:
        await ctx.send("You need at least 20 million Nerd coins")

@_bot.slash_command(description="Explore areas in order to find mining places")
async def explore(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Exploration command", value="This command can be used to explore places to mine. There are few places with different elements to get. After exploring you can use /explored to list the explored places and then use /mine command to start mining on those places and get elements.")
    await send_first_time_message(ctx, "explore", embed) 

    with open("mining.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    with open("places.json", 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)
    
    basic_places = ["new", "nonew"]
    final_basic_place = random.choice(basic_places)
    if final_basic_place == "new":
        if str(ctx.user.id) not in data:
            await ctx.send("First start your mining career using /start_mine")
        else:
            p = random.choice(list(data2))
            
            if p not in data[str(ctx.user.id)]["explored"]:
                embed = disnake.Embed(color=random.choice(colors))
                embed.add_field(name=f"Special area explored!", value=f"You have explored {p}")
                data[str(ctx.user.id)]["explored"].append(p)
                await ctx.send(embed=embed)
            
                with open("mining.json", 'w') as file:
                    json.dump (data, file)
            else:
                await ctx.send("Uh oh you re-explored a place you have already explored")
               
                
    else:
        if str(ctx.user.id) not in data:
            await ctx.send("First start your mining career using /start_mine")
        else:
            coords = ["32 08’59.96N, 110 50’09.03W", "27°22’50.10N, 33°37’54.62E", "4°17’21.49S 31°23’46.46E", "33.747252, -112.633853", "-33.836379, 151.080506", "50° 0’38.20N 110° 6’48.32W", "45° 7’25.87″N 123° 6’48.97″W", "-33.867886, -63.987", "41.303921, -81.901693", "40.452107, 93.742118", "37.563936, -116.85123", "43.645074, -115.993081", "38°29’0.16N 109°40’52.80W", "37.629562, -116.849556", "39.623119, -107.635353", "69.793° N, 108.241° W", "37.401573, -116.867808", "65.476721, -173.511416", "19°56’56.96S 69°38’1.83W", "40.458148, 93.393145", "30.541634, 47.825445", "37°39’16.06S 68°10’16.42W", "-25.344375, 131.034401", "38.265652, 105.9517", "20°56’15.47″S, 164°39’30.56″E", "35.027185, -111.022388", "6°53’53.00″ S 31°11’15.40″ E", "12°22’13.32″N, 23°19’20.18″E", "44.525049, -110.83819", "52.479750, 62.185667", "21.124039, -11.397509", "51.577718, -1.566620", "45.408080, -123.007866", "69.793000, -108.241000", "44° 14′ 39.38″, 7° 46′ 11.05″", "-17° 55′ 31.84″, 25° 51′ 29.60″"]
            c = random.choice(coords)
            if c not in data[str(ctx.user.id)]["explored"]:
                data[str(ctx.user.id)]["explored"].append(c)
                embed = disnake.Embed(color=random.choice(colors))
                embed.add_field(name=f"New area explored!", value=f"You have explored coordinate {c}")
                embed.set_footer(text="Coordinate is real, searchable on google maps.")
                await ctx.send(embed=embed)
        
                with open("mining.json", 'w') as file:
                    json.dump (data, file)
            else:
                await ctx.send("Uh oh you re-explored a place you have already explored")

@_bot.slash_command(description="Get the places you have explored.") 
async def explored(ctx):
    
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Explored location listing command", value="This command can be used to list all the places you have explored for mining. You can /explore places, /mine in those places and /sell_element which are collected by mining.")
    await send_first_time_message(ctx, "explored", embed) 

    with open("mining.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    embed = disnake.Embed(title=f"{ctx.user.name}'s explored places")
    iv = '\n'.join(data[str(ctx.user.id)]['explored'])
    embed.add_field(name=f"----------", value=iv)
    await ctx.send(embed=embed)

@_bot.slash_command(description="Mine in an place")
async def mine(ctx, place_name):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Mining command", value="If you have explored any place to mine, you can mine in that place. The name suggests what element you will get, just remember to type exact name (including capital letter). use /explored to list all places or /explore them. you can also /sell_element.")
    await send_first_time_message(ctx, "mine", embed) 

    coords = ["32 08’59.96N, 110 50’09.03W", "27°22’50.10N, 33°37’54.62E", "4°17’21.49S 31°23’46.46E", "33.747252, -112.633853", "-33.836379, 151.080506", "50° 0’38.20N 110° 6’48.32W", "45° 7’25.87″N 123° 6’48.97″W", "-33.867886, -63.987", "41.303921, -81.901693", "40.452107, 93.742118", "37.563936, -116.85123", "43.645074, -115.993081", "38°29’0.16N 109°40’52.80W", "37.629562, -116.849556", "39.623119, -107.635353", "69.793° N, 108.241° W", "37.401573, -116.867808", "65.476721, -173.511416", "19°56’56.96S 69°38’1.83W", "40.458148, 93.393145", "30.541634, 47.825445", "37°39’16.06S 68°10’16.42W", "-25.344375, 131.034401", "38.265652, 105.9517", "20°56’15.47″S, 164°39’30.56″E", "35.027185, -111.022388", "6°53’53.00″ S 31°11’15.40″ E", "12°22’13.32″N, 23°19’20.18″E", "44.525049, -110.83819", "52.479750, 62.185667", "21.124039, -11.397509", "51.577718, -1.566620", "45.408080, -123.007866", "69.793000, -108.241000", "44° 14′ 39.38″, 7° 46′ 11.05″", "-17° 55′ 31.84″, 25° 51′ 29.60″"]
    
    with open('mining.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  
    
    with open('places.json', 'r', encoding='utf-8') as file2:
        cool_places = json.load(file2)  
        
    if place_name in cool_places:
        element = cool_places[place_name]['element']
        price = cool_places[place_name]['price']
        data[str(ctx.user.id)]['elements'].append(element)
        
        with open('mining.json', 'w') as f:
            json.dump(data, f)
        
        await ctx.send(f"You have successfully mined {element} in {place_name}! It sells for {price} nerd coins.")
    
    elif place_name in coords:
        elements = ["Iron", "Copper", "Sodium"]
        element = random.choice(elements)
        data[str(ctx.user.id)]['elements'].append(element)
        
        with open('mining.json', 'w') as f:
            json.dump(data, f)
        
        await ctx.send(f"You have successfully mined {element} in {place_name}! It sells for a random price in range of 10k nerd coins.")
    
@_bot.slash_command(description="Sell an element")
async def sell_element(ctx, element_name: str):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Sell elements command", value="You can sell your collected elements using this command, just remember to use the exact name of element (including capital letter). You can get list of your elements using /elements. Only copper, iron and sodium have a random price in range of 10k nerd coins. You can /explore places and then /mine in those places to collect elements.")
    await send_first_time_message(ctx, "sell_element", embed) 

    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    with open('mining.json', 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    if element_name == "Jade":
        data[str(ctx.author.id)]["Bank"] += 12000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 12k nerd coins")
    
    elif element_name == "Crystal":
        data[str(ctx.author.id)]["Bank"] += 80000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 80k nerd coins")
    
    elif element_name == "Emerald":
        data[str(ctx.author.id)]["Bank"] += 18000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 18k nerd coins")
    
    elif element_name == "Silver":
        data[str(ctx.author.id)]["Bank"] += 50000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 50k nerd coins")
    
    elif element_name == "Sapphire":
        data[str(ctx.author.id)]["Bank"] += 24000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 24k nerd coins")
    
    elif element_name == "Diamond":
        data[str(ctx.author.id)]["Bank"] += 60000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 60k nerd coins")

    elif element_name == "Ruby":
        data[str(ctx.author.id)]["Bank"] += 32000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 32k nerd coins")

    elif element_name == "Topaz":
        data[str(ctx.author.id)]["Bank"] += 15000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 15k nerd coins")

    elif element_name == "Gold":
        data[str(ctx.author.id)]["Bank"] += 45000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 45k nerd coins")

    elif element_name == "Platinum":
        data[str(ctx.author.id)]["Bank"] += 70000
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for 70k nerd coins")
    
    elif element_name == "Copper":
        price = random.randrange(10000)
        data[str(ctx.author.id)]["Bank"] += price
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for {price} nerd coins")

    elif element_name == "Iron":
        price = random.randrange(10000)
        data[str(ctx.author.id)]["Bank"] += price
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for {price} nerd coins")

    elif element_name == "Sodium":
        price = random.randrange(10000)
        data[str(ctx.author.id)]["Bank"] += price
        data2[str(ctx.author.id)]["elements"] -= element_name

        await ctx.send(f"You have sold {element_name} for {price} nerd coins")
    
    else:
        await ctx.send("That's not a valid item name, please use the exact item name from by using /elements command.")
    
    with open('account.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)

    with open('mining.json', 'w', encoding='utf-8') as file2:
        json.dump(data2, file2)

@_bot.slash_command(descripton="Get list of collected elements")
async def elements(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Element listing command", value="You can get a list of all collected elements using this command. If you do not have any element or haven't started your mining career, you can do it using /start_mine. To mine elements you can first /explore places and then /mine in those places.")
    await send_first_time_message(ctx, "elements", embed) 
    
    with open('mining.json', 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    embed = disnake.Embed(title=f"{ctx.user.name}'s Elements")
    iv = '\n'.join(data2[str(ctx.user.id)]['elements'])
    embed.add_field(name=f"----------", value=iv)
    await ctx.send(embed=embed)



@_bot.slash_command(description="Disassemble an computer and take out it's parts, you can then sell them")
async def disassemble(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Disassemble computer command", value="If you have an computer and you want to disassemble it and get all the components out of it you can use this command.")
    await send_first_time_message(ctx, "disassemble", embed) 

    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]

    if any(computer in data[str(ctx.user.id)]['Inventory'] for computer in computers):
        data[str(ctx.user.id)]["Inventory"].append("Membrane Keyboard ⌨️")
        data[str(ctx.user.id)]["Inventory"].append("Monitor 🖥️")
        data[str(ctx.user.id)]["Inventory"].append("10 gb ram 💾")
        if "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾" in data[str(ctx.user.id)]['Inventory']: 
            data[str(ctx.user.id)]["Inventory"].remove("Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾")
        elif "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>" in data[str(ctx.user.id)]['Inventory']:
            data[str(ctx.user.id)]["Inventory"].remove("Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>")
        elif "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾" in data[str(ctx.user.id)]['Inventory']: 
            data[str(ctx.user.id)]["Inventory"].remove("Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾")
        elif "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>" in data[str(ctx.user.id)]['Inventory']:
            data[str(ctx.user.id)]["Inventory"].remove("Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>")
        elif "Computer🖱️🖥️⌨️💾" in data[str(ctx.user.id)]['Inventory']:
            data[str(ctx.user.id)]["Inventory"].remove("Computer🖱️🖥️⌨️💾")
        elif "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>" in data[str(ctx.user.id)]['Inventory']:
            data[str(ctx.user.id)]["Inventory"].remove("Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>")


        with open("account.json", 'w') as file:
            json.dump(data, file)

        await ctx.send("You have disassembled your computer, check your inventory.")
    else:
        await ctx.send("You don't have an computer how are you supposed to disassemble an void?")

@_bot.slash_command(description="Sell an item from your inventory")
async def sell(ctx, item_code: str):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Selling command", value="You can sell your items using this command. When selling your item, it's value would 5000 nerd coins decreased as it is an second hand item.")
    await send_first_time_message(ctx, "sell", embed) 

    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open("shop.json", 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    for item in data2:
        if item in data[str(ctx.user.id)]["Inventory"]:
            if item_code == data2[item]['code']:
                data[str(ctx.user.id)]["Inventory"].remove(item)
                p = data2[item]['price'] - 5000
                data[str(ctx.user.id)]["Bank"] += p
                
                with open("account.json", 'w') as file:
                    json.dump(data, file)

                await ctx.send(f"You have sold your item for {data2[item]['price'] - 5000} Nerd coins")
            else:
                pass
        else:
            pass

@_bot.slash_command(description="Get rates of crypto currency")
async def rates(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Rates command", value="This is rates command, this command gives the price of buyable-sellable crypto currencies in this bot. The price frequently changes according to the real time data. This command can also be used to know the codes of crypto currency which you can use while buying crypto using /buy_crypto <code>")
    await send_first_time_message(ctx, "rates", embed)       
    
    price = cryptocompare.get_price(['BTC', "ADA", "DOT", "RVN", "DOGE", "UNI", "SOL", "AVAX", "XRP", "BNB", "LTC", "MATIC"], ['INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR'])
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Bitcoin (btc)", value=price['BTC']["INR"])
    embed.add_field(name="Cordana (ada)", value=price['ADA']["INR"])
    embed.add_field(name="Polkadot (dot)", value=price['DOT']["INR"])
    embed.add_field(name="Ravencoin (rvn)", value=price['RVN']["INR"])
    embed.add_field(name="Dogecoin (doge)", value=price['DOGE']["INR"])
    embed.add_field(name="Uniswap (uni)", value=price['UNI']["INR"])
    embed.add_field(name="Solana (sol)", value=price['SOL']["INR"])
    embed.add_field(name="Avalanche (avax)", value=price['AVAX']["INR"])
    embed.add_field(name="XRP (xrp)", value=price['XRP']["INR"])
    embed.add_field(name="Binance coin (bnb)", value=price['BNB']["INR"])
    embed.add_field(name="LTC (ltc)", value=price['LTC']["INR"])
    embed.add_field(name="Polygon (matic)", value=price['MATIC']["INR"])
    await ctx.send(embed=embed)

async def crypt(ctx):
    with open('crypto.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(ctx.id) in data:
        return False
    else:
        data[str(ctx.id)] = {}
        data[str(ctx.id)]['btc'] = 0
        data[str(ctx.id)]['ada'] = 0
        data[str(ctx.id)]['dot'] = 0
        data[str(ctx.id)]['rvn'] = 0
        data[str(ctx.id)]['doge'] = 0
        data[str(ctx.id)]['uni'] = 0
        data[str(ctx.id)]['sol'] = 0
        data[str(ctx.id)]['avax'] = 0
        data[str(ctx.id)]['xrp'] = 0
        data[str(ctx.id)]['bnb'] = 0
        data[str(ctx.id)]['ltc'] = 0
        data[str(ctx.id)]['matic'] = 0
    
    with open('crypto.json', 'w') as f:
        json.dump(data, f)

@_bot.slash_command(description="Buy an crypto coin")
async def buy_crypto(ctx, crypto_code: str):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Buying crypto command", value="First you can use /rates command in order to get crypto currency's codes so that you can input those codes and can buy crypto currency. Cryptos are another way of earning money and also redeeming them. You can check your crypto balance using /crypto_bal and can redeem them using /redeem_crypto. Crypto values frequently keep changing according to real time data.")
    await send_first_time_message(ctx, "buy_crypto", embed)  

    await crypt(ctx)
    
    price = cryptocompare.get_price(['BTC', "ADA", "DOT", "RVN", "DOGE", "UNI", "SOL", "AVAX", "XRP", "BNB", "LTC", "MATIC"], ['INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR'])
    
    with open('crypto.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    with open('account.json', 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    if crypto_code == 'btc':
        if data2[str(ctx.user.id)]["Bank"] > price["BTC"]["INR"]:
            data[str(ctx.user.id)]['btc'] += 1
            await ctx.send("You bought one Bitcoin")
            data2[str(ctx.user.id)]["Bank"] -= price["BTC"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'ada':
        if data2[str(ctx.user.id)]["Bank"] > price["ADA"]["INR"]:
            data[str(ctx.user.id)]['ada'] += 1
            await ctx.send("You bought one Cordana crypto")
            data2[str(ctx.user.id)]["Bank"] -= price["ADA"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")


    elif crypto_code == 'dot':
        if data2[str(ctx.user.id)]["Bank"] > price["DOT"]["INR"]:
            data[str(ctx.user.id)]['dot'] += 1
            await ctx.send("You bought one Polkadot crypto")
            data2[str(ctx.user.id)]["Bank"] -= price["DOT"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'rvn':
        if data2[str(ctx.user.id)]["Bank"] > price["RVN"]["INR"]:
            data[str(ctx.user.id)]['rvn'] += 1
            await ctx.send("You bought one Ravencoin")
            data2[str(ctx.user.id)]["Bank"] -= price["RVN"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'doge':
        if data2[str(ctx.user.id)]["Bank"] > price["DOGE"]["INR"]:
            data[str(ctx.user.id)]['doge'] += 1
            await ctx.send("You bought one Dogecoin")
            data2[str(ctx.user.id)]["Bank"] -= price["DOGE"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'uni':
        if data2[str(ctx.user.id)]["Bank"] > price["UNI"]["INR"]:
            data[str(ctx.user.id)]['uni'] += 1
            await ctx.send("You bought one Uniswap crypto")
            data2[str(ctx.user.id)]["Bank"] -= price["UNI"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'sol':
        if data2[str(ctx.user.id)]["Bank"] > price["SOL"]["INR"]:
            data[str(ctx.user.id)]['sol'] += 1
            await ctx.send("You bought one Solana crypto")
            data2[str(ctx.user.id)]["Bank"] -= price["SOL"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'avax':
        if data2[str(ctx.user.id)]["Bank"] > price["AVAX"]["INR"]:
            data[str(ctx.user.id)]['avax'] += 1
            await ctx.send("You bought one Avalanche crypto")
            data2[str(ctx.user.id)]["Bank"] -= price["AVAX"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'xrp':
        if data2[str(ctx.user.id)]["Bank"] > price["XRP"]["INR"]:
            data[str(ctx.user.id)]['xrp'] += 1
            await ctx.send("You bought one XRP crypto")
            data2[str(ctx.user.id)]["Bank"] -= price["XRP"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'bnb':
        if data2[str(ctx.user.id)]["Bank"] > price["BNB"]["INR"]:
            data[str(ctx.user.id)]['bnb'] += 1
            await ctx.send("You bought one Binance coin")
            data2[str(ctx.user.id)]["Bank"] -= price["BNB"]["INR"]
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'ltc':
        if data2[str(ctx.user.id)]["Bank"] > price["LTC"]["INR"]:
            data[str(ctx.user.id)]['ltc'] += 1
            await ctx.send("You bought one LTC crypto")
            data2[str(ctx.user.id)]["Bank"] -= price["LTC"]["INR"]

            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        else:
            await ctx.send("You don't have enough money")

    elif crypto_code == 'matic':
        if data2[str(ctx.user.id)]["Bank"] > price["MATIC"]["INR"]:
            data[str(ctx.user.id)]['matic'] += 1
            await ctx.send("You bought one Polygon crypto")
            data2[str(ctx.user.id)]["Bank"] -= price["MATIC"]["INR"]
            
            with open('crypto.json', 'w') as file:
                json.dump(data, file)

            with open('account.json', 'w') as file2:
                json.dump(data2, file2)
        
        else:
            await ctx.send("You don't have enough money")

    else:
        await ctx.send("Invalid code, please use /rates to see rates and check the code written write to the name, use it.")

@_bot.slash_command(description="Redeem your crypto coins")
async def redeem_crypto(ctx, crypto_code: str, amount: int):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Redeem crypto command", value="You can redeem your crypto currencies into nerd coins using this command, input the crypto currency's code you want to redeem and amount of crypto you wanna redeem. Remember, the amount should exist in your balance and that crypto too.")
    await send_first_time_message(ctx, "redeem_crypto", embed)  

    await crypt(ctx)

    price = cryptocompare.get_price(['BTC', "ADA", "DOT", "RVN", "DOGE", "UNI", "SOL", "AVAX", "XRP", "BNB", "LTC", "MATIC"], ['INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR', 'INR'])

    with open("crypto.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open("account.json", 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    if data[str(ctx.user.id)][crypto_code] >= amount:
        data[str(ctx.user.id)][crypto_code] -= amount
        data2[str(ctx.user.id)]["Bank"] += price[crypto_code.upper()]['INR']
        await ctx.send(f"You sold one crypto for {price[crypto_code.upper()]['INR']} Nerd coins")

        with open("crypto.json", 'w') as file:
            json.dump(data, file)

        with open("account.json", 'w') as file2:
            json.dump(data2, file2)

    else:
        await ctx.send("You don't have that much crypto")

@_bot.slash_command(description='Get your crypto balance')
async def crypto_bal(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Crypto balance command", value="This command can be used to get your crypto currency balance.")
    await send_first_time_message(ctx, "crypto_bal", embed)  

    await crypt(ctx)
    with open("crypto.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    embed = disnake.Embed(color=random.choice(colors))
 
    embed.add_field(name="Bitcoin", value=data[str(ctx.user.id)]['btc'])
    embed.add_field(name="Cordana", value=data[str(ctx.user.id)]['ada'])
    embed.add_field(name="Polkadot", value=data[str(ctx.user.id)]['dot'])
    embed.add_field(name="Ravencoin", value=data[str(ctx.user.id)]['rvn'])
    embed.add_field(name="Dogecoin", value=data[str(ctx.user.id)]['doge'])
    embed.add_field(name="Uniswap", value=data[str(ctx.user.id)]['uni'])
    embed.add_field(name="Solana", value=data[str(ctx.user.id)]['sol'])
    embed.add_field(name="Avalanche", value=data[str(ctx.user.id)]['avax'])
    embed.add_field(name="XRP", value=data[str(ctx.user.id)]['xrp'])
    embed.add_field(name="Binance coin", value=data[str(ctx.user.id)]['bnb'])
    embed.add_field(name="LTC", value=data[str(ctx.user.id)]['ltc'])
    embed.add_field(name="Polygon", value=data[str(ctx.user.id)]['matic'])    

    await ctx.send(embed=embed)

@_bot.slash_command(description='Get help for commands')
async def help(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Help command", value="Get a list of commands using this command.")
    await send_first_time_message(ctx, "help", embed)  
    await ctx.send(view=Help())

@fun.sub_command(description='Get an topic to chat on')
async def topic(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Topic command", value="This command can be used to get a random topic, just a fun command used to get things to chat about when the chat is dead!")
    await send_first_time_message(ctx, "topic", embed)    

    lines = open("topics.txt", encoding='utf-8').read().splitlines()
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name='Topic', value=random.choice(lines))
    await ctx.send(embed=embed)

@fun.sub_command(description="Get user information")
async def userinfo(ctx, user: disnake.Member):
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name="User information command", value="To get some basic information about any user account including Status, ID and account creation date, PFP. This is a basic utility command.")
        await send_first_time_message(ctx, "userinfo", embed)    

        if user is None:
            color = disnake.Color(value=random.choice(colors))
            em = disnake.Embed(color=color, title=f'User Info: {ctx.user.name}')
            em.add_field(name='Status', value=f'{ctx.user.status}')       
            em.add_field(name='Account Created', value=ctx.message.author.created_at)
            em.add_field(name='ID', value=f'{ctx.user.id}')
            em.set_thumbnail(url=ctx.user.avatar.url)
            await ctx.send(embed=em)
        else:
            color = disnake.Color(value=random.choice(colors))
            em = disnake.Embed(color=color, title=f'User Info: {user.name}')
            em.add_field(name='Status', value=f'{user.status}')       
            em.add_field(name='Account Created', value=user.created_at)
            em.add_field(name='ID', value=f'{user.id}')
            em.set_thumbnail(url=user.avatar.url)
            await ctx.send(embed=em)        

async def learnp(ctx):
    await learning_points(ctx)
    await open_account(ctx)
    with open('learning_points.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    p = data[str(ctx.user.id)]['Physics']
    c = data[str(ctx.user.id)]['Chemistry']
    b = data[str(ctx.user.id)]['Biology']     
    cs =  data[str(ctx.user.id)]['Computer science']
    m = data[str(ctx.user.id)]['Maths']
     
    with open('account.json', 'r', encoding='utf-8') as file:
        data2 = json.load(file)

    if p == 15:
        await ctx.send("You have gained an Physics science degree")
        data2[str(ctx.user.id)]['Inventory'].append("Computer science degree")
        with open('account.json', 'w') as file:
            json.dump(data2, file)


async def log_in(user):
    with open('login.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['OS'] = ["Windows XP"]
        data[str(user.id)]['Programs'] = ["System files"]
    
    with open('login.json', 'w') as f:
        json.dump(data, f)
    
    return True

class Attack(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__(timeout=None)

        self.member = member

    @disnake.ui.button(label="Ransomware", style=disnake.ButtonStyle.red)
    async def ransomware(self, button: disnake.ui.Button, interaction: disnake.Interaction):

        computers = ['Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>', "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]["Inventory"] for computer in computers):
            with open("login.json", 'r', encoding='utf-8') as r:
                f = json.load(r)
            
            if "Ransomware" in f[str(interaction.user.id)]["Programs"]:
                possiblities = ["pc_locked", "pc_locked_not", "reverse_shelled"]
                geek_coins_amt = random.randrange(file[str(self.member.id)]['Crypto'])

                inv = file[str(interaction.user.id)]['Inventory']
                inv2 = file[str(self.member.id)]['Inventory']
                c = random.choice(possiblities)
                if c == "pc_locked":
                    if geek_coins_amt != 0:
                        file[str(interaction.user.id)]['Crypto'] += geek_coins_amt
                        file[str(self.member.id)]['Inventory'] -= geek_coins_amt
                        embed = disnake.Embed(color=random.choice(colors))
                        embed.add_field(name="Ransomware worked and you have gained", value=f"{geek_coins_amt} Crypto")
                        await interaction.response.send_message(embed=embed)
                        with open('account.json', 'w') as f:
                            json.dump(file, f)
                    else:
                        embed = disnake.Embed(color=random.choice(colors))
                        embed.add_field(name="Failed", value="Victim doesnt have any geek_coins")
                        await interaction.response.send_message(embed=embed)

                elif c == "pc_locked_not":
                    embed = disnake.Embed(color=random.choice(colors))
                    embed.add_field(name="Failed", value="Ransomware was not able to lock programs")
                    await interaction.response.send_message(embed=embed)

                elif "Antivirus <:blurple_shield:1001104190875107429>" in inv2:
                    embed = disnake.Embed(color=random.choice(colors))
                    embed.add_field(name="Failed", value="Victim had antivirus")
                    await interaction.response.send_message(embed=embed)

                elif c == 'reverse_shelled':
                    if "Antivirus <:blurple_shield:1001104190875107429>" in inv:
                        embed = disnake.Embed(color=random.choice(colors))
                        embed.add_field(name="Failed", value="The victim reverse shelled on your but glad you had antivirus")
                        await interaction.response.send_message(embed=embed)
                    else:
                        embed = disnake.Embed(color=random.choice(colors))
                        embed.add_field(name="Failed", value="victim wasn't a victim, now you are a victim, he reverse shelled on you, you paid him 5000 <:nerd_coin:992265892756979735>")
                        await interaction.response.send_message(embed=embed)
                        file[str(interaction.user.id)]['Bank'] -= 5000
                        with open('account.json', 'w') as f:
                            json.dump(file, f)
                
            else:
                embed = disnake.Embed(color=random.choice(colors))
                embed.add_field(name="Failed", value="You don't have an ransomware, create it using /software")
                await interaction.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Failed", value="You think you are gonna use an software without an computer? make one with /assemble if you have enough items")
            await interaction.response.send_message(embed=embed)
            
    
    @disnake.ui.button(label="Spyware", style=disnake.ButtonStyle.red)
    async def spyware(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('account.json', 'r', encoding='utf-8') as f:
            data2 = json.load(f)
        
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]

        if any(computer in data2[str(interaction.user.id)]['Inventory'] for computer in computers):
            if "Coin Booster <:DigitalTwo:1003623866272329748>" in data2[str(interaction.user.id)]["Inventory"]:
                with open("login.json", 'r', encoding='utf-8') as r:
                    f = json.load(r)
            
                if "Spyware" in f[str(interaction.user.id)]["Programs"]:
                    if "Antivirus <:blurple_shield:1001104190875107429>" not in data2[str(self.member.id)]["Inventory"]:
                        ps = ['yes', 'no']
                        choice = random.choice(ps)
                        if choice == 'yes':
                            amt = random.randrange(data2[str(self.member.id)]["Bank"])

                            if data2[str(self.member.id)]["Bank"] != 0:
                                data2[str(interaction.user.id)]['Bank'] += (amt * 2)
                                data2[str(self.member.id)]["Bank"] -= amt
                                with open('account.json', 'w') as f:
                                    json.dump(data2, f)
                                
                                embed = disnake.Embed(color=random.choice(colors))
                                embed.add_field(name="Sucess, You gain", value=f"{amt * 2} <:nerd_coin:992265892756979735>'")
                                await interaction.response.send_message(embed=embed)
                            else:
                                embed = disnake.Embed(color=random.choice(colors))
                                embed.add_field(name="Failed", value='Victim has no money')
                                await interaction.response.send_message(embed=embed)

                        else:
                            embed = disnake.Embed(color=random.choice(colors))
                            embed.add_field(name="Failed", value="You got none of victim data")
                            await interaction.response.send_message(embed=embed)
                    else:
                        embed = disnake.Embed(color=random.choice(colors))
                        embed.add_field(name="Failed", value="Victim had an antivirus")
                        await interaction.response.send_message(embed=embed)
                else:
                    embed = disnake.Embed(color=random.choice(colors))
                    embed.add_field(name="Failed", value="You don't have an spyware, create it using /software")
                    interaction.response.send_message(embed=embed)
            else:
                with open("login.json", 'r', encoding='utf-8') as r:
                    f = json.load(r)
            
                if "Spyware" in f[str(interaction.user.id)]["Programs"]:
                    if "Antivirus <:blurple_shield:1001104190875107429>" not in data2[str(self.member.id)]["Inventory"]:
                        ps = ['yes', 'no']
                        choice = random.choice(ps)
                        if choice == 'yes':
                            amt = random.randrange(data2[str(self.member.id)]["Bank"])

                            if data2[str(self.member.id)]["Bank"] != 0:
                                data2[str(interaction.user.id)]['Bank'] += amt
                                data2[str(self.member.id)]["Bank"] -= amt
                                with open('account.json', 'w') as f:
                                    json.dump(data2, f)
                                
                                embed = disnake.Embed(color=random.choice(colors))
                                embed.add_field(name="Sucess, You gain", value=f"{amt} <:nerd_coin:992265892756979735>'")
                                await interaction.response.send_message(embed=embed)
                            else:
                                embed = disnake.Embed(color=random.choice(colors))
                                embed.add_field(name="Failed", value='Victim has no money')
                                await interaction.response.send_message(embed=embed)

                        else:
                            embed = disnake.Embed(color=random.choice(colors))
                            embed.add_field(name="Failed", value="You got none of victim data")
                            await interaction.response.send_message(embed=embed)
                    else:
                        embed = disnake.Embed(color=random.choice(colors))
                        embed.add_field(name="Failed", value="Victim had an antivirus")
                        await interaction.response.send_message(embed=embed)
                else:
                    embed = disnake.Embed(color=random.choice(colors))
                    embed.add_field(name="Failed", value="You don't have an spyware, create it using /software")
                    interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("You don't have a computer, assemble one, make an program then run it")
                
    
    @disnake.ui.button(label="Malware", style=disnake.ButtonStyle.red)
    async def malware(self, button: disnake.ui.Button, interaction: disnake.Interaction): 
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]["Inventory"] for computer in computers):
            with open("login.json", 'r', encoding='utf-8') as r:
                f = json.load(r)
            
            if "Malware" in f[str(interaction.user.id)]["Programs"]:
                if "Antivirus <:blurple_shield:1001104190875107429>" in file[str(self.member.id)]["Inventory"]:
                    embed = disnake.Embed(color=random.choice(colors))
                    embed.add_field(name="Failed", value="Victim has an antivirus")
                    await interaction.response.send_message(embed=embed)
                
                else:

                    tem = ["Antivirus <:blurple_shield:1001104190875107429>", "AI Software <:galaxy_brain:1003621546050474034>", "Coin Booster <:DigitalTwo:1003623866272329748>", "Windows 10 <:windows_10:1003626037713842228>", "Kali linux <:kali:1003630422560886905>", 'no tem']
                    if any(item in file[str(self.member.id)]["Inventory"] for item in tem):
                        cc = random.choice(tem)
                        file[str(interaction.user.id)]['Inventory'].append(cc)
                        file[str(self.member.id)]["Inventory"].remove(cc)
                        embed = disnake.Embed(color=random.choice(colors))
                        embed.add_field(name="Success, your malware brought you", value=cc)
                        await interaction.response.send_message(embed=embed)
                        with open('account.json', 'w') as f:
                            json.dump(file, f)
                
                    else:
                        embed = disnake.Embed(color=random.choice(colors))
                        embed.add_field(name="Failed", value="Victim has nothing")
                        await interaction.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Failed", value="You don't have a computer, assemble one, make an program then run it")
            await interaction.response.send_message(embed=embed)

class Software(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Ransomware", style=disnake.ButtonStyle.blurple)
    async def ransomware(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f) 
        
        if any(computer in file[str(interaction.user.id)]["Inventory"] for computer in computers):
            await interaction.response.send_message("You have made an Ransomware, it is now in your programs")
            with open('login.json', 'r', encoding='utf-8') as login:
                d = json.load(login)
            
            d[str(interaction.user.id)]["Programs"].append("Ransomware")
            with open('login.json', 'w') as login:
                json.dump(d, login)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Failed", value="You don't have a computer, assemble one.")
            await interaction.response.send_message(embed=embed)
    
    @disnake.ui.button(label="Spyware", style=disnake.ButtonStyle.blurple)
    async def spyware(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]['Inventory'] for computer in computers):
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Success", value="You have made an Spyware, it is now in your programs")
            await interaction.response.send_message(embed=embed)
            with open('login.json', 'r', encoding='utf-8') as login:
                d = json.load(login)
            
            d[str(interaction.user.id)]["Programs"].append("Spyware")
            with open('login.json', 'w') as login:
                json.dump(d, login)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Failed", value="You don't have a computer, assemble one.")
            await interaction.response.send_message(embed=embed)
    
    @disnake.ui.button(label="Malware", style=disnake.ButtonStyle.blurple)
    async def malware(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]['Inventory'] for computer in computers):
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Success", value="You have made an Malware, it is now in your programs")
            await interaction.response.send_message(embed=embed)
            with open('login.json', 'r', encoding='utf-8') as login:
                d = json.load(login)
            
            d[str(interaction.user.id)]["Programs"].append("Malware")
            with open('login.json', 'w') as login:
                json.dump(d, login)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Failed", value="You don't have a computer, assemble one.")
            await interaction.response.send_message(embed=embed)
    
    @disnake.ui.button(label="Discord bot", style=disnake.ButtonStyle.blurple)
    async def disordbot(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]['Inventory'] for computer in computers):
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Success", value="You have made an Discord bot, it is now in your programs")
            await interaction.response.send_message(embed=embed)
            with open('login.json', 'r', encoding='utf-8') as login:
                d = json.load(login)
            
            await disnakebot(interaction)

            d[str(interaction.user.id)]["Programs"].append("Discord bot")
            with open('login.json', 'w') as login:
                json.dump(d, login)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Failed", value="You don't have a computer, assemble one.")
            await interaction.response.send_message(embed=embed)

    @disnake.ui.button(label="App", style=disnake.ButtonStyle.blurple)
    async def app(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]['Inventory'] for computer in computers):
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Success", value="You have made an App, it is now in your programs")
            await interaction.response.send_message(embed=embed)
            with open('login.json', 'r', encoding='utf-8') as login:
                d = json.load(login)
            
            await app(interaction)

            d[str(interaction.user.id)]["Programs"].append("App")
            with open('login.json', 'w') as login:
                json.dump(d, login)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Failed", value="You don't have a computer, assemble one.")
            await interaction.response.send_message(embed=embed)
    
    @disnake.ui.button(label="Website", style=disnake.ButtonStyle.blurple)
    async def web(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]['Inventory'] for computer in computers):
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Success", value="You have made an Website, it is now in your programs")
            await interaction.response.send_message(embed=embed)
            with open('login.json', 'r', encoding='utf-8') as login:
                d = json.load(login)
            
            await website(interaction)


            d[str(interaction.user.id)]["Programs"].append("Website")
            with open('login.json', 'w') as login:
                json.dump(d, login)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name="Failed", value="You don't have a computer, assemble one.")
            await interaction.response.send_message(embed=embed)

#CoolPreTeensAlt#9914   

async def disnakebot(user):
    with open('dbot.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Servers'] = 1
        data[str(user.id)]['Commands'] = 1       
    
    with open('dbot.json', 'w') as f:
        json.dump(data, f)
    
    return True

async def website(user):
    with open('web.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Signed in people'] = 1      
    
    with open('web.json', 'w') as f:
        json.dump(data, f)
    
    return True

async def app(user):
    with open('app.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Downloads'] = 1          
    
    with open('app.json', 'w') as f:
        json.dump(data, f)
    
    return True

class Web(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @disnake.ui.button(label="Advertise", style=disnake.ButtonStyle.blurple)
    async def ad(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open("account.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if data[str(interaction.user.id)]["Bank"] >= 10000:
            with open('web.json') as file2:
                data2 = json.load(file2)
            
            data2[str(interaction.user.id)]["Signed in people"] += random.randrange(10)
            data[str(interaction.user.id)]["Bank"] -= 10000

            with open("account.json", 'w') as file:
                json.dump(data, file)

            with open("web.json", 'w') as file2:
                json.dump(data2, file2)

            await interaction.response.send_message("You advertised your bot, number of people who have signed in have increased")
        
        else:
            await interaction.response.send_message("You need to have at least 10000 <:nerd_coin:992265892756979735> to advertise")
    
    @disnake.ui.button(label="Sell email datas", style=disnake.ButtonStyle.blurple)
    async def sell(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('web.json') as file2:
            data2 = json.load(file2)
        
        amt = data2[str(interaction.user.id)]["Signed in people"] * 20

        with open("account.json", 'r', encoding='utf-8') as file:
            data = json.load(file)

        data[str(interaction.user.id)]["Bank"] += amt

        with open("account.json", 'w') as file:
            json.dump(data, file)
        
        await interaction.response.send_message(f"You have sold all of email data you had for {amt} <:nerd_coin:992265892756979735>")
    
    @disnake.ui.button(label="Delete website", style=disnake.ButtonStyle.blurple)
    async def deletee(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('login.json', 'r', encoding='utf-8') as frik:
            drik = json.load(frik)
        
        drik[str(interaction.user.id)]["Programs"].remove("Website")
        
        with open('login.json', 'w') as frik:
            json.dump(drik, frik)
        
        await interaction.response.send_message("You have deleted your website")    

class App(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @disnake.ui.button(label="Advertise", style=disnake.ButtonStyle.blurple)
    async def ad(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open("account.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if data[str(interaction.user.id)]["Bank"] >= 1000:
            with open('app.json') as file2:
                data2 = json.load(file2)
            
            data2[str(interaction.user.id)]["Downloads"] += random.randrange(50)
            data[str(interaction.user.id)]["Bank"] -= 1000

            with open("account.json", 'w') as file:
                json.dump(data, file)

            with open("app.json", 'w') as file2:
                json.dump(data2, file2)

            await interaction.response.send_message("You advertised your bot, your downloads have increased")
        
        else: 
            await interaction.response.send_message("You need to have at least 1000 <:nerd_coin:992265892756979735> to advertise")
    
    @disnake.ui.button(label="Show ads", style=disnake.ButtonStyle.blurple)
    async def show(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('app.json') as file2:
            data2 = json.load(file2)

        if data2[str(interaction.user.id)]["Downloads"] >= 1000:
            with open("account.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            data[str(interaction.user.id)]["Bank"] += 10000
            
            with open("account.json", 'w') as file:
                json.dump(data, file)
            
            await interaction.response.send_message("You have shown ads in your app and have earned 10000 <:nerd_coin:992265892756979735>!")

        else:
            await interaction.response.send_message("You need at least 1000 downloads to show ads")

    @disnake.ui.button(label="Delete website", style=disnake.ButtonStyle.blurple)
    async def deletee(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('login.json', 'r', encoding='utf-8') as frik:
            drik = json.load(frik)
        
        drik[str(interaction.user.id)]["Programs"].remove("App")
        
        with open('login.json', 'w') as frik:
            json.dump(drik, frik)
        
        await interaction.response.send_message("You have deleted your website")    

class Dbot(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Advertise", style=disnake.ButtonStyle.blurple)
    async def ad(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open("account.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if data[str(interaction.user.id)]["Bank"] >= 7000:
            with open('dbot.json') as file2:
                data2 = json.load(file2)
            
            data2[str(interaction.user.id)]["Servers"] += random.randrange(10)
            data[str(interaction.user.id)]["Bank"] -= 7000
            
            with open("account.json", 'w') as file:
                json.dump(data, file)

            with open("dbot.json", 'w') as file2:
                json.dump(data2, file2)

            await interaction.response.send_message("You advertised your bot, servers have increased")
        
        else:
            await interaction.response.send_message("You need to have at least 7000 <:nerd_coin:992265892756979735> to advertise")
    
    @disnake.ui.button(label="Add command", style=disnake.ButtonStyle.blurple)
    async def cmd(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('dbot.json', 'r', encoding='utf-8') as file2:
            data2 = json.load(file2)
        
        data2[str(interaction.user.id)]["Commands"] += 1
        with open("dbot.json", 'w') as file2:
            json.dump(data2, file2)

        await interaction.response.send_message("You have added another command in your bot")
    
    @disnake.ui.button(label="Earn money", style=disnake.ButtonStyle.blurple)
    async def earn(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('dbot.json', 'r', encoding='utf-8') as file2:
            data2 = json.load(file2)
        
        if data2[str(interaction.user.id)]["Servers"] >= 100:
            with open("account.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            data[str(interaction.user.id)]["Bank"] += 100

            with open("account.json", 'w') as file:
                json.dump(data, file)

            await interaction.response.send_message("You have earned 100 <:nerd_coin:992265892756979735>")
        
        else:
            await interaction.response.send_message("You need to reach 100 servers in order to earn money")
    
    @disnake.ui.button(label="Delete bot", style=disnake.ButtonStyle.red)
    async def dele(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('login.json', 'r', encoding='utf-8') as frik:
            drik = json.load(frik)
        
        drik[str(interaction.user.id)]["Programs"].remove("Discord bot")
        
        with open('login.json', 'w') as frik:
            json.dump(drik, frik)
        
        await interaction.response.send_message("You have deleted your Discord bot")

@_bot.slash_command(description="Delete an program from your computer")
async def delete(ctx, program_name):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Delete programs command", value="If you have programmed any type of software in your computer you can delete it using this command. Remember, the software name should be correct and it should exist in your computer or the command wont work.")
    await send_first_time_message(ctx, "delete", embed)  

    with open("login.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    deletembed = disnake.Embed(color=random.choice(colors))
    failembed = disnake.Embed(color=random.choice(colors))
    howcandelte = disnake.Embed(color=random.choice(colors))
    failembed.add_field(name="Deletion failed", value="Can't remove system file")
    howcandelte.add_field(name='Deletion failed', value="How can you delete an file that doesnt exist?")
    deletembed.add_field(name='Deletion successful', value='Program has been removed')
    
    if program_name == "system file":
        await ctx.send(embed=failembed)
    
    elif program_name == "system files":
        await ctx.send(embed=failembed)
    
    elif program_name == "System file":
        await ctx.send(embed=failembed)
    
    elif program_name == "System files":
        await ctx.send(embed=failembed)
    
    elif program_name == "systemfile":
        await ctx.send(embed=failembed)
    
    elif program_name == "systemfiles":
        await ctx.send(embed=failembed)
    
    elif program_name == "Systemfiles":
        await ctx.send(embed=failembed)
    
    elif program_name == "Systemfiles":
        await ctx.send(embed=failembed)
    
    elif program_name == "Ransomware":
        if "Ransomware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Ransomware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        else:
            ctx.send(embed=howcandelte)
    
    elif program_name == "ransomware":
        if "Ransomware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Ransomware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        else:
            ctx.send(embed=howcandelte)
    
    elif program_name == "Ransom ware":
        if "Ransomware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Ransomware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        else:
            ctx.send(embed=howcandelte)
    
    elif program_name == "ransom ware":
        if "Ransomware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Ransomware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        else:
            ctx.send(embed=howcandelte)
    
    elif program_name == "Spyware":
        if "Spyware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Spyware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)

    elif program_name == "Spy ware":
        if "Spyware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Spyware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == "spyware":
        if "Spyware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Spyware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == "spy ware":
        if "Spyware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Spyware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == "Malware":
        if "Malware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Malware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == "malware":
        if "Malware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Malware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == "Mal ware":
        if "Malware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Malware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == "mal ware":
        if "Malware" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Malware")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == 'App':
        if "App" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("App")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == 'app':
        if "App" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("App")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == 'Discord bot':
        if "Discord bot" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Discord bot")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == 'disnakebot':
        if "Discord bot" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Discord bot")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == 'Discord bot':
        if "Discord bot" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Discord bot")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == 'disnakebot':
        if "Discord bot" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Discord bot")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == 'website':
        if "Website" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Website")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    elif program_name == 'Website':
        if "Website" in data[str(ctx.user.id)]["Programs"]:
            data[str(ctx.user.id)]["Programs"].remove("Website")
            await ctx.send(embed=deletembed)

            with open('login.json', 'w') as file:
                json.dump(data, file)
        
        else:
            await ctx.send(embed=howcandelte)
    
    else:
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(title="Deletion failed", value="Not an valid program")
        await ctx.send(embed=embed)
    
class Run(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
 
    @disnake.ui.button(label="Discord bot", style=disnake.ButtonStyle.blurple)
    async def dc(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]["Inventory"] for computer in computers):
            with open('login.json', 'r', encoding='utf-8') as f2:
                file2 = json.load(f2)
            
            with open('dbot.json', 'r', encoding='utf-8') as fri:
                dat = json.load(fri)
            
            if "Discord bot" in file2[str(interaction.user.id)]['Programs']:
                color = disnake.Color(value=random.choice(colors))
                embed = disnake.Embed(title="Discord bot", color=color)
                a = dat[str(interaction.user.id)]["Servers"]
                e = dat[str(interaction.user.id)]["Commands"]

                embed.add_field(name='Servers', value=a)
                embed.add_field(name='Commands', value=e)

                await interaction.response.send_message(embed=embed, view=Dbot())
            
            else:
                embed = disnake.Embed(color=random.choice(colors))
                embed.add_field(name='Running failed', value="You don't have this program in your computer")
                await interaction.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name='Running failed', value="You don't have a computer")
            await interaction.response.send_message(embed=embed)
    
    @disnake.ui.button(label="Website", style=disnake.ButtonStyle.blurple)
    async def webbo(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        computers = ["Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
        with open('account.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        
        if any(computer in file[str(interaction.user.id)]["Inventory"] for computer in computers):
            with open('login.json', 'r', encoding='utf-8') as f2:
                file2 = json.load(f2)
            
            with open('web.json', 'r', encoding='utf-8') as fri:
                dat = json.load(fri)
            
            if "Website" in file2[str(interaction.user.id)]['Programs']:
                color = disnake.Color(value=random.choice(colors))
                embed = disnake.Embed(title="Discord bot", color=color)
                a = dat[str(interaction.user.id)]['Signed in people']
                embed.add_field(name='Signed in people', value=a)
                await interaction.response.send_message(embed=embed, view=Web())
            else:
                embed = disnake.Embed(color=random.choice(colors))
                embed.add_field(name='Running failed', value="You don't have this program in your computer")
                await interaction.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(color=random.choice(colors))
            embed.add_field(name='Running failed', value="You don't have a computer")
            await interaction.response.send_message(embed=embed)

@_bot.slash_command(description='With this command you can run your Discord bot, app and website if you have it in your computer')
async def run(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Run program command", value="If you have built softwares in your computer you can use them using this command. All types of software options are available in the button menu but only those buttons will work which softwares exist in your computer. You can use this to earn nerd coins.")
    await send_first_time_message(ctx, "run", embed)  
    await ctx.send("Program selection", view=Run())

@_bot.event
async def coin_boost(message):
    await open_account(message)
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if "Coin Booster <:DigitalTwo:1003623866272329748>" in data[str(message.author.id)]["Inventory"]:
        await asyncio.sleep(7200)  
        data[str(message.author.id)]["Inventory"].remove("Coin Booster <:DigitalTwo:1003623866272329748>")
        with open('account.json', 'w') as file:
            json.dump(data, file)
    else:
        pass

@_bot.event
async def xp_boost(message):
    await open_account(message)
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if "AI Software <:galaxy_brain:1003621546050474034>" in data[str(message.author.id)]["Inventory"]:
        await asyncio.sleep(7200)  
        data[str(message.author.id)]["Inventory"].remove("AI Software <:galaxy_brain:1003621546050474034>")
        with open('account.json', 'w') as file:
            json.dump(data, file)
    else:
        pass

@_bot.event
async def xp_boost(message):
    await open_account(message)
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if "AI Software <:galaxy_brain:1003621546050474034>" in data[str(message.author.id)]["Inventory"]:
        await asyncio.sleep(7200)  
        data[str(message.author.id)]["Inventory"].remove("AI Software <:galaxy_brain:1003621546050474034>")
        with open('account.json', 'w') as file:
            json.dump(data, file)
    else:
        pass

@_bot.slash_command(description="Make softwares which will be added")
async def software(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Software creation command", value="You can create softwares using this command which can be used to earn nerd coins or steal nerd coins from someone.")
    await send_first_time_message(ctx, "software", embed)  
    
    await ctx.send(view=Software())

@_bot.slash_command(description="Use your spyware, ransomware and malware to gain items and earn money")
@commands.cooldown(1, 60 , commands.BucketType.user)
async def attack(ctx, member: disnake.Member):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Attack command", value="You can use this command to use different types of offensive softwares in your computer including malware, spyware or ransomware. These can be used on someone else's bank account and steal nerd coins from them or steal items from them. Remember, this is just a game not a real process.")
    await send_first_time_message(ctx, "attack", embed)  
    
    await ctx.send(view=Attack(member=member))

@attack.error
async def attack_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tim = datetime.timedelta(seconds = error.retry_after)
        await ctx.send(f"Wait for **{tim}** before running this command again") 

@_bot.slash_command(description="Assemble your computer!")
async def assemble(ctx):
    await log_in(ctx)
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Assemble computer command", value="A very useful command to create your computer, assemble it. If you have required items in your inventory. You need any type of keyboard, monitor, mouse, RAM in order to assemble your computer. A computer can be very useful in earning nerd coins. Please keep exploring commands to know more uses.")
    await send_first_time_message(ctx, "assemble", embed)  

    await open_account(ctx)
    with open('account.json', 'r', encoding='utf-8') as data:
        f = json.load(data)
    
    inv = f[str(ctx.user.id)]["Inventory"]
    
    keys = ['Membrane Keyboard ⌨️', "Mehcanical Keyboard <:RGBKeyboard:986490410849423441>", "Mehcanical Gaming Keyboard <:gamer_keyboard:987622731614945330>"]
    monitor = ["Wide Montior <:gaming_keyboard:987619238204305438>", "Ultra Wide Montior with Ipad <:programmershit:987628014722514984>", "Monitor 🖥️"]
     
    embed = disnake.Embed(color=random.choice(colors))
    if 'Mouse 🖱️' in inv:
        if any(k in inv for k in keys):
            if any(m in inv for m in monitor):
                if "10 gb ram 💾" in inv:
                        inv.append("Computer🖱️🖥️⌨️💾")
                elif "16 gb ram <:DiscordFloppy:987628788256997377>" in inv:
                        inv.append("Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>")
                else:
                    embed.add_field(name="Error occured", value="You don't have any ram")
                    await ctx.send(embed=embed)
            else:
                embed.add_field(name="Error occured", value="You don't have any monitor")
                await ctx.send(embed=embed)
        else:
            embed.add_field(name="Error occured", value="You don't have any keyboard")
            await ctx.send(embed=embed)
    else:
        embed.add_field(name="Error occured", value="You don't have mouse")
        await ctx.send(embed=embed)
   
    with open('account.json', 'w') as data:
        json.dump(f, data)
 
@_bot.slash_command(description="Log in to your computer and see your programs and os")
async def computer(ctx):
    await log_in(ctx.author)
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Computer login command", value="This command can be used to have a look at your computer and know what operating system you are using and what softwares you have on your computer.")
    await send_first_time_message(ctx, "computer", embed)  

    await open_account(ctx)
    with open('account.json', 'r', encoding='utf-8') as data:
        f = json.load(data)
    
    inv = f[str(ctx.user.id)]["Inventory"]
    computers = ["Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954>💾", "Computer🖱️🖥️⌨️<:AMD_Radeon_RX_6900_XT_GPU:987622463431122954><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555>💾", "Computer🖱️🖥️⌨️<:Nvidia_3090_GPU:987623191159660555><:DiscordFloppy:987628788256997377>", "Computer🖱️🖥️⌨️💾", "Computer🖱️🖥️⌨️<:DiscordFloppy:987628788256997377>"]
    if any(comp in inv for comp in computers):
        await log_in(ctx)
        with open('login.json', 'r', encoding='utf-8') as file:
            data = json.load(file) 
        
    
        os = data[str(ctx.user.id)]['OS']
        programs = data[str(ctx.user.id)]['Programs']
        embed = disnake.Embed(title=f"{ctx.user}'s Programs")
        o = '\n'.join(os)
        embed.add_field(name="Operating system", value=o)
        pro = '\n'.join(programs)
        embed.add_field(name="Programs", value=pro)
        await ctx.send(embed=embed)     

    else:
        
        await ctx.send("You don't have an computer")

@fun.sub_command(description="Ask an magic8ball question")
async def magic8ball(ctx, *, message:str):
        
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name="Magic 8 Ball command", value="This command can be used to get an answer to a question, the answer would be either yes/equivalent to yes or no/equivalent to no. THE NERD HAS VERY ACCURATE ANSWER SO WHATEVER IT WILL SAY WILL BE TRUE!")
        await send_first_time_message(ctx, "magic8ball", embed)    

        try:
            choices = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', ' Outlook good:', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Do not count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful.']
            color = disnake.Color(value=random.choice(colors))
            em = disnake.Embed(color=color, title=f"{message}")
            em.description = random.choice(choices) 
            em.set_author(name="Magic8ball", icon_url="")
            em.set_footer(text=f"Sent by {ctx.user}")
            await ctx.send(embed=em)
        except Forbidden:
            color = disnake.Color(value=random.choice(colors))
            em = disnake.Embed(color=color, title='Error ')
            em.description = 'Error code **{e.code}**: {e.error}'
            return await ctx.send(embed=em)

@_bot.slash_command(description='Earn some money')
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Daily nerd coins command", value="You can use this command to get daily nerd coins, you will get nerd coins in range of 1k daily.")
    await send_first_time_message(ctx, "daily", embed)  
    await open_account(ctx)
    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    nc = random.randrange(1000)
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Daily transaction successful", value=f"You got {nc} daily <:nerd_coin:992265892756979735>")
    await ctx.send(embed=embed)

    data[str(ctx.user.id)]['Bank'] += nc
    
    with open('account.json', 'w') as file:
        json.dump(data, file)

@_bot.slash_command(description='Earn some money')
@commands.cooldown(1, 604800, commands.BucketType.user)
async def weekly(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Weekly nerd coins command", value="You can use this command to get weekly nerd coins, you will get nerd coins in range of 5k weekly.")
    await send_first_time_message(ctx, "weekly", embed)  

    await open_account(ctx)
    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    nc = random.randrange(5000)
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Weekly transaction successful", value=f"You got {nc} weekly <:nerd_coin:992265892756979735>")
    await ctx.send(embed=embed)

    data[str(ctx.user.id)]['Bank'] += nc
    
    with open('account.json', 'w') as file:
        json.dump(data, file)

@_bot.slash_command(description='Earn some money')
@commands.cooldown(1, 2592000, commands.BucketType.user)
async def monthly(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Monthly nerd coins command", value="You can use this command to get monthly nerd coins, you will get nerd coins in range of 10k monthly.")
    await send_first_time_message(ctx, "monthly", embed)  

    await open_account(ctx)
    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    nc = random.randrange(10000)
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Monthly transaction successful", value=f"You got {nc} monthly <:nerd_coin:992265892756979735>")
    await ctx.send(embed=embed)

    data[str(ctx.user.id)]['Bank'] += nc
    
    with open('account.json', 'w') as file:
        json.dump(data, file)

@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tim = datetime.timedelta(seconds = error.retry_after)
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name='Command on cooldown', value=f"Wait for **{tim}** before running this command again")
        await ctx.send(embed=embed) 

@monthly.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tim = datetime.timedelta(seconds = error.retry_after)
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name='Command on cooldown', value=f"Wait for **{tim}** before running this command again")
        await ctx.send(embed=embed) 

@weekly.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tim = datetime.timedelta(seconds = error.retry_after)
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name='Command on cooldown', value=f"Wait for **{tim}** before running this command again")
        await ctx.send(embed=embed) 

@mod.sub_command(description="DM someone (mod)")
@commands.has_permissions(administrator = True)
async def dm(ctx, user: disnake.Member, *, msg):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Server welcoming logs command", value="A basic administrator command to DM someone using the bot.")
    await send_first_time_message(ctx, "dm", embed) 

    try:
        await user.send(msg)          
        await ctx.send("DM has been sent")
    except disnake.ext.commands.MissingPermissions:
        await ctx.send("You don't have permission to run this command")

@mod.sub_command(description="Warn someone (mod)")
@commands.has_permissions(administrator = True)
async def warn(ctx, *, reason):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Warn command", value="Warn any user using this command, requires administrator permissions.")
    await send_first_time_message(ctx, "warn", embed) 

    try:
        color = disnake.Color(value=random.choice(colors))
        em = disnake.Embed(color=color, title=f"WARNING: by {ctx.message.author.name} from **{ctx.user.guild.name}**.", description=f"{reason}")
        await ctx.user.send(embed=em)
        await ctx.send("DM has been sent")
    except disnake.ext.commands.MissingPermissions:
        await ctx.send("Sorry, you don't have permission to run this command")

@mod.sub_command(description="Clear messages (mod)")
@commands.has_permissions(manage_messages = True)
async def purge(ctx, num):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Message deletion command", value="Clear an specific amount of messages in an specific channel, requires 'manage messages' permission.")
    await send_first_time_message(ctx, "purge", embed) 


    try: 
        if int(num) is None:
            await ctx.send("How many messages would you like me to delete? Usage: !purge <number of msgs>")
        else:
            try:
                float(num)
            except ValueError:
                return await ctx.send("The number is invalid. Usage: !purge <number of msgs>")
            await ctx.channel.purge(limit=int(num)+1)
            msg = await ctx.send("Purged successfully")
            await asyncio.sleep(3)
            await msg.delete()
    except disnake.Forbidden:
            await ctx.send("Purge unsuccessful. The bot does not have Manage Messges permission.")
    except disnake.ext.commands.MissingPermissions:
        await ctx.send("Sorry, you don't have permission to run this command")

@mod.sub_command(description="Kick someone (mod)")
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: disnake.Member):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Kicking command", value="This command can be used to kick any member, requires 'kick members' permission.")
    await send_first_time_message(ctx, "kick", embed) 


    try:
        await ctx.send(f"{user.name} has been kicked")
        await user.kick()
    except disnake.Forbidden:
        await ctx.send("I don't have banning permissions")
    except disnake.ext.commands.MissingPermissions:
        await ctx.send("Sorry, you don't have permission to run this command")

@mod.sub_command(description="Ban someone (mod)")
@commands.has_permissions(ban_members = True)
async def ban(ctx, user: disnake.Member):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Banning command", value="This command can be used to ban any member, requires 'ban members' permission.")
    await send_first_time_message(ctx, "ban", embed) 


    try:
        await ctx.send(f"{user.name} has been banned from this server.")
        await user.ban()
    except disnake.Forbidden:
        await ctx.send("I don't have banning permissions")
    except disnake.ext.commands.MissingPermissions:
        await ctx.send("Sorry, you don't have permission to run this command")

@mod.sub_command(description="Mute someone")
@commands.has_permissions(ban_members=True)
async def mute(ctx, user: disnake.Member, mutetime=None):
        
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name="Muting command", value="Mute any memeber using this command, requires 'ban members' permission.")
        await send_first_time_message(ctx, "mute", embed) 


        try:
            if mutetime is None:
                await ctx.channel.set_permissions(user, send_messages=False)
                await ctx.send(f"{user.mention} has been muted")
            else:
                try:
                    mutetime =int(mutetime)
                    mutetime = mutetime * 60
                except ValueError:
                    return await ctx.send("Invalid time")
                await ctx.channel.set_permissions(user, send_messages=False)
                await ctx.send(f"{user.mention} has been muted")
                await asyncio.sleep(mutetime)
                await ctx.channel.set_permissions(user, send_messages=True)
                await ctx.send(f"{user.mention} has been unmuted.")
        except disnake.Forbidden:
            return await ctx.send("I could not mute the user. Make sure I have the manage channels permission.")
        except disnake.ext.commands.MissingPermissions:
            await ctx.send("Sorry, you don't have permission to run this command")

@_bot.event
async def on_error(event, *args, **kwargs):
    print(traceback.format_exc())
    print(event)

@mod.sub_command(description="Unmute someone")
@commands.has_permissions(ban_members=True)
async def unmute(ctx, user: disnake.Member):
        
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name="Unmuting command", value="Unmute any memeber using this command, requires 'ban members' permission.")
        await send_first_time_message(ctx, "unmute", embed) 


        await ctx.channel.set_permissions(user, send_messages=True)
        await ctx.send(f"{user.mention} has been unmuted")

@fun.sub_command(description="Get server information")
async def serverinfo(ctx):
        embed = disnake.Embed(color=random.choice(colors))
        embed.add_field(name="Server information command", value="A utility command can be used to get some basic information about the server command is ran in. It can provide Server name, Server ID, Owner name, Owner ID, Member count, Server region, Roles, Date created and server PFP.")
        await send_first_time_message(ctx, "serverinfo", embed)    

        guild = ctx.guild
        roles = [x.name for x in guild.roles]
        role_length = len(roles)
        roles = ', '.join(roles)
        channels = len(guild.channels)
        time = str(guild.created_at.strftime("%b %m, %Y, %A, %I:%M %p"))         
        em = disnake.Embed(description= "-", title='Server Info', colour=0x00ff00)
        em.set_thumbnail(url=guild.icon)
        em.add_field(name='__Server __', value=str(guild.name))
        em.add_field(name='__Server ID__', value=str(guild.id))
        em.add_field(name='__Owner__', value=str(guild.owner))
        em.add_field(name='__Owner ID__', value=guild.owner_id) 
        em.add_field(name='__Member Count__', value=str(guild.member_count))
        em.add_field(name='__Text/Voice Channels__', value=str(channels))
        em.add_field(name='__Server Region__', value='%s' % str(guild.region))
        em.add_field(name='__ Total Roles__', value='%s' % str(role_length))
        em.add_field(name='__Roles__', value='%s' % str(roles))
        em.set_footer(text='Created - %s' % time)        
        await ctx.send(embed=em)

@_bot.slash_command(description="Get an job")
async def job(ctx, jobname):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Getting job command", value="This command can be used to get a job, you need to use /jobs to get list of all the jobs and then copy the job you want to get, to get a job you need to have enough subject points requirements. To study you need to use /learn command and if your requirements match you can get a job. Having a job just gives you daily money, to earn money, after getting a job you need to use /work.")
    await send_first_time_message(ctx, "job  ", embed)  

    await learning_points(ctx)
    with open('learning_points.json', 'r', encoding='utf-8') as r:
        file = json.load(r)
    
    p = file[str(ctx.user.id)]['Physics']
    c = file[str(ctx.user.id)]['Chemistry']
    b = file[str(ctx.user.id)]['Biology']
    cs =  file[str(ctx.user.id)]['Computer science']
    m = file[str(ctx.user.id)]['Maths']

    await open_account(ctx)
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    jb = data[str(ctx.user.id)]['Job']
    inv = data[str(ctx.user.id)]['Inventory']

    with open('jobs.json', 'r', encoding='utf-8') as file:
        jobs = json.load(file)
    
    if p >= jobs[jobname]["Physics points"]:
        if c >= jobs[jobname]["Chemistry points"]:
            if b >= jobs[jobname]["Biology points"]:
                if cs >= jobs[jobname]["Computer science points"]:
                    if m >= jobs[jobname]["Maths points"]:
                        if len(jobs[jobname]["Required jobs"]) == 0:
                            await ctx.send(f"You can now do job as {jobname}")
                            jb.clear()
                            jb.append(jobname)
                            with open('account.json', 'w') as file:
                                json.dump(data, file) 

                        elif len(jobs[jobname]["Required jobs"][0]) != 0:
                            if jobs[jobname]["Required jobs"][0] in inv:
                                await ctx.send(f"You can now do job as {jobname}")
                                jb.clear()
                                jb.append(jobname)
                                with open('account.json', 'w') as file:
                                    json.dump(data, file) 
                            else:
                                await ctx.send(f"You need job of {jobs[jobname]['Required jobs']} to get this job")
                    else:
                        await ctx.send("You don't have enough maths points")
                else:
                    await ctx.send("You don't have enough computer science points")
            else:
                await ctx.send("You don't have enough biology points")
        else:
            await ctx.send("You don't have enough chemistry points")
    else:
        await ctx.send("You don't have enough physics points")

@_bot.slash_command(description="Leave your current job")
async def retire(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Retiring job command", value="This command can be used to retire from your current job, after that you can get a new job.")
    await send_first_time_message(ctx, "retire", embed)  
    await open_account(ctx)
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if len(data[str(ctx.user.id)]['Job']) == 0:
        await ctx.send("Get a job first then think of retire")

    else:
        await ctx.send("You have retired from your job")
        data[str(ctx.user.id)]['Job'].clear()
        with open('account.json', 'w') as file:
            json.dump(data, file)

@_bot.slash_command(description="Do some work in your job")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def work(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Work command", value="If you have a job you can work using this command daily. The cooldown is of 24 hours, meaning you can work and get money daily.")
    await send_first_time_message(ctx, "work", embed)  

    await open_account(ctx)
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    job = data[str(ctx.user.id)]['Job']
    
    if "Coin Booster <:DigitalTwo:1003623866272329748>" in data[str(ctx.user.id)]["Inventory"]:
        if len(job) != 0:
            jb = job[0]

            with open('jobs.json', 'r', encoding='utf-8') as file:
                jobs = json.load(file)

            sal = jobs[jb]['salary']
            new = sal + 5000
            data[str(ctx.user.id)]['Bank'] += new

            with open('account.json', 'w') as file:
                json.dump(data, file)
    
            await ctx.send(f"You have earned {new} <:nerd_coin:992265892756979735>")

        else:
            await ctx.send("You don't have a job") 
    else:
        if len(job) != 0:
            jb = job[0]

            with open('jobs.json', 'r', encoding='utf-8') as file:
                jobs = json.load(file)

            sal = jobs[jb]['salary']
            data[str(ctx.user.id)]['Bank'] += sal

            with open('account.json', 'w') as file:
                json.dump(data, file)
    
            await ctx.send(f"You have earned {sal} <:nerd_coin:992265892756979735>")

        else:
            await ctx.send("You don't have a job") 

@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tim = datetime.timedelta(seconds = error.retry_after)
        await ctx.send(f"Wait for **{tim}** seconds before running this command again") 
 
@_bot.slash_command(description="Check your balance")
async def bal(ctx):
    await open_account(ctx)
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Balance command", value="This command displays your account nerd coin balance, geek coin balance and your current job.")
    await send_first_time_message(ctx, "bal", embed)  

    await open_account(ctx)
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    bank = data[str(ctx.user.id)]['Bank']
    crpt = data[str(ctx.user.id)]['Crypto']
    jb = data[str(ctx.user.id)]['Job']

    embed = disnake.Embed(title=f"{ctx.user.name}'s stats")
    embed.add_field(name="Bank", value=bank)
    embed.add_field(name="Crypto", value=crpt) 
    embed.add_field(name="Job", value=jb)

    await ctx.send(embed=embed)

async def open_account(user):
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Bank'] = 0
        data[str(user.id)]['Job'] = []
        data[str(user.id)]['XP'] = 0
        data[str(user.id)]['Level'] = 0
        data[str(user.id)]['Inventory'] = ["🎒"]
        data[str(user.id)]['Crypto'] = 0
    
    with open('account.json', 'w') as f:
        json.dump(data, f)
    
    return True

@fun.sub_command(description="Hug someone!")
async def hug(ctx, member: disnake.Member):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Hug command", value="Hug people, what else?")
    await send_first_time_message(ctx, "hug", embed)    

    try:
        rand_hugs = random.choice(hug_links)
        await ctx.send(f'{rand_hugs}')
        await ctx.send(f'{member.mention} gets a hug.')
    except:
        pass


@_bot.slash_command(description="See the job board")
async def jobs(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Job board command", value="This command can be used to get list of all jobs available. If you match the requirements you can use /job to get a job and /work to do work and earn money. If you do not match requirements use /learn to learn subjects and collect points to match job requirements. Warning, some jobs require another job's experience.")
    await send_first_time_message(ctx, "jobs", embed)  

    with open('jobs.json', 'r', encoding='utf-8') as file:
        jobs = json.load(file)

    embed = disnake.Embed(title="Jobs")

    for job in jobs:
        jbb = '\n'.join(jobs[job]['Required jobs'])
        embed.add_field(name=f"{job.title()}:", value=f"{jobs[job]['description']}\n**Salary** - {jobs[job]['salary']}\n**Computer science points** - {jobs[job]['Computer science points']}\n**Physics points** - {jobs[job]['Physics points']}\n**Biology points** - {jobs[job]['Biology points']}\n**Chemistry points** - {jobs[job]['Chemistry points']}\n**Maths points** - {jobs[job]['Maths points']}\n**Required jobs** - {jbb}")

    await ctx.send(embed=embed)

@_bot.slash_command(description="Mine geek_coins currency if you have an laptop")
@commands.cooldown(1, 7200, commands.BucketType.user)
async def geek_coins(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Geek coin earning command", value="This command can be used to earn *Geek Coins*, another specialized coin which can be earned if you have a laptop. The expensive the laptop is the more geek coins you earn. You can redeem geek coins into nerd coins using /redeem. The cooldown is of 2 hours.")
    await send_first_time_message(ctx, "geek_coins", embed)  

    try:
        with open('account.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    
        await open_account(ctx)
        inv = data[str(ctx.user.id)]['Inventory']
        if "Laptop 💻" in inv: 
            geek_coins = random.randrange(2000)
            if geek_coins <= 1000:
                await ctx.send("Damn, you cannot find any geek coins currency")
            else:
                await ctx.send(f"You got {geek_coins} geek coins currency!")
                data[str(ctx.user.id)]['Crypto'] += geek_coins
            
                with open('account.json', 'w') as file:
                    json.dump(data, file)
    
        elif "MacBook <:MacBook:987624574202044447>" in inv:
            crpt = data[str(ctx.user.id)]['Crypto']
            geek_coins = random.randrange(2000)
            if geek_coins <= 900:
                await ctx.send("Damn, you cannot find any geek_coins currency")
            else:
                await ctx.send(f"You got {geek_coins} geek_coins currency!")
                data[str(ctx.user.id)]['Crypto'] += geek_coins
        
                with open('account.json', 'w') as file:
                    json.dump(data, file)

        else:
            await ctx.send("You don't have any laptop, buy an laptop")
    
    except commands.CommandOnCooldown:
        await ctx.send("Your command is on ann 30 second cooldown, wait for 30 seconds and try again")

@geek_coins.error
async def geek_coins_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
            tim = datetime.timedelta(seconds = error.retry_after)
            await ctx.send(f"Wait for **{tim}** before running this command again") 

@_bot.slash_command(description="Redeem an amount of geek coins currency you have")
async def redeem(ctx, amount):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Redeem nerd coins command", value="This command is used to convert geek coins into nerd coins. You can earn geek coins using /geek_coins command if you have a laptop.")
    await send_first_time_message(ctx, "redeem", embed)  

    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    await open_account(ctx)
    crpt = data[str(ctx.user.id)]['Crypto']
    
    if int(amount) > crpt:
        await ctx.send(f"You don't have {amount} geek_coins")
    elif int(amount) < 0:
        await ctx.send("Invalid amount")
    else:
        money = crpt * 2
        data[str(ctx.user.id)]['Bank'] += money
        data[str(ctx.user.id)]['Crypto'] -= int(amount)
        await ctx.send(f"You have redeemed {amount} geek_coins currency and have increased {money} <:nerd_coin:992265892756979735>")
        

        with open('account.json', 'w') as file:
            json.dump(data, file)

@_bot.slash_command(description="Open the shop")
async def shop(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Shop command", value="This commmand returns list of items available you can buy, the payment is only in nerd coins. You can buy an item using /buy, just remember to copy the item code you want to buy and paste it into the /buy command.")
    await send_first_time_message(ctx, "shop", embed)  
    
    with open('shop.json', 'r', encoding='utf-8') as file:
        items = json.load(file)

    embed = disnake.Embed(title="Shop")

    for item in items:
        embed.add_field(name=f"{item.title()}:", value=f"{items[item]['description']}\n**Price** - {items[item]['price']}\n**code** - {items[item]['code']}")

    await ctx.send(embed=embed)

@_bot.slash_command(description="Buy an item from the shop")
async def buy(ctx, code):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Buy command", value="With this command you can buy items from shop, use /shop to get item list and copy the item code you want to buy and paste it in the 'code' option of command.")
    await send_first_time_message(ctx, "buy", embed)  

    await open_account(ctx)
    
    with open('account.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('shop.json', 'r', encoding='utf-8') as file:
        items = json.load(file)
    
    for item in items:
        if item not in data[str(ctx.user.id)]['Inventory']:
            if code == items[item]['code']:
                if data[str(ctx.user.id)]['Bank'] <= items[item]['price']:
                    embed=disnake.Embed(color=random.choice(colors))
                    embed.add_field(name="Error", value=f"You don't have enough money to buy {item}")
                    await ctx.send(embed=embed)
                else:
                    embed=disnake.Embed(color=random.choice(colors))
                    embed.add_field(name="Success", value=f"You have bought {item}!")
                    await ctx.send(embed=embed)
            
                    inv = data[str(ctx.user.id)]['Inventory']
                    data[str(ctx.user.id)]['Bank'] -= items[item]['price']

                    inv.append(item)

                    with open('account.json', 'w') as file:
                        json.dump(data, file)
        else:
            pass

async def kali_installed(ctx):
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if "Kali linux <:kali:1003630422560886905>" in data[str(ctx.id)]["Inventory"]:
        print("KALI IN")
        with open("login.json", 'r', encoding='utf-8') as file2:
            data2 = json.load(file2)
        data2[str(ctx.user.id)]["OS"].clear()
        data2[str(ctx.user.id)]["OS"].append("Kali linux <:kali:1003630422560886905>")
        with open("login.json", 'w') as file2:
            json.dump(data2, file2)
        print("PROCESS 1 DONE")
        data[str(ctx.user.id)]["Inventory"].remove("Kali linux <:kali:1003630422560886905>")

        with open("account.json", 'w') as file:
            json.dump(data, file)
    
    else:
        pass

async def win10_installed(ctx):
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if "Windows 10 <:windows_10:1003626037713842228>" in data[str(ctx.id)]["Inventory"]:
        with open("login.json", 'r', encoding='utf-8') as file2:
            data2 = json.load(file2)
        data2[str(ctx.user.id)]["OS"].clear()
        data2[str(ctx.user.id)]["OS"].append("Windows 10 <:windows_10:1003626037713842228>")
        with open("login.json", 'w') as file2:
            json.dump(data2, file2)
        data[str(ctx.user.id)]["Inventory"].remove("Windows 10 <:windows_10:1003626037713842228>")

        with open("account.json", 'w') as file:
            json.dump(data, file)
    
    else:
        pass

@_bot.slash_command(description="Check your inventory")
async def inv(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Inventory command", value="This command displays your inventory. It wil display all the items you have bought and your computers, bought machines, collective items.")
    await send_first_time_message(ctx, "inv", embed)  
    
    with open('account.json') as file:
        data = json.load(file)

    embed = disnake.Embed(title=f"{ctx.user.name}'s Inventory")
    iv = '\n'.join(data[str(ctx.user.id)]['Inventory'])
    embed.add_field(name=f"----------", value=iv)
    await ctx.send(embed=embed)

@_bot.slash_command(description="See what subjects to learn")
async def subjects(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Subject list command", value="This command displays a list of subjects that can be learned to get a job. Remember the code of the subject and paste it in the /learn command to learn it.")
    await send_first_time_message(ctx, "subjects", embed)  

    embed = disnake.Embed(color=random.choice(colors))
    embed.set_author(name="Subjects")

    subjects = [("Physics (p)", "`This would help to get jobs related to physics`", False),
              ("Chemistry (c)", "`You can get jobs related to chemistry with this`", False),
              ("Biology (b)", "`You can get biology jobs with this`", False),
              ("Computer science (cs)", "`All jobs related to programmming might be opened`", False),
              ("Maths (m)", "`This subject's degree is necessary for many jobs`", False)]
        
    for name, value, inline in subjects:
        embed.add_field(name=name, value=value, inline=inline)
    
    await ctx.send(embed=embed)

async def learning_points(user):
    with open('learning_points.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Physics'] = 0
        data[str(user.id)]['Chemistry'] = 0
        data[str(user.id)]['Biology'] = 0
        data[str(user.id)]['Computer science'] = 0   
        data[str(user.id)]['Maths'] = 0

    with open('learning_points.json', 'w') as f:
        json.dump(data, f)
    
    return True



@_bot.slash_command(description="Learn an subject")
@commands.cooldown(1, 3600, commands.BucketType.user)
async def learn(ctx, subject):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Learn subjects command", value="This is a very useful command and can be used to learn an subject in order to get a job, use /subjects to get list of all available subject and copy the subject and paste it in this command to learn it. Cooldown is of one hour.")
    await send_first_time_message(ctx, "learn", embed)  

    await learning_points(ctx)
    with open('learning_points.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if subject == "Physics":
        data[str(ctx.user.id)]['Physics'] += 5
        await ctx.send("You have learned Physics for an hour and have gained 5 points in Physics")

    elif subject == "Chemistry":
        data[str(ctx.user.id)]['Chemistry'] += 5
        await ctx.send("You have learned Chemistry for an hour and have gained 5 points in Chemistry")
    
    elif subject == "Biology":
        data[str(ctx.user.id)]['Biology'] += 5
        await ctx.send("You have learned Biology for an hour and have gained 5 points in Biology")
    
    elif subject == "cs":
        data[str(ctx.user.id)]['Computer science'] += 5
        await ctx.send("You have learned Computer science for an hour and have gained 5 points in Computer science")
    
    elif subject == "Maths":
        data[str(ctx.user.id)]['Maths'] += 5
        await ctx.send("You have learned Maths for an hour and have gained 5 points in Maths")
    
    elif subject == "chemistry":
        data[str(ctx.user.id)]['Chemistry'] += 5
        await ctx.send("You have learned Chemistry for an hour and have gained 5 points in Chemistry")
    
    elif subject == "biology":
        data[str(ctx.user.id)]['Biology'] += 5
        await ctx.send("You have learned Biology for an hour and have gained 5 points in Biology")
    
    elif subject == "maths":
        data[str(ctx.user.id)]['Maths'] += 5
        await ctx.send("You have learned Maths for an hour and have gained 5 points in Maths")
    
    elif subject == "p":
        data[str(ctx.user.id)]['Physics'] += 5
        await ctx.send("You have learned Physics for an hour and have gained 5 points in Physics")
         
    elif subject == "c":
        data[str(ctx.user.id)]['Chemistry'] += 5
        await ctx.send("You have learned Chemistry for an hour and have gained 5 points in Chemistry")
    
    elif subject == "b":
        data[str(ctx.user.id)]['Biology'] += 5
        await ctx.send("You have learned Biology for an hour and have gained 5 points in Biology")
    
    elif subject == "m":
        data[str(ctx.user.id)]['Maths'] += 5
        await ctx.send("You have learned Maths for an hour and have gained 5 points in Maths")
    
    else:
        await ctx.send("Invalid subject")
    
    with open('learning_points.json', 'w') as file:
        json.dump(data, file)

@learn.error
async def learn_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
            tim = datetime.timedelta(seconds = error.retry_after)
            await ctx.send(f"Wait for **{tim}** before running this command again") 

@_bot.slash_command(description="Get top 10 richest people")
async def top(ctx,x=10):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Top 10 leaderboard command", value="This command can be used to get top 10 *Global* Leaderboard.")
    await send_first_time_message(ctx, "top", embed)  

    await open_account(ctx)
    with open('account.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    leader_board = {}
    total = []

    for user in users:
        name = int(user)    
        total_amtt = users[user]['Bank']
        leader_board[total_amtt] = name 
        total.append(total_amtt)

    total = sorted(total,reverse=True)

    embed = disnake.Embed(title=f'Top {x} Leaderboard', description='Top Rich People')
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        print(id_)
        member = await _bot.fetch_user(id_)
        embed.add_field(name=f'{index}. {member}', value=f'{amt} <:nerd_coin:992265892756979735>', inline=False)
        if index == x:
            break
        else:
            index +=1
    await ctx.send(embed=embed)


@_bot.slash_command(description="Check how much learning points you got in every subject")
async def learnpoints(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Subject points command", value="This command is used to check how many subject points you have. To learn a subject use /learn, to list all subjects use /subjects.")
    await send_first_time_message(ctx, "learnpoints", embed)  

    await learning_points(ctx)
    with open('learning_points.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    p = data[str(ctx.user.id)]['Physics']
    c = data[str(ctx.user.id)]['Chemistry']
    b = data[str(ctx.user.id)]['Biology']
    cs =  data[str(ctx.user.id)]['Computer science']
    m = data[str(ctx.user.id)]['Maths']

    embed = disnake.Embed(title=f"{ctx.user.name}'s Subjects Points")
    embed.add_field(name="Physics points", value=p)
    embed.add_field(name="Chemistry points", value=c)
    embed.add_field(name="Biology points", value=b)
    embed.add_field(name="Computer science points", value=cs)
    embed.add_field(name="Maths points", value=m)

    await ctx.send(embed=embed)

@_bot.slash_command(description="See your level card")
async def level(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Level card command", value="This command tells your level, the more you chat in the server this bot is in, the more XP you gain. Your XP is always safely stored so even if you leave the server or be in another server or bot is kicked, your XP will not go. Same thing is with all the currencies (nerd coin and geek coin), crypto currencies, inventory and learning points. To boost your XP you can buy XP booster in /shop.")
    await send_first_time_message(ctx, "level", embed)  

    userr = ctx.user
    
    await open_account(ctx)
    with open("account.json", "r") as f:
      data = json.load(f)

    xp = data[str(userr.id)]["XP"]
    lvl = data[str(userr.id)]["Level"]

    next_level_xp = (lvl+1) * 100
    xp_need = next_level_xp
    xp_have = data[str(userr.id)]["XP"]

    percentage = int(((xp_have * 100)/ xp_need))

    if percentage < 1:
      percentage = 0
    
    background = Editor(f"zIMAGE.png")
    profile = await load_image_async(str(userr.avatar.url))

    profile = Editor(profile).resize((150, 150)).circle_image()
    
    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    ima = Editor("zBLACK.png")
    background.blend(image=ima, alpha=.5, on_top=False)

    background.paste(profile.image, (30, 30))

    background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
    background.bar(
        (30, 220),
        max_width=650,
        height=40,
        percentage=percentage,
        fill="#ff9933",
        radius=20,
    )
    background.text((200, 40), str(userr.name), font=poppins, color="#ff9933")

    background.rectangle((200, 100), width=350, height=2, fill="#ff9933")
    background.text(
        (200, 130),
        f"Level : {lvl}"
        + f" XP : {xp} / {(lvl+1) * 100}",
        font=poppins_small,
        color=random.choice(colors)
    )

    card = disnake.File(fp=background.image_bytes, filename="zCARD.png")
    await ctx.send(file=card)

async def xp(ctx, amt):
    await open_account(ctx)
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  
    
    if ctx.id != _bot.user:
        data[str(ctx.id)]["XP"] += amt 
    else:
        pass

    with open('account.json', 'w') as file:
        json.dump(data, file)

async def lvl(message):
        with open("account.json", "r", encoding='utf-8') as f:
            data = json.load(f)

        with open("setup.json", "r", encoding='utf-8') as fi:
            da = json.load(fi)
    
        if "AI Software <:galaxy_brain:1003621546050474034>" in data[str(message.author.id)]["Inventory"]:
            if str(message.author.id) in data:
                xp = data[str(message.author.id)]['XP']
                lvl = data[str(message.author.id)]['Level']

                increased_xp = xp+35
                new_level = int(increased_xp/100)

                data[str(message.author.id)]['XP']=increased_xp

                with open("account.json", "w") as f:
                    json.dump(data, f)

                if new_level > lvl:
                    with open('setup.json', 'r', encoding='utf-8') as file2:
                        data2 = json.load(file2)
                    
                    if data2[str(message.guild.id)]['level'] != []:
                        channel = _bot.get_channel(int(data2[str(message.guild.id)]['level'][0]))
                        await channel.send(f"{message.author.mention} {data2[str(message.guild.id)]['levelm'][0]} [{new_level}]")
                    
                    else:
                        await message.reply(f"{message.author.mention} You leveled up to {new_level}")

                    data[str(message.author.id)]['Level']=new_level
                    data[str(message.author.id)]['XP']=0

                    with open("account.json", "w") as f:
                        json.dump(data, f)
            

        else:
            if str(message.author.id) in data:
                xp = data[str(message.author.id)]['XP']
                lvl = data[str(message.author.id)]['Level']

                increased_xp = xp+25
                new_level = int(increased_xp/100)

                data[str(message.author.id)]['XP']=increased_xp

                with open("account.json", "w") as f:
                    json.dump(data, f)

                if new_level > lvl:
                    with open('setup.json', 'r', encoding='utf-8') as file2:
                        data2 = json.load(file2)
                    
                    if data2[str(message.guild.id)]['level'] != []:
                        channel = _bot.get_channel(int(data2[str(message.guild.id)]['level'][0]))
                        await channel.send(f"{message.author.mention} {data2[str(message.guild.id)]['levelm'][0]} [{new_level}]")
                    
                    else:
                        await message.reply(f"{message.author.mention} You leveled up to {new_level}")
                    

                    data[str(message.author.id)]['Level']=new_level
                    data[str(message.author.id)]['XP']=0

                    with open("account.json", "w") as f:
                        json.dump(data, f)
        
                    

'''async def lvldetect(ctx):
    if not ctx.user.bot:
        await open_account(ctx)
        with open('account.json', 'r', encoding='utf-8') as file:
            data = json.load(file) 
    
        xp = data[str(ctx.user.id)]["XP"]
        lev = data[str(ctx.user.id)]["Level"]

        if lev == 5 and xp == 30: 
            await ctx.send("You got an degree")
        else:
            pass''' 


class VerificationButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(style=disnake.ButtonStyle.blurple, label="Verify Me", custom_id="verify_button")
        
    async def callback(self, interaction: disnake.MessageInteraction):
        member = interaction.user
        guild = interaction.guild
        
        if member == guild.owner:
            await interaction.response.send_message("Sorry, the server owner cannot be verified.", ephemeral=True)
            return
        
        verified_role = disnake.utils.get(guild.roles, name="Verified")
        
        if verified_role is None:
            verified_role = await guild.create_role(name="Verified")
        
        await member.add_roles(verified_role)
        await interaction.response.edit_message(content=f"{member.mention} has been verified!")

@_bot.slash_command(name="verify", description="Verify yourself with a button")
async def verification_command(ctx):
    await ctx.send("Verifying you...", ephemeral=True)
    verified_role = disnake.utils.get(ctx.guild.roles, name="Verified")
        
    if verified_role is None:
        verified_role = await ctx.guild.create_role(name="Verified")
        
    await ctx.author.add_roles(verified_role)

@fun.sub_command(description="Get an programming meme")
async def techiememe(ctx):
        subreddit = "ProgrammerHumor"
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        response_json = response.json()
        posts = response_json["data"]["children"]

        memes = []
        for post in posts:
            if post["data"]["post_hint"] == "image":
                memes.append(post["data"]["url"])

        if memes:
            meme_url = random.choice(memes)
            await ctx.send(meme_url)
        else:
            await ctx.send("Sorry, no memes found :(")
            
@fun.sub_command(description='Get an meme')
async def meme(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Meme command", value="This command provides memes from a reddit page called 'r/dankmemes'. It is filtered for only top memes.")
    await send_first_time_message(ctx, "meme", embed)    

    embed = disnake.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@fun.sub_command(description="Get a fact")
async def fact(ctx):
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if response.status_code == 200:
            data = response.json()
            fact = data["text"]
            embed = disnake.Embed(title="Random Fact", description=fact, color=disnake.Color.random())
            await ctx.send(embed=embed)
        else:
            await ctx.send("Oops! Something went wrong.")

@fun.sub_command(description="Get an cool image")
async def pic(ctx):
        url = "https://www.reddit.com/r/ImaginaryLandscapes/top.json?sort=top&t=week"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        response_json = response.json()
        posts = response_json["data"]["children"]

        art = []
        for post in posts:
            if post["data"]["post_hint"] == "image":
                art.append(post["data"]["url"])

        if art:
            art_url = random.choice(art)
            await ctx.send(art_url)
        else:
            await ctx.send("Sorry, no art found :(")

def embedding(text: str):
  text= disnake.Embed(
  description=f"**{text}**",
  color = 53380,
  )
  return(text)

@fun.sub_command(description="Get an random truth question")
async def truth(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Truth command", value="If you want to play truth, you can use this command.")
    await send_first_time_message(ctx, "truth", embed) 

    lines = open("truth.txt", encoding='utf-8').read().splitlines()
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name='Truth question', value=random.choice(lines))
    await ctx.send(embed=embed)

@fun.sub_command(description="Get an compliment")
async def compliment(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Compliment command", value="This command provides you a compliment")
    await send_first_time_message(ctx, "compliment", embed) 

    lines = open("compliments.txt", encoding='utf-8').read().splitlines()
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name='Compliment', value=random.choice(lines))
    await ctx.send(embed=embed)



async def loan_payment(user):
    with open('loan.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Loan'] = 0
    with open('loan.json', 'w') as f:
        json.dump(data, f)
    
    return True

@_bot.event
async def loan_payment_process(ctx):
    with open('loan.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if data[str(ctx.id)]['Loan'] == 0:
        pass
    
    else:
        await asyncio.sleep(259200)
        
        with open("account.json", 'r', encoding='utf-8') as data2:
            file2 = json.load(data2)
        
        if file2[str(ctx.user.id)]["Crypto"] != 0:
            file2[str(ctx.user.id)]["Crypto"] *= 0
            with open("account.json", 'w') as data2:
                json.dump(file2, data2)
        else:
            if len(file2[str(ctx.user.id)]["Inventory"]) != 0:
                file2[str(ctx.user.id)]["Inventory"].clear()
                with open("account.json", 'w') as data2:
                    json.dump(file2, data2)
            else:
                if file2[str(ctx.user.id)]["XP"] >= 500:
                    file2[str(ctx.user.id)]["XP"] -= 500
                    with open("account.json", 'w') as data2:
                        json.dump(file2, data2)
                else:
                    file2[str(ctx.user.id)]["XP"] *= 0
                    with open("account.json", 'w') as data2:
                        json.dump(file2, data2)
                
@_bot.slash_command(description="Pay amount for your loan")
async def pay(ctx, amount: int):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Loan payment command", value="You can pay your loan using this command. To check how much loan is left you can use /lend command.")
    await send_first_time_message(ctx, "pay", embed)  

    with open("account.json", 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)
    
    if data2[str(ctx.user.id)]['Bank'] >= 10000:
        with open("loan.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if amount <= data2[str(ctx.user.id)]['Bank'] :
            if amount <= data[str(ctx.user.id)]['Loan']:

                data[str(ctx.user.id)]['Loan'] -= amount

                with open("loan.json", 'w') as file:
                    json.dump(data, file)  
    
                data2[str(ctx.user.id)]['Bank'] -= amount

                with open("account.json", 'w') as file2:
                    json.dump(data2, file2)

                await ctx.send(f"You have paid {amount} <:nerd_coin:992265892756979735> for your loan")  
            
            else:
                await ctx.send("You cant pay money more than the loan")
        
        else:
            await ctx.send("You don't have enough money to pay your loan")
    
    else:
        await ctx.send("Have at least 10k <:nerd_coin:992265892756979735> to pay for loan")

@fun.sub_command(description="Get some dad jokes")
async def dadjokes(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Dad joke command", value="Dad jokes are stored in a file, with the help of real dads. This command provides you 100% natural dad jokes.")
    await send_first_time_message(ctx, "dadjokes", embed) 

    lines = open("dadjokes.txt", encoding='utf-8').read().splitlines()
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name='Dad joke', value=random.choice(lines))
    await ctx.send(embed=embed)

@_bot.slash_command(description="Check how much of your loan is left")
async def lend(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Loan amount command", value="You can use this command to know how much loan is left to pay. Pay loan by using /pay.")
    await send_first_time_message(ctx, "lend", embed)  
    with open("loan.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    embed = disnake.Embed(title='Your loan', color=random.choice(colors))
    embed.add_field(name='------', value=data[str(ctx.user.id)]["Loan"])
    await ctx.send(embed=embed)

@_bot.slash_command(description="Take loan from bank")
async def loan(ctx, amount: int):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Loaning command", value="You can get a loan using this command. To get a loan you need to have at least 10000 nerd coins and you can't get a loan less than 100000 nerd coins. Loan must be taken in 0s, for example 1000000/100000000/10000000. You can pay your loan using /pay. If you do not pay your loan in 3 days, your items will be taken by the nerd bank, if your items worth the value of loan then your loan will be payed but if still the loan will not be paid then all your crypto currencies will be taken. The deadline of paying any amount of loan is three days. You must pay it, or your inventory, crypto currencies, geek coins will be taken by the nerd bank. Between the process when the nerd bank is taking everything from you, you can't pay your loan.")
    await send_first_time_message(ctx, "loan", embed)  
    
    with open('account.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    with open('loan.json', 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)
    
    if data[str(ctx.user.id)]["Bank"] <= 10000:
        await ctx.send("You need to have at least 10000 <:nerd_coin:992265892756979735> in your bank because you have to pay 10000 per 2 hours")
    
    elif amount <= 100000:
        await ctx.send("You can't buy a loan less than 100000 <:nerd_coin:992265892756979735>")
    
    elif amount % 10 != 0:
        await ctx.send("You can have loan only in 0s for example, 100000/1000000/10000000 etc.")
    
    elif data2[str(ctx.user.id)]['Loan'] != 0:
        await ctx.send(f"You have a loan left of {data2[str(ctx.user.id)]['Loan']} <:nerd_coin:992265892756979735>")

    else:
        await ctx.send(f"You took loan of {amount} <:nerd_coin:992265892756979735>, you need to pay 10k <:nerd_coin:992265892756979735> {amount / 10000} times to finish your loan. You have 3 days to remaining to pay your loan")
        data[str(ctx.user.id)]["Bank"] += amount
        data2[str(ctx.user.id)]["Loan"] += amount

        with open("account.json", 'w') as file:
            json.dump(data, file)
        
        with open("loan.json", 'w') as file2:
            json.dump(data2, file2)

async def labs(user):
    with open('business.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.id) in data:
        return False
    else:
        data[str(user.id)] = {}
        data[str(user.id)]['Income'] = 100
        data[str(user.id)]['Facilities'] = []
        data[str(user.id)]['Bio-res'] = []
        data[str(user.id)]['Space-res'] = []
        data[str(user.id)]['Robo-res'] = []
    
    with open('business.json', 'w') as f: 
        json.dump(data, f)
    
class Spacelab(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Self destruction", style=disnake.ButtonStyle.blurple)
    async def dest(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('business.json', 'r', encoding='utf-8') as file:
            data = json.load(file) 
        
        data[str(interaction.user.id)]['Facilities'].remove("Space research sector 🔭")

        with open("business.json", 'w') as file:
            json.dump(data, file)

        await interaction.response.send_message("You have destroyed radiation lab")

class Radlab(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Self destruction", style=disnake.ButtonStyle.blurple)
    async def dest(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('business.json', 'r', encoding='utf-8') as file:
            data = json.load(file) 
        
        data[str(interaction.user.id)]['Facilities'].remove("Radiation sector ☣")

        with open("business.json", 'w') as file:
            json.dump(data, file)

        await interaction.response.send_message("You have destroyed radiation lab")

class Biolab(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Self destruction", style=disnake.ButtonStyle.blurple)
    async def dest(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('business.json', 'r', encoding='utf-8') as file:
            data = json.load(file) 
        
        data[str(interaction.user.id)]['Facilities'].remove("Bio-Lab sector 🦠")

        with open("business.json", 'w') as file:
            json.dump(data, file)

        await interaction.response.send_message("You have destroyed bio lab")

class Labs(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Get money", style=disnake.ButtonStyle.blurple)
    async def money(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('business.json', 'r', encoding='utf-8') as file:
            data = json.load(file)  
        
        with open("account.json", 'r', encoding='utf-8') as file2:
            data2 = json.load(file2)
        
        data2[str(interaction.user.id)]["Bank"] += data[str(interaction.user.id)]["Income"]

        with open("account.json", 'w') as file2:
            json.dump(data2, file2)
        
        await interaction.response.send_message(f"You have earned {data[str(interaction.user.id)]['Income']} <:nerd_coin:992265892756979735>")
    
    @disnake.ui.button(label="Bio-Lab sector 🦠", style=disnake.ButtonStyle.blurple)
    async def bio_lab(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('business.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        if "Bio-Lab sector 🦠" not in data[str(interaction.user.id)]["Facilities"]:
        
            with open("account.json", 'r', encoding='utf-8') as file2:
                data2 = json.load(file2)
        
            if data2[str(interaction.user.id)]["Bank"] >= 500000:
                data[str(interaction.user.id)]["Income"] += 1000
                data[str(interaction.user.id)]["Facilities"].append("Bio-Lab sector 🦠") 

                with open("account.json", 'w') as file2:
                    json.dump(data2, file2)

                with open("business.json", 'w') as file:
                    json.dump(data, file)

                await interaction.response.send_message("You have increased your income by 1000 <:nerd_coin:992265892756979735> and Bio-Lab sector 🦠 have been added in facilites.")
            
            else:
                await interaction.response.send_message("You need to have 500000 <:nerd_coin:992265892756979735>")

        else:          
            with open('business.json', 'r', encoding='utf-8') as file:
                data = json.load(file)  
            
            embed = disnake.Embed(title="Bio-Lab sector 🦠", color=random.choice(colors))
            await interaction.response.send_message(embed=embed, view=Biolab(), file=disnake.File('/media/codeinstein/Main/projects/bt/biolab.jpeg'))
    
    @disnake.ui.button(label="Radiation sector ☣", style=disnake.ButtonStyle.blurple)
    async def rad(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('business.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        if "Radiation sector ☣" not in data[str(interaction.user.id)]["Facilities"]:
        
            with open("account.json", 'r', encoding='utf-8') as file2:
                data2 = json.load(file2)
        
            if data2[str(interaction.user.id)]["Bank"] >= 600000:
                data[str(interaction.user.id)]["Income"] += 2000
                data[str(interaction.user.id)]["Facilities"].append("Radiation sector ☣") 

                with open("account.json", 'w') as file2:
                    json.dump(data2, file2)

                with open("business.json", 'w') as file:
                    json.dump(data, file)

                await interaction.response.send_message("You have increased your income by 2000 <:nerd_coin:992265892756979735> and Radiation sector ☣ have been added in facilites.")
            
            else:
                await interaction.response.send_message("You need to have 600000 <:nerd_coin:992265892756979735>")

        else:          
            with open('business.json', 'r', encoding='utf-8') as file:
                data = json.load(file)  
            
            embed = disnake.Embed(title="Radiation sector ☣", color=random.choice(colors))
            await interaction.response.send_message(embed=embed, view=Radlab(), file=disnake.File('/media/codeinstein/Main/projects/bt/radlab.jpeg'))
    
    @disnake.ui.button(label="Space research sector 🔭", style=disnake.ButtonStyle.blurple)
    async def sp(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with open('business.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        if "Space research sector 🔭" not in data[str(interaction.user.id)]["Facilities"]:
        
            with open("account.json", 'r', encoding='utf-8') as file2:
                data2 = json.load(file2)
        
            if data2[str(interaction.user.id)]["Bank"] >= 700000:
                data[str(interaction.user.id)]["Income"] += 3000
                data[str(interaction.user.id)]["Facilities"].append("Space research sector 🔭") 

                with open("account.json", 'w') as file2:
                    json.dump(data2, file2)

                with open("business.json", 'w') as file:
                    json.dump(data, file)

                await interaction.response.send_message("You have increased your income by 3000 <:nerd_coin:992265892756979735> and Radiation sector ☣ have been added in facilites.")
            
            else:
                await interaction.response.send_message("You need to have 700000 <:nerd_coin:992265892756979735>")

        else:          
            with open('business.json', 'r', encoding='utf-8') as file:
                data = json.load(file)  
            
            embed = disnake.Embed(title="Space research sector 🔭", color=random.choice(colors))
            await interaction.response.send_message(embed=embed, view=Spacelab(), file=disnake.File('/media/codeinstein/Main/projects/bt/spacelab.jpeg'))

@_bot.slash_command(description='Start your own laboratory')
async def laboratory(ctx):
    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Laboratory business command", value="You can use this command to start a lab business. Researching in lab and you can earn money very easily. To start this career you need to have 1 crore nerd coins. This is a very profitable business and a quick way to earn money.")
    await send_first_time_message(ctx, "laboratory", embed)  

    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    with open("business.json", 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)
    
    if data[str(ctx.user.id)]["Bank"] >= 10000000:
        if str(ctx.user.id) in data2:
            color = disnake.Color(value=random.choice(colors))
            embed = disnake.Embed(title=f"{ctx.user}'s Company", color=color)
            embed.add_field(name="Income", value=data2[str(ctx.user.id)]["Income"])
            await ctx.send(embed=embed, view=Labs())
        
        else:
            await labs(ctx)
            data[str(ctx.user.id)]["Bank"] -= 10000000
            with open("account.json", 'w') as file:
                json.dump(data, file)
            await ctx.send("You have started a lab now, check your lab using the same command.")
    
    else:
        await ctx.send("You need to have at least 10 millions of <:nerd_coin:992265892756979735> to start your own lab")

async def spem(user):
    with open('spam.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  

    if str(user.guild) in data:
        return False                    
    else:
        data[str(user.guild)] = {}
        data[str(user.guild)]['Spam'] = [1]
        data[str(user.guild)]['Dis'] = []
    
    with open('spam.json', 'w') as file:
        json.dump(data, file)  

@mod.sub_command(description="Set the level messages channel")
@commands.has_permissions(administrator=True)
async def levlog(ctx, channel_id, message):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Level up logs command", value="If you dont want level up messages in general channel, then use this command and set up the channel ID where you want the level up messages to be. Requires administrator permissions.")
    await send_first_time_message(ctx, "levlog", embed) 

    with open("setup.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if len(data[str(ctx.guild.id)]["level"]) == 0:
        if len(data[str(ctx.guild.id)]["levelm"]) == 0:
            data[str(ctx.guild.id)]["level"].append(channel_id)
            data[str(ctx.guild.id)]["levelm"].append(message)
            await ctx.send(f"You have set up leveling logs in {_bot.get_channel(channel_id)}")
            with open("setup.json", 'w') as file:
                json.dump(data, file)
        else:
            data[str(ctx.guild.id)]["levelm"].clear()
            with open("setup.json", 'w') as file:
                json.dump(data, file)
            data[str(ctx.guild.id)]["level"].append(channel_id)
            data[str(ctx.guild.id)]["levelm"].append(message)
            with open("setup.json", 'w') as file:
                json.dump(data, file)
            await ctx.send(f"You have set up new leveling logs in {_bot.get_channel(channel_id)}")
    else:
        data[str(ctx.guild.id)]["level"].clear()
        with open("setup.json", 'w') as file:
            json.dump(data, file)
        data[str(ctx.guild.id)]["level"].append(channel_id)
        data[str(ctx.guild.id)]["levelm"].append(message)
        with open("setup.json", 'w') as file:
            json.dump(data, file)
        await ctx.send(f"You have set up new leveling logs in {_bot.get_channel(channel_id)}")

@fun.sub_command(description="Flip a coin")
async def coinflip(ctx):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Coin flip command", value="Simple non-profit command to flip a coin for heads or tails")
    await send_first_time_message(ctx, "fact", embed) 

    coin = random.choice(['heads', 'tails'])
    await ctx.send(f"The coin landed on {coin}!")

@mod.sub_command(description="Enable or disable spam protection")
@commands.has_permissions(administrator = True)
async def spam(ctx): 

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Spam protection toggling command", value="The bot has spam protection enabled so that people cant spam and level up and also to protect this server from spamming. In revenge, the bot spams the DM of spammer. If you want this feature to be turned off then use this command. Remember, spam protection will still be turned on in leveling up system so that user doesnt cheat and that can't be toggled.")
    await send_first_time_message(ctx, "spam", embed) 

    await spem(ctx)
    
    with open('spam.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  
    if 1 in data[str(ctx.guild.id)]['Spam']:
        data[str(ctx.guild.id)]['Spam'][0] += 1
        color = disnake.Color(value=random.choice(colors))
        em = disnake.Embed(color=color, title="Spam protection")
        em.add_field(name='Enabled', value=data[str(ctx.guild.id)]['Spam'])
        await ctx.send(embed=em)
        await ctx.send("Spam protection is now disabled")
        with open('spam.json', 'w') as file:
            json.dump(data, file)  

    else:
        data[str(ctx.guild.id)]['Spam'][0] -= 1
        color = disnake.Color(value=random.choice(colors))
        em = disnake.Embed(color=color, title="Spam protection")
        em.add_field(name='Enabled', value=data[str(ctx.guild.id)]['Spam'])
        await ctx.send(embed=em)
        await ctx.send("Spam protection is now enabled")
    
        with open('spam.json', 'w') as file:
            json.dump(data, file)  

class SendConfirmView(disnake.ui.View):
    def __init__(self, ctx: commands.Context, money: int, sender: disnake.Member, receiver: disnake.Member):
        super().__init__(timeout=30.0)
        self.ctx = ctx
        self.money = money
        self.sender = sender
        self.receiver = receiver

    async def interaction_check(self, interaction: disnake.Interaction):
        return interaction.user.id == self.receiver.id

    @disnake.ui.button(label="Accept Money", style=disnake.ButtonStyle.green)
    async def confirm_gift(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        with open("account.json", 'r', encoding='utf-8') as file:
            data = json.load(file)

        data[str(self.receiver.id)]["Bank"] += self.money
        data[str(self.sender.id)]["Bank"] -= self.money
        with open("account.json", 'w') as file:
            json.dump(data, file)

        color = random.choice(colors)
        embed = disnake.Embed(color=color)
        embed.add_field(name="Success", value=f"{self.receiver.mention} has accepted your transaction of {self.money}.")
        await self.ctx.send(embed=embed)

    @disnake.ui.button(label="Decline Money", style=disnake.ButtonStyle.red)
    async def decline_gift(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        color = random.choice(colors)
        embed = disnake.Embed(color=color)
        embed.add_field(name="Money Declined", value=f"{self.receiver.mention} has declined your transaction of {self.money}.")
        await self.ctx.send(embed=embed, view=None)

@_bot.slash_command(description="Send money to someone")
async def send(ctx, member: disnake.Member, amount: int):

    embed = disnake.Embed(color=random.choice(colors))
    embed.add_field(name="Money sharing command", value="This command can be used to share money to someone, to get money in the reciever's account, they must accept the money. If they decline it. money will stay in sender's account. Once the reciever has accepted the nerd coins, sender can't have them back.")
    await send_first_time_message(ctx, "send", embed)  

    with open("account.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if amount >= data[str(ctx.user.id)]['Bank']:
        await ctx.send(f"You don't have that much money, how would you give it to {member}?")
    else:

        view = SendConfirmView(ctx, amount, ctx.author, member)
        await ctx.send(view=view)

@_bot.event
async def on_message(message):
    with open('spam.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  


    await spem(message)
    if message.guild.id in data:
        if 1 in data[str(message.guild.id)]['Spam']:

                global author_msg_counts

                author_id = message.author.id
                curr_time = datetime.datetime.now().timestamp() * 1000

                if not author_msg_times.get(author_id, False):
                    author_msg_times[author_id] = []

                author_msg_times[author_id].append(curr_time)
                expr_time = curr_time - time_window_milliseconds
                expired_msgs = [
                    msg_time for msg_time in author_msg_times[author_id]
                    if msg_time < expr_time
                ]

                for msg_time in expired_msgs:
                    author_msg_times[author_id].remove(msg_time)

                if len(author_msg_times[author_id]) > max_msg_per_window:
                    color = disnake.Color(value=random.choice(colors))
                    em = disnake.Embed(color=color, title=f"WARNING: by The Nerd from **{message.guild.name}**.",   description="You need to stop spamming")

                    await message.author.send(embed=em)
                
                else:
                    if not message.author.bot:
                        await rep(message.author)
                        await setups(message)
                        await markett(message.author)
                        await open_account(message.author)
                        await xp(message.author, 5)
                        await lvl(message)
                        await coin_boost(message)
                        await xp_boost(message)
                        await kali_installed(message.author)
                        await win10_installed(message.author)
                        await loan_payment(message.author)
                        await loan_payment_process(message.author)
                        await learning_points(message.author)
        
        else:   
            if not message.author.bot:
                await rep(message.author)
                await setups(message)
                await open_account(message.author)
                await crypt(message.author)
                await xp(message.author, 5)
                await lvl(message)
                await coin_boost(message)
                await xp_boost(message)
                await kali_installed(message.author)
                await win10_installed(message.author)
                await loan_payment(message.author)
                await loan_payment_process(message.author)
                await learning_points(message.author)

            else:
                pass
    
    else:   
            if not message.author.bot:
                await setups(message)
                await rep(message)
                await open_account(message.author)
                await crypt(message.author)
                await xp(message.author, 5)
                await lvl(message)
                await coin_boost(message)
                await xp_boost(message)
                await kali_installed(message.author)
                await win10_installed(message.author)
                await loan_payment(message.author)
                await loan_payment_process(message.author)
                await learning_points(message.author)


    await _bot.process_commands(message)

_bot.run("MTA5NTM0ODc3Mjg4NTc2MjE3OQ.GvjV9V.QQqX29z5VLOMqo-8R8f-KaD7X4Kdf1vrI6p4kw")      