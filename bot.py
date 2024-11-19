from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler

TOKEN = '7631236448:AAHUk7NH8PnnB4STRj0K6LGsDCncH7mdYNE'  # Ваш токен от BotFather
CHANNEL_LINK = 'https://t.me/+QJyC8NbFDbhkYTk6'  # Ссылка на ваш канал

# Состояния
AGE_CONFIRMATION, HUMAN_VERIFICATION = range(2)

# Стартовое сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! To proceed, you need to verify a few things.\n"
        "Step 1: Confirm that you are over 18 years old."
    )
    keyboard = [[InlineKeyboardButton("I am over 18", callback_data='over_18')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to confirm:", reply_markup=reply_markup)
    return AGE_CONFIRMATION

# Проверка возраста
async def age_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'over_18':
        await query.edit_message_text(
            text="✅ Thank you for confirming! Now, please verify that you are human."
        )
        keyboard = [[InlineKeyboardButton("I am human", callback_data='human')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Click the button below to confirm:", reply_markup=reply_markup)
        return HUMAN_VERIFICATION
    else:
        await query.edit_message_text(text="❌ You must confirm your age to proceed.")
        return AGE_CONFIRMATION

# Проверка "человек ли"
async def human_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'human':
        await query.edit_message_text(
            text="✅ Verification complete! Click the button below to join the channel."
        )
        keyboard = [[InlineKeyboardButton("Join the Channel", url=CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Click below:", reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await query.edit_message_text(text="❌ Verification failed. Please try again.")
        return HUMAN_VERIFICATION

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Verification process canceled.")
    return ConversationHandler.END

# Основной блок
def main():
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE_CONFIRMATION: [CallbackQueryHandler(age_confirmation)],
            HUMAN_VERIFICATION: [CallbackQueryHandler(human_verification)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=True  # Обрабатываем каждое сообщение
    )

    # Добавляем обработчик в приложение
    application.add_handler(conv_handler)

    # Запускаем приложение
    application.run_polling()

if __name__ == '__main__':
    main()