

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

__global_state = GlobalState(['HEADER_STR', 'CHECKSUM', 'LEN', 'LEN', 'LEN', 'LEN', 'LEN'])

__depth = 0


__max_depth = 35
__retry_attempts = 20


def _start():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		entries=[]
		

		
		try:
			__term_0 = _entries()
			entries.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _entries()
				entries[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', entries)

		

		return __term_0

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		final_entry=[]
		

		
		try:
			__term_0 = _final_entry()
			final_entry.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _final_entry()
				final_entry[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', final_entry)

		

		return __term_0

	# debug_print(_start.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [7, 3]
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


def _entries():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		entry=[]
		

		
		try:
			__term_0 = _entry()
			entry.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _entry()
				entry[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', entry)

		

		return __term_0

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		entry=[]
		entries=[]
		

		
		try:
			__term_0 = _entry()
			entry.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _entry()
				entry[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', entry)


		
		try:
			__term_1 = _entries()
			entries.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _entries()
				entries[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', entries)

		

		return __term_0+__term_1

	# debug_print(_entries.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1]
	__all_expansion_depths = [6, 7]
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
			# debug_print(f"Expansion succeeded for _entries: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _entries.__name__, __candidate_expansions)


def _entry():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		header=[]
		content=[]
		

		
		try:
			__term_0 = _header()
			header.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _header()
				header[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', header)


		
		try:
			__term_1 = _content()
			content.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _content()
				content[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', content)

		

		return __term_0+__term_1

	# debug_print(_entry.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _entry: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _entry.__name__, __candidate_expansions)


def _header():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		header_parts=[]
		

		__global_state.declare_and_initialize('HEADER_STR', "")
		HEADER_STR = HEADER_STR # for IDE variable binding


		__global_state.declare_and_initialize('CHECKSUM', None)
		CHECKSUM = CHECKSUM # for IDE variable binding


		


		__global_state.save_state()
		try:
			__term_3 = _header_parts()
			header_parts.append(__term_3)
			__counter = 0
			while not (CHECKSUM == oct(sum(HEADER_STR.encode('ascii')))[2:].rjust(6, '0') + '\0 '):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _header_parts()
				header_parts[-1] = __term_3
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', header_parts)

		

		__global_state.delete('CHECKSUM')


		__global_state.delete('HEADER_STR')

		return __term_3

	# debug_print(_header.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _header: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _header.__name__, __candidate_expansions)


def _header_parts():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		typeflag=[]
		uname=[]
		file_name=[]
		linked_file_name=[]
		dev_maj_num=[]
		gid=[]
		file_size=[]
		gname=[]
		file_mode=[]
		checksum=[]
		dev_min_num=[]
		uid=[]
		file_name_prefix=[]
		header_padding=[]
		nul=[]
		mod_time=[]
		

		
		try:
			__term_0 = _file_name()
			file_name.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _file_name()
				file_name[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name)


		HEADER_STR = file_name[0]


		
		try:
			__term_2 = _file_mode()
			file_mode.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _file_mode()
				file_mode[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_mode)


		HEADER_STR = HEADER_STR + file_mode[0]


		
		try:
			__term_4 = _uid()
			uid.append(__term_4)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_4 = _uid()
				uid[-1] = __term_4
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uid)


		HEADER_STR = HEADER_STR + uid[0]


		
		try:
			__term_6 = _gid()
			gid.append(__term_6)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_6 = _gid()
				gid[-1] = __term_6
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', gid)


		HEADER_STR = HEADER_STR + gid[0]


		
		try:
			__term_8 = _file_size()
			file_size.append(__term_8)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_8 = _file_size()
				file_size[-1] = __term_8
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_size)


		HEADER_STR = HEADER_STR + file_size[0]


		
		try:
			__term_10 = _mod_time()
			mod_time.append(__term_10)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_10 = _mod_time()
				mod_time[-1] = __term_10
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', mod_time)


		HEADER_STR = HEADER_STR + mod_time[0]


		
		try:
			__term_12 = _checksum()
			checksum.append(__term_12)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_12 = _checksum()
				checksum[-1] = __term_12
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', checksum)


		HEADER_STR = HEADER_STR + " "  * 8


		CHECKSUM = checksum[0]


		
		try:
			__term_15 = _typeflag()
			typeflag.append(__term_15)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_15 = _typeflag()
				typeflag[-1] = __term_15
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', typeflag)


		HEADER_STR = HEADER_STR + typeflag[0]


		
		try:
			__term_17 = _linked_file_name()
			linked_file_name.append(__term_17)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_17 = _linked_file_name()
				linked_file_name[-1] = __term_17
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', linked_file_name)


		HEADER_STR = HEADER_STR + linked_file_name[0]


		__term_19 = 'ustar'


		HEADER_STR = HEADER_STR + 'ustar'


		
		try:
			__term_21 = _nul()
			nul.append(__term_21)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_21 = _nul()
				nul[-1] = __term_21
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', nul)


		HEADER_STR = HEADER_STR + nul[0]


		__term_23 = '00'


		HEADER_STR = HEADER_STR + '00'


		
		try:
			__term_25 = _uname()
			uname.append(__term_25)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_25 = _uname()
				uname[-1] = __term_25
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uname)


		HEADER_STR = HEADER_STR + uname[0]


		
		try:
			__term_27 = _gname()
			gname.append(__term_27)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_27 = _gname()
				gname[-1] = __term_27
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', gname)


		HEADER_STR = HEADER_STR + gname[0]


		
		try:
			__term_29 = _dev_maj_num()
			dev_maj_num.append(__term_29)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_29 = _dev_maj_num()
				dev_maj_num[-1] = __term_29
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', dev_maj_num)


		HEADER_STR = HEADER_STR + dev_maj_num[0]


		
		try:
			__term_31 = _dev_min_num()
			dev_min_num.append(__term_31)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_31 = _dev_min_num()
				dev_min_num[-1] = __term_31
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', dev_min_num)


		HEADER_STR = HEADER_STR + dev_min_num[0]


		
		try:
			__term_33 = _file_name_prefix()
			file_name_prefix.append(__term_33)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_33 = _file_name_prefix()
				file_name_prefix[-1] = __term_33
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name_prefix)


		HEADER_STR = HEADER_STR + file_name_prefix[0]


		
		try:
			__term_35 = _header_padding()
			header_padding.append(__term_35)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_35 = _header_padding()
				header_padding[-1] = __term_35
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', header_padding)


		HEADER_STR = HEADER_STR + uname[0]

		

		return __term_0+__term_2+__term_4+__term_6+__term_8+__term_10+__term_12+__term_15+__term_17+__term_19+__term_21+__term_23+__term_25+__term_27+__term_29+__term_31+__term_33+__term_35

	# debug_print(_header_parts.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _header_parts: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _header_parts.__name__, __candidate_expansions)


def _file_name():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		file_name_chars=[]
		file_name_first_char=[]
		nuls=[]
		

		__global_state.declare_and_initialize('LEN', random.randint(0, 99) )
		LEN = LEN # for IDE variable binding


		
		try:
			__term_1 = _file_name_first_char()
			file_name_first_char.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _file_name_first_char()
				file_name_first_char[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name_first_char)


		
		try:
			__term_2 = _file_name_chars()
			file_name_chars.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _file_name_chars()
				file_name_chars[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name_chars)


		__global_state.save_state()
		try:
			__term_3 = _nuls()
			nuls.append(__term_3)
			__counter = 0
			while not (len(str(file_name_chars[0])) == LEN and len(str(nuls)) == 99 - LEN):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _nuls()
				nuls[-1] = __term_3
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nuls)

		

		__global_state.delete('LEN')

		return __term_1+__term_2+__term_3

	# debug_print(_file_name.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _file_name: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _file_name.__name__, __candidate_expansions)


def _file_name_chars():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		file_name_char=[]
		file_name_chars=[]
		

		
		try:
			__term_0 = _file_name_char()
			file_name_char.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _file_name_char()
				file_name_char[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name_char)


		
		try:
			__term_1 = _file_name_chars()
			file_name_chars.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _file_name_chars()
				file_name_chars[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name_chars)

		

		return __term_0+__term_1

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		file_name_char=[]
		

		
		try:
			__term_0 = _file_name_char()
			file_name_char.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _file_name_char()
				file_name_char[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name_char)

		

		return __term_0

	# debug_print(_file_name_chars.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _file_name_chars: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _file_name_chars.__name__, __candidate_expansions)


def _file_mode():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		space=[]
		octal_digits=[]
		nul=[]
		

		
		try:
			__term_0 = _octal_digits()
			octal_digits.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digits()
				octal_digits[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)


		
		try:
			__term_1 = _space()
			space.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _space()
				space[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', space)


		__global_state.save_state()
		try:
			__term_2 = _nul()
			nul.append(__term_2)
			__counter = 0
			while not (len(str(octal_digits[0])) == 6):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _nul()
				nul[-1] = __term_2
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nul)

		

		return __term_0+__term_1+__term_2

	# debug_print(_file_mode.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _file_mode: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _file_mode.__name__, __candidate_expansions)


def _uid():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		space=[]
		octal_digits=[]
		nul=[]
		

		
		try:
			__term_0 = _octal_digits()
			octal_digits.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digits()
				octal_digits[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)


		
		try:
			__term_1 = _space()
			space.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _space()
				space[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', space)


		__global_state.save_state()
		try:
			__term_2 = _nul()
			nul.append(__term_2)
			__counter = 0
			while not (len(str(octal_digits[0])) == 6):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _nul()
				nul[-1] = __term_2
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nul)

		

		return __term_0+__term_1+__term_2

	# debug_print(_uid.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _uid: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _uid.__name__, __candidate_expansions)


def _gid():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		space=[]
		octal_digits=[]
		nul=[]
		

		
		try:
			__term_0 = _octal_digits()
			octal_digits.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digits()
				octal_digits[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)


		
		try:
			__term_1 = _space()
			space.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _space()
				space[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', space)


		__global_state.save_state()
		try:
			__term_2 = _nul()
			nul.append(__term_2)
			__counter = 0
			while not (len(str(octal_digits[0])) == 6):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _nul()
				nul[-1] = __term_2
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nul)

		

		return __term_0+__term_1+__term_2

	# debug_print(_gid.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _gid: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _gid.__name__, __candidate_expansions)


def _file_size():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		space=[]
		octal_digits=[]
		file_size_beginning=[]
		

		
		try:
			__term_0 = _file_size_beginning()
			file_size_beginning.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _file_size_beginning()
				file_size_beginning[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_size_beginning)


		
		try:
			__term_1 = _octal_digits()
			octal_digits.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _octal_digits()
				octal_digits[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)


		__global_state.save_state()
		try:
			__term_2 = _space()
			space.append(__term_2)
			__counter = 0
			while not (len(str(octal_digits[0])) == 2):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _space()
				space[-1] = __term_2
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', space)

		

		return __term_0+__term_1+__term_2

	# debug_print(_file_size.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _file_size: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _file_size.__name__, __candidate_expansions)


def _file_size_beginning():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '000000001'

		

		return __term_0

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '000000000'

		

		return __term_0

	# debug_print(_file_size_beginning.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _file_size_beginning: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _file_size_beginning.__name__, __candidate_expansions)


def _mod_time():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		space=[]
		octal_digits=[]
		

		
		try:
			__term_0 = _octal_digits()
			octal_digits.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digits()
				octal_digits[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)


		__global_state.save_state()
		try:
			__term_1 = _space()
			space.append(__term_1)
			__counter = 0
			while not (len(str(octal_digits[0])) == 11):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _space()
				space[-1] = __term_1
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', space)

		

		return __term_0+__term_1

	# debug_print(_mod_time.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _mod_time: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _mod_time.__name__, __candidate_expansions)


def _checksum():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		space=[]
		octal_digits=[]
		

		
		try:
			__term_0 = _octal_digits()
			octal_digits.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digits()
				octal_digits[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)


		__global_state.save_state()
		try:
			__term_1 = _space()
			space.append(__term_1)
			__counter = 0
			while not (len(str(octal_digits[0])) == 6):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _space()
				space[-1] = __term_1
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', space)

		

		return __term_0+__term_1

	# debug_print(_checksum.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _checksum: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _checksum.__name__, __candidate_expansions)


def _typeflag():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '0'

		

		return __term_0

	# debug_print(_typeflag.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _typeflag: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _typeflag.__name__, __candidate_expansions)


def _linked_file_name():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		file_name_chars=[]
		file_name_first_char=[]
		nuls=[]
		

		__global_state.declare_and_initialize('LEN', random.randint(0, 99) )
		LEN = LEN # for IDE variable binding


		
		try:
			__term_1 = _file_name_first_char()
			file_name_first_char.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _file_name_first_char()
				file_name_first_char[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name_first_char)


		
		try:
			__term_2 = _file_name_chars()
			file_name_chars.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _file_name_chars()
				file_name_chars[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', file_name_chars)


		__global_state.save_state()
		try:
			__term_3 = _nuls()
			nuls.append(__term_3)
			__counter = 0
			while not (len(str(file_name_chars[0])) == LEN and len(str(nuls)) == 99 - LEN):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _nuls()
				nuls[-1] = __term_3
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nuls)

		

		__global_state.delete('LEN')

		return __term_1+__term_2+__term_3

	# debug_print(_linked_file_name.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _linked_file_name: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _linked_file_name.__name__, __candidate_expansions)


def _uname():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		uname_chars=[]
		uname_first_char=[]
		nuls=[]
		

		__global_state.declare_and_initialize('LEN', random.randint(0, 31) )
		LEN = LEN # for IDE variable binding


		
		try:
			__term_1 = _uname_first_char()
			uname_first_char.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _uname_first_char()
				uname_first_char[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uname_first_char)


		
		try:
			__term_2 = _uname_chars()
			uname_chars.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _uname_chars()
				uname_chars[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uname_chars)


		__global_state.save_state()
		try:
			__term_3 = _nuls()
			nuls.append(__term_3)
			__counter = 0
			while not (len(str(uname_chars[0])) == LEN and len(str(nuls)) == 31 - LEN):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _nuls()
				nuls[-1] = __term_3
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nuls)

		

		__global_state.delete('LEN')

		return __term_1+__term_2+__term_3

	# debug_print(_uname.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _uname: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _uname.__name__, __candidate_expansions)


def _gname():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		uname_chars=[]
		uname_first_char=[]
		nuls=[]
		

		__global_state.declare_and_initialize('LEN', random.randint(0, 31) )
		LEN = LEN # for IDE variable binding


		
		try:
			__term_1 = _uname_first_char()
			uname_first_char.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _uname_first_char()
				uname_first_char[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uname_first_char)


		
		try:
			__term_2 = _uname_chars()
			uname_chars.append(__term_2)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _uname_chars()
				uname_chars[-1] = __term_2
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uname_chars)


		__global_state.save_state()
		try:
			__term_3 = _nuls()
			nuls.append(__term_3)
			__counter = 0
			while not (len(str(uname_chars[0])) == LEN and len(str(nuls)) == 31 - LEN):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_3 = _nuls()
				nuls[-1] = __term_3
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nuls)

		

		__global_state.delete('LEN')

		return __term_1+__term_2+__term_3

	# debug_print(_gname.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _gname: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _gname.__name__, __candidate_expansions)


def _uname_chars():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		uname_chars=[]
		uname_char=[]
		

		
		try:
			__term_0 = _uname_char()
			uname_char.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _uname_char()
				uname_char[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uname_char)


		
		try:
			__term_1 = _uname_chars()
			uname_chars.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _uname_chars()
				uname_chars[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uname_chars)

		

		return __term_0+__term_1

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		uname_char=[]
		

		
		try:
			__term_0 = _uname_char()
			uname_char.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _uname_char()
				uname_char[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', uname_char)

		

		return __term_0

	# debug_print(_uname_chars.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _uname_chars: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _uname_chars.__name__, __candidate_expansions)


def _uname_first_char():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'a'

		

		return __term_0

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'b'

		

		return __term_0

	def __expansion_2():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'c'

		

		return __term_0

	def __expansion_3():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'd'

		

		return __term_0

	def __expansion_4():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'e'

		

		return __term_0

	def __expansion_5():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'f'

		

		return __term_0

	def __expansion_6():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'g'

		

		return __term_0

	def __expansion_7():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'h'

		

		return __term_0

	def __expansion_8():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'i'

		

		return __term_0

	def __expansion_9():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'j'

		

		return __term_0

	def __expansion_10():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'k'

		

		return __term_0

	def __expansion_11():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'l'

		

		return __term_0

	def __expansion_12():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'm'

		

		return __term_0

	def __expansion_13():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'n'

		

		return __term_0

	def __expansion_14():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'o'

		

		return __term_0

	def __expansion_15():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'p'

		

		return __term_0

	def __expansion_16():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'q'

		

		return __term_0

	def __expansion_17():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'r'

		

		return __term_0

	def __expansion_18():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 's'

		

		return __term_0

	def __expansion_19():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 't'

		

		return __term_0

	def __expansion_20():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'u'

		

		return __term_0

	def __expansion_21():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'v'

		

		return __term_0

	def __expansion_22():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'w'

		

		return __term_0

	def __expansion_23():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'x'

		

		return __term_0

	def __expansion_24():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'y'

		

		return __term_0

	def __expansion_25():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'z'

		

		return __term_0

	def __expansion_26():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '_'

		

		return __term_0

	# debug_print(_uname_first_char.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1, __expansion_2, __expansion_3, __expansion_4, __expansion_5, __expansion_6, __expansion_7, __expansion_8, __expansion_9, __expansion_10, __expansion_11, __expansion_12, __expansion_13, __expansion_14, __expansion_15, __expansion_16, __expansion_17, __expansion_18, __expansion_19, __expansion_20, __expansion_21, __expansion_22, __expansion_23, __expansion_24, __expansion_25, __expansion_26]
	__all_expansion_depths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	__all_expansion_constraints = [(True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True)]
	__all_expansion_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
			# debug_print(f"Expansion succeeded for _uname_first_char: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _uname_first_char.__name__, __candidate_expansions)


def _uname_char():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'a'

		

		return __term_0

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'b'

		

		return __term_0

	def __expansion_2():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'c'

		

		return __term_0

	def __expansion_3():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'd'

		

		return __term_0

	def __expansion_4():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'e'

		

		return __term_0

	def __expansion_5():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'f'

		

		return __term_0

	def __expansion_6():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'g'

		

		return __term_0

	def __expansion_7():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'h'

		

		return __term_0

	def __expansion_8():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'i'

		

		return __term_0

	def __expansion_9():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'j'

		

		return __term_0

	def __expansion_10():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'k'

		

		return __term_0

	def __expansion_11():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'l'

		

		return __term_0

	def __expansion_12():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'm'

		

		return __term_0

	def __expansion_13():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'n'

		

		return __term_0

	def __expansion_14():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'o'

		

		return __term_0

	def __expansion_15():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'p'

		

		return __term_0

	def __expansion_16():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'q'

		

		return __term_0

	def __expansion_17():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'r'

		

		return __term_0

	def __expansion_18():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 's'

		

		return __term_0

	def __expansion_19():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 't'

		

		return __term_0

	def __expansion_20():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'u'

		

		return __term_0

	def __expansion_21():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'v'

		

		return __term_0

	def __expansion_22():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'w'

		

		return __term_0

	def __expansion_23():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'x'

		

		return __term_0

	def __expansion_24():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'y'

		

		return __term_0

	def __expansion_25():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = 'z'

		

		return __term_0

	def __expansion_26():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '0'

		

		return __term_0

	def __expansion_27():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '1'

		

		return __term_0

	def __expansion_28():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '2'

		

		return __term_0

	def __expansion_29():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '3'

		

		return __term_0

	def __expansion_30():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '4'

		

		return __term_0

	def __expansion_31():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '5'

		

		return __term_0

	def __expansion_32():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '6'

		

		return __term_0

	def __expansion_33():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '7'

		

		return __term_0

	def __expansion_34():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '8'

		

		return __term_0

	def __expansion_35():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '9'

		

		return __term_0

	def __expansion_36():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '_'

		

		return __term_0

	def __expansion_37():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = '-'

		

		return __term_0

	# debug_print(_uname_char.__name__, __depth)
	__all_expansions = [__expansion_0, __expansion_1, __expansion_2, __expansion_3, __expansion_4, __expansion_5, __expansion_6, __expansion_7, __expansion_8, __expansion_9, __expansion_10, __expansion_11, __expansion_12, __expansion_13, __expansion_14, __expansion_15, __expansion_16, __expansion_17, __expansion_18, __expansion_19, __expansion_20, __expansion_21, __expansion_22, __expansion_23, __expansion_24, __expansion_25, __expansion_26, __expansion_27, __expansion_28, __expansion_29, __expansion_30, __expansion_31, __expansion_32, __expansion_33, __expansion_34, __expansion_35, __expansion_36, __expansion_37]
	__all_expansion_depths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	__all_expansion_constraints = [(True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True), (True)]
	__all_expansion_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
			# debug_print(f"Expansion succeeded for _uname_char: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _uname_char.__name__, __candidate_expansions)


def _dev_maj_num():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		space=[]
		octal_digits=[]
		nul=[]
		

		
		try:
			__term_0 = _octal_digits()
			octal_digits.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digits()
				octal_digits[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)


		
		try:
			__term_1 = _space()
			space.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _space()
				space[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', space)


		__global_state.save_state()
		try:
			__term_2 = _nul()
			nul.append(__term_2)
			__counter = 0
			while not (len(octal_digits[0]) == 6):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _nul()
				nul[-1] = __term_2
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nul)

		

		return __term_0+__term_1+__term_2

	# debug_print(_dev_maj_num.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _dev_maj_num: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _dev_maj_num.__name__, __candidate_expansions)


def _dev_min_num():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		space=[]
		octal_digits=[]
		nul=[]
		

		
		try:
			__term_0 = _octal_digits()
			octal_digits.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digits()
				octal_digits[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)


		
		try:
			__term_1 = _space()
			space.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _space()
				space[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', space)


		__global_state.save_state()
		try:
			__term_2 = _nul()
			nul.append(__term_2)
			__counter = 0
			while not (len(octal_digits[0]) == 6):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _nul()
				nul[-1] = __term_2
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nul)

		

		return __term_0+__term_1+__term_2

	# debug_print(_dev_min_num.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _dev_min_num: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _dev_min_num.__name__, __candidate_expansions)


def _file_name_prefix():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		nuls=[]
		

		__global_state.save_state()
		try:
			__term_0 = _nuls()
			nuls.append(__term_0)
			__counter = 0
			while not (len(nuls[0]) == 155):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _nuls()
				nuls[-1] = __term_0
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nuls)

		

		return __term_0

	# debug_print(_file_name_prefix.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _file_name_prefix: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _file_name_prefix.__name__, __candidate_expansions)


def _header_padding():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		nuls=[]
		

		__global_state.save_state()
		try:
			__term_0 = _nuls()
			nuls.append(__term_0)
			__counter = 0
			while not (len(nuls[0]) == 12):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _nuls()
				nuls[-1] = __term_0
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nuls)

		

		return __term_0

	# debug_print(_header_padding.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _header_padding: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _header_padding.__name__, __candidate_expansions)


def _content():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		chars=[]
		nuls=[]
		

		__global_state.declare_and_initialize('LEN', random.randint(0, 512) )
		LEN = LEN # for IDE variable binding


		
		try:
			__term_1 = _chars()
			chars.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _chars()
				chars[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', chars)


		__global_state.save_state()
		try:
			__term_2 = _nuls()
			nuls.append(__term_2)
			__counter = 0
			while not (len(str(chars[0])) == LEN and len(str(nuls[0])) == 512 - LEN):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_2 = _nuls()
				nuls[-1] = __term_2
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nuls)

		

		__global_state.delete('LEN')

		return __term_1+__term_2

	# debug_print(_content.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _content: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _content.__name__, __candidate_expansions)


def _chars():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		chars=[]
		character=[]
		

		
		try:
			__term_0 = _character()
			character.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _character()
				character[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', character)


		
		try:
			__term_1 = _chars()
			chars.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _chars()
				chars[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', chars)

		

		return __term_0+__term_1

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		character=[]
		

		
		try:
			__term_0 = _character()
			character.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _character()
				character[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', character)

		

		return __term_0

	# debug_print(_chars.__name__, __depth)
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


def _final_entry():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		nuls=[]
		

		__global_state.save_state()
		try:
			__term_0 = _nuls()
			nuls.append(__term_0)
			__counter = 0
			while not (len(str(nuls[0])) == 1024):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _nuls()
				nuls[-1] = __term_0
				__counter += 1
			__global_state.delete_saved_state()
		except IterationException as e:
			__global_state.delete_saved_state()
			raise IterationException('Failed to get expansion for ', nuls)

		

		return __term_0

	# debug_print(_final_entry.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _final_entry: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _final_entry.__name__, __candidate_expansions)


def _nuls():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		nuls=[]
		nul=[]
		

		
		try:
			__term_0 = _nul()
			nul.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _nul()
				nul[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', nul)


		
		try:
			__term_1 = _nuls()
			nuls.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _nuls()
				nuls[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', nuls)

		

		return __term_0+__term_1

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		nul=[]
		

		
		try:
			__term_0 = _nul()
			nul.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _nul()
				nul[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', nul)

		

		return __term_0

	# debug_print(_nuls.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _nuls: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _nuls.__name__, __candidate_expansions)


def _octal_digits():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		octal_digits=[]
		octal_digit=[]
		

		
		try:
			__term_0 = _octal_digit()
			octal_digit.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digit()
				octal_digit[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digit)


		
		try:
			__term_1 = _octal_digits()
			octal_digits.append(__term_1)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_1 = _octal_digits()
				octal_digits[-1] = __term_1
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digits)

		

		return __term_0+__term_1

	def __expansion_1():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		
		octal_digit=[]
		

		
		try:
			__term_0 = _octal_digit()
			octal_digit.append(__term_0)
			__counter = 0
			while not (True):
				__global_state.restore_state()
				if __counter >= __retry_attempts:
					raise IterationException('Too many attempts')
				__term_0 = _octal_digit()
				octal_digit[-1] = __term_0
				__counter += 1
			
		except IterationException as e:
			
			raise IterationException('Failed to get expansion for ', octal_digit)

		

		return __term_0

	# debug_print(_octal_digits.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _octal_digits: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _octal_digits.__name__, __candidate_expansions)


def _octal_digit():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = str(regex("[0-7]"))
		

		

		return __term_0

	# debug_print(_octal_digit.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _octal_digit: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _octal_digit.__name__, __candidate_expansions)


def _character():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = str(regex("[0-9a-zA-Z]"))
		

		

		return __term_0

	# debug_print(_character.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _character: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _character.__name__, __candidate_expansions)


def _file_name_first_char():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = str(regex("[a-zA-Z0-9]|_"))
		

		

		return __term_0

	# debug_print(_file_name_first_char.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _file_name_first_char: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _file_name_first_char.__name__, __candidate_expansions)


def _file_name_char():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = str(regex("[0-9a-zA-Z]"))
		

		

		return __term_0

	# debug_print(_file_name_char.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _file_name_char: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _file_name_char.__name__, __candidate_expansions)


def _nul():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = str(regex('\x00'))
		

		

		return __term_0

	# debug_print(_nul.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _nul: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _nul.__name__, __candidate_expansions)


def _space():
	global __depth
	
	def __expansion_0():
		global HEADER_STR, CHECKSUM, LEN, LEN, LEN, LEN, LEN
		

		

		__term_0 = ' '

		

		return __term_0

	# debug_print(_space.__name__, __depth)
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
			# debug_print(f"Expansion succeeded for _space: {__temp}")
			__global_state.delete_saved_state()
			__depth -= 1
			return __temp
		except IterationException as e:
			__candidate_indexes.pop()
			__candidate_weights.pop(__index)
			__depth -= 1
			__global_state.restore_state()
	__global_state.delete_saved_state()
	raise IterationException('All expansions failed for:', _space.__name__, __candidate_expansions)


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

