from classes import game 

rules = game.Rules()

print('Welcome!')
print('\n\nIf you want to procede fast enter "/automatic" instead of position')
print('\nAttention: Auto mode might be more stupid than computer!')

name = input("Enter your name : ")
print(f"Hello {name}")

print("On which size of map do you want to play?")
size = input('Please enter size as [nr_row,nr_col]')

try:
    size = size.replace('[','').replace(']','')
    print('your answer was:')
    print(size)
    if ',' in size:
        print(1)
        nr1,nr2 = size.split(',')
    elif ' ' in size:
        print(2)
        nr1,nr2 = size.split(' ')
    # print(f'i see nr1 as {nr1}')
    # print(f'i see nr2 as {nr2}')
    nr1 = int(nr1)
    nr2 = int(nr2)
    rules.nr_rows = nr1
    rules.nr_cols = nr2
except:
    print("Your input could not be processed.")
    print("A size of 7x7 will be set.")
    rules.nr_rows = 7
    rules.nr_cols = 7
rules.adjust_ship_amount_to_map()
for i in range(2,10):
    a = rules.__getattribute__(f'nr_ships_L{i}')
    print(f'ships of length {i}: {a}')

print(f'chosen field size: {rules.nr_rows},{rules.nr_cols}')
map1 = game.BattleMap(rules,name)
map1.print_my_own()

map2 = game.BattleMap(rules,'computer3')
# map2.print_opponent()
map2.print_my_own()

# game_instance = game.Game(rules,map1,map2)
# game_instance.start_game()
