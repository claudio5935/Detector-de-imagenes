mport discord
from discord.ext import commands

# Configuración de los permisos del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado exitosamente como {bot.user}")

@bot.command()
async def check(ctx):
    # Verifica si el mensaje del usuario contiene archivos adjuntos
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            # Comprueba la extensión del archivo para asegurarse de que sea una imagen
            if any(
                attachment.filename.lower().endswith(ext)
                for ext in [".png", ".jpg", ".jpeg", ".webp"]
            ):
                # Genera un nombre único utilizando el ID del archivo adjunto
                file_name = f"image_{attachment.id}_{attachment.filename}"
                
                # Guarda la imagen en la carpeta del proyecto
                await attachment.save(file_name)
                await ctx.send(
                    f"✅ ¡Imagen recibida! Se ha guardado correctamente como: `{file_name}`"
                )
            else:
                await ctx.send(
                    "❌ El archivo enviado no es un formato de imagen válido (PNG, JPG, JPEG, WEBP)."
                )
    else:
        await ctx.send(
            "⚠️ No se encontró ninguna imagen en tu mensaje. Por favor, adjunta una imagen al usar el comando '!check'."
        )

# Coloca aquí el Token de tu Bot de Discord (entre las comillas)
bot.run("TU_DISCORD_BOT_TOKEN")