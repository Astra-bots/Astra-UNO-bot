import random


COLORS = [
    "🔴 قرمز",
    "🔵 آبی",
    "🟢 سبز",
    "🟡 زرد"
]


NUMBERS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
]


SPECIAL_CARDS = [
    "+2"
]


WILD_CARDS = [
    "🌈 تغییر رنگ",
    "🌈 +4"
]



def create_deck():

    deck = []


    # کارت‌های عددی
    for color in COLORS:

        for number in NUMBERS:

            deck.append(
                {
                    "color": color,
                    "value": number
                }
            )


            # اعداد به جز صفر دوباره تکرار می‌شوند
            if number != "0":

                deck.append(
                    {
                        "color": color,
                        "value": number
                    }
                )



    # کارت +2
    for color in COLORS:

        for _ in range(2):

            deck.append(
                {
                    "color": color,
                    "value": "+2"
                }
            )



    # کارت‌های وحشی
    for _ in range(4):

        deck.append(
            {
                "color": "wild",
                "value": "🌈 تغییر رنگ"
            }
        )

        deck.append(
            {
                "color": "wild",
                "value": "🌈 +4"
            }
        )


    random.shuffle(deck)

    return deck



def draw_card(deck):

    if len(deck) == 0:
        return None

    return deck.pop()
