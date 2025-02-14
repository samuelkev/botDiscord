import requests
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
API_KEY = "your_api_key"
TOKEN = "your_token"

@bot.command()
async def clima(ctx, *, cidade):
    api_key = API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt-br"
    resposta = requests.get(url).json()
    if resposta["cod"] != 200:
        await ctx.send("Cidade não encontrada.")
        return

    temperatura = resposta["main"]["temp"]
    sensacao = resposta["main"]["feels_like"]
    vento = resposta["wind"]["speed"]*3.6

    await ctx.send(f"Clima em {cidade.capitalize()} 🌡\nTemperatura: {temperatura:.1f}°C\nSensação Térmica: {sensacao:.1f}°C\nVelocidade do Vento: {vento:.2f} km/h")
    
@bot.command()
async def converter(ctx, valor: float, moeda_origem: str, moeda_destino: str):
    moeda_origem = moeda_origem.upper()
    moeda_destino = moeda_destino.upper()
    url = f"https://economia.awesomeapi.com.br/last/{moeda_origem}-{moeda_destino}"
    resposta = requests.get(url).json()
    cotacao = float(resposta[f"{moeda_origem}{moeda_destino}"]["bid"])
    resultado = valor*cotacao
    await ctx.send(f"💰{valor} {moeda_origem} equivale a {resultado:.2f} {moeda_destino}")

@bot.event
async def mensagem(message):
    if message.author == bot.user:
        return
    if message.content.lower() == "oi bot":
        await message.channel.send("Olá! Como posso ajudar?")
    if message.content.lower() == "fale tchau":
        await message.channel.send("Tchau")
    
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)

