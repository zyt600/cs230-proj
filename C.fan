<start> ::= <statement>

<statement> ::= <block> | 'if' <paren_expr> ' ' <statement> ' else ' <statement> | 'if' <paren_expr> ' ' <statement> | 'while' <paren_expr> ' ' <statement> | 'do ' <statement> ' while' <paren_expr> ';' | <expr> ';' | ';'

<block> ::= '{' <statements> '}'

<statements> ::= <block_statement> <statements> | ''

<block_statement> ::= <statement> | <declaration>

<declaration> ::= 'int ' <id> ' = ' <expr> ';' | 'int ' <id> ';'

<paren_expr> ::= '(' <expr> ')'

<expr> ::= <id> ' = ' <expr> | <test>

<test> ::= <sum> ' < ' <sum> | <sum>

<sum> ::= <sum> ' + ' <term> | <sum> ' - ' <term> | <term>

<term> ::= <paren_expr> | <id> | <int_>

<id> ::= <ascii_lowercase_letter>

<int_> ::= <digit>{1,5}

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
                    else:
                        DEC.add(identifier)
                        NO_REDEC.add(identifier)

                elif not check_valid_util(child, DEC, NO_REDEC):
                    return False

            return True

        elif tree.symbol.name() == "<expr>":
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

        elif tree.symbol.name() == "<term>":
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

    else:
        return True


def check_valid(tree):
    DEC = set()
    NO_REDEC = set()
    return check_valid_util(tree, DEC, NO_REDEC)