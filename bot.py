import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Clé API Telegram
TELEGRAM_API_KEY = '7044574411:AAFxdsxuq3kfwneKewngfbzqVx3OrhCtLcM'

# ID Telegram de ton bot
CHAT_ID = '7104713412'

# URL de l'API externe comme dans le script Java
API_URL = "https://kaiz-apis.gleeze.com/api/gpt-4o"

# Configurer le logging pour suivre les erreurs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction pour démarrer le bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salut ! Pose-moi une question et je vais y répondre avec GPT.")

# Fonction pour traiter les messages et obtenir des réponses de l'API GPT
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text  # Message de l'utilisateur

    if user_message.startswith('/'):
        return  # Ignorer les commandes

    try:
        # Préparer la requête pour l'API GPT
        params = {
            'q': user_message,
            'uid': update.message.from_user.id  # ID de l'utilisateur pour personnaliser l'appel
        }

        # Effectuer la requête à l'API
        response = requests.get(API_URL, params=params)

        # Vérifier si la réponse est correcte
        if response.status_code == 200:
            data = response.json()  # Extraire les données JSON de la réponse
            bot_reply = data.get('response', 'Désolé, je n'ai pas pu générer une réponse.')

            # Styliser et ajouter des emojis à la réponse
            styled_reply = bot_reply + " 😎🔥"  # Tu peux styliser comme tu veux ici

            # Envoi de la réponse générée par l'API sur Telegram
            update.message.reply_text(styled_reply)
        else:
            update.message.reply_text("Désolé, une erreur est survenue lors de la génération de la réponse. 😞")
            logger.error(f"Erreur de l'API GPT : {response.status_code}")
    
    except Exception as e:
        update.message.reply_text("Désolé, une erreur est survenue. Veuillez réessayer plus tard.")
        logger.error(f"Erreur : {e}")

# Fonction pour gérer les erreurs
def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Fonction principale pour démarrer le bot
def main():
    # Crée une instance de l'Updater avec le token de ton bot Telegram
    updater = Updater(TELEGRAM_API_KEY, use_context=True)

    # Obtiens le dispatcher pour enregistrer les gestionnaires de commandes
    dispatcher = updater.dispatcher

    # Ajoute un gestionnaire pour la commande /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Ajoute un gestionnaire pour les messages texte
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Ajoute un gestionnaire pour les erreurs
    dispatcher.add_error_handler(error)

    # Démarre le bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
