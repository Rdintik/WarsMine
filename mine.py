import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Включаем необходимые намерения (Intents)
intents = discord.Intents.default()
intents.message_content = True 

# Создаем бота с префиксом "!" и включенными слэш-командами
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} готов к работе!')
    # Синхронизируем слэш-команды, чтобы они появились в Discord
    await bot.tree.sync()

# --- СЛЭШ-КОМАНДА (/bot) ---
# Она появится в Discord, если вы нажмете на кнопку слэша "/" и начнете печатать "bot"
@bot.tree.command(name="bot", description="Бот пишет сообщение на месте от своего имени")
async def bot_command(interaction: discord.Interaction):
    # interaction.channel — это канал, где была вызвана команда
    # interaction.response.send_message — отвечает на команду пользователя
    
    await interaction.response.send_message(
        "Привет! Я бот, и я пишу это сообщение прямо здесь, на месте. \n"
        "Купи донат в /donate, чтобы получить /fly!", 
        ephemeral=False # Если True, сообщение увидит только вы. Ставим False, чтобы видели все.
    )

# --- ТЕКСТОВАЯ КОМАНДА (!bot) (на случай если слэши не работают) ---
@bot.command(name='bot')
async def text_bot(ctx):
    await ctx.send(
        "Привет! Я бот, и я пишу это сообщение прямо здесь, на месте. \n"
        "Купи донат в /donate, чтобы получить /fly!"
    )

# Запуск бота
bot.run(TOKEN)
