<start> ::= <translation_unit>

<translation_unit> ::= <function_def>

<function_def> ::= 'int main(void) ' <block>

<statement> ::= <matched>

<matched> ::= <block> | 'while' <paren_expr> ' ' <matched> | 'do ' <matched> ' while' <paren_expr> ';' | <expr> ';' | ';'

<block> ::= '{' <statements> '}'

<statements> ::= <block_statement> <statements> | ''

<block_statement> ::= <statement> | <declaration>

<declaration> ::= 'int ' <id> ' = ' <expr> ';' | 'int ' <id> ';'

<paren_expr> ::= '(' <expr> ')'

<expr> ::= <id> ' = ' <expr> | <test>

<test> ::= <sum> ' < ' <sum> | <sum>

# no left recursion
<sum> ::= <term> <sum_tail>
<sum_tail> ::= ' + ' <term> <sum_tail> | ' - ' <term> <sum_tail> | ''

<term> ::= <paren_expr> | <id> | <int_>

<id> ::= <ascii_lowercase_letter>

# decimal only, no leading zeros (except 0)
<int_> ::= '0' | <nonzero_digit> | <nonzero_digit> <digit> | <nonzero_digit> <digit> <digit> | <nonzero_digit> <digit> <digit> <digit> | <nonzero_digit> <digit> <digit> <digit> <digit>

<nonzero_digit> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

<ascii_lowercase_letter> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'

where check_valid(<start>)

def check_valid_util(tree, DEC, NO_REDEC):
    if tree.is_non_terminal:
        if tree.symbol.name() == "<block>":
            NEW_DEC = DEC.copy()
            NEW_NO_REDEC = set()
            for child in tree._children:
                if not check_valid_util(child, NEW_DEC, NEW_NO_REDEC):
                    return False
            return True

        elif tree.symbol.name() == "<declaration>":
            for child in tree._children:
                if child.is_non_terminal and child.symbol.name() == "<id>":
                    identifier = str(child)
                    if identifier in NO_REDEC:
                        return False
                    DEC.add(identifier)
                    NO_REDEC.add(identifier)
                elif not check_valid_util(child, DEC, NO_REDEC):
                    return False
            return True

        elif tree.symbol.name() == "<expr>" or tree.symbol.name() == "<term>":
            for child in tree._children:
                if child.is_non_terminal and child.symbol.name() == "<id>":
                    if len(DEC) == 0:
                        return False
                    identifier = str(child)
                    if identifier not in DEC:
                        return False
                elif not check_valid_util(child, DEC, NO_REDEC):
                    return False
            return True

        else:
            for child in tree._children:
                if not check_valid_util(child, DEC, NO_REDEC):
                    return False
            return True
    return True

def check_valid(tree):
    DEC = set()
    NO_REDEC = set()
    return check_valid_util(tree, DEC, NO_REDEC)
