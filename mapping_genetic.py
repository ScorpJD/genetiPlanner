import numpy as np
import random

class Individual():
	def __init__(self, genes):
		self.genes = genes
		self.fitness = 0
		self.path = []
		self.state = (0,0,0)
		self.target = (7,7)


def initialise(environment, pop_size):
	cur_gen = []
	for i in range(pop_size):
		initial_tr = np.array(np.random.choice(['F', 'L', 'R'], size = (4,8,8), p = [0.67,0.16,0.17]))
		initial_tr[0][np.where(environment == 1)] = 'X'
		initial_tr[1][np.where(environment == 1)] = 'X'
		initial_tr[2][np.where(environment == 1)] = 'X'
		initial_tr[3][np.where(environment == 1)] = 'X'
		individual = Individual(initial_tr)
		cur_gen.append(individual)
	return cur_gen

def travel(cur_gen, environment, steps):
	for individual in cur_gen:
		for step_index in range(steps):
			cur_coordinates = (individual.state[0], individual.state[1])
			cur_orientation = individual.state[2]
			if(cur_coordinates[0] >= len(environment) or cur_coordinates[1] >= len(environment[0].T) or cur_coordinates[0] < 0 or cur_coordinates[1] < 0):
				print "EXITTING GRID at " + str(cur_coordinates) #+ str(len(environment)) + "," + str(len(environment[0].T))
				break
			(individual.path).append(cur_coordinates)
			motion_prim = individual.genes[cur_orientation][cur_coordinates]
			print individual.state
			print motion_prim
			
			if(motion_prim == 'F'):
				if(cur_orientation == 0):
					individual.state = map(sum, zip(individual.state, (0,1,0))) 
				elif(cur_orientation == 1):
					individual.state = map(sum, zip(individual.state, (-1,0,0)))
				elif(cur_orientation == 2):
					individual.state = map(sum, zip(individual.state, (0,-1,0)))
				elif(cur_orientation == 3):
					individual.state = map(sum, zip(individual.state, (1,0,0)))
			elif(motion_prim == 'L'):
				individual.state = (individual.state[0], individual.state[1], (individual.state[2] + 1)%4)
			elif(motion_prim == 'R'):
				individual.state = (individual.state[0], individual.state[1], (individual.state[2] - 1)%4)
			elif(motion_prim == 'X'):
				break


def main():
	environment = np.matrix([[0,0,1,1,0,0,0,0],
							 [0,0,1,1,0,0,0,0],
							 [0,0,0,0,0,1,0,0],
							 [0,0,1,0,0,1,0,0],
							 [0,0,0,0,0,1,0,0],
							 [0,0,1,0,0,0,0,0],
							 [0,0,1,1,0,0,0,0],
							 [0,0,1,1,0,0,0,0]])
	print environment[2].T[5]

	cur_gen = initialise(environment, 1)
	travel(cur_gen, environment, 5)
	for i in cur_gen:
		print i.genes
		print i.path
		print i.genes[i.state[2]][i.state[0]][i.state[1]]
		print i.state






if __name__ == '__main__':
	main()