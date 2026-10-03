import os
import discord
from discord import app_commands
from discord.ext import commands

# ----------------- НАСТРОЙКИ -----------------
# Считываем токен из переменной BOT_TOKEN на хостинге
TOKEN = os.getenv("BOT_TOKEN")

WELCOME_CHANNEL_ID = 123456789012345678  # Замени на ID канала для приветствий
ALLOWED_ROLE_ID = 123456789012345678     # Замени на ID роли, которой разрешено использовать /bc
# ---------------------------------------------

intents = discord.Intents.default()
intents.members = True  # Нужно для отслеживания входа новых участников
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Бот {bot.user} успешно запущен!")
    try:
        synced = await bot.tree.sync()
        print(f"Синхронизировано слэш-команд: {len(synced)}")
    except Exception as e:
        print(f"Ошибка синхронизации команд: {e}")


# --- 1. ПРИВЕТСТВИЕ НОВЫХ ИГРОКОВ ---
@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="👋 Добро пожаловать на сервер!",
            description=f"Привет, {member.mention}! Рады видеть тебя на сервере.\nОзнакомься с правилами и приятной игры!",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Участник №{member.guild.member_count}")
        await channel.send(embed=embed)


# --- 2. КОМАНДА /bc ДЛЯ ОБЪЯВЛЕНИЙ ---
@bot.tree.command(name="bc", description="Опубликовать объявление в выбранный канал от лица бота")
@app_commands.describe(
    target_channel="Канал, куда нужно отправить сообщение",
    title="Заголовок объявления",
    text="Текст объявления (можно использовать \\n для переноса строк)",
    image="Картинка или баннер для объявления"
)
async def broadcast(
    interaction: discord.Interaction,
    target_channel: discord.TextChannel,
    title: str,
    text: str,
    image: discord.Attachment = None
):
    # Проверка прав: Пользователь должен быть админом ИЛИ иметь специальную роль
    user_roles = [role.id for role in interaction.user.roles]
    has_permission = interaction.user.guild_permissions.administrator or (ALLOWED_ROLE_ID in user_roles)

    if not has_permission:
        await interaction.response.send_message(
            "❌ У вас нет прав для использования этой команды!", 
            ephemeral=True
        )
        return

    # Заменяем '\n' на реальный перенос строки
    formatted_text = text.replace("\\n", "\n")

    # Создаем Embed
    embed = discord.Embed(
        title=title,
        description=formatted_text,
        color=discord.Color.from_rgb(47, 49, 54)  # Тёмно-серый стиль Discord
    )

    if image:
        embed.set_image(url=image.url)

    embed.set_footer(
        text=f"Опубликовал: {interaction.user.display_name}", 
        icon_url=interaction.user.display_avatar.url
    )

    try:
        await target_channel.send(embed=embed)
        await interaction.response.send_message(
            f"✅ Объявление успешно отправлено в {target_channel.mention}!", 
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Ошибка при отправке: {e}", 
            ephemeral=True
        )

# Проверка наличия переменной BOT_TOKEN
if not TOKEN:
    print("ОШИБКА: Токен не найден! Укажи BOT_TOKEN в переменной окружения на хостинге.")
else:
    bot.run(TOKEN)
