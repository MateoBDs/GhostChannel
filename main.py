import os
import discord
from discord.ext import commands
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

# ====== WEB SERVER (HACK PARA RENDER) ======
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

# ====== DISCORD BOT ======
TOKEN = os.getenv("TOKEN")

SERVIDORES_PERMITIDOS = [
    1502216163084472381,
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
