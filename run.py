from classes import game 

# two default values
rules = game.Rules()
AI = 'computer2'

print('Welcome!')
print('\nIf you want to procede fast enter "/automatic" instead of position')
print('\nAttention: Auto mode might be more stupid than computer!')

name = input("\nEnter your name (or nothing for fast start) : ")
if name:
    print(f"Hello {name}")

    print("On which size of map do you want to play?")
    size = input('\nPlease enter size as [nr_row,nr_col] : ')

    try:
        size = size.replace('[','').replace(']','')
        if ',' in size:
            nr1,nr2 = size.split(',')
        elif ' ' in size:
            nr1,nr2 = size.split(' ')
        nr1 = int(nr1)
        nr2 = int(nr2)
        if nr1 < 4:
            nr1 = 4
            print("Adjusted minimal row amount to 4")
        if nr2 < 5:
            nr2 = 5
            print("Adjusted minimal column amount to 5")
        if nr1 > 26:
            nr1 = 26
            print("Adjusted minimal row amount to 26")
        if nr2 > 26:
            nr2 = 26
            print("Adjusted minimal column amount to 26")
        rules.nr_rows = nr1
        rules.nr_cols = nr2
    except:
        print("\n\tYour input could not be processed.")
        print("\nA size of 7x7 will be set.")
        rules.nr_rows = 7
        rules.nr_cols = 7
    rules.adjust_ship_amount_to_map()

    # difficulty
    print('Against who do you want to play?')
    oponent = input("[1] - Computer1 ; [2] - Computer2 ; [3] - Computer3 : ")
    if '1' in oponent:
        AI = 'computer1'
    elif '2' in oponent:
        AI = 'computer2'
    elif '3' in oponent:
        AI = 'computer3'
    else:
        print('\n\tI choose "Computer2" for you.')
else:
    rules = game.Rules()

map1 = game.BattleMap(rules,name)
map1.print_my_own()

map2 = game.BattleMap(rules,AI)
# map2.print_opponent()
map2.print_my_own()

game_instance = game.Game(rules,map1,map2)
game_instance.start_game()
