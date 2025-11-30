

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

__global_state = GlobalState(['HOSTS', 'ORIGIN'])

__depth = 0


__max_depth = 35
__retry_attempts = 20


def _start():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		zone_file=[]
		

		__global_state.declare_and_initialize('HOSTS', ['ns1', 'mail', 'www'])
		HOSTS = HOSTS # for IDE variable binding


		__global_state.declare_and_initialize('ORIGIN', 'example.com.')
		ORIGIN = ORIGIN # for IDE variable binding


		
		try:
			__term_2 = _zone_file()
			zone_file.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _zone_file()
				zone_file[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', zone_file)

		

		__global_state.delete('ORIGIN')


		__global_state.delete('HOSTS')

		return __term_2

	# debug_print(_start.__name__, __depth)
	__all_expansions = [__expansion_0]
	__all_expansion_depths = [6]
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


def _zone_file():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		soa_section=[]
		records_section=[]
		

		
		try:
			__term_0 = _soa_section()
			soa_section.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _soa_section()
				soa_section[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', soa_section)


		__term_1 = '\n'


		
		try:
			__term_2 = _records_section()
			records_section.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _records_section()
				records_section[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', records_section)

		

		return __term_0+__term_1+__term_2

	# debug_print(_zone_file.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _zone_file: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _zone_file.__name__, __candidate_expansions)


def _soa_section():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		soa_section=[]
		directive=[]
		

		
		try:
			__term_0 = _directive()
			directive.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _directive()
				directive[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', directive)


		__term_1 = '\n'


		
		try:
			__term_2 = _soa_section()
			soa_section.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _soa_section()
				soa_section[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', soa_section)

		

		return __term_0+__term_1+__term_2

	def __expansion_1():
		global HOSTS, ORIGIN
		
		soa_section=[]
		comment=[]
		

		
		try:
			__term_0 = _comment()
			comment.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _comment()
				comment[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', comment)


		__term_1 = '\n'


		
		try:
			__term_2 = _soa_section()
			soa_section.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _soa_section()
				soa_section[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', soa_section)

		

		return __term_0+__term_1+__term_2

	def __expansion_2():
		global HOSTS, ORIGIN
		
		ws=[]
		soa_record_entry=[]
		

		
		try:
			__term_0 = _ws()
			ws.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _ws()
				ws[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_1 = _soa_record_entry()
			soa_record_entry.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _soa_record_entry()
				soa_record_entry[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', soa_record_entry)

		

		return __term_0+__term_1

	# debug_print(_soa_section.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1, __expansion_2]
	__all_expansion_depths = [5, 5, 4]
	__all_expansion_constraints = [(True), (True), (True)]
	__all_expansion_weights = [1, 1, 1]
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
			# debug_print(f"Expansion succeeded for _soa_section: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _soa_section.__name__, __candidate_expansions)


def _soa_record_entry():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		ws=[]
		soa_rdata=[]
		

		__term_0 = '@'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		__term_2 = 'IN'


		
		try:
			__term_3 = _ws()
			ws.append(__term_3)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _ws()
				ws[-1] = __term_3
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		__term_4 = 'SOA'


		
		try:
			__term_5 = _ws()
			ws.append(__term_5)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_5 = _ws()
				ws[-1] = __term_5
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_6 = _soa_rdata()
			soa_rdata.append(__term_6)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_6 = _soa_rdata()
				soa_rdata[-1] = __term_6
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', soa_rdata)


		HOSTS.append('@')

		

		return __term_0+__term_1+__term_2+__term_3+__term_4+__term_5+__term_6

	def __expansion_1():
		global HOSTS, ORIGIN
		
		ws=[]
		domain_name=[]
		soa_rdata=[]
		

		
		try:
			__term_0 = _domain_name()
			domain_name.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _domain_name()
				domain_name[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_name)


		HOSTS.append(domain_name[-1])


		
		try:
			__term_2 = _ws()
			ws.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _ws()
				ws[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		__term_3 = 'IN'


		
		try:
			__term_4 = _ws()
			ws.append(__term_4)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_4 = _ws()
				ws[-1] = __term_4
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		__term_5 = 'SOA'


		
		try:
			__term_6 = _ws()
			ws.append(__term_6)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_6 = _ws()
				ws[-1] = __term_6
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_7 = _soa_rdata()
			soa_rdata.append(__term_7)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_7 = _soa_rdata()
				soa_rdata[-1] = __term_7
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', soa_rdata)

		

		return __term_0+__term_2+__term_3+__term_4+__term_5+__term_6+__term_7

	# debug_print(_soa_record_entry.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [3, 3]
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
			# debug_print(f"Expansion succeeded for _soa_record_entry: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _soa_record_entry.__name__, __candidate_expansions)


def _records_section():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		line=[]
		records_section=[]
		

		
		try:
			__term_0 = _line()
			line.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _line()
				line[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', line)


		__term_1 = '\n'


		
		try:
			__term_2 = _records_section()
			records_section.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _records_section()
				records_section[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', records_section)

		

		return __term_0+__term_1+__term_2

	def __expansion_1():
		global HOSTS, ORIGIN
		
		line=[]
		

		
		try:
			__term_0 = _line()
			line.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _line()
				line[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', line)

		

		return __term_0

	# debug_print(_records_section.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [2, 1]
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
			# debug_print(f"Expansion succeeded for _records_section: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _records_section.__name__, __candidate_expansions)


def _line():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		directive=[]
		

		
		try:
			__term_0 = _directive()
			directive.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _directive()
				directive[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', directive)

		

		return __term_0

	def __expansion_1():
		global HOSTS, ORIGIN
		
		resource_record=[]
		

		
		try:
			__term_0 = _resource_record()
			resource_record.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _resource_record()
				resource_record[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', resource_record)

		

		return __term_0

	def __expansion_2():
		global HOSTS, ORIGIN
		
		comment=[]
		

		
		try:
			__term_0 = _comment()
			comment.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _comment()
				comment[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', comment)

		

		return __term_0

	def __expansion_3():
		global HOSTS, ORIGIN
		

		

		__term_0 = ''

		

		return __term_0

	# debug_print(_line.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1, __expansion_2, __expansion_3]
	__all_expansion_depths = [2, 3, 1, 0]
	__all_expansion_constraints = [(True), (True), (True), (True)]
	__all_expansion_weights = [1, 1, 1, 1]
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


def _directive():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		ws=[]
		domain_name=[]
		

		__term_0 = '$ORIGIN'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _domain_name()
			domain_name.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _domain_name()
				domain_name[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_name)


		ORIGIN = domain_name[-1]

		

		return __term_0+__term_1+__term_2

	def __expansion_1():
		global HOSTS, ORIGIN
		
		ws=[]
		time_val=[]
		

		__term_0 = '$TTL'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _time_val()
			time_val.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _time_val()
				time_val[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', time_val)

		

		return __term_0+__term_1+__term_2

	# debug_print(_directive.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [2, 1]
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
			# debug_print(f"Expansion succeeded for _directive: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _directive.__name__, __candidate_expansions)


def _resource_record():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		ws=[]
		rr_data=[]
		owner=[]
		class_opt=[]
		

		
		try:
			__term_0 = _owner()
			owner.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _owner()
				owner[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', owner)


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _class_opt()
			class_opt.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _class_opt()
				class_opt[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', class_opt)


		
		try:
			__term_3 = _ws()
			ws.append(__term_3)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _ws()
				ws[-1] = __term_3
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_4 = _rr_data()
			rr_data.append(__term_4)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_4 = _rr_data()
				rr_data[-1] = __term_4
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', rr_data)

		

		return __term_0+__term_1+__term_2+__term_3+__term_4

	# debug_print(_resource_record.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _resource_record: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _resource_record.__name__, __candidate_expansions)


def _owner():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		domain_label=[]
		

		
		try:
			__term_0 = _domain_label()
			domain_label.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _domain_label()
				domain_label[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_label)


		HOSTS.append(domain_label[-1])

		

		return __term_0

	def __expansion_1():
		global HOSTS, ORIGIN
		

		

		__term_0 = '@'

		

		return __term_0

	def __expansion_2():
		global HOSTS, ORIGIN
		

		

		__term_0 = ''

		

		return __term_0

	# debug_print(_owner.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1, __expansion_2]
	__all_expansion_depths = [1, 0, 0]
	__all_expansion_constraints = [(True), (True), (True)]
	__all_expansion_weights = [1, 1, 1]
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
			# debug_print(f"Expansion succeeded for _owner: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _owner.__name__, __candidate_expansions)


def _class_opt():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = 'IN'

		

		return __term_0

	def __expansion_1():
		global HOSTS, ORIGIN
		

		

		__term_0 = ''

		

		return __term_0

	# debug_print(_class_opt.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _class_opt: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _class_opt.__name__, __candidate_expansions)


def _rr_data():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		ws=[]
		ipv4_addr=[]
		

		__term_0 = 'A'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _ipv4_addr()
			ipv4_addr.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _ipv4_addr()
				ipv4_addr[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ipv4_addr)

		

		return __term_0+__term_1+__term_2

	def __expansion_1():
		global HOSTS, ORIGIN
		
		ws=[]
		ipv6_addr=[]
		

		__term_0 = 'AAAA'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _ipv6_addr()
			ipv6_addr.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _ipv6_addr()
				ipv6_addr[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ipv6_addr)

		

		return __term_0+__term_1+__term_2

	def __expansion_2():
		global HOSTS, ORIGIN
		
		ws=[]
		target_host=[]
		

		__term_0 = 'NS'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _target_host()
			target_host.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _target_host()
				target_host[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', target_host)

		

		return __term_0+__term_1+__term_2

	def __expansion_3():
		global HOSTS, ORIGIN
		
		ws=[]
		target_host=[]
		

		__term_0 = 'CNAME'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _target_host()
			target_host.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _target_host()
				target_host[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', target_host)

		

		return __term_0+__term_1+__term_2

	def __expansion_4():
		global HOSTS, ORIGIN
		
		ws=[]
		priority=[]
		target_host=[]
		

		__term_0 = 'MX'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _priority()
			priority.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _priority()
				priority[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', priority)


		
		try:
			__term_3 = _ws()
			ws.append(__term_3)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _ws()
				ws[-1] = __term_3
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_4 = _target_host()
			target_host.append(__term_4)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_4 = _target_host()
				target_host[-1] = __term_4
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', target_host)

		

		return __term_0+__term_1+__term_2+__term_3+__term_4

	def __expansion_5():
		global HOSTS, ORIGIN
		
		ws=[]
		txt_string=[]
		

		__term_0 = 'TXT'


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _txt_string()
			txt_string.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _txt_string()
				txt_string[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', txt_string)

		

		return __term_0+__term_1+__term_2

	# debug_print(_rr_data.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1, __expansion_2, __expansion_3, __expansion_4, __expansion_5]
	__all_expansion_depths = [1, 1, 1, 1, 1, 1]
	__all_expansion_constraints = [(True), (True), (True), (True), (True), (True)]
	__all_expansion_weights = [1, 1, 1, 1, 1, 1]
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
			# debug_print(f"Expansion succeeded for _rr_data: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _rr_data.__name__, __candidate_expansions)


def _ipv4_addr():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = str(regex("((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d)\\.?\\b){4}"))
		

		

		return __term_0

	# debug_print(_ipv4_addr.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _ipv4_addr: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _ipv4_addr.__name__, __candidate_expansions)


def _ipv6_addr():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = str(regex("([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}"))
		

		

		return __term_0

	# debug_print(_ipv6_addr.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _ipv6_addr: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _ipv6_addr.__name__, __candidate_expansions)


def _target_host():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		domain_label=[]
		

		__term_0 = str(random.choice(HOSTS))
		domain_label.append(__term_0)

		

		return __term_0

	def __expansion_1():
		global HOSTS, ORIGIN
		
		domain_name=[]
		

		
		try:
			__term_0 = _domain_name()
			domain_name.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _domain_name()
				domain_name[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_name)

		

		return __term_0

	# debug_print(_target_host.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [0, 2]
	__all_expansion_constraints = [HOSTS != [], (True)]
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
			# debug_print(f"Expansion succeeded for _target_host: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _target_host.__name__, __candidate_expansions)


def _soa_rdata():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		time_val=[]
		serial_num=[]
		email_addr=[]
		ws=[]
		domain_name=[]
		

		
		try:
			__term_0 = _domain_name()
			domain_name.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _domain_name()
				domain_name[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_name)


		
		try:
			__term_1 = _ws()
			ws.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _ws()
				ws[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_2 = _email_addr()
			email_addr.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _email_addr()
				email_addr[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', email_addr)


		
		try:
			__term_3 = _ws()
			ws.append(__term_3)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _ws()
				ws[-1] = __term_3
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		__term_4 = '('


		
		try:
			__term_5 = _ws()
			ws.append(__term_5)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_5 = _ws()
				ws[-1] = __term_5
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_6 = _serial_num()
			serial_num.append(__term_6)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_6 = _serial_num()
				serial_num[-1] = __term_6
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', serial_num)


		
		try:
			__term_7 = _ws()
			ws.append(__term_7)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_7 = _ws()
				ws[-1] = __term_7
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_8 = _time_val()
			time_val.append(__term_8)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_8 = _time_val()
				time_val[-1] = __term_8
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', time_val)


		
		try:
			__term_9 = _ws()
			ws.append(__term_9)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_9 = _ws()
				ws[-1] = __term_9
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_10 = _time_val()
			time_val.append(__term_10)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_10 = _time_val()
				time_val[-1] = __term_10
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', time_val)


		
		try:
			__term_11 = _ws()
			ws.append(__term_11)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_11 = _ws()
				ws[-1] = __term_11
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_12 = _time_val()
			time_val.append(__term_12)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_12 = _time_val()
				time_val[-1] = __term_12
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', time_val)


		
		try:
			__term_13 = _ws()
			ws.append(__term_13)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_13 = _ws()
				ws[-1] = __term_13
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		
		try:
			__term_14 = _time_val()
			time_val.append(__term_14)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_14 = _time_val()
				time_val[-1] = __term_14
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', time_val)


		
		try:
			__term_15 = _ws()
			ws.append(__term_15)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_15 = _ws()
				ws[-1] = __term_15
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', ws)


		__term_16 = ')'

		

		return __term_0+__term_1+__term_2+__term_3+__term_4+__term_5+__term_6+__term_7+__term_8+__term_9+__term_10+__term_11+__term_12+__term_13+__term_14+__term_15+__term_16

	# debug_print(_soa_rdata.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _soa_rdata: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _soa_rdata.__name__, __candidate_expansions)


def _priority():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = str(regex("[0-9]{1,5}"))
		

		

		return __term_0

	# debug_print(_priority.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _priority: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _priority.__name__, __candidate_expansions)


def _txt_string():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = '"'


		__term_1 = str(rstr(string.ascii_letters + string.digits + " -_=", 5, 20))
		


		__term_2 = '"'

		

		return __term_0+__term_1+__term_2

	# debug_print(_txt_string.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _txt_string: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _txt_string.__name__, __candidate_expansions)


def _domain_name():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		domain_label=[]
		

		
		try:
			__term_0 = _domain_label()
			domain_label.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _domain_label()
				domain_label[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_label)


		__term_1 = '.'


		
		try:
			__term_2 = _domain_label()
			domain_label.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _domain_label()
				domain_label[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_label)


		__term_3 = '.'

		

		return __term_0+__term_1+__term_2+__term_3

	def __expansion_1():
		global HOSTS, ORIGIN
		
		domain_label=[]
		

		
		try:
			__term_0 = _domain_label()
			domain_label.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _domain_label()
				domain_label[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_label)

		

		return __term_0

	# debug_print(_domain_name.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [1, 1]
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
			# debug_print(f"Expansion succeeded for _domain_name: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _domain_name.__name__, __candidate_expansions)


def _domain_label():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = str(rstr(string.ascii_lowercase, 3, 8))
		

		

		return __term_0

	# debug_print(_domain_label.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _domain_label: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _domain_label.__name__, __candidate_expansions)


def _email_addr():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		
		domain_label=[]
		

		
		try:
			__term_0 = _domain_label()
			domain_label.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _domain_label()
				domain_label[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_label)


		__term_1 = '.'


		
		try:
			__term_2 = _domain_label()
			domain_label.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _domain_label()
				domain_label[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', domain_label)

		

		return __term_0+__term_1+__term_2

	# debug_print(_email_addr.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _email_addr: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _email_addr.__name__, __candidate_expansions)


def _serial_num():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = str(regex("202[0-5](0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[0-9]{2}"))
		

		

		return __term_0

	# debug_print(_serial_num.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _serial_num: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _serial_num.__name__, __candidate_expansions)


def _time_val():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = str(regex("[1-9][0-9]{2,4}"))
		

		

		return __term_0

	# debug_print(_time_val.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _time_val: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _time_val.__name__, __candidate_expansions)


def _ws():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = str(regex("[ \\t]+"))
		

		

		return __term_0

	# debug_print(_ws.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _ws: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _ws.__name__, __candidate_expansions)


def _comment():
	global __depth
	
	def __expansion_0():
		global HOSTS, ORIGIN
		

		

		__term_0 = ';'


		__term_1 = str(rstr(string.printable, 5, 20))
		

		

		return __term_0+__term_1

	# debug_print(_comment.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _comment: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _comment.__name__, __candidate_expansions)


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

