🐶 PupByte Telegram Bot - PupByteBot

Description:
-------------
Ye bot fun Tap-to-Earn game jaisa hai Hamster Combat style me.
Features:
1. /start → Welcome message + animated PupByte logo + referral code
2. /tap → Earn coins with emoji animation
3. /profile → Check your coins, level, and referral code
4. /daily → Claim daily bonus coins
5. /leaderboard → Top 5 players with coins + medals
6. Referral system → Invite friends, both get 50 coins

Folder Structure:
-----------------
PupByteBot/
│
├── bot.py             # Main bot code
├── requirements.txt   # Python library dependencies
└── README.txt         # Instructions & guide

Setup Instructions:
------------------
1. Install Python 3.8+ on PC or Pydroid 3 on Android
2. Install required library:
   pip install -r requirements.txt
3. Add your Telegram BOT_TOKEN:
   - On Railway: Environment Variable BOT_TOKEN
   - On local: Replace TOKEN in bot.py (not recommended)
4. Run bot:
   python bot.py  (or Run in Pydroid 3)
5. Test commands in Telegram:
   /start, /tap, /profile, /daily, /leaderboard

Notes:
------
- Ensure users.json file is created automatically on first run to store data
- Keep bot.py updated for any new features
- Referral codes are unique per user
- Bot works best when hosted on Railway or any 24/7 server