import discord
import requests
from discord.ext import commands
import json
import asyncio
import time
import datetime
from datetime import datetime , timedelta
#from functions import *
#from LikesViews import *
#from LikeViewscall import *
#import Profil_info_script
#import friendcode_script
#import premium_functions
#import premium_lv
#import premiumcall

#buy to boost <> Discord Saad#2240

intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
launch_flag = True
bot = commands.Bot(command_prefix="!", intents=intents)

user_email = ""
user_password = ""

premium_role = 0  # ID of the premium role
owner_id = 0 # owner role id
free_likes_channel_id = 0 # WHERE FREE LIKES CAN BE USED ONLY
premium_channel_id = 0 # PREMIUM ChANNEL ID
announce_channel = 0 # ANNOUNCEMENT FROM BOT _ CHANEL ID *(WHERE TO SEND)
staff_channel_id = 0 #STAFF CHANEL ID
premium_log_channel_id = 0  # ID of the log channel to send premium  logs
likes_views_log_channel_ID = 0 # ID OF LOGS CHANNEL FOR LIKES AND VIEWS
premium_xp_channel_id = 0
premium_lv_channel_id = 0
premium_gems_channel_id = 0
premium_lv_logs_channel_id = 0
premium_commands_chanel_id = 0

bot.remove_command('help')

PREMIUM_USER_DATA_FILE = "premium_user_data.json"

@bot.event
async def on_ready():
    bot.user_data = {}
    print(f"Bot connected as {bot.user.name}")
    print('Bot is ready!')
    print('Loop starting')
    bot.loop.create_task(process_command_queue())
    print('Loop 1 started ( QUEUE STARTED FREE LIKE VIEW COMMAND)')
    bot.loop.create_task(process_command_queue_like())
    print('Loop 2 started ( QUEUE STARTED PREMIUM LIKE COMMAND)')
    bot.loop.create_task(process_command_queue_view())
    print('Loop 3 started ( QUEUE STARTED PREMIUM VIEW COMMAND)')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name='Likes and Views'
    ))
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name='Your Commands'
    ))
    await bot.wait_until_ready()
    while not bot.is_closed():
        if is_new_day():
            reset_balances()
            print("New day! Balances have been reset.")
        await asyncio.sleep(60)  # Check every minute



@bot.command()
async def helpme(ctx):
    embed = discord.Embed(title="Bot Help ! ", description="List of available commands:", color=discord.Color.blue())
    embed.add_field(name="!daily [friendcode]", value="Get Daily 25 Likes And Views (FREE FOR EVERYONE)",inline=True)
    embed.add_field(name="!resolve [friendcode]", value="Resolve Your friendcode ",inline=False)
    embed.add_field(name="!profile", value="Displays your profile information",inline=False)
    embed2 = discord.Embed(title="Bot Premium Help ! ", description="List of available commands:", color=discord.Color.blue())
    embed2.add_field(name="!login", value="Login into your account safely (premium)",inline=False)
    embed2.add_field(name="!logout", value="Logout from your account (premium)",inline=False)
    embed2.add_field(name="!dailygems", value="Get Gems Boost daily (premium)",inline=False)
    embed2.add_field(name="!dailyxp", value="Get daily xp boosting (premium)",inline=False)
    embed2.add_field(name="!wallet", value="Displays your likes and views remaining (premium)",inline=False)
    embed2.add_field(name="!dailylikes {amount} {friendcode}", value="For example !dailylikes 500 xyz-xyz (premium)",inline=False)
    embed2.add_field(name="!dailyviews {amount} {friendcode}", value="For example !dailyviews 500 xyz-xyz (premium)",inline=False)


    embed.set_thumbnail(url="https://i.gifer.com/NRI0.gif")
    embed.set_thumbnail(url="https://i.gifer.com/NRI0.gif")
    embed2.set_thumbnail(url="https://i.gifer.com/67Pg.gif")
    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)

@bot.command()
@commands.has_role(owner_id)
async def announce(ctx, *, message):
    announcement_channel = bot.get_channel(announce_channel)
    if announcement_channel:
        await announcement_channel.send(message)
        await ctx.send('Announcement sent to the announcement channel.')
    else:
        await ctx.send('Announcement channel not found.')

@bot.command()
@commands.has_role(owner_id)
async def staff(ctx, *, message):
    staff_channel = bot.get_channel(staff_channel_id)
    if staff_channel:
        await staff_channel.send(message)
        await ctx.send('Message sent to the staff channel.')
    else:
        await ctx.send('Staff channel not found.')

def in_freelikeschannel():
    async def predicate(ctx):
        return ctx.channel.id == free_likes_channel_id
    return commands.check(predicate)

command_queue = asyncio.Queue()
command_queue_like = asyncio.Queue()
command_queue_view = asyncio.Queue()

@bot.command()
@in_freelikeschannel()
@commands.cooldown(1, 0, commands.BucketType.user)  # 43200 seconds = 12 hours
async def daily(ctx, message):
    await ctx.send(f"Buy to boost @discord Username : Saad#2240 {ctx.author.mention}")
    #await ctx.send(f"Your Command is in queue please be patient {ctx.author.mention}")
    #await command_queue.put((ctx, message))

#$ PROFCAESS QUEUE

async def process_command_queue():
    while True:
        if not command_queue.empty():
            start_time = time.time()  # Get the start time of command processing
            ctx, message = await command_queue.get()

            cleaned_message = message.replace('-', '')
            #id = friendcode_script.login_and_convert_friendcode(cleaned_message)
            if id == 0:
                await ctx.send(f"Error: Wrong  Friend-code {ctx.author.mention}")
                command_queue.task_done()
                continue
            #data_redata_received = Profil_info_script.login_and_convert_friendcode(cleaned_message)
            #username = data_redata_received['data']['main']['profile']['result']['username']
           # like = data_redata_received['data']['main']['profile']['result']['likes']
           # hits = data_redata_received['data']['main']['profile']['result']['hits']
           # level = data_redata_received['data']['main']['xp']['result']['lkwd']['avakinlife']['level']
            thumbnail_url = f"https://media.avakin.life/thumbnails/{id}:profile_headshot:256x256"

            embed = discord.Embed(title="Likes and Views are now being sent", color=discord.Color.blue())
            embed.set_thumbnail(url=thumbnail_url)
            embed.add_field(name="After completion you will be notified", value=" ", inline=False)
           # embed.add_field(name="Username", value=username, inline=False)
           # embed.add_field(name="Likes", value=like, inline=True)
           # embed.add_field(name="Views", value=hits, inline=True)
           # embed.add_field(name="Level", value=level, inline=True)
            await ctx.send(f"Now Processing your request! {ctx.author.mention}...")
            await ctx.send(embed=embed)

            #await process(id) # Buy to boost

            elapsed_time = time.time() - start_time
            if elapsed_time > 600:  # If elapsed time is greater than 10 minutes (600 seconds)
                print(f"There was some error from your side Please try again {ctx.author.mention}")
                command_queue.task_done()  # Mark the command as done

            log_channel = ctx.guild.get_channel(likes_views_log_channel_ID)
            log_embed = discord.Embed(
                title="Your Likes and views have been sent 25 Views and 25 Likes Enjoy !",
                description=f"You can enjoy daily free likes views :) {ctx.author.mention}",
                color=discord.Color.green()
            )
            await log_channel.send(f"{ctx.author.mention}:tada: :tada: ")
            await log_channel.send(embed=log_embed)

            # Mark the command as done in the queue
            command_queue.task_done()
        else:
            # Wait for a while before checking the queue again
            await asyncio.sleep(1)


@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = round(error.retry_after / 3600)  # Convert seconds to hours and round it
        await ctx.send(f"{ctx.author.mention}, you can use the `likes` command again in {remaining_time} hours.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"{ctx.author.mention}, This command can only be used in the specific Free likes channel.")


@bot.command()
async def resolve(ctx, message):
    cleaned_message = message.replace('-', '')
    #id = friendcode_script.login_and_convert_friendcode(cleaned_message)
    await ctx.send(f"Resolved ID  : {id} ")


@bot.command()
async def profile(ctx, message):
    cleaned_message = message.replace('-', '')
    #data_redata_received = Profil_info_script.login_and_convert_friendcode(cleaned_message)
    #username = data_redata_received['data']['main']['profile']['result']['username']
    #like = data_redata_received['data']['main']['profile']['result']['likes']
    #hits = data_redata_received['data']['main']['profile']['result']['hits']
    #level = data_redata_received['data']['main']['xp']['result']['lkwd']['avakinlife']['level']
    #friend = data_redata_received['data']['main']['profile']['result']['friends_count']
    #await ctx.send(f"Data : \n Username : {username} \n Likes : {like} \n Hits : {hits} \n Level : {level} \n Friends : {friend} ")
    await ctx.send("Buy to use all features")


@bot.command()
@commands.has_role(premium_role)
async def login(ctx):
    server_id = str(ctx.guild.id)
    #check_file_exists(server_id)

    user_id = str(ctx.author.id)

   # if is_user_logged_in(server_id, user_id):
   #     await ctx.send(f"{ctx.author.mention} You are already logged in.")
   #     return
    await ctx.send("Buy to use all features")

    await ctx.send("Please check your DMs for the login process.")

    dm_channel = await ctx.author.create_dm()
    await dm_channel.send("Enter your email:")
    email_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    await dm_channel.send("Enter your password:")
    password_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    email = email_msg.content
    password = password_msg.content

   #if is_email_taken(server_id, email):
    #    await dm_channel.send("This email is in use , if this is an error please create a support ticket.")
    #    return

    login_url = "demo.api/auth"# purchase to use boosting

    login_headers = {
        #Headers for api
    }

    login_payload = {
        #request body
    }

    response = requests.post(login_url, headers=login_headers, json=login_payload)

    if response.status_code == 200:
        print("LOGIN SUCCESS!")
        #save_credentials(server_id, user_id, email, password)
        #await dm_channel.send("You have been Logged in securely! Please Have fun using our boosting Service :tada: \n \n                                                                                                                          Boss Boosting V2")
    else:
        #await dm_channel.send("Dear User, Your login info is not correct, please type !login again in server to retry")
        print("Connection error:", response.status_code, response.text)
        await ctx.send("Buy to use all features")


@bot.command()
@commands.has_role(premium_role)
async def logout(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    #if not is_user_logged_in(server_id, user_id):
    #    await ctx.send(f"{ctx.author.mention} You are not logged in. Please Type !login")
    #    return

    #change_user_id(server_id, user_id)
    await ctx.send(f"{ctx.author.mention} You have been Logged out")




def inxpchannel():
    async def predicate(ctx):
        if ctx.channel.id != premium_xp_channel_id:
            await ctx.send("You can't use this command in this channel, use Premium XP Channel")
            return False
        return True
    return commands.check(predicate)


@bot.command()
@commands.has_role(premium_role)
@inxpchannel()
@commands.cooldown(1, 86400, commands.BucketType.user)  # 43200 seconds = 12 hours
async def dailyxp(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    #if not is_user_logged_in(server_id, user_id):
    #    await ctx.send(f"{ctx.author.mention} You are not logged in. Please Type !login")
    #    return

    #email, password = get_credentials(server_id, user_id)
    await ctx.send(f"{ctx.author.mention} Your Daily XP boost will start when purchased")
    #await login_and_collect_xp(email, password) # purchase to use the boosting
    await ctx.send(f"{ctx.author.mention} Discord Saadd#2240.")




def in_gemschannel():
    async def predicate(ctx):
        if ctx.channel.id != premium_gems_channel_id:
            await ctx.send("You can't use this command in this channel, Please use assigned Premium gems Boosting Channel")
            return False
        return True
    return commands.check(predicate)


@bot.command()
@commands.has_role(premium_role)
@in_gemschannel()
@commands.cooldown(1, 86400, commands.BucketType.user)  # 43200 seconds = 12 hours
async def dailygems(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    #if not is_user_logged_in(server_id, user_id):
    #    await ctx.send(f"{ctx.author.mention}You are not logged in.")
    #    return

    #email, password = get_credentials(server_id, user_id)
    await ctx.send(f"{ctx.author.mention} Daily Gems Collection ! Buy to boost")

    #loop = asyncio.get_event_loop()
    #await loop.run_in_executor(None, gems_script.login_and_collect_gems, email, password) Purchase to use the gems boost script

    await ctx.send(f"{ctx.author.mention}! Buy to boost @discord Username : Saad#2240")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Please try again. use !helpme to get command list !! Buy to boost @discord Username : Saad#2240 ")

@bot.event
async def on_message(message):
    if not message.author.bot:
        await bot.process_commands(message)

@bot.command()
async def hi(ctx):
    user = ctx.message.author
    await ctx.send(f"Hi, {user.name}!")


async def start(email2, passowrd2):
    print("getting user email and password ")
    global user_email
    global user_password
    user_email = email2
    user_password = passowrd2
    #login_and_collect_xp() #purchase the script to use it


# Function to load premium user data from file
def load_premium_user_data():
    try:
        with open(PREMIUM_USER_DATA_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

# Function to save premium user data to file
def save_premium_user_data(data):
    with open(PREMIUM_USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Function to check if a user has premium role
def has_premium_role(user):
    premium_role_id = premium_role  # Replace with the actual premium role ID
    return any(role.id == premium_role_id for role in user.roles)

# Function to reset balances for all premium users
def reset_balances():
    data = load_premium_user_data()
    for user_id in data:
        data[user_id]["likes_balance"] += 0
        data[user_id]["views_balance"] += 0
    save_premium_user_data(data)

# Function to check if it's a new day
def is_new_day():
    current_time = datetime.now().time()
    return current_time.hour == 0 and current_time.minute == 0

# Command: !wallet
@bot.command()
async def wallet(ctx):
    user = ctx.author
    data = load_premium_user_data()

    if has_premium_role(user):
        user_id = str(user.id)
        if user_id in data:
            likes_balance = data[user_id]["likes_balance"]
            views_balance = data[user_id]["views_balance"]

            if is_new_day():
                reset_balances()
                await ctx.send("New day! Balances have been reset.")
            else:
                embed = discord.Embed(title="Premium User Daily Balance", color=0x00ff00)
                embed.add_field(name="Likes Balance", value=likes_balance, inline=False)
                embed.add_field(name="Views Balance", value=views_balance, inline=False)
                embed.set_thumbnail(url="https://onlinepngtools.com/images/examples-onlinepngtools/sunset.gif")
                await ctx.send(embed=embed)
        else:
            if user_id == "000" or user_id == "000": # to remove users from getting daily balance

                data[user_id] = {"likes_balance": 0, "views_balance": 0}  # Create user data if not found
            else:
                data[user_id] = {"likes_balance": 0, "views_balance": 0}  # Create user data if not found
            save_premium_user_data(data)
            await ctx.send("Created your brand new wallet! Type !wallet again to see your balance.")

            #data[user_id] = {"likes_balance": 13000, "views_balance": 13000}  # Create user data if not found
            #save_premium_user_data(data)
            #await ctx.send("No user data found. Created new user data.")
    else:
        await ctx.send("This command is only available to premium users.")



def inlikeschannel():
    async def predicate(ctx):
        if ctx.channel.id != premium_lv_channel_id:
            await ctx.send("You can't use this command in this channel., Use premium likes/views channel")
            return False
        return True
    return commands.check(predicate)



# Command: !dailylikes {amount} {friendcode}
@bot.command()
@commands.has_role(premium_role)
@inlikeschannel()
async def dailylikes(ctx, amount: int, friendcode :str):
    if amount <= 0:
        await ctx.send("Amount must be positive.")
        return
    user = ctx.author
    data = load_premium_user_data()

    if has_premium_role(user):
        user_id = str(user.id)
        if user_id in data:
            likes_balance = data[user_id]["likes_balance"]
            if amount <= likes_balance:
                data[user_id]["likes_balance"] -= amount
                save_premium_user_data(data)
                # await command_queue.put((ctx, message))
                await ctx.send(f"Successfully sending {amount} likes from your balance!")
                await command_queue_like.put((ctx, amount, friendcode))
                await ctx.send(f"{ctx.author.mention} Now Command is in Queue , Please be patient! {amount} likes will be sent soon")

            else:
                await ctx.send("Insufficient likes balance.")
        else:
            await ctx.send("No user data found. Please use the !wallet command first.")
    else:
        await ctx.send("This command is only available to premium users.")


def inlikeschannel():
    async def predicate(ctx):
        if ctx.channel.id != premium_lv_channel_id:
            await ctx.send("You can't use this command in this channel.")
            return False
        return True
    return commands.check(predicate)


# Command: !dailyviews {amount} {friendcode}
@bot.command()
@inlikeschannel()
@commands.has_role(premium_role)
async def dailyviews(ctx, amount: int, friendcode: str):
    if amount <= 0:
        await ctx.send("Amount must be positive.")
        return
    user = ctx.author
    data = load_premium_user_data()

    if has_premium_role(user):
        user_id = str(user.id)
        if user_id in data:
            views_balance = data[user_id]["views_balance"]
            if amount <= views_balance:
                data[user_id]["views_balance"] -= amount
                save_premium_user_data(data)
                await ctx.send(f"{ctx.author.mention} Successfully used {amount} views from your balance!")
                await command_queue_view.put((ctx, amount, friendcode))
                await ctx.send(f"{ctx.author.mention} Command is in Queue , Please be patient!")
            else:
                await ctx.send("Insufficient views balance.")
        else:
            await ctx.send("No user data found. Please use the !wallet command first.")
    else:
        await ctx.send("This command is only available to premium users.")



async def process_command_queue_like():
    while True:
        if not command_queue_like.empty():
            ctx, amount , message = await command_queue_like.get()

            cleaned_message = str(message.replace('-', ''))
            #id = friendcode_script.login_and_convert_friendcode(cleaned_message)
            if id == 0:
                await ctx.send(f"Error: Wrong  Friend-code {ctx.author.mention}")
                command_queue_like.task_done()
                continue
            #data_redata_received = Profil_info_script.login_and_convert_friendcode(cleaned_message)
            #username = data_redata_received['data']['main']['profile']['result']['username']
            #like = data_redata_received['data']['main']['profile']['result']['likes']
           # hits = data_redata_received['data']['main']['profile']['result']['hits']
            #level = data_redata_received['data']['main']['xp']['result']['lkwd']['avakinlife']['level']
            thumbnail_url = f"https://media.avakin.life/thumbnails/{id}:profile_headshot:256x256"

            embed = discord.Embed(title="Likes are now being sent", color=discord.Color.blue())
            embed.set_thumbnail(url=thumbnail_url)
            embed.add_field(name="After completion you will be notified", value=" ", inline=False)
           # embed.add_field(name="Username", value=username, inline=False)
           # embed.add_field(name="Likes", value=like, inline=True)
           # embed.add_field(name="Views", value=hits, inline=True)
            #embed.add_field(name="Level", value=level, inline=True)
            await ctx.send(f"Now Processing your request! {ctx.author.mention}...")
            await ctx.send(embed=embed)

            v=0
            #await premiumcall.p_process(id,amount,v)

            log_channel = ctx.guild.get_channel(premium_lv_logs_channel_id)
            log_embed = discord.Embed(
                title=f"{amount} Likes have been sent !",
                description=f"{amount} Like Balance has been deducted from your balance :) {ctx.author.mention}",
                color=discord.Color.green()
            )
            await log_channel.send(f"{ctx.author.mention}:tada: :tada: ")
            await log_channel.send(embed=log_embed)

            # Mark the command as done in the queue
            command_queue_like.task_done()
        else:
            # Wait for a while before checking the queue again
            await asyncio.sleep(1)

async def process_command_queue_view():
    while True:
        if not command_queue_view.empty():
            ctx, amount , message = await command_queue_view.get()

            cleaned_message = str(message.replace('-', ''))
            #id = friendcode_script.login_and_convert_friendcode(cleaned_message)
            if id == 0:
                await ctx.send(f"Error: Wrong  Friend-code {ctx.author.mention}")
                command_queue_view.task_done()
                continue
            #data_redata_received = Profil_info_script.login_and_convert_friendcode(cleaned_message)
           # username = data_redata_received['data']['main']['profile']['result']['username']
           # like = data_redata_received['data']['main']['profile']['result']['likes']
           # hits = data_redata_received['data']['main']['profile']['result']['hits']
           # level = data_redata_received['data']['main']['xp']['result']['lkwd']['avakinlife']['level']
            thumbnail_url = f"https://media.avakin.life/thumbnails/{id}:profile_headshot:256x256"

            embed = discord.Embed(title="Views are now being sent", color=discord.Color.blue())
            embed.set_thumbnail(url=thumbnail_url)
            embed.add_field(name="After completion you will be notified", value=" ", inline=False)
            #embed.add_field(name="Username", value=username, inline=False)
            #embed.add_field(name="Likes", value=like, inline=True)
            #embed.add_field(name="Views", value=hits, inline=True)
            #embed.add_field(name="Level", value=level, inline=True)
            await ctx.send(f"Now Processing your request! {ctx.author.mention}...")
            await ctx.send(embed=embed)


            Lg=0
            #await premiumcall.p_process(id,Lg,amount)

            log_channel = ctx.guild.get_channel(likes_views_log_channel_ID)
            log_embed = discord.Embed(
                title=f"{amount} Views have been sent !",
                description=f"{amount} Views Balance has been deducted from your balance :) {ctx.author.mention}",
                color=discord.Color.green()
            )
            await log_channel.send(f"{ctx.author.mention}:tada: :tada: ")
            await log_channel.send(embed=log_embed)

            # Mark the command as done in the queue
            command_queue_view.task_done()
        else:
            # Wait for a while before checking the queue again
            await asyncio.sleep(1)




def is_specific_user():
    def predicate(ctx):
        return ctx.author.id == 00
    return commands.check(predicate)

# Command: !updatelikes @user {amount}
@bot.command()
@is_specific_user()
async def updatelikes(ctx, member: discord.Member, amount: int):
    user = ctx.author
    data = load_premium_user_data()

    if has_premium_role(user):
        user_id = str(member.id)
        if user_id in data:
            data[user_id]["likes_balance"] += amount
            save_premium_user_data(data)
            await ctx.send(f"Updated likes balance for {member.mention} by {amount}.")
        else:
            await ctx.send(f"No user data found for {member.mention}. Please use the !wallet command first.")
    else:
        await ctx.send("This command is only available to premium users.")

# Command: !updateviews @user {amount}
@bot.command()
@is_specific_user()
async def updateviews(ctx, member: discord.Member, amount: int):
    user = ctx.author
    data = load_premium_user_data()

    if has_premium_role(user):
        user_id = str(member.id)
        if user_id in data:
            data[user_id]["views_balance"] += amount
            save_premium_user_data(data)
            await ctx.send(f"Updated views balance for {member.mention} by {amount}.")
        else:
            await ctx.send(f"No user data found for {member.mention}. Please use the !wallet command first.")
    else:
        await ctx.send("This command is only available to premium users.")



bot.run('Token here')
