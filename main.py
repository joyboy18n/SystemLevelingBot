import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome, Boss. The System is now online.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Player data storage (for demo; use database in production)
players = {}

# Player template
def create_player(user_id):
    return {
        "level": 1,
        "exp": 0,
        "next_level_exp": 100,
        "hp": 100,
        "mp": 50,
        "strength": 5,
        "agility": 5,
        "stamina": 5,
        "intelligence": 5,
        "sense": 5,
        "aura": 0,
        "title": "Novice Hunter",
        "fatigue": 0,
        "inventory": [],
        "skills": ["Basic Slash"],
        "quests": [],
        "dungeon_logs": []
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        players[user_id] = create_player(user_id)
        await update.message.reply_text("Welcome to the System, Hunter. Your path begins now.")
    else:
        await update.message.reply_text("System already active. Use /profile to check your status.")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if player:
        profile_text = f"""
        *Level:* {player['level']} ({player['exp']}/{player['next_level_exp']} EXP)
        *HP:* {player['hp']}  |  *MP:* {player['mp']}
        *Stats:* STR: {player['strength']} | AGI: {player['agility']} | STA: {player['stamina']}\nINT: {player['intelligence']} | SEN: {player['sense']} | AURA: {player['aura']}
        *Title:* {player['title']}
        *Fatigue:* {player['fatigue']} / 100
        """
        await update.message.reply_markdown(profile_text)
    else:
        await update.message.reply_text("You have not started the system. Use /start to begin.")

async def skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if player:
        skills_list = "\n".join(f"- {s}" for s in player['skills'])
        await update.message.reply_text(f"*Skills:*
{skills_list}", parse_mode='Markdown')

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if player:
        if player['inventory']:
            inventory_list = "\n".join(f"- {item}" for item in player['inventory'])
        else:
            inventory_list = "Empty"
        await update.message.reply_text(f"*Inventory:*\n{inventory_list}", parse_mode='Markdown')

async def dungeon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if player:
        if player['dungeon_logs']:
            logs = "\n".join(player['dungeon_logs'])
        else:
            logs = "No dungeons cleared yet."
        await update.message.reply_text(f"*Dungeon Logs:*\n{logs}", parse_mode='Markdown')

async def system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    explanation = """
*System Guide:*
- *Leveling:* Gain EXP through quests and dungeons.
- *Titles:* Unlocked on achievements, grant passive boosts.
- *Fatigue:* Increases with activity, resets daily.
- *Skills:* Active/passive abilities gained with level and dungeons.
- *Inventory:* Holds your gear and items.
- *Shop:* Buy items and gear (future feature).
- *Dungeon Logs:* Tracks all your battles.
"""
    await update.message.reply_markdown(explanation)

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Settings coming soon.")

# Add Quest Command (simplified)
async def quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)
    if player:
        quest = "Daily Push-ups - 10 reps"
        player['quests'].append(quest)
        await update.message.reply_text(f"New Quest Added:\n{quest}")

# Add EXP gain and level-up system (example)
def gain_exp(player, amount):
    player['exp'] += amount
    if player['exp'] >= player['next_level_exp']:
        player['level'] += 1
        player['exp'] -= player['next_level_exp']
        player['next_level_exp'] = int(player['next_level_exp'] * 1.2)
        player['hp'] += 10
        player['mp'] += 5
        player['strength'] += 1
        player['agility'] += 1
        player['stamina'] += 1
        player['intelligence'] += 1
        player['sense'] += 1

app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("skills", skills))
app.add_handler(CommandHandler("inventory", inventory))
app.add_handler(CommandHandler("dungeon", dungeon))
app.add_handler(CommandHandler("system", system))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(CommandHandler("quest", quest))

print("Bot running...")
app.run_polling()
