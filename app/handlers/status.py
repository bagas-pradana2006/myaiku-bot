from telegram import Update
from telegram.ext import ContextTypes

from monitoring.system import (
    get_cpu_usage,
    get_memory,
    get_disk,
)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cpu = get_cpu_usage()

    ram = get_memory()

    disk = get_disk()

    await update.message.reply_text(
        f"""
🖥 Home Server

🟢 Server Online

⚡ CPU
{cpu} %

🧠 RAM
{ram['used']} / {ram['total']} GB
({ram['percent']}%)

💾 Disk
{disk['used']} / {disk['total']} GB
({disk['percent']}%)
"""
    )