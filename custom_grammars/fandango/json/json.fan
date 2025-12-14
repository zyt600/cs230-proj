<start> ::= <json>

<json> ::= <value>

<value> ::= <json_obj> | <list> | <string> | <integer> | <boolean>

<json_obj> ::= '{' <ws_opt> <key_values> <ws_opt> '}'

<key_values> ::= '' | <pair> | <pair> <ws_opt> ',' <ws_opt> <key_values>

<pair> ::= <key> <ws_opt> ':' <ws_opt> <value>

<key> ::= <string>

<string> ::= '"' <letters> '"'

<letters> ::= <l1> | <l2> | <l3> | <l4> | <l5> | <l6> | <l7>
<l1> ::= <ascii_lowercase_letter>
<l2> ::= <l1> <ascii_lowercase_letter>
<l3> ::= <l2> <ascii_lowercase_letter>
<l4> ::= <l3> <ascii_lowercase_letter>
<l5> ::= <l4> <ascii_lowercase_letter>
<l6> ::= <l5> <ascii_lowercase_letter>
<l7> ::= <l6> <ascii_lowercase_letter>

<list> ::= '[' <ws_opt> <values_opt> <ws_opt> ']'

<values_opt> ::= '' | <values>

<values> ::= <value> | <value> <ws_opt> ',' <ws_opt> <values>

<boolean> ::= 'true' | 'false'

<integer> ::= <digits>

<digits> ::= <d1> | <d2> | <d3> | <d4> | <d5>
<d1> ::= <digit>
<d2> ::= <d1> <digit>
<d3> ::= <d2> <digit>
<d4> ::= <d3> <digit>
<d5> ::= <d4> <digit>

<ascii_lowercase_letter> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'

<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

<ws_opt> ::= '' | ' '

where unique_keys(<key_values>)

def unique_keys(key_values):
    def collect_keys(tree):
        if tree is None:
            return []
        if tree.is_non_terminal:
            if tree.symbol.name() == "<key>":
                return [str(tree)]
            if tree.symbol.name() == "<value>":
                return []
            out = []
            for child in tree._children:
                out.extend(collect_keys(child))
            return out
        return []

    keys = collect_keys(key_values)
    return len(keys) == len(set(keys))
