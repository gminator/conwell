from django.db import models
import random
import os
import time
"""
There are far easier ways to echieve this result, but my intention is to show a good understanding of OOP, DRY, Seperation of Concerns, SOLID and unit testing. 

For this reason I chose write the game in an OOP style, which is need in order to facalite good unit test. 

This solution additionally focuses on  validation of user and good Error Handeling, since the shell script will be accpeting user parameters to: 
- Establish the grid size
- Select cells cells or how many random cells to generate 
- Generations to run 

This application also features a basic API which similar return JSON containing the host name & IP. This is to demostrate that I have solid understanding of 
how API's are constructed & consumed. 

The App is also deployed out with a PostGress DB for Token Authentication 
"""

class GameException(Exception):pass

#Grid Exceptions
class LengthNotSet(GameException):pass
class HeightNotSet(GameException):pass
class OutOfBOunds(GameException):pass


#Cell Exceptions
class XCoordNotSet(GameException):pass
class YCoordNotSet(GameException):pass
class GridNotSet(GameException):pass


ALIVE = "[#]"
DEAD  = "[ ]"


class Grid(object):

	def __init__(self,l:int = None, h:int = None, generations:int = 0, selected:int=None, rt:int=None, *args, **kargs):
		self.l = l
		self.h = h
		self.generations = generations + 1
		self.validate()
		self.make()
		if selected: self.select(selected)
		if rt: self.random(rt)

	def random(self,r:int = 0):
		cells = random.sample(list(self.cells.keys()), r)
		for coords in cells:
			self.cells[coords].state = ALIVE

	def validate(self,):
		"""
		Validate 

		Check that grid is correct

		-- Return
		boolean True|False

		-- Raises
		LengthNotSet
		HeightNotSet
		"""
		if not self.l:
			raise LengthNotSet("Length cannot be %s" % self.l)

		if not self.h:
			raise HeightNotSet("Hieght cannot be %s" % self.h)

	def make(self,):
		"""
		Make 

		Make a 2D array that stores 
		the cells 

		-- Returns
		tuple (list index, list cells )  i.e ( [(x,y),..], [Cell(..),] )
		"""

		self.cells = {}
		for y in range(1, self.h + 1):
			for x in range(1, self.l + 1):
				self.cells[(x,y)] = Cell(self, x, y) 
		return self.cells

	def select(self, points:list):
		"""
		Select 

		Manuall set initial state 

		- Return 
		void 
		""" 
		if points:
			for i in points:
				coords = tuple([ int(i) for i in i.split(",")])
				self.cells[coords].state = ALIVE

	def cell_at(self,x,y):
		"""
		Cell At

		Retrieve cell @ a given index

		- Return 
		Cell

		- Raise 
		OutOfBound if no cell can be found @ x,y
		"""
		try:
			return self.cells[(x,y)]
		except:
			raise OutOfBOunds("No Cell @ (%s,%s)" % (x,y))

	def __str__(self,):
		"""
		To String

		Print grid to a string 

		-- Returns 
		str output 
		"""
		output = ""
		current = ""
		for coords,cell in self.cells.items():
			x,y = coords
			if y != current:
				current = y
				output += "\n"
			output += str(cell)
		return output.strip()

	def crawl(self,):
		for coords, cell in self.cells.items():
			self.cells[coords].play()

		for coords, cell in self.cells.items():
			self.cells[coords].apply()
		

	def run(self,grab=False):
		store = []
		for i in range(1, self.generations):
			os.system("clear")

			self.crawl()
			gen = "Generation: %s" % i
			store.append(gen + "\n" + str(self))
			if not grab:
				print(gen)
				print(self)
				time.sleep(0.5)

		return store


class Cell(object):

	def __init__(self, grid:Grid = None, x:int = None, y:int = None, state:str = DEAD):
		self.grid = grid
		self.x = x
		self.y = y
		self.state = state
		self.next = state
		self.validate()

	def validate(self,):
		"""
		Validate 

		Check that all manditory params are set
		and within the right bounds
		- Return 
		boolean True|False

		- Raise 
		GridNotSet
		XCoordNotSet
		YCoordNotSet
		OutOfBOunds
		"""
		if not self.grid: raise GridNotSet("Grid Not Set")
		if not self.x: raise XCoordNotSet("X coord cannot be null")
		if not self.y: raise YCoordNotSet("Y coord cannot be null")
		

		if  self.x > self.grid.l or self.y > self.grid.h: raise OutOfBOunds("Cell(%s,%s) is out of bounds [%s,%s]" % (self.x, self.y, self.grid.l, self.grid.h))

	def is_alive(self,):
		"""
		Is Alive

		Check to seee if cell is alive
		- Return 
		boolean True|False
		"""
		return self.state == ALIVE

	def neighbors(self,):
		"""
		Neghbors 

		Get surroudning cells

		- Returns 
		list [Cell(),..]
		"""
		radius = (
			(self.x - 1, self.y), #left
			(self.x -1, self.y + 1), #left up adjacent
			(self.x, self.y + 1), #up, 
			(self.x + 1, self.y + 1), #Right Up Adjacent,
			(self.x + 1, self.y), #Right,
			(self.x + 1, self.y - 1), #Right Down Adjacent 
			(self.x, self.y -1), #Down
			(self.x -1, self.y -1), #Left Down Adjecent
		)

		cells = []
		for x,y in radius:
			try:
				cells.append(self.grid.cell_at(x,y))
			except OutOfBOunds as e:pass


		return cells


	def living_neighbors(self,):
		return [ c for c in self.neighbors() if c.is_alive()]

	def under_populated(self,):
		"""
		Under Populated
		Any live cell with fewer than two live neighbours dies, as if by underpopulation.

		- Return
		boolean True|False
		"""
		return len(self.living_neighbors()) < 2 and self.is_alive()

	def can_survive(self,):
		"""
		Can Survice
		Any live cell with two or three live neighbours lives on to the next generation.

		- Return
		boolean True|False
		"""
		ln = len(self.living_neighbors()) 
		return (ln == 3 or ln == 2) and self.is_alive()



	def over_populated(self,):
		"""
		Over Populated
		Any live cell with more than three live neighbours dies, as if by overpopulation.

		- Return
		boolean True|False
		"""
		return len(self.living_neighbors()) > 3 and self.is_alive()


	def can_be_born(self,):
		"""
		Can Be Born
		Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

		- Return
		boolean True|False
		"""
		return len(self.living_neighbors()) == 3 and not self.is_alive()

	def play(self,):
		"""
		Play

		Play this cells life cycle
		"""
		#print("%s,%s has %s live neighbours and is currently %s" % (self.x, self.y, len(self.living_neighbors()), self.state))
		if self.can_be_born() or self.can_survive():
			self.next = ALIVE

		if self.over_populated() or self.under_populated():
			self.next = DEAD

		#print("%s,%s has to %s" % (self.x, self.y, self.state))

	def apply(self):
		self.state = self.next

	def __str__(self,):
		return self.state

#docker exec -it conwell python manage.py  play -l 20 -w 20 -p 1,1 2,2 1,2 2,3 3,1 3,3 5,5 6,5 7,5 6,6 6,7 6,8 10,10 9,10 9,9 -g 100


#Ocilator
#docker exec -it conwell python manage.py  play -l 20 -w 20 -p 3,2 3,3 3,4 -g 100

#docker exec -it conwell python manage.py  play -l 20 -w 20 -p 3,5 4,5 5,5 4,4 5,4 6,4  10,4 10,5 10,6 -g 200




#docker exec -it conwell python manage.py  play -l 20 -w 20 -c 100 -g 100
#docker exec -it conwell python manage.py  play -l 20 -w 20 -p 1,1 2,2 1,2 2,3 3,1 3,3 5,5 6,5 7,5 6,6 6,7 6,8 10,10 9,10 9,9 1,10 2,10 3,10 2,9 3,9 3,8 1,20 2,20 3,20 4,20 4,19 2,19 2,18 2,17  20,20 20,19 19,19 17,19 16,19 16,17 17,17 -g 100

