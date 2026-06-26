import pandas as pd

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

try:
    from config import TOKEN
except ModuleNotFoundError:
    TOKEN = os.getenv("TOKEN")


# Загружаем Excel
df = pd.read_excel(
    "students.xlsx",
    dtype={"ИИН": str}
)
print("✅ Бот запущен")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! 👋\n\n"
        "Введите свой ИИН (12 цифр)."
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    iin = update.message.text.strip()

    # Проверяем ИИН
    if not iin.isdigit() or len(iin) != 12:
        await update.message.reply_text(
            "❌ ИИН должен состоять ровно из 12 цифр."
        )
        return

    # Поиск
    result = df[
    df["ИИН"]
    .astype(str)
    .str.strip()
    == iin
]

    if result.empty:
        await update.message.reply_text(
            "❌ Пользователь с таким ИИН не найден."
        )
        return

    row = result.iloc[0]

    text = f"""
👤 <b>ФИО</b>
{row["ФИО"]}

📊 <b>Баллы</b>
{row["Баллы"]}

📄 <b>Договор</b>
{row["Договор"]}

📒 <b>Дневник</b>
{row["Дневник"]}

📑 <b>Отчет</b>
{row["Отчет"]}

📅 <b>Сроки сдачи</b>
{row["Сроки сдачи"]}

📚 <b>Кол. стр. (12–15)</b>
{row["Кол. стр. (12-15)"]}

📝 <b>Требования по отчету</b>
{row["Требования по отчету"]}

🤖 <b>Структура отчета</b>
{row["Структура отчета"]}
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    print("✅ Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()