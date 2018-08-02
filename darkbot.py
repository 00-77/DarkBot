import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import colorsys
import random
import os

client = Bot(description="DarkBot Bot is best", command_prefix="d!", pm_help = True)
client.remove_command('help')
newUserMessage = """Welcome to Our Server. Hope you will be active here. Check Our server rules and never try to break any rules."""


@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('--------')
    print('Started Dark BOT')
    print('Created by Utkarsh')
    return await client.change_presence(game=discord.Game(name='Looking for d!help'))

def is_owner(ctx):
    return ctx.message.author.id == "420525168381657090"

@client.command(pass_context = True)
@commands.check(is_owner)
async def shutdown():
    await client.logout()



@client.event
async def on_member_join(member):
     print("In our server" + member.name + " just joined")
     await client.send_message(member, newUserMessage)
     print("Sent message to " + member.name)

@client.event
async def on_member_remove(member):
    serverchannel = member.server.default_channel
    msg = "Bye Bye {0}! We will miss you :(. ".format(member.mention)
    await client.send_message(serverchannel, msg)

@client.event
async def on_member_join(member):
    if member.server.id == "404622530129690624":
     print("In our server" + member.name + " just joined")
     nickname = '[GGC]' + member.name
     await client.change_nickname(member, nickname)

@client.event
async def on_member_leave(member):
     server = member.server
     fmt = '{0.mention} just left {1.name}!'
     await client.send_message(server, fmt.format(member, server))

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)     
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)

    
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def setup(ctx):
    author = ctx.message.author
    server = ctx.message.server
    mod_perms = discord.Permissions(manage_messages=True, kick_members=True, manage_nicknames =True,mute_members=True)
    admin_perms = discord.Permissions(ADMINISTRATOR=True)

    await client.create_role(author.server, name="Owner", permissions=admin_perms)
    await client.create_role(author.server, name="Admin", permissions=admin_perms)
    await client.create_role(author.server, name="Senior Moderator", permissions=mod_perms)
    await client.create_role(author.server, name="G.O.H")
    await client.create_role(author.server, name="Moderator", permissions=mod_perms)
    await client.create_role(author.server, name="Muted")
    
    await client.create_role(author.server, name="Friend of Owner")
    await client.create_role(author.server, name="Verified")
    everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
    user_perms = discord.PermissionOverwrite(read_messages=True)
    user = discord.ChannelPermissions(target=server.default_role, overwrite=user_perms)
    private_perms = discord.PermissionOverwrite(read_messages=False)
    private = discord.ChannelPermissions(target=server.default_role, overwrite=private_perms)    
    await client.create_channel(server, '🎉welcome🎉',everyone)
    await client.create_channel(server, '🎯rules🎯',everyone)
    await client.create_channel(server, '🎥featured-content🎥',everyone)
    await client.create_channel(server, '📢announcements📢',everyone)
    await client.create_channel(server, 'private_chat',private)
    await client.create_channel(server, '🎮general_chat🎮',user)
    await client.create_channel(server, '🎮general_media🎮',user)
    await client.create_channel(server, '👍bots_zone👍',user)
    await client.create_channel(server, '🎥youtube_links🎥',user)
    await client.create_channel(server, '🎥giveaway_links🎥',user)
    await client.create_channel(server, '🎥other_links🎥',user)
    await client.create_channel(server, '🔥Music Zone🔥', type=discord.ChannelType.voice)
    await client.create_channel(server, '🔥music_command🔥s',user)
    await client.create_channel(server, '🔥Chill Zone🔥', type=discord.ChannelType.voice)
    
@client.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await client.change_nickname(user, nickname)
    await client.delete_message(ctx.message)

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)     
async def poll(ctx, question, *options: str):
        if len(options) <= 1:
            await client.say('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await client.say('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['👍', '👎']
        else:
            reactions = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001f51f']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=question, description=''.join(description), color = discord.Color((r << 16) + (g << 8) + b))
        react_message = await client.say(embed=embed)
        for reaction in reactions[:len(options)]:
            await client.add_reaction(react_message, reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await client.edit_message(react_message, embed=embed)
        
@client.command(pass_context = True)
async def googlefy(ctx, *, msg = None):
    if not msg: await client.say("Please specify a string")
    else:
        await client.say('http://lmgtfy.com/?q=' + msg)
    return

@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Help')
    embed.add_field(name = 'd!help ',value ='Explaines all the commands',inline = False)
    embed.add_field(name = 'd!authlink ',value ='Use it to get authorizing link to authorize this bot to your server.',inline = False)
    embed.add_field(name = 'd!xp ',value ='Use it to check your chatting experience',inline = False)
    embed.add_field(name = 'd!technews ',value ='Use it to get tech news',inline = False)
    embed.add_field(name = 'd!googlefy ',value ='Use it like ``d!googlegy <string>``.',inline = False)
    embed.add_field(name = 'd!spacenews ',value ='Use it to get space news',inline = False)
    embed.add_field(name = 'd!phynews ',value ='Use it to get physycs',inline = False)
    embed.add_field(name = 'd!verify ',value ='Use it to get verified role. Note- It needs proper setup.',inline = False)
    embed.add_field(name = 'd!removemod(Admins Only)',value ='Use it like ``d!removemod @user`` to remove him from mod. Note-You need Moderator role in your server below darkbot to use it.',inline = False)
    embed.add_field(name = 'd!makemod(Admins Only)',value ='Use it like ``d!makemod @user`` to make him mod. Note-You need Moderator role in your server below darkbot to use it.',inline = False)
    embed.add_field(name = 'd!friend(Owners only) ',value ='Use it like ``d!friend @user`` to give anyone Friend of Owner role',inline = False)
    embed.add_field(name = 'd!poll(Mods only) ',value ='Use it like ``d!poll "Question" "Option1" "Option2" ..... "Option9"``.',inline = False)
    embed.add_field(name = 'd!setnick(Mods only)',value ='Use it like ``d!setnick @user <New nickname>`` to change the nickname of tagged user.',inline = False)
    embed.add_field(name = 'd!english(Mods only)',value ='Use it like ``d!english @user`` when someone speaks languages other than English.',inline = False)
    embed.add_field(name = 'd!serverinfo(Mods only) ',value ='Use it like ``d!serverinfo`` to get server info',inline = False)
    embed.add_field(name = 'd!userinfo(Mods only) ',value ='Use it like ``d!userinfo @user`` to get some basic info of tagged user',inline = False)
    embed.add_field(name = 'd!kick(Mods only)',value ='Use it like ``d!kick @user`` to kick any user',inline = False)
    embed.add_field(name = 'd!clear(Mods only)',value ='Use it like ``d!clear <number>`` to clear any message',inline = False)
    embed.add_field(name = 'd!mute(Mods only)',value ='Use it like ``d!mute @user <time>`` to mute any user',inline = False)
    embed.add_field(name = 'd!unmute(Mods only) ',value ='Use it like ``d!unmute @user`` to unmute anyone',inline = False)
    embed.add_field(name = 'd!ban(Mods only) ',value ='Use it like ``d!ban @user`` to ban any user',inline = False)
    embed.add_field(name = 'd!rules(Mods only)',value ='Use it like ``d!rules @user <violation type>`` to warn user',inline = False)
    embed.add_field(name = 'd!warndm(Mods only)',value ='Use it like ``d!warndm @user <violation type in one word>`` to warn any user in dm',inline = False)
    embed.add_field(name = 'd!norole(Mods only) ',value ='Use it like ``d!norole @user`` to warn anyone if he/she asks for promotion',inline = False)
    await client.send_message(author,embed=embed)


@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     
async def kick(ctx,user:discord.Member):

    if ctx.message.author.server_permissions.kick_members: 
        await client.say('==>')      
        await client.delete_message(ctx.message)

    try:
        await client.kick(user)
        await client.say(user.name+' was kicked. Good bye '+user.name+'!')
        await client.delete_message(ctx.message)


    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('kick failed.')
        return		 	

@client.command(pass_context = True)
@commands.has_permissions(manage_messages=True)  
async def clear(ctx, number):

    if ctx.message.author.server_permissions.ban_members: 
         mgs = [] #Empty list to put all the messages in the log
         number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx.message.channel, limit = number+1):
        mgs.append(x)             
        
    try:
        await client.delete_messages(mgs)          
        await client.say(str(number)+' messages deleted')

    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('clear failed.')
        return			


    await client.delete_messages(mgs)   	

@client.command(pass_context=True)
    
@commands.has_permissions(mute_members=True)      

async def mute(ctx,user:discord.Member):
    if ctx.message.author.server_permissions.mute_members: 
             
       role = discord.utils.get(ctx.message.server.roles,name='Muted')  
    try:
        await client.add_roles(ctx.message.mentions[0], role)	 		
        await client.say('Muted '+user.name+' :mute: ')
          

    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('mute failed.')
        return    	



@client.command(pass_context=True)
    
@commands.has_permissions(mute_members=True)      

async def unmute(ctx,user:discord.Member):
    if ctx.message.author.server_permissions.mute_members: 
             
       role = discord.utils.get(ctx.message.server.roles,name='Muted')       

    try:
        await client.remove_roles(ctx.message.mentions[0], role)	 		
        await client.say('Unmuted '+user.name+' :rofl: ')
    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('mute failed.')
        return        	

    	 		


@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)      
async def ban(ctx,user:discord.Member):

    if ctx.message.author.server_permissions.ban_members: 
        await client.say('==>')      

    try:
        await client.ban(user)
        await client.say(user.name+' was banned. Good bye '+user.name+'!')

    except discord.Forbidden:

        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('ban failed.')
        return		 



@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     


async def unban(ctx):
    ban_list = await client.get_bans(ctx.message.server)

    # Show banned users
    await client.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))

    # Unban last banned user
    if not ban_list:
    	
        await client.say('Ban list is empty.')
        return
    try:
        await client.unban(ctx.message.server, ban_list[-1])
        await client.say('Unbanned user: `{}`'.format(ban_list[-1].name))
    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('unban failed.')
        return		      	 		 		  
  
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def say(ctx, *, msg = None):
    await client.delete_message(ctx.message)

    if not msg: await client.say("Please specify a message to send")
    else: await client.say(msg)
    return

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def rules(ctx, *, msg = None):
    await client.delete_message(ctx.message)

    if not msg: await client.say("Please specify a user to warn")
    else: await client.say(msg + ', Please Read Rules again and never break any one of them again otherwise i will mute/kick/ban you next time.')
    return

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def warndm(ctx, member: discord.Member):
    await client.delete_message(ctx.message)
    await client.send_message(member, ', Please Read <#469507420826238996> and never break any one of them again otherwise i will mute/kick/ban you next time.')
    return

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def dm(ctx, member: discord.Member , msg = None):
    await client.delete_message(ctx.message)
    await client.send_message(member, msg)
    return

@client.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def bans(ctx):
    '''Gets A List Of Users Who Are No Longer With us'''
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of The Banned Idiots", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)

@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     

async def serverinfo(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def norole(ctx, *, msg = None):
    await client.delete_message(ctx.message)

    if not msg: await client.say("Please specify a user to warn")
    else: await client.say(msg + ', Please Do not ask for promotions check Rules again.')
    return

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def english(ctx, *, msg = None):
    await client.delete_message(ctx.message)

    if not msg: await client.say("Please specify a user to warn")
    else: await client.say(msg + ', Please do not use languages other than **English.**')
    return
    
@client.command(pass_context=True)
async def unverify(ctx):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='Unverified')
    await client.add_roles(ctx.message.author, role)
    
@client.command(pass_context=True)
async def verify(ctx):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='Verified')
    await client.add_roles(ctx.message.author, role)
    
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def friend(ctx, user:discord.Member,):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='Friend of Owner')
    await client.add_roles(ctx.message.mentions[0], role)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def makemod(ctx, user:discord.Member):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='Moderator')
    await client.add_roles(ctx.message.mentions[0], role)
    
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def removemod(ctx, user:discord.Member):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='Moderator')
    await client.remove_roles(ctx.message.mentions[0], role)

client.run(os.getenv('Token'))
