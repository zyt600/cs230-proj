<start> ::= <json>;

<json> ::= <value>;

<value> ::= <json_obj> | <list> | <string> | <integer> | <boolean>;

# ----- Objects -----
# Keep <key_values> present (possibly empty) so constraints can always reference it.
<json_obj> ::= '{' <ws_opt> <key_values> <ws_opt> '}';

<key_values> ::= '' | <pair> | <pair> <ws_opt> ',' <ws_opt> <key_values>;

<pair> ::= <key> <ws_opt> ':' <ws_opt> <value>;

<key> ::= <string>;

# ----- Strings -----
# Quoted lowercase strings with 1..7 letters (constraint also enforces this).
<string> ::= '"' <letters> '"';
<letters> ::= <ascii_lowercase_letter> | <ascii_lowercase_letter> <letters>;

# ----- Lists -----
<list> ::= '[' <ws_opt> <values_opt> <ws_opt> ']';
<values_opt> ::= '' | <values>;
<values> ::= <value> | <value> <ws_opt> ',' <ws_opt> <values>;

# ----- Booleans / Integers -----
<boolean> ::= 'true' | 'false';

<integer> ::= <digits>;
<digits> ::= <digit> | <digit> <digits>;

# ----- Whitespace -----
<ws_opt> ::= '' | ' ';

# ----- Character classes -----
<ascii_lowercase_letter> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z';
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

# ------------------------------------------------------------
# Constraints:
# 1) Keys within each object are unique
# 2) String length (letters only) <= 7
# 3) Integer digit-length <= 5
# ------------------------------------------------------------
where unique_keys(<key_values>) and (len(str(<string>)) - 2) <= 7 and len(str(<integer>)) <= 5


def unique_keys(key_values):
    """
    Returns True iff all <key> occurrences inside this <key_values> subtree are unique.
    Works even when <key_values> is empty ('').
    """

    def all_keys(tree):
        if tree is None:
            return []

        if tree.is_non_terminal:
            # Only collect keys; ignore values
            if tree.symbol.name() == "<key>":
                return [str(tree)]

            if tree.symbol.name() == "<value>":
                return []

            keys = []
            for child in tree._children:
                keys.extend(all_keys(child))
            return keys

        return []

    keys_in_obj = all_keys(key_values)
    return len(keys_in_obj) == len(set(keys_in_obj))
