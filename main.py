import os
import discord
import asyncio
from discord.ext import commands
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

# ====== WEB SERVER (RENDER 24/7 KEEP ALIVE) ======
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

# ====== CONFIG ======
TOKEN = os.getenv("TOKEN")

SERVIDORES_PERMITIDOS = [
    1502216163084472381,
]

# ====== DISCORD BOT ======
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== COMANDO RESET EVENTO ======
@bot.command()
@commands.has_permissions(administrator=True)
async def mamamia(ctx, cantidad: int):
    if ctx.guild is None:
        return

    if ctx.guild.id not in SERVIDORES_PERMITIDOS:
        await ctx.send("Servidor no autorizado.")
        return

    cantidad = max(1, min(cantidad, 50))

    await ctx.send("⚠️ Eliminando canales...")

    # ====== BORRAR CANALES ======
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.3)  # evita rate limit
        except:
            pass

    await asyncio.sleep(3)

    await ctx.send("📁 Creando nuevos canales...")

    # ====== CREAR CANALES ======
    for i in range(cantidad):
        try:
            await ctx.guild.create_text_channel(f"evento-{i+1}")
            await asyncio.sleep(0.2)
        except:
            pass

    await ctx.send(f"✅ Listo. Se eliminaron los canales anteriores y se crearon {cantidad} canales.")

# ====== START BOT ======
bot.run(TOKEN)
