import numpy as np
# https://docs.python.org/3/library/string.html#string.ascii_lowercase
from string import ascii_lowercase as letters

class Rules():
    '''
    object to store and access rules
    '''

    def __init__(self):
        self.number_cols = 12
        self.number_rows = 12
        self.nr_ships_L2 = 5
        self.nr_ships_L3 = 4
        self.nr_ships_L4 = 3


class Field():
    '''
    object to keep track of:
        ship positions
        discovered positions
    providing dummy to fill with visualisation signs
    '''

    def __init__(self,rules):
        self.positions_ships      = np.zeros([rules.number_cols, rules.number_rows],'int')
        self.positions_discovered = np.zeros([rules.number_cols, rules.number_rows],'int')
        self.field_dummy = rules.number_cols*[' '.join(rules.number_cols*['%s'])]


class BattleMap(Field):
    '''
    class to give a Field the necessary functionality to interact with
    '''
    
    def __init__(self,rules):
        
        if rules.number_cols > 26:
            rules.number_cols = 26
            print('\nAlert, number of columns has been adjusted to 26. \
            Code is not prepared to handle more than one letter as coordinate!')
        # if rules.number_rows > 26:
        #     rules.number_rows = 26
        #     print('\nAlert, number of rows has been adjusted to 26. \
        #   Code is not prepared to handle more than one letter as coordinate!')

        super().__init__(rules)
        self._prepare_decorator(rules)   
        # class attributes
        # meaning defined by key! replace value for different visualisation!
        self.visualisation = {\
            '0': '.',
            '1': 'G',
            '2': 'o',
            '3': 'c',
            '5': 'O',
            '6': '@',
            '7': 'x'}
        self.last_discovered = (-1,-1)
        # deploy ships
        self._deploy_ships_randomly(rules)

    def _deploy_ships_randomly(self,rules):
        '''
        randomly distributes ships on the map 
        amount defined in the nr_ships_L* attribute of the rules object
        '''
        # collecting demanded ships
        ship_attr = [ a for a in rules.__dir__() if 'nr_ships_L' in a]
        ship_len  = [ int(ship[10:]) for ship in ship_attr]
        ship_len.sort(reverse=True)

        #prepare 
        success = False
        i_max = 100
        i = 0
        print(ship_attr)

        while not success and i < i_max:
            for sl in ship_len:
                attr = 'nr_ships_L%i' %sl
                for i_ship in range(rules.__getattribute__(attr)):
                    success = False
                    j = 0
                    while not success and j < i_max:
                        [success,pos] = self._position_ship(length=sl)
                        j += 1
                    print(f'{j} attempts to position single ship')
                    if success:
                        for p in pos:
                            self.positions_ships[p] = 1
            i += 1
        print(f'{i} attempts to position all ships')
        if not success:
            print(pos)
            message = '\n\nCould not deploy all ships as intended.' +\
                    '\nPlease try again or decrease number of ships in rules!'
            raise RuntimeError(message)

    def _position_ship(self,length):
        '''
        randomly try to position one ship of given length
        and 
        return success state and position
        '''
        nr,nc = self.positions_ships.shape
        # choose start pos:
        x = np.random.randint(0,nc - length + 1)
        y = np.random.randint(0,nr - length + 1)
        # choose direction south or east and collect all points
        d = np.random.randint(2)
        if d == 0:
            pos = [(x,y+i) for i in range(length)]
        elif d == 1:
            pos = [(x+i,y) for i in range(length)]
        # check collision with neighbouring ships
        return self._check_neighbours(pos), pos

    def _check_neighbours(self,positions):
        '''
        return True if no ship on position and if no neighbours on position
        '''
        nr,nc = self.positions_ships.shape
        for pos in positions:
            if self.positions_ships[pos]:
                return False
            if pos[0] > 0 and self.positions_ships[pos[0]-1,pos[1]]:
                return False
            if pos[0] < nr-1 and self.positions_ships[pos[0]+1,pos[1]]:
                return False
            if pos[1] > 0 and self.positions_ships[pos[0],pos[1]-1]:
                return False
            if pos[1] < nc-1 and self.positions_ships[pos[0],pos[1]+1]:
                return False
        return True

    def _prepare_decorator(self,rules):
        '''
        prepare dummy part for field to be filled with data
        and 
        prepare decorator
        '''
        space_letter = 2
        space_nr = np.int8(np.floor( np.log10( rules.number_rows )) + 2)
        spacer_nbr = ''.join(space_nr*[' '])
        line_letters = \
            spacer_nbr \
            + ''.join((space_letter-1)*[' ']).join(letters[:rules.number_cols]) \
            + spacer_nbr
        
        placing = ' ' + ' '.join(rules.number_cols*['%s']) + ' '
        center = \
            [''.join(\
            [str.rjust(str(i),space_nr-1), placing, str.ljust(str(i),space_nr-1)]\
            ) for i in range(rules.number_rows)]
        # https://dev.to/ra1nbow1/8-ways-to-add-an-element-to-the-beginning-of-a-list-and-string-in-python-925
        s = [line_letters] + center + [line_letters]
        
        self.decorator_lines = '\n'.join(s)
        
    def print_my_own(self):
        '''
        as set in the self.visualisation:
        # . - unopened / unopened and no ship - 0 -   small sign, indicating free space
        # G - ship, if no hit                   - 1 -   big sign as like still swimming
        # o - hit before / empty    - 2 -   empty sign 
        # O - hit before / empty    - 4 -   empty sign 
        # c - ship hit              - 3 -   small sign and open as like hit 
        # @ - ship hit              - 6 -   ship, if last hit
        # x - targeted              - 7 -    
        '''
        # 0 - no ship, not uncovered  |
        # 1 - ship                      | ship *1  
        # 2 - uncoverd empty                    | 
        # 3 - uncoverd ship                  |        | uncovered *2
        # 4 - last but uncovered - impossible
        # 5 - last hit, empty                 |        |
        # 6 - last hit, ship                |        |        | last *3
        # 7 - targeted (no calculation)

        # calculate visualisation
        field = self.positions_ships + 2*self.positions_discovered
        if -1 not in self.last_discovered:
            field[self.last_discoverd] += 3
        # transform to list of strings
        state_str = [ str(i) for i in field.reshape(field.size) ]
        # replace with desired symbols
        state_str = [ self.visualisation[s] for s in state_str ]
        s = self.decorator_lines
        #print(field)
        s = self.decorator_lines %(*state_str[:],)
        
        print(s)
