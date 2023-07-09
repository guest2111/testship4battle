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
		self.nr_ships_L2 = 3
		self.nr_ships_L3 = 2
		self.nr_ships_L4 = 1


class Field():
	'''
	object to keep track of:
		ship positions
		discovered positions
	providing dummy to fill with visualisation signs
	'''

	def __init__(self,rules):
		# https://www.statology.org/numpy-array-to-int/
		self.positions_ships      = np.zeros([rules.number_cols, rules.number_rows]).astype(int)
		self.positions_discovered = np.zeros([rules.number_cols, rules.number_rows]).astype(int)
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
		# 	rules.number_rows = 26
		# 	print('\nAlert, number of rows has been adjusted to 26. \
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
		# G - ship, if no hit	     		  - 1 -   big sign as like still swimming
		# o - hit before / empty    - 2 -   empty sign 
		# O - hit before / empty    - 4 -   empty sign 
		# c - ship hit              - 3 -   small sign and open as like hit 
		# @ - ship hit              - 6 -   ship, if last hit
		# x - targeted              - 7 -    
		'''
		# 0 - no ship, not uncovered  |
		# 1 - ship				      | ship *1  
		# 2 - uncoverd empty				    | 
		# 3 - uncoverd ship				  |	    | uncovered *2
		# 4 - last but uncovered - impossible
		# 5 - last hit, empty 				|		|
		# 6 - last hit, ship				|		|		| last *3
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
