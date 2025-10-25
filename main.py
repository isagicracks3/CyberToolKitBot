import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler,
    CallbackQueryHandler, ContextTypes,
    MessageHandler,
    filters
)
from datetime import datetime
import pytz

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = "8158607310:AAHqSKzNAaixc199vyF5Kiuvl6-1xBpn7A4"
UPI_ID = "subhammandloi1999@ibl"
START_TIME = datetime.now(pytz.timezone('Asia/Kolkata'))
ADMIN_ID = 7098912960  # Your admin ID

# Database simulation (in a real bot, use a proper database)
user_db = set()
order_db = []
order_today = 0
revenue_today = 0

# Service details dictionary
SERVICE_DETAILS = {
    # Wordlist Vault
    'wl_1': ("1M+ Combos", "₹49", "Basic wordlist for security testing"),
    'wl_2': ("5M+ Combos", "₹99", "Medium-sized wordlist collection"),
    'wl_3': ("10M+ Combos", "₹149", "Large wordlist for professionals"),
    'wl_4': ("100M+ Darknet Leaks", "₹179", "Premium leaked password database"),

    # Virtual Numbers
    'num_1': ("6-Hour Temp Number", "₹49", "Temporary number for short verifications"),
    'num_2': ("12-Hour Number", "₹79", "Extended duration virtual number"),
    'num_3': ("24-Hour Number", "₹99", "Full day virtual number service"),
    'num_4': ("Lifetime Number", "₹199", "Permanent virtual number"),

    # Anonymous Emails
    'email_1': ("10 Temp Emails", "₹39", "Small batch of temporary emails"),
    'email_2': ("50 Temp Emails", "₹79", "Medium batch of temporary emails"),
    'email_3': ("100 Temp Emails", "₹149", "Large batch of temporary emails"),

    # Phone Monitoring
    'monitor_1': ("Basic Monitoring", "₹99", "Essential phone tracking features"),
    'monitor_2': ("Advanced Tracking", "₹199", "Comprehensive monitoring suite"),
    'monitor_3': ("Full Spy Suite", "₹299", "Complete monitoring package"),

    # Instagram Growth
    'ig_1': ("100 Followers", "₹49", "Small follower boost"),
    'ig_2': ("500 Followers", "₹99", "Medium follower package"),
    'ig_3': ("1000 Followers", "₹199", "Large follower package"),

    # Free Fire Hacks
    'ff_1': ("Basic Hacks", "₹99", "Essential game enhancements"),
    'ff_2': ("Premium Cheats", "₹199", "Advanced game features"),
    'ff_3': ("VIP Package", "₹299", "Complete game package"),

    # PC Optimization
    'pc_1': ("Basic Optimization", "₹49", "Essential PC tuning"),
    'pc_2': ("Performance Boost", "₹99", "Enhanced performance package"),
    'pc_3': ("Ultimate Tuning", "₹199", "Complete PC optimization"),

    # Password Recovery
    'pass_1': ("Basic Recovery", "₹99", "Simple password recovery"),
    'pass_2': ("Advanced Cracking", "₹199", "Complex password solutions"),
    'pass_3': ("Premium Recovery", "₹299", "Complete recovery package"),

    # Special Bundles
    'bundle_1': ("Starter Bundle", "₹199", "Beginner's toolkit"),
    'bundle_2': ("Pro Bundle", "₹399", "Professional package"),
    'bundle_3': ("Ultimate Bundle", "₹699", "Complete cyber toolkit"),
}

# ====================
# HELPER FUNCTIONS
# ====================

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == ADMIN_ID

def add_user(user_id: int):
    """Add user to database"""
    user_db.add(user_id)

def add_order(amount: int):
    """Add order to database"""
    global order_today, revenue_today
    order_today += 1
    revenue_today += amount
    order_db.append((datetime.now(pytz.timezone('Asia/Kolkata')), amount))

def reset_daily_stats():
    """Reset daily stats at midnight"""
    global order_today, revenue_today
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    if now.hour == 0 and now.minute == 0:
        order_today = 0
        revenue_today = 0

# ====================
# KEYBOARD GENERATORS
# ====================

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔐 Wordlist Vault", callback_data='wordlist')],
        [InlineKeyboardButton("📞 Virtual Numbers", callback_data='numbers')],
        [InlineKeyboardButton("📧 Anonymous Emails", callback_data='emails')],
        [InlineKeyboardButton("📱 Phone Monitoring", callback_data='monitoring')],
        [InlineKeyboardButton("📸 Instagram Growth", callback_data='instagram')],
        [InlineKeyboardButton("🎮 Free Fire Hacks", callback_data='freefire')],
        [InlineKeyboardButton("💻 PC Optimization", callback_data='pc')],
        [InlineKeyboardButton("🔑 Password Recovery", callback_data='password')],
        [InlineKeyboardButton("🎁 Special Bundles", callback_data='bundles')],
        [InlineKeyboardButton("ℹ️ About CyberToolkit", callback_data='about')],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')]
    ])

def admin_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data='admin_stats')],
        [InlineKeyboardButton("📢 Broadcast to All", callback_data='admin_broadcast')],
        [InlineKeyboardButton("📩 Broadcast to Specific", callback_data='admin_broadcast_specific')],
        [InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def payment_keyboard(service_code):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Pay via UPI", callback_data=f'pay_{service_code}')],
        [InlineKeyboardButton("🆔 Reveal My ID", callback_data='show_my_id')],
        [InlineKeyboardButton("📲 Contact Support", url='https://t.me/opanshuff2k')],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')]
    ])

# ====================
# COMMAND HANDLERS
# ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    add_user(user.id)

    # Send alert to admin about new user
    new_user_alert = (
        "🚨 *NEW USER ALERT* 🚨\n\n"
        f"🆔 *User ID:* `{user.id}`\n"
        f"👤 *Name:* {user.full_name}\n"
        f"🔗 *Username:* @{user.username if user.username else 'N/A'}\n"
        f"📅 *Joined at:* {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"🌐 *Total Users Now:* {len(user_db)}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=new_user_alert,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Failed to send new user alert to admin: {e}")

    welcome_message = (
        "👋 *WELCOME TO CYBERTOOLKIT!* 👋\n\n"
        "⚡ *YOUR ULTIMATE DESTINATION FOR* ⚡\n"
        "🔐 *CYBERSECURITY TOOLS &* 🔐\n"
        "💻 *HACKING RESOURCES* 💻\n\n"
        "🌐 *Explore our collection and stay anonymous!* 🌐\n"
        "⚠️ *Note: For legal/educational use only*"
    )

    # Add admin menu button if user is admin
    if is_admin(user.id):
        keyboard = [
            [InlineKeyboardButton("🔐 Wordlist Vault", callback_data='wordlist')],
            [InlineKeyboardButton("📞 Virtual Numbers", callback_data='numbers')],
            [InlineKeyboardButton("📧 Anonymous Emails", callback_data='emails')],
            [InlineKeyboardButton("📱 Phone Monitoring", callback_data='monitoring')],
            [InlineKeyboardButton("📸 Instagram Growth", callback_data='instagram')],
            [InlineKeyboardButton("🎮 Free Fire Hacks", callback_data='freefire')],
            [InlineKeyboardButton("💻 PC Optimization", callback_data='pc')],
            [InlineKeyboardButton("🔑 Password Recovery", callback_data='password')],
            [InlineKeyboardButton("🎁 Special Bundles", callback_data='bundles')],
            [InlineKeyboardButton("ℹ️ About CyberToolkit", callback_data='about')],
            [InlineKeyboardButton("🛠️ Admin Panel", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        reply_markup = main_menu_keyboard()

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    terms_text = (
        "📜 *Terms & Conditions*\n\n"
        "1. All tools are for educational/authorized use only\n"
        "2. No refunds after delivery\n"
        "3. We don't support illegal activities\n"
        "4. Delivery time may vary\n\n"
        "By using this bot you agree to these terms."
    )
    await update.message.reply_text(terms_text, parse_mode="Markdown")

# ====================
# ADMIN COMMANDS
# ====================

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command handler"""
    user = update.effective_user
    if not is_admin(user.id):
        await update.message.reply_text("⚠️ You are not authorized to use this command.")
        return

    await update.message.reply_text(
        "🛠️ *Admin Panel* 🛠️\n\nSelect an option:",
        reply_markup=admin_keyboard(),
        parse_mode="Markdown"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics (admin only)"""
    user = update.effective_user
    if not is_admin(user.id):
        await update.message.reply_text("⚠️ You are not authorized to use this command.")
        return

    reset_daily_stats()
    uptime = datetime.now(pytz.timezone('Asia/Kolkata')) - START_TIME
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    stats_text = (
        "📊 *Bot Statistics*\n\n"
        f"⏱ Uptime: {days} days, {hours} hours, {minutes} minutes\n"
        f"👥 Total users: {len(user_db)}\n"
        f"🛒 Today's orders: {order_today}\n"
        f"💰 Today's revenue: ₹{revenue_today}\n\n"
        f"📈 All-time orders: {len(order_db)}\n"
        f"💵 All-time revenue: ₹{sum(amount for _, amount in order_db)}"
    )
    await update.message.reply_text(stats_text, parse_mode="Markdown")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users or specific user (admin only)"""
    user = update.effective_user
    if not is_admin(user.id):
        await update.message.reply_text("⚠️ You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("Usage:\n/broadcast <message> - Send to all users\n/broadcast <user_id> <message> - Send to specific user")
        return

    # Check if first argument is a user ID (numeric)
    if len(context.args) > 1 and context.args[0].isdigit():
        try:
            target_user = int(context.args[0])
            message = " ".join(context.args[1:])

            if not message:
                await update.message.reply_text("Please include a message to send.")
                return

            try:
                await context.bot.send_message(
                    chat_id=target_user,
                    text=f"\n\n{message}",
                    parse_mode="Markdown"
                )
                await update.message.reply_text(f"✅ Message sent to user {target_user} successfully!")
            except Exception as e:
                await update.message.reply_text(f"⚠️ Failed to send message to user {target_user}. Error: {str(e)}")
        except ValueError:
            await update.message.reply_text("Invalid user ID. Must be a number.")
    else:
        # Broadcast to all users
        message = " ".join(context.args)
        success = 0
        failed = 0

        for user_id in user_db:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"📢 *Broadcast Message:*\n\n{message}",
                    parse_mode="Markdown"
                )
                success += 1
            except Exception as e:
                logger.error(f"Failed to send to {user_id}: {e}")
                failed += 1

        await update.message.reply_text(
            f"📊 Broadcast completed:\n✅ Success: {success}\n❌ Failed: {failed}"
        )

# ====================
# MESSAGE HANDLER
# ====================

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all user messages"""
    user = update.effective_user

    # Forward photos/screenshots to admin with user info
    if update.message.photo:
        photo = update.message.photo[-1]  # Get highest resolution photo
        caption = update.message.caption if update.message.caption else "No caption"

        user_info = (
            f"📸 *New Screenshot from User*\n\n"
            f"🆔 *ID:* `{user.id}`\n"
            f"📛 *Name:* {user.full_name}\n"
            f"🔗 *Username:* @{user.username if user.username else 'N/A'}\n\n"
            f"📝 *Caption:* {caption}"
        )

        try:
            # Forward the photo to admin
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=photo.file_id,
                caption=user_info,
                parse_mode="Markdown"
            )

            # Notify user that screenshot was received
            await update.message.reply_text(
                "✅ Your screenshot has been received! We'll process your order shortly.",
                reply_markup=back_to_menu_keyboard()
            )
        except Exception as e:
            logger.error(f"Failed to forward photo to admin: {e}")
            await update.message.reply_text("⚠️ Failed to process your screenshot. Please try again.")

    # Handle other messages
    elif update.message.text or update.message.caption:
        message = update.message.text or update.message.caption

        # Forward to admin if not from admin
        if not is_admin(user.id):
            try:
                user_info = (
                    f"👤 *New Message from User*\n\n"
                    f"🆔 *ID:* `{user.id}`\n"
                    f"📛 *Name:* {user.full_name}\n"
                    f"🔗 *Username:* @{user.username if user.username else 'N/A'}\n\n"
                    f"📝 *Message:*\n{message}"
                )

                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=user_info,
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Failed to forward message to admin: {e}")

# ====================
# BUTTON HANDLERS
# ====================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user = query.from_user

    # Admin panel handlers
    if query.data == 'admin_panel' and is_admin(user.id):
        await query.edit_message_text(
            text="🛠️ *Admin Panel* 🛠️\n\nSelect an option:",
            reply_markup=admin_keyboard(),
            parse_mode="Markdown"
        )

    elif query.data == 'admin_stats' and is_admin(user.id):
        reset_daily_stats()
        uptime = datetime.now(pytz.timezone('Asia/Kolkata')) - START_TIME
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        stats_text = (
            "📊 *Admin Statistics*\n\n"
            f"⏱ Uptime: {days} days, {hours} hours, {minutes} minutes\n"
            f"👥 Total users: {len(user_db)}\n"
            f"🛒 Today's orders: {order_today}\n"
            f"💰 Today's revenue: ₹{revenue_today}\n\n"
            f"📈 All-time orders: {len(order_db)}\n"
            f"💵 All-time revenue: ₹{sum(amount for _, amount in order_db)}"
        )
        await query.edit_message_text(
            text=stats_text,
            reply_markup=admin_keyboard(),
            parse_mode="Markdown"
        )

    elif query.data == 'admin_broadcast' and is_admin(user.id):
        await query.edit_message_text(
            text="📢 *Admin Broadcast*\n\nUse /broadcast <message> to send a message to all users or /broadcast <user_id> <message> to send to specific user.",
            reply_markup=admin_keyboard(),
            parse_mode="Markdown"
        )

    elif query.data == 'admin_broadcast_specific' and is_admin(user.id):
        await query.edit_message_text(
            text="📩 *Broadcast to Specific User*\n\nUse /broadcast <user_id> <message> to send a message to a specific user.",
            reply_markup=admin_keyboard(),
            parse_mode="Markdown"
        )

    # Main menu items
    elif query.data == 'wordlist':
        keyboard = [
            [InlineKeyboardButton("💰 ₹49 - 1M+ Combos", callback_data='wl_1')],
            [InlineKeyboardButton("💎 ₹99 - 5M+ Combos", callback_data='wl_2')],
            [InlineKeyboardButton("⚡ ₹149 - 10M+ Combos", callback_data='wl_3')],
            [InlineKeyboardButton("☠️  ₹199 - 100M+ Darknet Leaks", callback_data='wl_4')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="🔐 *WORDLIST VAULT* 🔐\n\nChoose your wordlist package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'numbers':
        keyboard = [
            [InlineKeyboardButton("⏳ ₹49 - 6-Hour Temp", callback_data='num_1')],
            [InlineKeyboardButton("⌛ ₹99 - 12-Hour", callback_data='num_2')],
            [InlineKeyboardButton("⏱️  ₹149 - 24-Hour", callback_data='num_3')],
            [InlineKeyboardButton("🏆 ₹199 - Lifetime", callback_data='num_4')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="📞 *VIRTUAL NUMBERS* 📞\n\nChoose your virtual number package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'emails':
        keyboard = [
            [InlineKeyboardButton("📧 ₹39 - 10 Temp Emails", callback_data='email_1')],
            [InlineKeyboardButton("📨 ₹79 - 50 Temp Emails", callback_data='email_2')],
            [InlineKeyboardButton("📩 ₹149 - 100 Temp Emails", callback_data='email_3')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="📧 *ANONYMOUS EMAILS* 📧\n\nChoose your email package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'monitoring':
        keyboard = [
            [InlineKeyboardButton("📱 ₹99 - Basic Monitoring", callback_data='monitor_1')],
            [InlineKeyboardButton("📲 ₹199 - Advanced Tracking", callback_data='monitor_2')],
            [InlineKeyboardButton("🕵️ ₹299 - Full Spy Suite", callback_data='monitor_3')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="📱 *PHONE MONITORING* 📱\n\n*Legal Use Only*\nChoose your monitoring package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'instagram':
        keyboard = [
            [InlineKeyboardButton("📊 ₹49 - 100 Followers", callback_data='ig_1')],
            [InlineKeyboardButton("📈 ₹99 - 500 Followers", callback_data='ig_2')],
            [InlineKeyboardButton("🚀 ₹149 - 1000 Followers", callback_data='ig_3')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="📸 *INSTAGRAM GROWTH* 📸\n\nChoose your growth package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'freefire':
        keyboard = [
            [InlineKeyboardButton("🔫 ₹99 - Basic Hacks", callback_data='ff_1')],
            [InlineKeyboardButton("💣 ₹199 - Premium Cheats", callback_data='ff_2')],
            [InlineKeyboardButton("👑 ₹299 - VIP Package", callback_data='ff_3')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="🎮 *FREE FIRE HACKS* 🎮\n\n*For educational purposes only*\nChoose your hack package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'pc':
        keyboard = [
            [InlineKeyboardButton("🛠️ ₹49 - Basic Optimization", callback_data='pc_1')],
            [InlineKeyboardButton("⚡ ₹99 - Performance Boost", callback_data='pc_2')],
            [InlineKeyboardButton("🚀 ₹199 - Ultimate Tuning", callback_data='pc_3')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="💻 *PC OPTIMIZATION* 💻\n\nChoose your optimization package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'password':
        keyboard = [
            [InlineKeyboardButton("🔑 ₹99 - Basic Recovery", callback_data='pass_1')],
            [InlineKeyboardButton("🔓 ₹199 - Advanced Cracking", callback_data='pass_2')],
            [InlineKeyboardButton("💎 ₹299 - Premium Recovery", callback_data='pass_3')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="🔑 *PASSWORD RECOVERY* 🔑\n\n*For legal recovery purposes only*\nChoose your recovery package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'bundles':
        keyboard = [
            [InlineKeyboardButton("🎁 ₹199 - Starter Bundle", callback_data='bundle_1')],
            [InlineKeyboardButton("💼 ₹399 - Pro Bundle", callback_data='bundle_2')],
            [InlineKeyboardButton("📦 ₹699 - Ultimate Bundle", callback_data='bundle_3')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')],
        ]
        await query.edit_message_text(
            text="🎁 *SPECIAL BUNDLES* 🎁\n\nChoose your bundle package:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'about':
        about_text = (
            "🔍 *About CyberToolkit*\n\n"
            "We provide premium cybersecurity tools and digital empowerment solutions:\n\n"
            "• 🔐 Premium Wordlists for security research\n"
            "• 📞 Virtual Numbers for anonymous comms\n"
            "• 📧 Temp Emails to protect your identity\n"
            "• 📱 Device Monitoring (legal use only)\n"
            "• 📈 Social Media Growth tools\n"
            "• 🎮 Gaming enhancements\n"
            "• 💻 PC Optimization kits\n\n"
            "*Mission*: To equip professionals with powerful yet ethical tools.\n\n"
            "⚠️ *Disclaimer*: All tools are for educational/authorized purposes only.\n\n"
            "📩 Support: @opanshuff2k"
        )
        await query.edit_message_text(
            text=about_text,
            reply_markup=back_to_menu_keyboard(),
            parse_mode="Markdown"
        )

    elif query.data == 'show_my_id':
        await query.edit_message_text(
            text=f"🆔 *Your Telegram ID:* `{user.id}`\n\n"
                 "Please include this ID when contacting support or making payments.",
            reply_markup=back_to_menu_keyboard(),
            parse_mode="Markdown"
        )

    elif query.data in SERVICE_DETAILS:
        name, price, description = SERVICE_DETAILS[query.data]
        payment_message = (
            f"🛒 *{name} Package* 🛒\n\n"
            f"💵 *Price:* {price}\n"
            f"📝 *Description:* {description}\n\n"
            "⚡ *Payment Method:*\n"
            f"• UPI: `{UPI_ID}`\n\n"
            "📌 *After Payment:*\n"
            "1. Send payment screenshot\n"
            "2. Include your Telegram ID\n"
            "3. We'll deliver within 1 hour\n\n"
            "🛡️ *Guarantee:* Full refund if not delivered"
        )
        await query.edit_message_text(
            text=payment_message,
            reply_markup=payment_keyboard(query.data),
            parse_mode="Markdown"
        )

    elif query.data.startswith('pay_'):
        service_code = query.data[4:]
        name, price, _ = SERVICE_DETAILS[service_code]
        amount = int(price.replace('₹', ''))
        add_order(amount)

        await query.edit_message_text(
            text=f"💳 *Payment Instructions for {name}* 💳\n\n"
                 f"Please send {price} to our UPI ID:\n\n"
                 f"🔹 *UPI ID:* `{UPI_ID}`\n\n"
                 "📸 After payment, send screenshot to @opanshuff2k with:\n"
                 "- Your Telegram ID\n"
                 "- Service purchased\n\n"
                 "⏳ *Delivery time:* 10-60 minutes\n"
                 "🛡️ *Guarantee:* Full refund if not delivered",
            reply_markup=back_to_menu_keyboard(),
            parse_mode="Markdown"
        )

    elif query.data == 'main_menu':
        if is_admin(user.id):
            keyboard = [
                [InlineKeyboardButton("🔐 Wordlist Vault", callback_data='wordlist')],
                [InlineKeyboardButton("📞 Virtual Numbers", callback_data='numbers')],
                [InlineKeyboardButton("📧 Anonymous Emails", callback_data='emails')],
                [InlineKeyboardButton("📱 Phone Monitoring", callback_data='monitoring')],
                [InlineKeyboardButton("📸 Instagram Growth", callback_data='instagram')],
                [InlineKeyboardButton("🎮 Free Fire Hacks", callback_data='freefire')],
                [InlineKeyboardButton("💻 PC Optimization", callback_data='pc')],
                [InlineKeyboardButton("🔑 Password Recovery", callback_data='password')],
                [InlineKeyboardButton("🎁 Special Bundles", callback_data='bundles')],
                [InlineKeyboardButton("ℹ️ About CyberToolkit", callback_data='about')],
                [InlineKeyboardButton("🛠️ Admin Panel", callback_data='admin_panel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = main_menu_keyboard()

        await query.edit_message_text(
            text="🔥 *MAIN MENU* 🔥\n\nWhat service do you need?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# ====================
# ERROR HANDLER
# ====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# ====================
# MAIN FUNCTION
# ====================

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("terms", terms))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Button handler
    application.add_handler(CallbackQueryHandler(button))

    # Message handler (for all non-command messages)
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_messages))

    # Error handler
    application.add_error_handler(error_handler)

    # Start bot
    application.run_polling()

if __name__ == "__main__":
    main()
