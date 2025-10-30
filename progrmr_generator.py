

import random
import sys
import argparse
import warnings
import time
import typing
import string
import sre_parse
from re import Pattern
from rstr.xeger import Xeger
from rstr import rstr # Can do Regex() trick again to cache for performance

DEBUG = 0
# debug_print = print if DEBUG else lambda *args, **kwargs: None

class GlobalState:

    def __init__(self, all_state_vars) -> None:
        from collections import defaultdict

        # list of all self.variable_stacks, includes variables declared but not overwritten yet
        self.all_state_variables = all_state_vars
        self.declared_variables = set()

        self.variable_stacks = defaultdict(list)
        self.saved_states = []

    def _push(self, variable_name):
        value = globals()[variable_name]
        self.variable_stacks[variable_name].append(value)

    def _pop(self, variable_name):
        return self.variable_stacks[variable_name].pop()

    def save_state(self):
        current_state = {}
        for variable_name in self.declared_variables:
            value = globals()[variable_name]
            current_state[variable_name] = (
                value.copy() if isinstance(value, (dict, list, set)) else value
            )
        self.saved_states.append(current_state)

    def restore_state(self):
        if not self.saved_states:
            raise StateException("No saved state to restore.")
        for variable_name, value in self.saved_states[-1].items():
            globals()[variable_name] = value
        for variable_name in self.declared_variables - self.saved_states[-1].keys():
            if variable_name in globals():
                del globals()[variable_name]
        self.declared_variables = set(self.saved_states[-1].keys())

    def delete_saved_state(self):
        if not self.saved_states:
            raise StateException("No saved state to delete.")
        self.saved_states.pop()

    def declare_and_initialize(self, variable_name, value=None):
        if variable_name in globals():
            self._push(variable_name)
        self.declared_variables.add(variable_name)
        globals()[variable_name] = value

    def delete(self, variable_name):
        del globals()[variable_name]
        if self.variable_stacks[variable_name]:
            globals()[variable_name] = self._pop(variable_name)
        else:
            self.declared_variables.remove(variable_name)

    def check_empty(self):
        for var in self.variable_stacks:
            if self.variable_stacks[var]:
                print(self.variable_stacks)
                raise StateException(
                    f"Global state variable stack for {var} is not empty: {self.variable_stacks[var]}"
                )
        assert len(self.saved_states) == 0, "Saved states are not empty."
        assert len(self.declared_variables) == 0, "Variable stacks are not empty."

    def reset(self):
        self.declared_variables = set()
        self.variable_stacks.clear()
        self.saved_states.clear()
        for var in self.all_state_variables:
            if var in globals():
                del globals()[var]


class Regex(Xeger):
    parsed = {}

    # override the Xeger.xeger() method to cache patterns
    def xeger(self, string_or_regex: str) -> str:
        try:
            pattern = typing.cast(Pattern[str], string_or_regex).pattern
        except AttributeError:
            pattern = typing.cast(str, string_or_regex)

        if pattern not in self.parsed:
            self.parsed[pattern] = sre_parse.parse(pattern)

        parsed = self.parsed[pattern]
        result = self._build_string(parsed)
        self._cache.clear()
        return result

    def __call__(self, string_or_regex: str) -> str:
        return self.xeger(string_or_regex)


class IterationException(Exception):
    pass


class StateException(Exception):
    pass


class ConditionException(Exception):
    pass


regex = Regex()

__global_state = GlobalState(['FIRST'])

__depth = 0


__max_depth = 30
__retry_attempts = 20


def _start():
	global __depth
	
	def __expansion_0():
		global FIRST
		
		line=[]
		

		__global_state.declare_and_initialize('FIRST', None)
		FIRST = FIRST # for IDE variable binding


		
		try:
			__term_1 = _line()
			line.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _line()
				line[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', line)


		
		try:
			__term_2 = _line()
			line.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _line()
				line[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', line)


		
		try:
			__term_3 = _line()
			line.append(__term_3)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _line()
				line[-1] = __term_3
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', line)


		
		try:
			__term_4 = _line()
			line.append(__term_4)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_4 = _line()
				line[-1] = __term_4
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', line)


		
		try:
			__term_5 = _line()
			line.append(__term_5)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_5 = _line()
				line[-1] = __term_5
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', line)

		

		__global_state.delete('FIRST')

		return __term_1+__term_2+__term_3+__term_4+__term_5

	# debug_print(_start.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [5]
	__all_expansion_constraints = [(True)]
	__all_expansion_weights = [1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _start: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _start.__name__, __candidate_expansions)


def _line():
	global __depth
	
	def __expansion_0():
		global FIRST
		
		age=[]
		person_name=[]
		

		
		try:
			__term_0 = _person_name()
			person_name.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _person_name()
				person_name[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', person_name)


		__term_1 = ','


		
		try:
			__term_2 = _age()
			age.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _age()
				age[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', age)


		__term_3 = '\n'

		

		return __term_0+__term_1+__term_2+__term_3

	# debug_print(_line.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [4]
	__all_expansion_constraints = [(True)]
	__all_expansion_weights = [1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _line: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _line.__name__, __candidate_expansions)


def _person_name():
	global __depth
	
	def __expansion_0():
		global FIRST
		
		first=[]
		last=[]
		

		
		try:
			__term_0 = _first()
			first.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _first()
				first[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', first)


		__term_1 = ' '


		
		try:
			__term_2 = _last()
			last.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _last()
				last[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', last)

		

		return __term_0+__term_1+__term_2

	# debug_print(_person_name.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [3]
	__all_expansion_constraints = [(True)]
	__all_expansion_weights = [1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _person_name: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _person_name.__name__, __candidate_expansions)


def _first():
	global __depth
	
	def __expansion_0():
		global FIRST
		
		name=[]
		

		
		try:
			__term_0 = _name()
			name.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _name()
				name[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', name)


		FIRST = str(name[-1])

		

		return __term_0

	# debug_print(_first.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [2]
	__all_expansion_constraints = [(True)]
	__all_expansion_weights = [1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _first: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _first.__name__, __candidate_expansions)


def _last():
	global __depth
	
	def __expansion_0():
		global FIRST
		
		name=[]
		

		
		try:
			__term_0 = _name()
			name.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _name()
				name[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', name)

		

		return __term_0

	# debug_print(_last.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [2]
	__all_expansion_constraints = [(True)]
	__all_expansion_weights = [1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _last: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _last.__name__, __candidate_expansions)


def _name():
	global __depth
	
	def __expansion_0():
		global FIRST
		
		char_string=[]
		

		__global_state.save_state()
		try:
			__term_0 = _char_string()
			char_string.append(__term_0)
			__counter = 0
			while not (len(str(char_string[-1])) >= 2 and len(str(char_string[-1])) <= 10):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _char_string()
				char_string[-1] = __term_0
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', char_string)

		

		return __term_0

	# debug_print(_name.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [1]
	__all_expansion_constraints = [(True)]
	__all_expansion_weights = [1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _name: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _name.__name__, __candidate_expansions)


def _age():
	global __depth
	
	def __expansion_0():
		global FIRST
		
		number=[]
		

		__global_state.save_state()
		try:
			__term_0 = _number()
			number.append(__term_0)
			__counter = 0
			while not (int(number[-1]) >= 25 and int(number[-1]) <= 35):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _number()
				number[-1] = __term_0
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', number)

		

		return __term_0

	def __expansion_1():
		global FIRST
		
		number=[]
		

		__global_state.save_state()
		try:
			__term_0 = _number()
			number.append(__term_0)
			__counter = 0
			while not (int(number[-1]) >= 50 and int(number[-1]) <= 60):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _number()
				number[-1] = __term_0
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', number)

		

		return __term_0

	# debug_print(_age.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [2, 2]
	__all_expansion_constraints = [FIRST.startswith('A'), not FIRST.startswith('A')]
	__all_expansion_weights = [1, 1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _age: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _age.__name__, __candidate_expansions)


def _number():
	global __depth
	
	def __expansion_0():
		global FIRST
		
		digit=[]
		

		
		try:
			__term_0 = _digit()
			digit.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _digit()
				digit[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', digit)

		

		return __term_0

	def __expansion_1():
		global FIRST
		
		number=[]
		digit=[]
		

		
		try:
			__term_0 = _number()
			number.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _number()
				number[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', number)


		
		try:
			__term_1 = _digit()
			digit.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _digit()
				digit[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', digit)

		

		return __term_0+__term_1

	# debug_print(_number.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [1, 2]
	__all_expansion_constraints = [(True), (True)]
	__all_expansion_weights = [1, 1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _number: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _number.__name__, __candidate_expansions)


def _char_string():
	global __depth
	
	def __expansion_0():
		global FIRST
		

		

		__term_0 = str(regex("[A-Z]"))
		


		__term_1 = str(regex("[a-z]+"))
		

		

		return __term_0+__term_1

	# debug_print(_char_string.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [0]
	__all_expansion_constraints = [(True)]
	__all_expansion_weights = [1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _char_string: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _char_string.__name__, __candidate_expansions)


def _digit():
	global __depth
	
	def __expansion_0():
		global FIRST
		

		

		__term_0 = str(regex("[0-9]"))
		

		

		return __term_0

	# debug_print(_digit.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [0]
	__all_expansion_constraints = [(True)]
	__all_expansion_weights = [1]
	__candidate_expansions = []
	__candidate_weights = []
	__candidate_indexes = []
	candidates = 0
	for i, expansion in enumerate(__all_expansions):
		if __all_expansion_depths[i]+__depth <= __max_depth and __all_expansion_constraints[i]:
			__candidate_expansions.append(expansion)
			__candidate_weights.append(__all_expansion_weights[i])
			__candidate_indexes.append(candidates)
			candidates += 1
	__global_state.save_state()
	while __candidate_expansions:
		[__index] = random.choices(__candidate_indexes, weights=__candidate_weights)
		try:
			__depth += 1
			__temp = __candidate_expansions.pop(__index)()
			# debug_print(f"Expansion succeeded for _digit: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _digit.__name__, __candidate_expansions)


def generate_root():
	# __global_state.check_empty() # For development only to verify correctness.
	# __global_state.reset() # Shouldn't need it, state should undo itself when exiting it's scope
	while True:
		try:
			result = _start()
			return result
		except IterationException as e:
			pass
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Process some parameters.")
	parser.add_argument("--debug", type=int, default=0, help="Enable debug output (0 or 1)")
	parser.add_argument("--retry_attempts", type=int, default=__retry_attempts, help="Number of retry attempts")
	parser.add_argument("--max_depth", type=int, default=__max_depth, help="Maximum depth for recursion")
	parser.add_argument("-n", "--num_iters", type=int, default=1, help="Number of iterations to run (0 for infinite)")
	parser.add_argument("-t", "--timeout", type=float, default=0, help="Timeout in seconds for each iteration (0 for no timeout)")
	parser.add_argument("-d", "--output_dir", type=str, default=None, help="Directory to save output files")
	
	args = parser.parse_args()

	if args.retry_attempts < 1:
		print("Retry attempts must be at least 1")
		sys.exit(1)

	if args.max_depth < __max_depth:
		warnings.warn(f"Warning: Max depth must be at least {__max_depth} for this ProGRMR", RuntimeWarning)
		args.max_depth = __max_depth

	if args.num_iters < 0:
		warnings.warn("Warning: Number of iterations must be at least 0", RuntimeWarning)
		args.num_iters = 1
	elif args.num_iters == 0:
		args.num_iters = sys.maxsize

	if args.timeout < 0:
		warnings.warn("Warning: Timeout must be at least 0", RuntimeWarning)
		args.timeout = 0
		
	if args.output_dir is None:
		warnings.warn("Warning: Output directory not specified, printing to stdout", RuntimeWarning)

	DEBUG = args.debug
	output_dir = args.output_dir

	__retry_attempts = args.retry_attempts
	__max_depth = args.max_depth

	generated_strings = set()
	end_time = time.time() + args.timeout
	for _ in range(args.num_iters):
		generated_strings.add(generate_root())
		if args.timeout > 0 and time.time() > end_time:
			break
	
	if output_dir:
		for i, string in enumerate(generated_strings):
			output_file = output_dir + "/" + str(i) + ".txt"
			with open(output_file, "w") as f:
				f.write(string)
	else:
		for string in generated_strings:
			print(string)

