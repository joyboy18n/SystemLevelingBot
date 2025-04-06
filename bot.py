import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from system import create_player, get_profile, train, view_inventory, view_shop, view_quests, view_dungeons, view_titles

TOKEN = "8158349318:AAGZskcZlJu-LNW9W3iUjS0miDHnXP8IVzM"

logging.basicConfig(level=logging.INFO)

app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name
    create_player(user_id, name)
    await update.message.reply_text(f"Welcome to The System, {name}!\nUse /profile to view your stats.")

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", lambda u, c: u.message.reply_text(get_profile(str(u.effective_user.id)))))
app.add_handler(CommandHandler("train", lambda u, c: u.message.reply_text(train(str(u.effective_user.id)))))
app.add_handler(CommandHandler("inventory", lambda u, c: u.message.reply_text(view_inventory(str(u.effective_user.id)))))
app.add_handler(CommandHandler("shop", lambda u, c: u.message.reply_text(view_shop())))
app.add_handler(CommandHandler("quests", lambda u, c: u.message.reply_text(view_quests(str(u.effective_user.id)))))
app.add_handler(CommandHandler("dungeon", lambda u, c: u.message.reply_text(view_dungeons(str(u.effective_user.id)))))
app.add_handler(CommandHandler("titles", lambda u, c: u.message.reply_text(view_titles(str(u.effective_user.id)))))

app.run_polling()

import json
import os
import random

DB = "players.json"

def load_data():
    if os.path.exists(DB):
        with open(DB, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

def create_player(user_id, name):
    data = load_data()
    if user_id not in data:
        data[user_id] = {
            "name": name,
            "level": 1,
            "xp": 0,
            "hp": 100,
            "mp": 50,
            "fatigue": 0,
            "stats": {"Strength": 5, "Agility": 5, "Stamina": 5, "Intelligence": 5, "Sense": 5},
            "titles": ["Newbie"],
            "skills": ["Basic Punch"],
            "inventory": ["Starter Potion"],
            "quests": ["Train once"],
            "dungeon_log": []
        }
        save_data(data)

def get_profile(user_id):
    data = load_data()
    user = data[user_id]
    return f"Name: {user['name']}\nLevel: {user['level']}\nXP: {user['xp']}/100\nHP: {user['hp']}\nMP: {user['mp']}\nFatigue: {user['fatigue']}\nStats: {user['stats']}\nTitles: {user['titles']}"

def train(user_id):
    data = load_data()
    user = data[user_id]
    if user["fatigue"] >= 100:
        return "You're too fatigued. Rest before training again!"
    user["xp"] += 20
    user["fatigue"] += 20
    if user["xp"] >= 100:
        user["xp"] -= 100
        user["level"] += 1
        for stat in user["stats"]:
            user["stats"][stat] += 1
    save_data(data)
    return f"Training complete! +20 XP\nLevel: {user['level']}\nXP: {user['xp']}/100\nFatigue: {user['fatigue']}"

def view_inventory(user_id):
    data = load_data()
    return f"Inventory: {data[user_id]['inventory']}"

def view_shop():
    return "Shop:\n1. HP Potion - 10 coins\n2. MP Potion - 15 coins\n(Shop items coming soon)"

def view_quests(user_id):
    data = load_data()
    return f"Quests: {data[user_id]['quests']}"

def view_dungeons(user_id):
    data = load_data()
    return "Dungeon log: " + ", ".join(data[user_id]["dungeon_log"]) if data[user_id]["dungeon_log"] else "No dungeons yet."

def view_titles(user_id):
    data = load_data()
    return f"Titles unlocked: {data[user_id]['titles']}"