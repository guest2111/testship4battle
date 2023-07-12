from classes import game 

rules = game.Rules()

print('Welcome!')
print('\n\nIf you want to procede fast enter "/automatic" instead of position')
print('\nAttention: Auto mode might be more stupid than computer!')

name = input("Enter your name : ")
map1 = game.BattleMap(rules,name)
# map1.print_my_own()

map2 = game.BattleMap(rules,'computer2')
# map2.print_opponent()

game_instance = game.Game(rules,map1,map2)
game_instance.start_game()
