from io import BytesIO
import re
import textwrap
from typing import Tuple
from PIL import Image, ImageDraw, ImageOps

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler

from bot.media import FONT_MD, TECSONE
from bot.utils import only_eagle, re_command, re_emojis


@only_eagle
def tecsone(update: Update, ctx: CallbackContext):
    center = (540, 370)
    max_size = (1080, 740)
    template = TECSONE
    default = "TECSONE!"
    text_width = 32

    other_image = None

    if update.message is not None and update.message.reply_to_message is not None:
        if update.message.reply_to_message.photo is not None:
            if len(update.message.reply_to_message.photo) > 0:
                photo = update.message.reply_to_message.photo[-1]
                byte_array = BytesIO(photo.get_file().download_as_bytearray())
                other_image = Image.open(byte_array)
                default = ""
        if update.message.reply_to_message.text is not None:
            if len(update.message.reply_to_message.text) > 0:
                default = update.message.reply_to_message.text

    message = (
        re_command.sub(r"", update.message.text.strip())
        if len(ctx.args) > 0
        else default
    )

    background = Image.new("RGB", template.size, color="black")
    draw = ImageDraw.Draw(background)

    if len(message) >= 0:
        message = message.strip()  # clean start and end
        message = re_emojis.sub(r"", message)  # remove emojis
        message = "\n".join(
            textwrap.wrap(message, width=text_width, replace_whitespace=False)
        )
        draw.multiline_text(
            center,
            message,
            anchor="mm",
            align="center",
            font=FONT_MD,
            fill=(255, 255, 255, 255),
        )

    if other_image is not None:
        other_image = ImageOps.contain(other_image, max_size)
        offset = (
            center[0] - other_image.width // 2,
            center[1] - other_image.height // 2,
        )
        background.paste(other_image, offset)
        other_image.close()

    background.paste(template, (0, 0), template)

    bio = BytesIO()
    bio.name = "meme.png"
    background.save(bio, "JPEG")
    bio.seek(0)
    update.message.reply_photo(bio)

    background.close()
    bio.close()


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("tecsone", tecsone))