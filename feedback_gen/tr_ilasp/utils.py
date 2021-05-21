def split_literals(string, deliminator=','):
    split = []
    buffer = ""
    count = 0

    for c in string:
        if count == 0 and c == deliminator:
            split.append(buffer.strip())
            buffer = ""
        else:
            if c == '(':
                count += 1
            elif c == ')':
                count -= 1
            buffer += c
        if count < 0:
            paren_error(string)
    split.append(buffer.strip())
    return split


def type_error(type, rule_and_type):
    print("Type error in {} in {}".format(type, rule_and_type))


def concat_literal(literal):
    result = ""
    for i in range(len(literal)):
        c = literal[i]
        if c == ' ' or c == ')':
            continue
        if c not in [',', '(']:
            result += c
        elif i != len(literal) - 1:
            result += "_"
    return result


def check_paren_literal(literal, rule):
    count = 0
    for c in literal:
        if c == '(':
            count += 1
        elif c == ')':
            count -= 1

    if count != 0:
        print("Parentheses does not match in literal {} in rule {}".format(literal, rule))
        exit()
    pass


def paren_error(rule):
    print("Parentheses does not match in theory {}".format(rule))
    exit()


def fullstop_error(rule):
    print("Full Stop (.) does not match in theory {}".format(rule))
    exit()


def variable_literals(root, theory):
    result_set = set()
    type_dict = theory.types
    variable_literals_help(root, type_dict, result_set)
    if len(result_set) == 0:
        return None
    result = ""
    for literals in result_set:
        result += literals + ", "
    result = result[:-2] + "."
    return result


def variable_literals_help(root, type_dict, result_set):
    value = root.val[0]
    if value.isupper():
        result_set.add("{}({})".format(type_dict[root.val], root.val))
    for child in root.children:
        variable_literals_help(child, type_dict, result_set)


def build_inverse_dict(type_dict):
    inverse_dict = {}
    for variable, type in type_dict.items():
        if type not in inverse_dict:
            inverse_dict[type] = []
        inverse_dict[type].append(variable)
    return inverse_dict
