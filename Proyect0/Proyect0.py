import re

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
direction = ['front', 'back', 'left', 'right']
cardinality = ['north', 'south', 'east', 'west']
turn = ['left', 'right', 'around']

# Initialize a symbol table to store variables and functions
symbol_set = set()


# Define a function for error reporting
def report_error(message):
    print("Syntax Error:", message)


def read_file():
    filename = 'Ejemplo2.txt'
    with open(filename, 'r') as file:
        instructions = file.read()
    return instructions


# Tokenizer function
def tokenize(instructions):
    pattern = r'\w+|[.,!?;(){}\[\]=]'
    tokens = re.findall(pattern, instructions)
    tokens = [token.lower() for token in tokens]

    return tokens


# Checks if the token is an alphanumeric string

def isAlphabetical(token):
    if token[0].isalpha() or token[0] == '_':
        for char in token[1:]:
            if not (char.isalnum() or char == '_'):
                return False
        return True
    return False


# Checks if the token is a number
def isNumeric(token):
    return token.isdigit()


# Parse variable definitions
def parse_variable(tokens, index):
    if index < len(tokens) and tokens[index] == "defvar":
        index += 1
        if index < len(tokens) and isAlphabetical(tokens[index]):
            variable_name = tokens[index]
            index += 1
            if index < len(tokens) and isNumeric(tokens[index]):
                # Variable definition is valid
                symbol_set.add(variable_name)
                return index + 1
    return -1


# Parse variable assignments
def parse_assignment(tokens, index):
    if index < len(tokens) and isAlphabetical(tokens[index]):
        variable_name = tokens[index]
        index += 1
        if index < len(tokens) and tokens[index] == "=":
            index += 1
            if index < len(tokens) and isNumeric(tokens[index]):
                # Variable assignment is valid
                symbol_set.add(variable_name)
                return index + 1
    return -1


# Parse the jump command
def parse_jump(tokens, index):
    if index < len(tokens) and tokens[index] == "jump":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in list(symbol_set) + numbers:
                index += 1
                if index < len(tokens) and tokens[index] == ",":
                    index += 1
                    if index < len(tokens) and isNumeric(tokens[index]):
                        index += 1
                        if index < len(tokens) and tokens[index] == ")":
                            index += 1
                            if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                                return index + 1
                            # Process the jump command with x and y values

    return -1


# Parse the walk command
def parse_walk(tokens, index):
    if index < len(tokens) and tokens[index] == "walk":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in list(symbol_set) + numbers:
                index += 1
                if index < len(tokens) and tokens[index] == ")":
                    # Process the walk(v) command
                    return index + 1
                elif index < len(tokens) and tokens[index] == ",":
                    index += 1
                    if index < len(tokens) and tokens[index] in cardinality + direction:
                        index += 1
                        if index < len(tokens) and tokens[index] == ")":
                            index += 1
                            if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                                return index + 1
                            # Process the walk(v, D) command of walk(v, O) command

    return -1


# Parse the leap command
def parse_leap(tokens, index):
    if index < len(tokens) and tokens[index] == "leap":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in list(symbol_set) + numbers:
                index += 1
                if index < len(tokens) and tokens[index] == ")":
                    # Process the leap(v) command
                    return index + 1
                elif index < len(tokens) and tokens[index] == ",":
                    index += 1
                    if index < len(tokens) and tokens[index] in cardinality + direction:
                        index += 1
                        if index < len(tokens) and tokens[index] == ")":
                            index += 1
                            if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                                return index + 1
                            # Process the leap(v, D) command or leap(v, O) command

    return -1


# Parse the turn
def parse_turn(tokens, index):
    if index < len(tokens) and tokens[index] == "turn":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in turn:
                index += 1
                if index < len(tokens) and tokens[index] == ")":
                    index += 1
                    if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                        return index + 1
                    # Process the turn(D) command

    return -1


# Parse the turnto
def parse_turnto(tokens, index):
    if index < len(tokens) and tokens[index] == "turnto":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in cardinality:
                index += 1
                if index < len(tokens) and tokens[index] == ")":
                    index += 1
                    if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                        return index + 1
                    # Process the turnto(O) command

    return -1


# Parse the drop
def parse_drop(tokens, index):
    if index < len(tokens) and tokens[index] == "drop":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in list(symbol_set) + numbers:
                index += 1
                if index < len(tokens) and tokens[index] == ")":
                    index += 1
                    if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                        return index + 1
                    # Process the drop(v) command

    return -1


# Parse the get
def parse_get(tokens, index):
    if index < len(tokens) and tokens[index] == "get":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in list(symbol_set) + numbers:
                index += 1
                if index < len(tokens) and tokens[index] == ")":
                    index += 1
                    if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                        return index + 1
                    # Process the drop(v) command

    return -1


# Parse the grab
def parse_grab(tokens, index):
    if index < len(tokens) and tokens[index] == "grab":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in list(symbol_set) + numbers:
                index += 1
                if index < len(tokens) and tokens[index] == ")":
                    index += 1
                    if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                        return index + 1
                    # Process the grab(v) command

    return -1


# Parse the letgo
def parse_letgo(tokens, index):
    if index < len(tokens) and tokens[index] == "letgo":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] in list(symbol_set) + numbers:
                index += 1
                if index < len(tokens) and tokens[index] == ")":
                    index += 1
                    if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                        return index + 1
                    # Process the letgo(v) command

    return -1


# Parse the nop
def parse_nop(tokens, index):
    if index < len(tokens) and tokens[index] == "nop":
        index += 1
        if index < len(tokens) and tokens[index] == "(":
            index += 1
            if index < len(tokens) and tokens[index] == ")":
                index += 1
                if index < len(tokens) and tokens[index] == ";" or tokens[index] == "}":
                    return index + 1
                # Process the nop() command

    return -1


def parse_simple_commands(tokens, index):
    if (exit_index := parse_assignment(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_jump(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_walk(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_leap(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_turn(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_turnto(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_drop(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_get(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_grab(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_letgo(tokens, index)) != -1:
        return exit_index

    if (exit_index := parse_nop(tokens, index)) != -1:
        return exit_index

    return -1


# Tokenize the program and parse it
tokens = tokenize(read_file())


# Parse procedure definitions
def parse_procedure(tokens, index):
    if index < len(tokens) and tokens[index] == "defproc":
        index += 1
        if index < len(tokens) and isAlphabetical(tokens[index]):
            procedure_name = tokens[index]
            index += 1
            if index < len(tokens) and tokens[index] == "(":
                index += 1
                # Parse parameters
                parameters = []
                while index < len(tokens) and tokens[index] != ")":
                    if isAlphabetical(tokens[index]):
                        parameters.append(tokens[index])
                        symbol_set.add(tokens[index])
                        index += 1
                        if index < len(tokens) and tokens[index] == ",":
                            index += 1
                        elif index < len(tokens) and tokens[index] != ")":
                            break
                    else:
                        report_error("Invalid parameter name")
                        return -1
                if index < len(tokens) and tokens[index] == ")":
                    index += 1
                    if index < len(tokens) and tokens[index] == "{":
                        index += 1
                        while index < len(tokens) and tokens[index] != "}":
                            if (exit_index := parse_simple_commands(tokens, index)) != -1:
                                index = exit_index
                            else:
                                return -1

                            if index < len(tokens) and tokens[index] == ";":
                                index += 1

                        if index < len(tokens) and tokens[index] == "}":
                            # Procedure definition is valid
                            symbol_set.add(procedure_name)
                            return index + 1

    return -1


# Main parsing function
def parse_program(tokens):
    index = 0
    passing = True
    while index < len(tokens) and passing:
        if (exit_index := parse_variable(tokens, index)) != -1:
            index = exit_index
            continue

        if (exit_index := parse_procedure(tokens, index)) != -1:
            index = exit_index
            print(index)
            continue

        if (exit_index := parse_simple_commands(tokens, index)) != -1:
            index = exit_index
            continue

        passing = False

    return passing


# Parse a condition (facing(O), can(C), not: cond)
def parse_condition(tokens, index):
    if index < len(tokens):
        if tokens[index] == "facing":
            index += 1
            if index < len(tokens) and tokens[index] == "(":
                index += 1
                if index < len(tokens) and tokens[index] in cardinality:
                    index += 1
                    if index < len(tokens) and tokens[index] == ")":
                        return index + 1

        elif tokens[index] == "can":
            index += 1
            if index < len(tokens) and tokens[index] == "(":
                index += 1
                if (exit_index := parse_simple_commands(tokens, index)) != -1:
                    return exit_index

        elif tokens[index] == "not":
            index += 1
            if index < len(tokens) and tokens[index] == ":":
                index += 1
                if (exit_index := parse_condition(tokens, index)) != -1:
                    return exit_index
    return -1


def parse_control_structure(tokens, index):
    if index < len(tokens):
        if tokens[index] == "if":
            return parse_if_statement(tokens, index)
        elif tokens[index] == "while":
            return parse_while_loop(tokens, index)
        elif tokens[index] == "repeat":
            return parse_repeat_times(tokens, index)
    return -1


# Parse for if statement

def parse_if_statement(tokens, index):
    if index < len(tokens) and tokens[index] == "if":
        index += 1
        # Parse the condition
        if (exit_index := parse_condition(tokens, index)) != -1:
            index = exit_index
        else:
            report_error("Invalid condition in if statement")
            return -1

        # Parse the true block
        if index < len(tokens) and tokens[index] == "{":
            index += 1
            while index < len(tokens) and tokens[index] != "}":
                if (exit_index := parse_control_structure(tokens, index)) != -1:
                    index = exit_index
                elif (exit_index := parse_simple_commands(tokens, index)) != -1:
                    index = exit_index
                else:
                    report_error("Invalid statement in if block")
                    return -1

                if index < len(tokens) and tokens[index] == ";":
                    index += 1

            if index < len(tokens) and tokens[index] == "}":
                index += 1
            else:
                report_error("Missing '}' in if statement")
                return -1
        else:
            report_error("Missing '{' in if statement")
            return -1

        # Parse the else block (optional)
        if index < len(tokens) and tokens[index] == "else":
            index += 1
            if index < len(tokens) and tokens[index] == "{":
                index += 1
                while index < len(tokens) and tokens[index] != "}":
                    if (exit_index := parse_control_structure(tokens, index)) != -1:
                        index = exit_index
                    elif (exit_index := parse_simple_commands(tokens, index)) != -1:
                        index = exit_index
                    else:
                        report_error("Invalid statement in else block")
                        return -1

                    if index < len(tokens) and tokens[index] == ";":
                        index += 1

                if index < len(tokens) and tokens[index] == "}":
                    index += 1
                else:
                    report_error("Missing '}' in else block")
                    return -1

        return index

    return -1


# Parse for while loop

def parse_while_loop(tokens, index):
    if index < len(tokens) and tokens[index] == "while":
        index += 1
        # Parse the condition
        if (exit_index := parse_condition(tokens, index)) != -1:
            index = exit_index
        else:
            report_error("Invalid condition in while loop")
            return -1

        # Parse the loop body
        if index < len(tokens) and tokens[index] == "{":
            index += 1
            while index < len(tokens) and tokens[index] != "}":
                if (exit_index := parse_control_structure(tokens, index)) != -1:
                    index = exit_index
                elif (exit_index := parse_simple_commands(tokens, index)) != -1:
                    index = exit_index
                else:
                    report_error("Invalid statement in while loop body")
                    return -1

                if index < len(tokens) and tokens[index] == ";":
                    index += 1

            if index < len(tokens) and tokens[index] == "}":
                index += 1
            else:
                report_error("Missing '}' in while loop")
                return -1
        else:
            report_error("Missing '{' in while loop")
            return -1

        return index

    return -1


# Parse function for the repeat times

def parse_repeat_times(tokens, index):
    if index < len(tokens) and tokens[index] == "repeat":
        index += 1
        # Parse the number of times to repeat
        if index < len(tokens) and isNumeric(tokens[index]):
            index += 1
        else:
            report_error("Invalid repeat times value")
            return -1

        # Parse the loop body
        if index < len(tokens) and tokens[index] == "{":
            index += 1
            while index < len(tokens) and tokens[index] != "}":
                if (exit_index := parse_control_structure(tokens, index)) != -1:
                    index = exit_index
                elif (exit_index := parse_simple_commands(tokens, index)) != -1:
                    index = exit_index
                else:
                    report_error("Invalid statement in repeat times loop body")
                    return -1

                if index < len(tokens) and tokens[index] == ";":
                    index += 1

            if index < len(tokens) and tokens[index] == "}":
                index += 1
            else:
                report_error("Missing '}' in repeat times loop")
                return -1
        else:
            report_error("Missing '{' in repeat times loop")
            return -1

        return index

    return -1


if parse_program(tokens):
    print("Yes, the program has correct syntax.")
else:
    print("No, the program has syntax errors.")
