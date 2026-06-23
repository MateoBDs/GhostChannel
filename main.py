import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

SERVIDORES_PERMITIDOS = [
    123456789012345678,
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def mamamia(ctx, cantidad: int):
    if ctx.guild is None:
        return

    if ctx.guild.id not in SERVIDORES_PERMITIDOS:
        await ctx.send("Servidor no autorizado.")
        return

    cantidad = min(cantidad, 50)

    for i in range(cantidad):
        await ctx.guild.create_text_channel(f"evento-{i+1}")

    await ctx.send(f"Se crearon {cantidad} canales.")

bot.run(TOKEN)
