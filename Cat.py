from operator import xor
import random
import numpy as np
from enum import Enum
import random

from roulette import roulette

class Behavior(Enum):
	SEEKING = 1
	TRACING = 2


class Cat:
	def __init__(self, behavior, dimesions_size, initial_position, 
				initial_velocity, constants, objective_fn):
		self.behavior = behavior
		self._positions = np.ones(dimesions_size) * initial_position
		self._velocities = np.ones(dimesions_size) * initial_velocity
		self._dimension_size = dimesions_size
		self._constants = constants
		self._objective_fn = objective_fn

	def __lt__(self, other):
		return self.evaluate() < other.evaluate()

	def evaluate(self):
		return self._objective_fn(self._positions)

	def move(self, gbest):
		if self.behavior == Behavior.SEEKING:
			return self._seeking_mode_move()
			
		elif self.behavior == Behavior.TRACING:
			return self._tracing_mode_move(gbest)
	
		else:
			raise Exception("Invalid behavior for Cat")
	
	def copy(self):
		copy = Cat(
				behavior=self.behavior, 
				dimesions_size=self._dimension_size,
				initial_position=0, 
				initial_velocity=0, 
				constants=self._constants,
				objective_fn=self._objective_fn
				) 

		copy._positions = np.copy(self._positions)
		copy._velocities = np.copy(self._velocities)

		return copy

	def _seeking_mode_move(self):
		cats = self._make_copies_and_mutate()

		# Representing this cat
		cats.append(self) 

		return self._choose_best_fitted_cat(cats)

	def _tracing_mode_move(self, gbest):
		for dimension in range(0, self._dimension_size):
			self._update_velocities(dimension, gbest)
			self._update_positions(dimension)

		return self

	def _make_copies_and_mutate(self):
		cats = [self.copy() for _ in range(0, self._constants['SPM'])]

		for cat in cats:
			cat._mutate()
		
		return cats

	def _mutate(self):
		for _ in range(0, self._constants['CDC']):
			do_mutation = random.uniform(0, 1) <= self._constants['PMO']
			if not do_mutation:
				return
			
			random_dimension = random.randrange(0, self._dimension_size)
			cur_value = self._positions[random_dimension]
			self._positions[random_dimension] = (
				0 if cur_value == 1 else 1
			)

	def _update_velocities(self, dimension, gbest):
		r1 = random.randrange(0, 2)
		velocityVal = int(self._velocities[dimension])

		self._velocities[dimension] = (
			xor(r1, velocityVal) 
			and (gbest._positions[dimension] or self._positions[dimension])
		)

	def _update_positions(self, dimension):
		self._positions[dimension] = (
			self._positions[dimension] or self._velocities[dimension]
		)

	def _choose_best_fitted_cat(self, cats):
		cats_fitness_values = (
			[self._objective_fn(cat._positions) for cat in cats]
		)
		
		chosen_cat = roulette(cats, cats_fitness_values)
		return chosen_cat