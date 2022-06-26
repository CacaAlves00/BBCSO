import operator
import math
import random
import sys

from Cat import Behavior, Cat

class BBCSO:
	def __init__(self, n_cats, dimensions, constants, objective_fn):
		self._n_cats = n_cats
		self._constants = constants
		self._cats = []

		self._init_cats(dimensions, objective_fn)

	def _init_cats(self, dimensions, objective_fn):
		for _ in range(0,self._n_cats):
			self._cats.append(Cat(
				dimesions_size=dimensions,
				behavior=None,
				initial_position=0,
				initial_velocity=0,
				constants=self._constants,
				objective_fn=objective_fn
			))

	def run(self, iterations):
		for _ in range(0, iterations):
			self._setup_gbest()

			self._choose_cats2tracing_or_seeking_mode()

			self._move_cats()

		self._setup_gbest()
		return self._gbest
	
	def _setup_gbest(self):
		self._gbest = self._cats[0]
		gbest_fitness = 0.0

		for cat in self._cats:
			cur_fitness = cat.evaluate()
			
			if (cur_fitness > gbest_fitness):
				self._gbest = cat
				gbest_fitness = cur_fitness

	def _choose_cats2tracing_or_seeking_mode(self):
		# Sorting by fitness - greatest fitness come first
		self._cats.sort(reverse=True)

		n_cats2choose4tracing_mode = (
			math.floor(self._constants['MR'] * self._n_cats)
		)

		for cat_index in range(0, n_cats2choose4tracing_mode):
			self._cats[cat_index].behavior = Behavior.TRACING

		for cat_index in range(n_cats2choose4tracing_mode, self._n_cats):
			self._cats[cat_index].behavior = Behavior.SEEKING

	def _move_cats(self):
		for cat_idx in range(0, self._n_cats):
			self._cats[cat_idx] = self._cats[cat_idx].move(self._gbest)