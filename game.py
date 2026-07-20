from cards import create_deck, draw_card


def create_game():

    deck = create_deck()

    player_hand = []
    bot_hand = []


    for _ in range(7):
        player_hand.append(draw_card(deck))
        bot_hand.append(draw_card(deck))


    current_card = draw_card(deck)


    while current_card["color"] == "wild":
        deck.append(current_card)
        current_card = draw_card(deck)



    return {

        "deck": deck,

        "player": player_hand,

        "bot": bot_hand,

        "current": current_card,

        "winner": None,

        "waiting_color": False,

        "pending_card": None

    }



def can_play(card, current):


    # کارت‌های Wild همیشه قابل بازی هستند
    if card["color"] == "wild":
        return True


    # رنگ یکی باشد
    if card["color"] == current["color"]:
        return True


    # عدد یا قدرت یکی باشد
    if card["value"] == current["value"]:
        return True


    return False




def play_card(game, player, index):


    card = game[player].pop(index)


    game["current"] = card



    if len(game[player]) == 0:

        game["winner"] = player



    return card





def draw_cards(game, player, amount=1):


    cards = []


    for _ in range(amount):

        card = draw_card(game["deck"])


        if card:

            game[player].append(card)

            cards.append(card)



    return cards





def apply_effect(game, card, target):


    if card["value"] == "+2":


        draw_cards(
            game,
            target,
            2
        )



    elif card["value"] == "🌈 +4":


        draw_cards(
            game,
            target,
            4
        )





def set_wild_color(game, color):


    if game["current"]["color"] == "wild":

        game["current"]["color"] = color
