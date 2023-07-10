from classes import game 

rules = game.Rules()

map1 = game.BattleMap(rules)
map1.print_my_own()

map2 = game.BattleMap(rules)
map2.print_opponent()

game_instance = game.set_up_game(rules)
game_instance.start_game()
