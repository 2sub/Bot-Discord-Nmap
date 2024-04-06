import discord
import subprocess
import asyncio
import ipaddress
import requests
import socket  
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

local_ip_ranges = [
    ipaddress.IPv4Network('127.0.0.0/8'),
    ipaddress.IPv4Network('10.0.0.0/8'),
    ipaddress.IPv4Network('172.16.0.0/12'),
    ipaddress.IPv4Network('192.168.0.0/16'),
]

@bot.event
async def on_ready():
    print(f'{bot.user} connect')


@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(title="Aide", description="Voici la liste des commandes disponibles :", color=discord.Color.blue())
    embed.add_field(name="!nmap [ip]", value="Effectue un scan Nmap sur l'adresse IP fournie.", inline=False)
    embed.add_field(name="!ping [ip]", value="Effectue un ping vers l'adresse IP fournie.", inline=False)
    embed.add_field(name="!scan [url]", value="Effectue un scan HTTP sur l'URL fournie.", inline=False)
    await ctx.send(embed=embed)



@bot.command(name='nmap')
async def nmap_command(ctx, *args):
    if not args:
        await ctx.send("Veuillez fournir les arguments nécessaires.")
        return

    target_ip = args[-1]  
    if is_local_ip(target_ip):
        await ctx.send("Les scans d'adresses IP locales ne sont pas autorisés.")
        return

    try:
        result = await run_nmap(args)
        embed = discord.Embed(title="Résultat de Nmap", description=f"```\n{result}\n```", color=discord.Color.green())
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Erreur Nmap", description=f"Une erreur s'est produite : {e}", color=discord.Color(0xFF5733)) # Rouge intense
        await ctx.send(embed=embed)

def is_local_ip(ip):
    ip_obj = ipaddress.IPv4Address(ip)
    for local_range in local_ip_ranges:
        if ip_obj in local_range:
            return True
    return False

async def run_command(command, args):
    try:
        process = await asyncio.create_subprocess_exec(command, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return f"Commande exécutée avec succès:\n{stdout.decode('latin-1')}"
        else:
            return f"Erreur lors de l'exécution de la commande:\n{stderr.decode('latin-1')}"
    except Exception as e:
        raise e

@bot.command(name='ping')
async def ping_command(ctx, *args):
    if not args:
        await ctx.send("Veuillez fournir une adresse IP à ping.")
        return

    target_ip = args[-1]
    if is_local_ip(target_ip):
        await ctx.send("Les pings vers des adresses IP locales ne sont pas autorisés.")
        return

    try:
        result = await run_command("ping", args)
        embed_color = discord.Color.green() if "Commande exécutée avec succès" in result else discord.Color(0xFF5733) # Rouge intense
        embed = discord.Embed(title="Résultat du Ping", description=f"```\n{result}\n```", color=embed_color)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Erreur Ping", description=f"Une erreur s'est produite : {e}", color=discord.Color(0xFF5733)) # Rouge intense
        await ctx.send(embed=embed)

async def run_nmap(args):
    return await run_command("nmap", args)

@bot.command(name='scan')
async def scan_command(ctx, url):
    try:
        full_url = "https://" + url
        response = requests.get(full_url)
        if response.status_code == 200:
            headers = response.headers
            await ctx.send(f"En-têtes HTTP pour {full_url} :\n```{headers}```")
            
            ip_address = get_ip_address(url)
            if ip_address:
                embed = discord.Embed(title="Adresse IP", description=f"L'adresse IP de {url} est : {ip_address}", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Erreur de Résolution", description=f"Impossible de résoudre l'adresse IP de {url}", color=discord.Color(0xFF5733)) # Rouge intense
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Erreur HTTP", description=f"Le lien {full_url} n'est pas accessible. Code d'état : {response.status_code}", color=discord.Color(0xFF5733)) # Rouge intense
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Erreur", description=f"Une erreur s'est produite : {e}", color=discord.Color(0xFF5733)) # Rouge intense
        await ctx.send(embed=embed)

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

bot.run('TOKEN')
