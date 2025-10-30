<start> ::= <person_name> ',' <age>

<person_name> ::= <first> ' ' <last>

<first> ::= <name>
<last> ::= <name>

<name> ::= <ascii_uppercase_letter><ascii_lowercase_letter>+

<age> ::= <digit>+

where is_valid_entry(int(<age>), str(<first>), str(<name>))


def is_valid_entry(age, first_name, name):
    if len(name) >= 2 and len(name) <= 10:
        if first_name.startswith('A'):
            if age >= 25 and age <= 35:
                return True
            else:
                return False
        else:
            if age >= 50 and age <= 60:
                return True
            else:
                return False
    else:
        return False