from classes import game

# two default values
rules = game.Rules()
AI = "Advanced AI"

print("Welcome!")

pname = input("\nEnter your name (or nothing for fast start) : ")
if pname:
    print(f"Hello {pname}")

    print("On which size of map do you want to play?")
    print("Minimal size is: [4,5]")
    print("Maximal size is: 26 26")
    size = input("\nPlease enter size as [number_row,number_col] : ")

    try:
        size = size.replace("[", "").replace("]", "")
        if "," in size:
            nr1, nr2 = size.split(",")
        elif " " in size:
            nr1, nr2 = size.split(" ")
        else:
            nr1 = size
            nr2 = ""
        nr1 = int(nr1)
        if not nr2:
            nr2 = nr1
        nr2 = int(nr2)
        if nr1 < 4:
            nr1 = 4
            print("Adjusted row amount to minimal value of 4")
        if nr2 < 5:
            nr2 = 5
            print("Adjusted column amount to minimal value of 5")
        if nr1 > 26:
            nr1 = 26
            print("Adjusted row amount to maximal value of 26")
        if nr2 > 26:
            nr2 = 26
            print("Adjusted column amount to maximal value of 26")
        rules.nr_rows = nr1
        rules.nr_cols = nr2
    except ValueError:
        print("\n\tYour input could not be processed.")
        print("\nA size of 7x7 will be set.")
        rules.nr_rows = 7
        rules.nr_cols = 7
    rules.adjust_ship_amount_to_map()

    # difficulty
    print("Choose difficulty:")
    oponent = input("[1] - Easy ; [2] - Advanced ; [3] - Hard : ")
    if "1" in oponent or "easy" in oponent.lower():
        AI = "Easy AI"
    elif "2" in oponent or "advanced" in oponent.lower():
        AI = "Advanced AI"
    elif "3" in oponent or "hard" in oponent.lower():
        AI = "Hard AI"
    else:
        print('\n\tI choose "Advanced" for you.')
else:
    pname = "Player"
    rules = game.Rules()

map1 = game.BattleMap(rules, pname)

map2 = game.BattleMap(rules, AI)

game_instance = game.Game(rules, map1, map2)
game_instance.start_game()
