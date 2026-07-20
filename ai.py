from collections import Counter

from game import can_play


def choose_color(hand):

    colors = []

    for card in hand:

        if card["color"] != "wild":
            colors.append(card["color"])


    if not colors:
        return "🔴 قرمز"


    most_common = Counter(colors).most_common(1)

    return most_common[0][0]



def bot_choose_card(game):

    hand = game["bot"]
    current = game["current"]


    possible_cards = []


    for index, card in enumerate(hand):

        if can_play(card, current):

            possible_cards.append(
                (index, card)
            )


    # اگر هیچ کارتی ندارد
    if not possible_cards:
        return None



    # اولویت کارت‌های قوی
    priority = {
        "🌈 +4": 4,
        "+2": 3,
        "🌈 تغییر رنگ": 2
    }


    best = possible_cards[0]


    for item in possible_cards:

        if priority.get(item[1]["value"], 1) > priority.get(best[1]["value"], 1):

            best = item



    return best[0]



def bot_play(game):

    index = bot_choose_card(game)


    if index is None:
        return None


    card = game["bot"].pop(index)


    game["current"] = card


    if card["color"] == "wild":

        game["current"]["color"] = choose_color(
            game["bot"]
        )


    return card
