import numpy as np
# https://docs.python.org/3/library/string.html#string.ascii_lowercase
from string import ascii_lowercase as letters

class Rules():
    '''
    object to store and access rules
    '''

    def __init__(self):
        self.nr_cols = 7
        self.nr_rows = 7
        self.nr_ships_L2 = 3
        self.nr_ships_L3 = 2
        self.nr_ships_L4 = 1
        self.nr_ships_L5 = 0
        self.nr_ships_L6 = 0
        self.nr_ships_L7 = 0
        self.nr_ships_L8 = 0
        self.nr_ships_L9 = 0

    def get_ship_lengths(self):
        ''' return list of length of ships given in attributes '''
        ship_attr = [ a for a in self.__dir__() if 'nr_ships_L' in a]
        ship_len  = [ int(ship[10:]) for ship in ship_attr]
        return ship_len

    def adjust_ship_amount_to_map(self):
        ''' 
        give opportunity to adjust ship amount according to space
        calculation is done approximately
        '''
        # when ship positioned at border it consumes less area than estimated
        area = (1+self.nr_cols) * (1+self.nr_rows)
        lens = self.get_ship_lengths()
        min_spaces = [(4*len)**1.5 for len in lens]
        # for i,sl in enumerate(lens):
        pars = 1
        dividor = 1.8
        for sl in lens:
            pars /= dividor
            min_space = 4 + (3*sl+3)**1.0
            allowed_number = pars*area / min_space
            possible_amount = round(allowed_number)
            # print(f'the length {sl} gets {possible_amount} ships')
            self.__setattr__(f'nr_ships_L{sl}', possible_amount)

class Field():
    '''
    object to keep track of:
        ship positions
        discovered positions
    providing dummy to fill with visualisation signs
    '''

    def __init__(self,rules):
        self.pos_ships      = np.zeros([rules.nr_rows, rules.nr_cols],'int')
        self.pos_discovered = np.zeros([rules.nr_rows, rules.nr_cols],'int')
        self.field_dummy = rules.nr_cols*[' '.join(rules.nr_cols*['%s'])]


class BattleMap(Field):
    '''
    class to give a Field the necessary functionality to interact with
    '''
    instances = []

    def __init__(self,rules,player):
        self._rules = rules
        if rules.nr_cols > 26:
            rules.nr_cols = 26
            print('\nAlert, number of columns has been adjusted to 26. \
            Code is not prepared to handle more than one letter as coordinate!')
        # if rules.nr_rows > 26:
        #     rules.nr_rows = 26
        #     print('\nAlert, number of rows has been adjusted to 26. \
        #   Code is not prepared to handle more than one letter as coordinate!')

        super().__init__(rules)
        self._prepare_decorator(rules)   
        # class attributes
        # meaning defined by key! replace value for different visualisation!
        self.visualisation = {\
            '0': '.',
            '1': 'G',
            '2': ' ',
            '3': 'c',
            '5': 'O',
            '6': '@',
            '7': 'x'}
        self.last_discovered = (-1,-1)
        self.bool_automatic = False
        self.player = player
        # deploy ships
        self._deploy_ships_randomly(rules)
        self.__class__.instances.append(self)

    def _deploy_ships_randomly(self,rules):
        '''
        randomly distributes ships on the map 
        amount defined in the nr_ships_L* attribute of the rules object
        '''
        # ship can not be deploy in last rows horizontal and
        # in last columns vertically
        # maybe improve deploying later !!!
        # collecting demanded ships
        ship_len = self._rules.get_ship_lengths()
        ship_len.sort(reverse=True)

        #prepare 
        success = False
        i_max = 250
        i = 0

        while not success and i < i_max:
            for sl in ship_len:
                attr = 'nr_ships_L%i' %sl
                for i_ship in range(rules.__getattribute__(attr)):
                    success = False
                    j = 0
                    while not success and j < i_max:
                        [success,pos] = self._position_ship(length=sl)
                        j += 1
                    # print(f'{j} attempts to position single ship')
                    if success:
                        for p in pos:
                            self.pos_ships[p] = 1
            i += 1
        # print(f'{i} attempts to position all ships')
        if not success:
            message = '\n\nCould not deploy all ships as intended.' +\
                    '\nPlease try again or decrease number of ships in rules!'
            raise RuntimeError(message)

    def _position_ship(self,length):
        '''
        randomly try to position one ship of given length
        and 
        return success state and position
        '''
        nr,nc = self.pos_ships.shape
        # choose direction south or east and collect all points
        d = np.random.randint(2)
        # choose start pos:
        if d == 0:
            x = np.random.randint(0,nc)
            y = np.random.randint(0,nr - length + 1)
            pos = [(y+i,x) for i in range(length)]
        elif d == 1:
            x = np.random.randint(0,nc - length + 1)
            y = np.random.randint(0,nr)
            pos = [(y,x+i) for i in range(length)]
        # check collision with neighbouring ships
        return self._check_neighbours(pos), pos
        
    def _check_neighbours(self,positions):
        '''
        return True if no ship on position and if no neighbours on position
        '''
        nr,nc = self.pos_ships.shape
        for pos in positions:
            if self.pos_ships[pos]:
                return False
            if pos[0] > 0 and self.pos_ships[pos[0]-1,pos[1]]:
                return False
            if pos[0] < nr-1 and self.pos_ships[pos[0]+1,pos[1]]:
                return False
            if pos[1] > 0 and self.pos_ships[pos[0],pos[1]-1]:
                return False
            if pos[1] < nc-1 and self.pos_ships[pos[0],pos[1]+1]:
                return False
        return True

    def _prepare_decorator(self,rules):
        '''
        prepare dummy part for field to be filled with data
        and 
        prepare decorator
        '''
        space_letter = 2
        space_nr = np.int8(np.floor( np.log10( rules.nr_rows )) + 2)
        spacer_nbr = ''.join(space_nr*[' '])
        line_letters = \
            spacer_nbr \
            + ''.join((space_letter-1)*[' ']).join(letters[:rules.nr_cols]) \
            + spacer_nbr
        
        placing = ' ' + ' '.join(rules.nr_cols*['%s']) + ' '
        center = \
            [''.join(\
            [str.rjust(str(i),space_nr-1), placing, str.ljust(str(i),space_nr-1)]\
            ) for i in range(rules.nr_rows)]
        # https://dev.to/ra1nbow1/8-ways-to-add-an-element-to-the-beginning-of-a-list-and-string-in-python-925
        s = [line_letters] + center + [line_letters]
        
        self.decorator_lines = '\n'.join(s)
        
    def print_my_own(self):
        '''
        print map openly
        
        as set in the self.visualisation:
        # . - unopened / unopened and no ship - 0 -   small sign, indicating free space
        # G - ship, if no hit                   - 1 -   big sign as like still swimming
        #   - hit before / empty    - 2 -   empty sign 
        # O - hit before / empty    - 4 -   empty sign 
        # c - ship hit              - 3 -   small sign and open as like hit 
        # @ - ship hit              - 6 -   ship, if last hit
        # x - targeted              - 7 -    
        '''
        # 0 - no ship, not uncovered  |
        # 1 - ship                      | ship *1  
        # 2 - uncoverd empty                    | 
        # 3 - uncoverd ship                     |        | uncovered *2
        # 4 - last but uncovered - impossible
        # 5 - last hit, empty                   |        |
        # 6 - last hit, ship                    |        |        | last *3
        # 7 - targeted (no calculation)

        # calculate visualisation
        field = self.pos_ships + 2*self.pos_discovered
        if -1 not in self.last_discovered:
            field[self.last_discovered] += 3
        # transform to list of strings
        state_str = [ str(i) for i in field.reshape(field.size) ]
        # replace with desired symbols
        state_str = [ self.visualisation[s] for s in state_str ]
        s = self.decorator_lines
        #print(field)
        s = self.decorator_lines %(*state_str[:],)
        
        print(f"\n{self.player}'s map:")
        print(s)
        
    def print_visualisation(self):
        ''' print expanation of visualisation symbols '''
        print(f'\n{self.player}`s map is visualised with following symbols:')
        print(f"'0': {self.visualisation['0']} - unopened position")
        print(f"'1': {self.visualisation['1']} - " +\
            "ship, unhit (not visible to opponent)")
        print(f"'2': {self.visualisation['2']} - opened position but empty")
        print(f"'3': {self.visualisation['3']} - hit ship position")
        print(f"'5': {self.visualisation['5']} - "+\
            "last targeted if empty position")
        print(f"'6': {self.visualisation['6']} - "+\
            "last targeted if ship / last hit")
        print(f"'7': {self.visualisation['7']} - "+\
            "actual targeted position (not applicable on web interface)")

    def print_opponent(self):
        '''
        print the map to console as to opponent
        '''
        
        # calculate visualisation
        field = self.pos_ships + 2*self.pos_discovered
        if -1 not in self.last_discovered:
            field[self.last_discovered] += 3
        # hide not opened positions
        unopened = self.pos_discovered == 0
        field[unopened] = 0
        # transform to list of strings
        state_str = [ str(i) for i in field.reshape(field.size) ]
        # replace with desired symbols
        state_str = [ self.visualisation[s] for s in state_str ]
        s = self.decorator_lines
        #print(field)
        s = self.decorator_lines %(*state_str[:],)
        
        print(f"\n{self.player}'s map:")
        print(s)

    def get_ship_position(self,pos):
        '''
        collect all connected ship positions,
        thus returnin all positions of one ship
        
        input: pos - (x,y)
        '''
        if self.pos_ships[pos] == 0:
            return []
        ans = [pos]
        pos0,pos1 = self.pos_ships.shape
        pos0 -= 1
        pos1 -= 1
        # detect direction
        if pos[0] > 0 and self.pos_ships[pos[0]-1,pos[1]] \
            or pos[0] < pos0 and self.pos_ships[pos[0]+1,pos[1]]:
                i = 1
                while pos[0] + i <= pos0 and self.pos_ships[pos[0]+i,pos[1]]:
                    ans.append( (pos[0]+i,pos[1]) )
                    i += 1
                i = -1
                while pos[0]+i >= 0 and self.pos_ships[pos[0]+i,pos[1]]:
                    ans.append( (pos[0]+i,pos[1]) )
                    i -= 1
        elif pos[1] > 1 and self.pos_ships[pos[0],pos[1]-1] \
            or pos[1] < pos0 and self.pos_ships[pos[0],pos[1]+1]:
                i = 1
                while pos[1] + i <= pos1 and self.pos_ships[pos[0],pos[1]+i]:
                    ans.append( (pos[0],pos[1]+i) )
                    i += 1
                i = -1
                while pos[1]+i >= 0 and self.pos_ships[pos[0],pos[1]+i]:
                    ans.append( (pos[0],pos[1]+i) )
                    i -= 1
        return ans
        
    def check_ship_sunk(self,pos):
        '''
        check whether all given positions are discovered
        
        input: pos - [(x1,y1),...]
        '''
        for p in pos:
            if not self.pos_discovered[p]:
                return False
        return True        

    def check_all_ship_sunk(self):
        ''' check for game over '''
        inds = self.pos_ships == 1
        all_disovered = np.all( self.pos_discovered[inds] == 1 )
        return all_disovered

    def guess_randomly(self):
        '''
        make a random guess of position to open
        '''
        # https://numpy.org/doc/stable/reference/generated/numpy.argwhere.html
        possible_positions = np.argwhere( self.pos_discovered == 0 )
        possible_positions = [(v[0], v[1]) for v in possible_positions]
        if len(possible_positions) == 0:
            return (0,0)
        ind = np.random.randint(0,len(possible_positions))
        return possible_positions[ind]

class Game():
    '''
    instance for running game
    input: Rules instance
    '''
    
    def __init__(self,rules,map1,map2):
        # map1 is one's own map
        # map2 is opponents map
        self.map1 = map1
        self.map2 = map2
        self._rules = rules
        self._len_letter = int(np.ceil(rules.nr_cols/26))
        self.cols = letters[:rules.nr_cols]
        self.rows = [str(int(i)) for i in range(rules.nr_rows)]
        # set computer difficulty
        if 'Easy' in self.map2.player:
            self.difficulty = 1
        elif 'Advanced' in self.map2.player:
            self.difficulty = 2
        elif 'Hard' in self.map2.player:
            self.difficulty = 3
        else:
            self.difficulty = 1

    def ask_position(self,mapa):
        ''' ask user for position to uncover '''
        if mapa.bool_automatic == True:
            inp = input("Continue automatic guess? Hit enter or Yes or 1 or y to confirm!")
            if inp in ['y','Y','Yes','1','']:
                return mapa.guess_randomly()
            elif len(inp) > 0 and inp[0] == '/' and inp in '/quit':
                self.map1.pos_discovered = np.ones(self.map1.pos_discovered.shape,dtype='int')
                return (-1,-1)
            else:
                mapa.bool_automatic = False
                inp = input("Which position do you want to target? : ")
        else:
            inp = input("Which position do you want to target? : ")
        if len(inp)== 1 and inp[0] == '/':
            mapa.bool_automatic = True
            return mapa.guess_randomly()
        if len(inp) > 0 and inp[0] == '/' and inp in '/quit':
            self.map1.pos_discovered = np.ones(self.map1.pos_discovered.shape,dtype='int')
            return (-1,-1)
        if len(inp) > 0 and inp[0] == '/' and inp in '/automatic':
            mapa.bool_automatic = True
            return mapa.guess_randomly()
        if len(inp) < self._len_letter + 1:
            print("\n"+\
            "\nPlease enter a position in the format 'xy123'"+\
            "\nproviding the position of column with the indicated letter"+\
            "\nand the position of the row with the indicated number.")
            return self.ask_position(mapa)
        x = letters.find( inp[:self._len_letter] )
        if x == -1:
            print("No valid letter given as first sign of answer.")
            print("Please enter a position in the format 'xy123'")
            return self.ask_position(mapa)
        try:
            y = int( inp[self._len_letter:] )
        except:
            print(f'No number could be recoqnised after {inp[:self._len_letter]}')
            print("Please enter a position in the format 'xy123'")
            return self.ask_position(mapa)
        if x < 0 or self._rules.nr_cols <= x:
            print('\n\nPlease give a number for row in between'+\
            f' 0 and {self._rules.nr_rows-1} !')
            return self.ask_position(mapa)
        if y < 0 or self._rules.nr_rows <= y:
            print('\n\nPlease give a letter for column in between'+\
            f' a and {letters[self._rules.nr_cols-1]} !')
            return self.ask_position(mapa)
        if mapa.pos_discovered[y,x] == 1:
            print('\n\nYou can not choose a position twice!')
            return self.ask_position(mapa)
        return (y,x)
        
    def discover_position(self,mapa):
        ''' open last chosen position '''
        if mapa.last_discovered == (-1,-1): return
        mapa.pos_discovered[mapa.last_discovered] = 1
        # check ship sunk
        if mapa.pos_ships[mapa.last_discovered]:
            pos_ship = mapa.get_ship_position(mapa.last_discovered)
            if mapa.check_ship_sunk(pos_ship):
                self.explode_positions(mapa,pos_ship)

    def explode_positions(self,mapa,pos):
        ''' uncover directly neighboring positions '''
        p0,p1 = mapa.pos_discovered.shape
        p0 -= 1
        p1 -= 1
        for p in pos:
            if p[0] > 0:
                mapa.pos_discovered[p[0]-1,p[1]] = 1
            if p[0] < p0:
                mapa.pos_discovered[p[0]+1,p[1]] = 1
            if p[1] > 0:
                mapa.pos_discovered[p[0],p[1]-1] = 1
            if p[1] < p1:
                mapa.pos_discovered[p[0],p[1]+1] = 1
      
    def start_game(self):
        ''' starting a while loop until game finished '''

        self.map1.print_visualisation()
        self.map2.print_visualisation()
        print('\nIf you want to procede quickly, enter "/automatic" instead of position')
        print('Attention: Auto mode might be more stupid than computer!')
        print('By entering "/quit" instead of position, you can quit anytime.') 
        while True:
            ans1 = self.turn_player1()
            if not ans1: break
            if ans1:
                ans2 = self.turn_player2()
                if not ans2: break
        print('____________________________________________________')
        self.map1.print_my_own()
        self.map2.print_my_own()
        print('\nGame is over! Thanks for playing till the end!\n')

    def turn_player1(self):
        ''' 
        methode for turn of player1

        returns True if opponent has ships left
        returns False if all of opponent ships sunk
        '''
        self.map1.print_my_own()
        self.map2.print_opponent()
        self.map2.last_discovered = self.ask_position(self.map2)
        self.discover_position(self.map2)
        if self.map2.check_all_ship_sunk():
            print('____________________________________________________')
            print(f'\nPlayer {self.map1.player} has won!')
            return False
        if self.map2.pos_ships[self.map2.last_discovered] == 1:
            # repeat
            return self.turn_player1()
        return True

    def computer_choice(self):
        '''
        strategies how computer guesses next position
        '''
        # easy
        if self.difficulty == 1:
            return self.map1.guess_randomly()
        # medium
        elif self.difficulty == 2:
            # continue with unsunk but hit ships
            guess = self._target_unsunk_but_hit_ship()
            if guess: 
                return guess
            # otherwise
            return self.map1.guess_randomly()
        # advanced
        elif self.difficulty == 3:
            # continue with unsunk but hit ships
            guess = self._target_unsunk_but_hit_ship()
            if guess:
                print('guessing for hit ship:')
                print(guess)
                return guess
            # simple diagonal pattern 
            print('diagonal')
            return self._guess_on_diagonal_pattern()
            # otherwise
            print('random')
            return self.map1.guess_randomly()

    def _guess_on_diagonal_pattern(self):
            # a good (not best) order for getting a hit fast
            # simple diagonal approach
            opos = self.map1.pos_discovered
            ship = self.map1.pos_ships
            nr,nc = ship.shape
            control = np.arange(ship.size).reshape(ship.shape)
            # # get even indices
            even = ([y for y in range(nr) for x in range(nc) if (x+y)%2 == 0]\
                ,[x for y in range(nr) for x in range(nc) if (x+y)%2 == 0])
            control_even = [control[(even[0][i],even[1][i])] \
                for i in range(len(even[0]))]
            # even_indices_linear = [x for x in range(nr*nc,2)]

            # weighting indices
            # https://numpy.org/doc/stable/reference/generated/numpy.bartlett.html
            col_weight = np.bartlett(nc)
            row_weight = np.bartlett(nr)
            w_mat = np.array(\
                [[rw*cw for cw in col_weight] for rw in row_weight] )
            # multiplicated weight
            w_list = [y*x for y in row_weight for x in col_weight]
            # w_mat  = np.array(w_list).reshape([nr,nc])
            # sorted indices of multiplicated weight
            ind_ord = np.argsort(w_list)[::-1]
            ord1 = [e for e in ind_ord if e%2]
            ord2 = [e for e in ind_ord if not e%2]
            # revert to 2d indication
            for i in ind_ord:
                x = i%nc
                y = int((i-x)/nc)
                if control[(y,x)] in control_even and \
                    self.map1.pos_discovered[(y,x)] == 0:
                    return (y,x)
            for i in ind_ord:
                x = i%nc
                y = int((i-x)/nc)
                if self.map1.pos_discovered[(y,x)] == 0: return (y,x)

    def _target_unsunk_but_hit_ship(self):
        '''
        find hit ships, which are not sunk yet
        and guess a position next to them
        '''
        # find hit ship which is not sunk
        # (it is not sunk, if there are unopened field next to hitsnr
        opos = self.map1.pos_discovered
        ship = self.map1.pos_ships
        hits = np.argwhere(2 == ship + opos)
        pos0,pos1 = ship.shape
        pos0 -= 1
        pos1 -= 1
        for pos in hits:
            direction = self.get_direction_of_hit(self.map1,pos,hits)
            p0,p1 = pos
            if direction == 0:
                if 0 < p0 and opos[p0-1,p1] == 0:
                    return (p0-1,p1)
                if p0 < pos0 and opos[p0+1,p1] == 0:
                    return (p0+1,p1)
            if direction == 1:
                if 0  < p1   and opos[p0,p1-1] == 0:
                    return (p0,p1-1)
                if p1 < pos1 and opos[p0,p1+1] == 0:
                    return (p0,p1+1)
        return ()

    def get_direction_of_hit(self,mapa,pos,hits):
        ''' returning direction of hit ship if visible '''
        # get neighbours
        i = hits.tolist().index(list(pos))
        if i > 0:
            if hits[i-1][0] == pos[0]:
                return 1
            if hits[i-1][1] == pos[1]:
                return 0
        if i < len(hits) - 1:
            if hits[i+1][0] == pos[0]: 
                return 1
            if hits[i+1][1] == pos[1]:
                return 0
        return np.random.randint(2)

    def turn_player2(self):
        '''
        methode for turn of player1

        returns True if opponent has ships left
        returns False if all of opponent ships sunk
        '''
        # self.map2.print_my_own()
        # self.map1.print_opponent()
        # self.map1.last_discovered = self.map1.guess_randomly()
        self.map1.last_discovered = self.computer_choice()
        self.discover_position(self.map1)
        if self.map1.check_all_ship_sunk():
            print('____________________________________________________')
            print(f'\nPlayer {self.map2.player} has won!')
            return False
        if self.map1.pos_ships[self.map1.last_discovered] == 1:
            # repeat
            self.map1.print_my_own()
            self.map2.print_opponent()
            return self.turn_player2()
        return True
