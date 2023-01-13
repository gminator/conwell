from django.test import TestCase
from game.models import *
from unittest.mock import patch
from unittest_data_provider import data_provider

# Create your tests here.

class GridTest(TestCase):


	validate = lambda: (
		( 
			#10x10 grid
			(None,None, LengthNotSet),
			#(4,Non, ),
			(2,None, HeightNotSet),

			(10,10, None),
		)

	)

	@data_provider(validate)
	def test_validate(self,length, height, exception):
		try:
			Grid(length, height)
			self.assertTrue(not exception)
		except Exception as e:
			self.assertTrue(type(e) is exception)



	make = lambda: (
		( 
			#10x10 grid
			(10,10, ),

			#4x4 grid
			(4,4, ),

			#4x4 grid
			(4,2, ),
		)

	)

	@data_provider(make)
	def test_make(self,length,height):
		grid = Grid(length, height)
		cells  = grid.make()
		#raise Exception(cells)
		self.assertEquals(len(cells), height * length, "Index (%s) do match expected len of %s" % (len(cells), height * length))
		# self.assertEquals(len(cells), height, "Y axis(%s) does not match expected lengh of %s" % (len(cells), height))
		# for y,c in cells.items():
		# 	self.assertEquals(len(c), length, "X axis(%s) @ Y = %s does not match expected lengh of %s" % (len(c), y, length))


	to_string = lambda: (
		( 
			#x,y 10x10 grid
			(2,2, "[ ][ ]\n[ ][ ]"),
			(2,3, "[ ][ ]\n[ ][ ]\n[ ][ ]"),
			(3,2, "[ ][ ][ ]\n[ ][ ][ ]"),
		)

	)

	@data_provider(to_string)
	def test_to_string(self,length,height, output):
		grid = Grid(length, height)
		self.assertEquals(str(grid), output)


	select = lambda: (
		( 
			#x,y 10x10 grid
			(2,2, ["1,1", "2,2"], "[#][ ]\n[ ][#]"),

			(2,2, ["1,2", "2,1"], "[ ][#]\n[#][ ]"),

		)

	)

	@data_provider(select)
	def test_select(self,length,height, selected, output):
		grid = Grid(length, height)
		grid.select(selected)
		self.assertEquals(str(grid), output)

	cell_at = lambda: (
		( 
			#x,y 10x10 grid
			(2,2, ["1,1", "2,2"], {1 : {1 : ALIVE}, 1 : {2 : DEAD}}),

			(2,2, ["1,2", "2,1"], {1 : {1 : DEAD}, 1 : {2 : ALIVE}}),

		)

	)

	@data_provider(cell_at)
	def test_cell_at(self,length,height, selected, output):
		grid = Grid(length, height)
		grid.select(selected)
		for x,ys in output.items():
			for y,state in ys.items():
				cell = grid.cell_at(x,y)
				self.assertEquals(cell.state, state)


class CellTest(TestCase):


	validate = lambda: (
		( 
				#No XCoord 
			(None, None,None, GridNotSet),
		
			#No XCoord 
			(Grid(2,2), None,None, XCoordNotSet),
		
			#No YCoord 
			(Grid(2,2), 2,None, YCoordNotSet),

			#No Y Too High
			(Grid(2,2), 2,5, OutOfBOunds),
			

			#No x Too High
			(Grid(2,2), 3,1, OutOfBOunds),
			
			#Valid
			(Grid(2,2), 2, 1, None),
		)

	)

	@data_provider(validate)
	def test_validate(self,grid,x,y, exception):
		try:
			Cell(grid, x,y)
			self.assertTrue(not exception)
		except GameException as e:
			self.assertTrue(type(e) is exception)



	is_alive = lambda: (
		( 
			
			#Valid
			(Grid(2,2), 2, 1, ALIVE, True),
			(Grid(2,2), 2, 1, DEAD, False),
		)

	)

	@data_provider(is_alive)
	def test_is_alive(self,grid,x,y, state, output):
		cell = Cell(grid, x,y, state)
		self.assertEquals(output, cell.is_alive())

	neighbors = lambda: (
		( 
			
			#3 neighbors, corner piece
			( Cell(Grid(4,4), 1,1), 3),
			( Cell(Grid(4,4), 1,4), 3),
			( Cell(Grid(4,4), 4,1), 3),
			( Cell(Grid(4,4), 4,4), 3),


			#4 neighbors, side pieces
			( Cell(Grid(4,4), 1,2), 5),
			( Cell(Grid(4,4), 4,2), 5),
			( Cell(Grid(4,4), 2,1), 5),
			( Cell(Grid(4,4), 2,4), 5),
	

			#10 neighbors, side pieces
			( Cell(Grid(4,4), 2,2), 8),
		)

	)

	@data_provider(neighbors)
	def test_neighbors(self,cell, neighbors):
		self.assertEquals(len(cell.neighbors()), neighbors)

	living_neighbors = lambda: (
		( 
			
			#3 neighbors, corner piece
			( Cell(Grid(4,4,1,["1,2", "2,2"]), 1,1), 2),
			( Cell(Grid(4,4,1,["1,2", "2,2", "2,1"]), 1,1), 3),
			( Cell(Grid(10,10,1,["1,2", "2,2", "3,2", "1,1", "3,1"]), 2,1), 5),
			( Cell(Grid(4,4,1,["2,1"]), 2,2), 1),
			( Cell(Grid(4,4,), 2,2), 0),
		)

	)

	@data_provider(living_neighbors)
	def test_living_neighbors(self,cell, neighbors):
		#print("\n%s" % cell.grid)
		self.assertEquals(len(cell.living_neighbors()), neighbors)


	under_populated = lambda: (
		( 
			
			#2 cell But Not Alive
			( Cell(Grid(4,4,1,["1,2", "2,2",]), 1,1), False),

			( Cell(Grid(4,4,1,["1,2", "2,2",]), 1,1, ALIVE), False),

			#2 cell Is Alive
			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1"]), 1,1), False),

			#1 cell Is Alive
			( Cell(Grid(4,4,1,["1,2"]), 1,1, ALIVE), True),
		)

	)

	@data_provider(under_populated)
	def test_under_populated(self,cell, result):
		self.assertEquals(cell.under_populated(), result)


	can_survive = lambda: (
		( 
			
			#2 cell But Not Alive
			( Cell(Grid(4,4,1,["1,2", "2,2",]), 1,1, ALIVE), True),

			#2 cell Is Alive
			( Cell(Grid(4,4,1,["1,2", "2,2", "2,1"]), 1,1, ALIVE), True),

			#1 cell Is Alive
			( Cell(Grid(4,4,1,["1,2"]), 1,1, ALIVE), False),
		)

	)

	@data_provider(can_survive)
	def test_can_survive(self,cell, result):
		self.assertEquals(cell.can_survive(), result)



	over_populated = lambda: (
		( 
			
			#2 cell But Not Alive
			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1, ALIVE), True),

			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1), False),

			#2 cell Is Alive
			( Cell(Grid(4,4,1,["1,2", "2,2", "2,1"]), 1,1, ALIVE), False),

			#1 cell Is Alive
			( Cell(Grid(4,4,1,["1,2"]), 1,1, ALIVE), False),
		)

	)

	@data_provider(over_populated)
	def test_over_populated(self,cell, result):
		self.assertEquals(cell.over_populated(), result)




	can_be_born = lambda: (
		( 
			
			#2 cell But Not Alive
			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1, ALIVE), False),

			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1), False),

			#2 cell Is Alive
			( Cell(Grid(4,4,1,["1,2", "2,2", "2,1"]), 1,1, ALIVE), False),

			( Cell(Grid(4,4,1,["1,2", "2,2", "2,1"]), 1,1), True),

			#1 cell Is Alive
			( Cell(Grid(4,4,1,["1,2"]), 1,1, ALIVE), False),
		)

	)

	@data_provider(can_be_born)
	def test_can_be_born(self,cell, result):
		self.assertEquals(cell.can_be_born(), result)




	play = lambda: (
		( 
			
			#2 cell But Not Alive
			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1, ALIVE), True, True, False, False, ALIVE),
			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1, ALIVE), False, True, False, False, ALIVE),
			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1, ALIVE), True, False, False, False, ALIVE),

			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1, ALIVE), True, False,True, False, DEAD),
			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1, ALIVE), True, False,False, True, DEAD),
			( Cell(Grid(4,4,1,["1,2", "2,2", "1,1","3,2"]), 2,1, ALIVE), True, False,True, True, DEAD),

		)

	)

	@data_provider(play)
	def test_play(self,cell, can_survive, can_be_born, under_populated, over_populated, state):
		with patch.object(Cell, 'can_survive', return_value=can_survive) as mock:
			with patch.object(Cell, 'can_be_born', return_value=can_be_born) as mock:
				with patch.object(Cell, 'under_populated', return_value=under_populated) as mock:
					with patch.object(Cell, 'over_populated', return_value=over_populated) as mock:
						cell.play()
						self.assertEquals(cell.next, state)
