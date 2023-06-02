# The-Nerd

A unique themed and multi purpose discord bot, for your server! with a large economy system running many tasks behind the mask!

• 100+ commands

• Unique themed economy

• A never ending fictional game

• Bunch of different usable items

• Robot pets

• Active development and new features always coming up

• Levelling system and leaderboards

The Nerd has 100+ commands to make your server a better place and a fun place. It has one of the most unique economy systems you will ever find in discord bots. It has some unique moderator features as well such as spam protection. You can add it from the button below. You can also join support server to report any error in the bot or any kind of support. Have fun!

# Use The Nerd's commands in your bots!

```bash
pip install thenerd
```

```py

import thenerd
import disnake # pip install disnake
from disnake.ext import commands
intents = disnake.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help') # Important

@bot.slash_command()
async def example(ctx):
    await thenerd.meme(ctx)
    
# Put this code at the end of your file

@bot.event
async def on_message(message):
        with open('spam.json', 'r', encoding='utf-8') as file:
            data = json.load(file)  
                
        if not message.author.bot:
            try:
                await setups(message)
                await xp(message.author, 5)
                await lvl(message)
                await open_account(message.author)
                await taxes(message)
                await run_tas(message)
                await crypt(message.author)
                await coin_boost(message)
                await xp_boost(message)
                await kali_installed(message.author)
                await win10_installed(message.author)
                await loan_payment(message.author)
                await loan_payment_process(message.author)
                await learning_points(message.author)
                await tax_alert(message)
                await tax_payment_process(message)
                await loan_alert(message)
                await markett(message.author)
                await rep(message)
            except:
                pass
        else:
                pass

        await bot.process_commands(message)  

```
When using thenerd framework in your bots, the footer of credits will be there. If you want to remove it, E-mail at **aryapraneil@gmail.com**.

**Add The Nerd and view all of it's command**: https://discord.com/api/oauth2/authorize?client_id=1095348772885762179&permissions=70368744177655&scope=bot

**Join our server**: https://discord.gg/HqY4BWmgS9

**The Nerd's website**: https://thenerd.onrender.com/

**Vote The Nerd**: https://discordbotlist.com/bots/the-nerd/upvote | https://top.gg/bot/1095348772885762179/vote 

**Donation**

<a href="https://www.buymeacoffee.com/enginesteinl" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
<a href='https://ko-fi.com/enginestein' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' />
