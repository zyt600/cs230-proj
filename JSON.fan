<start> ::= <json>

<json> ::= <value>

<value> ::= <json_obj> | <list> | <string> | <integer> | <boolean>

<json_obj> ::= '{' <key_values> '}' | '{}'

<key_values> ::= <pair> | <pair> ', ' <key_values>

<pair> ::= <key> ':' <value>

<key> ::= <string>

<string> ::= '"' <ascii_lowercase_letter>+ '"'

<list> ::= '[' <values> ']' | '[]'

<values> ::= <value> ',' <values> | <value>;

<boolean> ::= 'true' | 'false'

<integer> ::= <digit>+

# This code ensures that all keys within a JSON object block are unique

where unique_keys(<key_values>)

def unique_keys(key_values):
    def all_keys(tree):
    if tree.is_non_terminal:
        if tree.symbol.name() == "<key>": return [str(tree)]

        elif tree.symbol.name() == "<value>": return []

        keys = []
        for child in tree._children:
            keys.extend(all_keys(child))

        return keys

    else: return []

    keys_in_json_block = all_keys(key_values)
    return len(keys_in_json_block) == len(set(keys_in_json_block))