import telebot
import json
import random
import time
import os

# Bot token from environment variable (for server security)
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# Load user data
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save user data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

users = load_data()

# Generate referral code
def generate_referral():
    return str(random.randint(1000,9999))

# Animated Tap Effect
def animate_tap(coins):
    emojis = ["💥","✨","🔥","⚡","🎯","💫","🎉"]
    return f"{random.choice(emojis)} You earned {coins} Coins {random.choice(emojis)}"

# Level-Up Animation
def animate_level(level):
    effects = ["🎇","🎆","🌟","🚀","🔥","🏅"]
    return f"{''.join(random.choices(effects, k=5))} Level Up! You are now Level {level} {''.join(random.choices(effects, k=5))}"

# Start command with animated logo & referral
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    msg_text = message.text.split()
    
    logo = "🐶 PupByte Bot 🐾"
    
    if user_id not in users:
        users[user_id] = {
            "coins": 0,
            "level": 1,
            "referral_code": generate_referral()
        }
        # Check referral
        if len(msg_text) > 1:
            ref_code = msg_text[1]
            for uid, u in users.items():
                if u.get("referral_code") == ref_code:
                    users[uid]["coins"] += 50
                    users[user_id]["coins"] += 50
                    bot.send_message(uid, f"🎉 Your friend joined! +50 Coins")
                    break
        save_data(users)

    bot.reply_to(message,
        f"{logo}\n\n"
        f"💰 Tap /tap to earn coins\n"
        f"📊 Check /profile\n"
        f"🎁 Daily Bonus /daily\n"
        f"🏆 Leaderboard /leaderboard\n"
        f"🔗 Referral Code: {users[user_id]['referral_code']}\n"
        f"Share: /start {users[user_id]['referral_code']} to invite friends!"
    )

# Tap command
@bot.message_handler(commands=['tap'])
def tap(message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        users[user_id] = {"coins": 0, "level": 1, "referral_code": generate_referral()}

    earned = users[user_id]["level"]
    users[user_id]["coins"] += earned

    # Level up
    level_msg = ""
    if users[user_id]["coins"] >= users[user_id]["level"] * 100:
        users[user_id]["level"] += 1
        level_msg = animate_level(users[user_id]["level"]) + "\n"

    save_data(users)

    bot.reply_to(message, animate_tap(earned) + "\n" + level_msg +
                 f"💰 Coins: {users[user_id]['coins']}")

# Profile command
@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = str(message.from_user.id)
    if user_id in users:
        u = users[user_id]
        bot.reply_to(message,
            f"👤 Your Profile\n"
            f"💰 Coins: {u['coins']}\n"
            f"⭐ Level: {u['level']}\n"
            f"🔗 Referral Code: {u['referral_code']}"
        )
    else:
        bot.reply_to(message, "❌ First type /start")

# Daily bonus command
@bot.message_handler(commands=['daily'])
def daily(message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        users[user_id] = {"coins": 0, "level": 1, "referral_code": generate_referral()}

    user = users[user_id]
    now = int(time.time())
    last_claim = user.get("last_daily", 0)

    if now - last_claim >= 86400:
        bonus = 100 + user["level"]*10
        user["coins"] += bonus
        user["last_daily"] = now
        save_data(users)
        bot.reply_to(message, f"🎁 Daily Bonus Claimed!\n💰 You received {bonus} Coins")
    else:
        remaining = 86400 - (now - last_claim)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        bot.reply_to(message, f"⏰ Daily already claimed!\nCome back in {hours}h {minutes}m")

# Leaderboard command (animated)
@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    top_users = sorted(users.items(), key=lambda x: x[1]['coins'], reverse=True)[:5]
    msg = "🏆 PupByte Leaderboard 🏆\n\n"
    medals = ["🥇","🥈","🥉","🎖️","🎖️"]
    for i, (uid, u) in enumerate(top_users, start=0):
        msg += f"{medals[i]} User {uid} - {u['coins']} Coins\n"
    bot.reply_to(message, msg)

# Start polling
print("🐾 PupByte Bot Started...")
bot.polling()