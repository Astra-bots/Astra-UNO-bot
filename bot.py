import os

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from game import (
    create_game,
    can_play,
    play_card,
    draw_cards,
    apply_effect,
    set_wild_color
)

from ai import bot_play



load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


games = {}





def card_text(card):

    return f"{card['color']} {card['value']}"





def game_keyboard(game):

    keyboard = []


    for index, card in enumerate(game["player"]):

        if can_play(card, game["current"]):

            keyboard.append(
                [
                    InlineKeyboardButton(
                        card_text(card),
                        callback_data=f"card_{index}"
                    )
                ]
            )



    keyboard.append(
        [
            InlineKeyboardButton(
                "🃏 کارت بکش",
                callback_data="draw"
            )
        ]
    )


    return InlineKeyboardMarkup(keyboard)





def color_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔴 قرمز",
                    callback_data="color_🔴 قرمز"
                ),
                InlineKeyboardButton(
                    "🔵 آبی",
                    callback_data="color_🔵 آبی"
                )
            ],
            [
                InlineKeyboardButton(
                    "🟢 سبز",
                    callback_data="color_🟢 سبز"
                ),
                InlineKeyboardButton(
                    "🟡 زرد",
                    callback_data="color_🟡 زرد"
                )
            ]
        ]
    )






async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id


    games[user_id] = create_game()


    game = games[user_id]


    await update.message.reply_text(

        "🃏 Astra UNO شروع شد!\n\n"
        f"کارت وسط:\n"
        f"{card_text(game['current'])}\n\n"
        "کارت خودت را انتخاب کن:",

        reply_markup=game_keyboard(game)

    )






async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):


    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    if user_id not in games:

        return



    game = games[user_id]


    data = query.data





    # انتخاب رنگ Wild

    if data.startswith("color_"):


        color = data.replace(
            "color_",
            ""
        )


        set_wild_color(
            game,
            color
        )


        game["waiting_color"] = False



        apply_effect(
            game,
            game["pending_card"],
            "bot"
        )



        bot_play(game)



    # کارت کشیدن

    elif data == "draw":


        draw_cards(
            game,
            "player"
        )




    # بازی کارت

    elif data.startswith("card_"):


        index = int(
            data.split("_")[1]
        )


        card = game["player"][index]



        if not can_play(
            card,
            game["current"]
        ):

            return



        played = play_card(
            game,
            "player",
            index
        )



        if played["color"] == "wild":


            game["waiting_color"] = True

            game["pending_card"] = played



            await query.edit_message_text(

                "🌈 رنگ بعدی را انتخاب کن:",

                reply_markup=color_keyboard()

            )

            return




        apply_effect(
            game,
            played,
            "bot"
        )



        if game["winner"]:

            await query.edit_message_text(
                "🏆 تو بردی!"
            )

            return



        bot_play(game)



        if game["winner"]:

            await query.edit_message_text(
                "🤖 ربات برد!"
            )

            return






    await query.edit_message_text(

        f"🃏 کارت وسط:\n"
        f"{card_text(game['current'])}\n\n"
        f"کارت تو: {len(game['player'])}\n"
        f"کارت ربات: {len(game['bot'])}",

        reply_markup=game_keyboard(game)

    )






def main():


    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(play)
    )


    print("Astra UNO Started 🃏")


    app.run_polling()





if __name__ == "__main__":

    main()
