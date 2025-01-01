from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random, datetime

# Remplacez par votre token API
API_TOKEN = "8191740195:AAElItof0jfiEFJu2d5zX-CZLvR5tUb9qaY"

# Limite de prédictions (par défaut : 5)
MAX_PREDICTIONS = 5
user_predictions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_predictions[chat_id] = 0
    keyboard = [[InlineKeyboardButton("Prédire", callback_data='predict')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Bienvenue ! Cliquez sur 'Prédire' pour commencer.",
        reply_markup=reply_markup
    )

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id

    # Vérifie si l'utilisateur a dépassé sa limite
    if chat_id in user_predictions and user_predictions[chat_id] >= MAX_PREDICTIONS:
        await query.edit_message_text(
            text="❌ Vous avez atteint la limite de prédictions. "
                 "Contactez +22656967818 pour obtenir un accès illimité avec le code : 'Tall@2008'."
        )
        return

    # Générer des prédictions
    now = datetime.datetime.now()
    cote_a = round(random.uniform(4.00, 25.00), 2)
    cote_b = round(random.uniform(4.00, 25.00), 2)
    assurance = round(random.uniform(3.00, 6.00), 2)
    time1 = (now + datetime.timedelta(minutes=random.randint(2, 5))).strftime("%H:%M")
    time2 = (now + datetime.timedelta(minutes=random.randint(3, 6))).strftime("%H:%M")

    prediction_text = (
        f"🧨 MARC LUCKYJET V2 🧨\n\n"
        f"*HEURE : {time1} — {time2}\n"
        f"*COTE : x{min(cote_a, cote_b)} — x{max(cote_a, cote_b)}\n"
        f"*ASSURANCE : x{assurance}\n\n"
        f"*Ces cotes viendront dans l'intervalle donné !*"
    )

    # Envoyer la prédiction
    user_predictions[chat_id] += 1
    keyboard = [[InlineKeyboardButton("Nouvelle Prédiction", callback_data='predict')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=prediction_text, reply_markup=reply_markup)

def main():
    application = ApplicationBuilder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(predict, pattern="predict"))

    application.run_polling()

if __name__ == "__main__":
    main()
