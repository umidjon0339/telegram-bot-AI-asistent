from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatAction
import asyncio
import google.generativeai as genai


BOT_TOKEN = ""
GEMINI_API_KEY = ""

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! 🤖 I am Gemini AI bot. Ask me anything!")

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Step 1: Acknowledge the message & show waiting message
    response = f"You said: {user_text}\n\nGemini is working on your request. Please wait a moment . . ."
    await update.message.reply_text(response)

    # Step 2: Show typing...
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )
    await asyncio.sleep(2)  # simulate thinking

    # Step 3: Get Gemini AI response
    try:
        result = model.generate_content(user_text)
        reply_text = result.text if result and result.text else "⚠️ Sorry, I couldn't generate a response."

    except Exception as e:
        reply_text = f"❌ Error: {e}"

    # Step 4: Send Gemini's response
    await update.message.reply_text(reply_text)

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Gemini AI Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
