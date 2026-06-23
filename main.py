import os
import discord
import asyncio
from discord.ext import commands
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

# =========================
# 🌐 KEEP ALIVE (RENDER)
# =========================
def run_web():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot activo")

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

Thread(target=run_web).start()

# =========================
# 🔐 CONFIG
# =========================
TOKEN = os.getenv("TOKEN")

SERVIDORES_PERMITIDOS = [
    1502216163084472381,
]

# =========================
# 🤖 BOT SETUP
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# 💣 RESET COMANDO
# =========================
@bot.command()
@commands.has_permissions(administrator=True)
async def mamamia(ctx, cantidad: int):

    if ctx.guild is None:
        return

    if ctx.guild.id not in SERVIDORES_PERMITIDOS:
        await ctx.send("❌ Servidor no autorizado.")
        return

    cantidad = max(1, min(cantidad, 50))

    await ctx.send("⚠️ Iniciando reset del servidor...")

    guild = ctx.guild

    # =========================
    # 🔥 BORRAR CANALES
    # =========================
    channels = guild.channels[:]

    for channel in channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.2)  # evita rate limits
        except Exception as e:
            print(f"Error borrando canal: {e}")

    await asyncio.sleep(3)

    # =========================
    # 📁 CREAR CANALES
    # =========================
    created = 0

    for i in range(cantidad):
        try:
            await guild.create_text_channel(f"evento-{i+1}")
            created += 1
            await asyncio.sleep(0.2)
        except Exception as e:
            print(f"Error creando canal: {e}")

    print(f"Canales creados: {created}")

# =========================
# 🚀 RUN BOT
# =========================
bot.run(TOKEN)
