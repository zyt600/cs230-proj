

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

__global_state = GlobalState(['KEYS'])

__depth = 0


__max_depth = 25
__retry_attempts = 20


def _start():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		json=[]
		

		
		try:
			__term_0 = _json()
			json.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _json()
				json[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', json)

		

		return __term_0

	# debug_print(_start.__name__, __depth)
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


def _json():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		value=[]
		

		
		try:
			__term_0 = _value()
			value.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _value()
				value[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', value)

		

		return __term_0

	# debug_print(_json.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _json: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _json.__name__, __candidate_expansions)


def _value():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		json_obj=[]
		

		
		try:
			__term_0 = _json_obj()
			json_obj.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _json_obj()
				json_obj[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', json_obj)

		

		return __term_0

	def __expansion_1():
		global KEYS
		
		lst=[]
		

		
		try:
			__term_0 = _lst()
			lst.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _lst()
				lst[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', lst)

		

		return __term_0

	def __expansion_2():
		global KEYS
		
		strng=[]
		

		
		try:
			__term_0 = _strng()
			strng.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _strng()
				strng[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', strng)

		

		return __term_0

	def __expansion_3():
		global KEYS
		
		integer=[]
		

		__global_state.save_state()
		try:
			__term_0 = _integer()
			integer.append(__term_0)
			__counter = 0
			while not (len(integer[0]) <= 5):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _integer()
				integer[-1] = __term_0
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', integer)

		

		return __term_0

	def __expansion_4():
		global KEYS
		
		boolean=[]
		

		
		try:
			__term_0 = _boolean()
			boolean.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _boolean()
				boolean[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', boolean)

		

		return __term_0

	# debug_print(_value.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1, __expansion_2, __expansion_3, __expansion_4]
	__all_expansion_depths = [1, 1, 2, 1, 1]
	__all_expansion_constraints = [(True), (True), (True), (True), (True)]
	__all_expansion_weights = [1, 1, 1, 1, 1]
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
			# debug_print(f"Expansion succeeded for _value: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _value.__name__, __candidate_expansions)


def _json_obj():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		key_values=[]
		

		__global_state.declare_and_initialize('KEYS', set() )
		KEYS = KEYS # for IDE variable binding


		__term_1 = '{'


		
		try:
			__term_2 = _key_values()
			key_values.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _key_values()
				key_values[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', key_values)


		__term_3 = '}'

		

		__global_state.delete('KEYS')

		return __term_1+__term_2+__term_3

	def __expansion_1():
		global KEYS
		

		

		__term_0 = '{}'

		

		return __term_0

	# debug_print(_json_obj.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [5, 0]
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
			# debug_print(f"Expansion succeeded for _json_obj: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _json_obj.__name__, __candidate_expansions)


def _key_values():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		pair=[]
		

		
		try:
			__term_0 = _pair()
			pair.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _pair()
				pair[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', pair)

		

		return __term_0

	def __expansion_1():
		global KEYS
		
		key_values=[]
		pair=[]
		

		
		try:
			__term_0 = _pair()
			pair.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _pair()
				pair[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', pair)


		__term_1 = ', '


		
		try:
			__term_2 = _key_values()
			key_values.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _key_values()
				key_values[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', key_values)

		

		return __term_0+__term_1+__term_2

	# debug_print(_key_values.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [4, 5]
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
			# debug_print(f"Expansion succeeded for _key_values: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _key_values.__name__, __candidate_expansions)


def _pair():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		key=[]
		value=[]
		

		
		try:
			__term_0 = _key()
			key.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _key()
				key[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', key)


		__term_1 = ':'


		__global_state.save_state()
		try:
			__term_2 = _value()
			value.append(__term_2)
			__counter = 0
			while not (key[0] not in KEYS):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _value()
				value[-1] = __term_2
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', value)


		KEYS.add(key[0])

		

		return __term_0+__term_1+__term_2

	# debug_print(_pair.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _pair: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _pair.__name__, __candidate_expansions)


def _key():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		strng=[]
		

		
		try:
			__term_0 = _strng()
			strng.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _strng()
				strng[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', strng)

		

		return __term_0

	# debug_print(_key.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _key: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _key.__name__, __candidate_expansions)


def _strng():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		chars=[]
		

		__term_0 = '"'


		__global_state.save_state()
		try:
			__term_1 = _chars()
			chars.append(__term_1)
			__counter = 0
			while not (len(chars[0]) <= 5):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _chars()
				chars[-1] = __term_1
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', chars)


		__term_2 = '"'

		

		return __term_0+__term_1+__term_2

	# debug_print(_strng.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _strng: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _strng.__name__, __candidate_expansions)


def _chars():
	global __depth
	
	def __expansion_0():
		global KEYS
		

		

		__term_0 = str(regex("[A-Za-z0-9]+"))
		

		

		return __term_0

	# debug_print(_chars.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _chars: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _chars.__name__, __candidate_expansions)


def _lst():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		values=[]
		

		__term_0 = '['


		
		try:
			__term_1 = _values()
			values.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _values()
				values[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', values)


		__term_2 = ']'

		

		return __term_0+__term_1+__term_2

	def __expansion_1():
		global KEYS
		

		

		__term_0 = '[]'

		

		return __term_0

	# debug_print(_lst.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [3, 0]
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
			# debug_print(f"Expansion succeeded for _lst: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _lst.__name__, __candidate_expansions)


def _values():
	global __depth
	
	def __expansion_0():
		global KEYS
		
		values=[]
		value=[]
		

		
		try:
			__term_0 = _value()
			value.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _value()
				value[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', value)


		__term_1 = ', '


		
		try:
			__term_2 = _values()
			values.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _values()
				values[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', values)

		

		return __term_0+__term_1+__term_2

	def __expansion_1():
		global KEYS
		
		value=[]
		

		
		try:
			__term_0 = _value()
			value.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _value()
				value[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', value)

		

		return __term_0

	# debug_print(_values.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [3, 2]
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
			# debug_print(f"Expansion succeeded for _values: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _values.__name__, __candidate_expansions)


def _integer():
	global __depth
	
	def __expansion_0():
		global KEYS
		

		

		__term_0 = str(regex("[0-9]|[1-9][0-9]+"))
		

		

		return __term_0

	# debug_print(_integer.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _integer: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _integer.__name__, __candidate_expansions)


def _boolean():
	global __depth
	
	def __expansion_0():
		global KEYS
		

		

		__term_0 = 'true'

		

		return __term_0

	def __expansion_1():
		global KEYS
		

		

		__term_0 = 'false'

		

		return __term_0

	# debug_print(_boolean.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [0, 0]
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
			# debug_print(f"Expansion succeeded for _boolean: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _boolean.__name__, __candidate_expansions)


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

