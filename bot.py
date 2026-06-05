from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = "8886471513:AAHl59e2GyAA2Pc2t0qPx_XYolKmp4UNbH8"
ADMIN_ID = 7735749850

CARD_NUMBER = "6219861832731722"
CARD_OWNER = "علی رنجی نوحدانی"

PLAN = 1
RECEIPT = 2

plans = {
    "30 گیگ": "300,000 تومان",
    "50 گیگ": "450,000 تومان",
    "100 گیگ": "750,000 تومان",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["30 گیگ"], ["50 گیگ"], ["100 گیگ"]]

    await update.message.reply_text(
        "سلام 👋\n\n"
        "پلن موردنظر خود را انتخاب کنید.\n\n"
        "تمام پلن‌ها بدون محدودیت زمان و کاربر هستند و فقط محدودیت حجمی دارند.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

    return PLAN


async def choose_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    plan = update.message.text

    if plan not in plans:
        await update.message.reply_text("لطفاً یکی از پلن‌ها را انتخاب کنید.")
        return PLAN

    context.user_data["plan"] = plan

    await update.message.reply_text(
        f"پلن انتخابی: {plan}\n"
        f"قیمت: {plans[plan]}\n\n"
        f"شماره کارت:\n{CARD_NUMBER}\n"
        f"به نام: {CARD_OWNER}\n\n"
        "لطفاً مبلغ را رند واریز نکنید.\n"
        "مثال: به جای 4,500,000 ریال مبلغی مانند 4,498,000 یا 4,504,200 ریال واریز کنید.\n\n"
        "در توضیحات تراکنش عبارت «خرید VPN» یا موارد مشابه ننویسید.\n\n"
        "پس از پرداخت، تصویر رسید را ارسال کنید."
    )

    return RECEIPT


async def receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("لطفاً تصویر رسید را ارسال کنید.")
        return RECEIPT

    user = update.effective_user
    plan = context.user_data.get("plan", "-")

    photo = update.message.photo[-1].file_id

    caption = (
        "🔔 سفارش جدید\n\n"
        f"👤 نام: {user.full_name}\n"
        f"🆔 یوزرنیم: @{user.username if user.username else 'ندارد'}\n"
        f"🔢 آیدی عددی: {user.id}\n\n"
        f"📦 پلن: {plan}"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption
    )

    await update.message.reply_text(
        "✅ رسید شما ثبت شد.\n"
        "پس از بررسی پرداخت، سفارش شما تأیید خواهد شد."
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات لغو شد.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PLAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_plan)],
            RECEIPT: [MessageHandler(filters.PHOTO, receipt)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
