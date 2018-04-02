import numpy as np
import math
import random

class Individual():
	def __init__(self, genes):
		self.genes = genes
		self.fitness = 0
		self.path = []
		self.state = (7,4)
		self.target = (7,7)

def smart_initialise(environment, pop_size):
	cur_gen = []
	while len(cur_gen) <(pop_size):
		initial_genes = np.array(np.random.choice(['0'], size = (8,8), p = [1]))
		for i in range(len(environment)):
			for j in range(len(environment[0].T)):
				possible_vals = ['U', 'D', 'L', 'R']
				if(i == 0 or environment[i-1].T[j] == 1 or initial_genes[i-1][j] == 'D'):
					possible_vals.remove('U')
				if(i == len(environment)-1 or environment[i+1].T[j] == 1):
					possible_vals.remove('D')
				if(j == 0 or environment[i].T[j-1] == 1 or initial_genes[i][j-1] == 'R'):
					possible_vals.remove('L')
				if(j == len(environment[0].T)-1 or environment[i].T[j+1] == 1):
					possible_vals.remove('R')


				if(len(possible_vals) > 0):
					prob = 1.0/(len(possible_vals))
					initial_genes[i][j] = np.random.choice(possible_vals, p = [prob]*len(possible_vals))
				else:
					initial_genes[i][j] = np.random.choice(['R', 'L', 'D', 'U'], p = [0.25,0.25,0.25,0.25])
		cur_gen.append(Individual(initial_genes))
	return cur_gen

def initialise(environment, pop_size):
	cur_gen = []
	for i in range(pop_size):
		initial_tr = np.array(np.random.choice(['R', 'L', 'D', 'U'], size = (8,8), p = [0.25,0.25,0.25,0.25]))
		initial_tr[np.where(environment == 1)] = 'X'
		individual = Individual(initial_tr)
		cur_gen.append(individual)
	return cur_gen

def travel(cur_gen, environment, steps):
	for individual in cur_gen:
		for step_index in range(steps):
			cur_coordinates = (individual.state[0], individual.state[1])
			if(cur_coordinates[0] >= len(environment) or cur_coordinates[1] >= len(environment[0].T) or cur_coordinates[0] < 0 or cur_coordinates[1] < 0):
				# print "EXITTING GRID at " + str(cur_coordinates) #+ str(len(environment)) + "," + str(len(environment[0].T))
				break
			(individual.path).append(cur_coordinates)
			motion_prim = individual.genes[cur_coordinates]
			# print individual.state
			# print motion_prim
			
			if(motion_prim == 'R'):
				individual.state = tuple(map(sum, zip(individual.state, (0,1))))
			elif(motion_prim == 'U'):
				individual.state = tuple(map(sum, zip(individual.state, (-1,0))))
			elif(motion_prim == 'L'):
				individual.state = tuple(map(sum, zip(individual.state, (0,-1))))
			elif(motion_prim == 'D'):
				individual.state = tuple(map(sum, zip(individual.state, (1,0))))
			elif(motion_prim == 'X'):
				break


def distance(initial, final):
	return round(math.sqrt((initial[0] - final[0])**2 + (initial[1] - final[1])**2))

def calculate_fitness(cur_gen, environment):
	temp = 0
	betterness_coefficient = 1
	path_length_coefficient = 0.01
	collision_coefficient = 2
	target_coefficient = 4
	exploration_coefficient = 2


	for individual in cur_gen:
		individual.fitness += betterness_coefficient*(distance(individual.path[0],individual.target) - distance(individual.path[len(individual.path) - 1],individual.target))
		individual.fitness -= path_length_coefficient*len(individual.path) 
		if(environment[individual.path[len(individual.path) - 1]]):
			individual.fitness = individual.fitness/collision_coefficient
		if(individual.target in individual.path):
			individual.fitness = individual.fitness*target_coefficient
			if temp==0:
				print "Computed .... Improving now"
				temp = 1
		if(individual.path[len(individual.path)-1][0] >= len(environment) or individual.path[len(individual.path)-1][1] >= len(environment[0].T) or individual.path[len(individual.path)-1][0] < 0 or individual.path[len(individual.path)-1][1] < 0):
			individual.fitness = individual.fitness/collision_coefficient

		# print individual.fitness
		individual.fitness += exploration_coefficient*len(set(individual.path))
		if(individual.fitness < 0):
			individual.fitness = 0

def crossover(p1, p2, environment):
	mutation_probability = 0.01

	# print p1.genes
	# print p2.genes

	crossover_matrix = np.array(np.random.choice([True, False], size = (8,8), p = [p1.fitness/(p1.fitness + p2.fitness), 1 - p1.fitness/(p1.fitness + p2.fitness)]))
	crossover_matrix = np.where(crossover_matrix, p1.genes, p2.genes)

	# print crossover_matrix

	mutation_matrix = np.array(np.random.choice([True, False], size = (8,8), p = [1 - mutation_probability, mutation_probability]))
	crossover_matrix = np.where(mutation_matrix, crossover_matrix, np.random.choice(['U', 'L', 'R', 'D']))
	crossover_matrix[np.where(environment == 1)] = 'X'

	return crossover_matrix

def mating(cur_gen, environment):
	prob_list = []
	for individual in cur_gen:
		prob_list.append(individual.fitness)
	s = sum(prob_list)
	for i in range(len(prob_list)-1):
		prob_list[i] = prob_list[i]/s

	defficient = 1 - sum(prob_list)
	max_index = prob_list.index(max(prob_list))
	prob_list[max_index] += defficient
	# print prob_list

	new_gen = []


	while(len(new_gen) < len(cur_gen)):
		parent1 = np.random.choice(cur_gen, p = prob_list)
		parent2 = np.random.choice(cur_gen, p = prob_list)
		# print(parent1.fitness, parent2.fitness)

		child_genes = crossover(parent1, parent2, environment)
		new_gen.append(Individual(child_genes))
	return (new_gen)


def main():

	n_generations = 30

	environment = np.matrix([[0,0,1,1,0,0,0,0],
							 [0,0,1,1,0,0,0,0],
							 [0,0,0,0,0,1,0,0],
							 [0,0,1,0,0,1,0,0],
							 [0,0,0,0,0,1,0,0],
							 [0,0,1,0,0,0,0,0],
							 [0,0,1,1,0,0,0,0],
							 [0,0,1,1,0,0,0,0]])

	environment = np.matrix([[0,0,1,0,0,0,0,0],
							 [0,0,1,0,0,1,0,0],
							 [0,0,1,0,0,1,0,0],
							 [0,0,1,0,0,1,0,0],
							 [0,0,1,0,0,1,0,0],
							 [0,0,1,0,0,1,0,0],
							 [0,0,1,0,0,1,0,0],
							 [0,0,0,0,0,1,0,0]])
	# print environment[2].T[5]

	cur_gen = smart_initialise(environment, 300)
	print cur_gen[0].genes
	for gen_index in range(n_generations):
		print gen_index
		# print cur_gen[gen_index].fitness
		# print cur_gen[0].genes
		# print cur_gen[1].genes
		travel(cur_gen, environment, 20)#int(gen_index/5)*3+5)
		calculate_fitness(cur_gen, environment)
		next_gen = mating(cur_gen, environment)
		cur_gen = next_gen

	# best_individual = cur_gen[cur_gen.index(max(cur_gen, key = cur_gen.fitness))]
	travel(cur_gen,environment,20)
	calculate_fitness(cur_gen, environment)
	best_individual = cur_gen[0]
	for individual in cur_gen:
		if individual.fitness > best_individual.fitness:
			best_individual = individual
	print best_individual.genes
	print best_individual.path




if __name__ == '__main__':
	main()