import os
import discord
import asyncio
import logging
from discord.ext import commands
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

# =========================
# 🔐 SERVIDOR ÚNICO (TU SERVER)
# =========================
GUILD_ID = 1501321773570986176

# =========================
# 🌐 KEEP ALIVE
# =========================
def run_web():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot activo")

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

Thread(target=run_web, daemon=True).start()

# =========================
# 📊 LOGS
# =========================
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot")

# =========================
# 🤖 BOT
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# 💾 LOG CHANNEL
# =========================
log_channel_id = None

# =========================
# 🔒 BLOQUEO GLOBAL
# =========================
def check_guild(ctx):
    return ctx.guild and ctx.guild.id == GUILD_ID

# =========================
# 📌 SET LOG CHANNEL
# =========================
@bot.command()
async def setlog(ctx, channel: discord.TextChannel):

    if not check_guild(ctx):
        return

    global log_channel_id
    log_channel_id = channel.id

    await ctx.send(f"✅ Canal de logs configurado: {channel.mention}")

# =========================
# 💣 EVENTO (PROTEGIDO)
# =========================
@bot.command()
@commands.has_permissions(administrator=True)
async def mamamia(ctx, cantidad: int):

    if not check_guild(ctx):
        return

    cantidad = max(1, min(cantidad, 50))

    await ctx.send("⚠️ Ejecutando evento...")

    guild = ctx.guild

    # borrar canales
    for ch in list(guild.channels):
        try:
            await ch.delete()
            await asyncio.sleep(0.2)
        except:
            pass

    await asyncio.sleep(2)

    # crear canales
    for i in range(cantidad):
        try:
            await guild.create_text_channel(f"evento-{i+1}")
            await asyncio.sleep(0.2)
        except:
            pass

    # =========================
    # 📤 LOGS
    # =========================
    if log_channel_id:
        channel = guild.get_channel(log_channel_id)

        if channel:
            embed = discord.Embed(
                title="🔥 Registro de Evento",
                color=discord.Color.red()
            )

            embed.add_field(name="📊 Canales creados", value=str(cantidad), inline=False)
            embed.add_field(name="🏷️ Servidor", value=guild.name, inline=False)

            await channel.send(embed=embed)

# =========================
# 🚀 START
# =========================
bot.run(os.getenv("TOKEN"))
