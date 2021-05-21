from .utils import split_literals


class Node:
    def __init__(self, val):
        self.val = val
        self.children = []
    def __str__(self):
        return 'Node({}, Children: {})'.format(self.val, len(self.children))


class Variable(Node):
    def __init__(self, type, value):
        Node.__init__(self, value)
        self.type = type
    def __str__(self):
        return 'Variable({})'.format(self.type)


class Constant(Node):
    def __init__(self, id, value):
        Node.__init__(self, value)
        self.id = id
    def __str__(self):
        return 'Constant({})'.format(self.id)


def build_tree(literal):
    split = literal.split('(', maxsplit=1)
    if len(split) == 1:
        return Node(split[0])
    root = Node(split[0])
    arguments = split[1][:-1]
    children_literals = split_literals(arguments)
    for children_literal in children_literals:
        root.children.append(build_tree(children_literal))
    return root


def build_predicate(tree):
    result = tree.val
    if len(tree.children) > 0:
        result += "("
        for i in range(len(tree.children)):
            child = tree.children[i]
            if len(tree.children) >= 2 and i != len(tree.children) - 1:
                result += build_predicate(child) + ", "
            else:
                result += build_predicate(child)
        result += ")"
    return result


def build_modeh_from_tree(tree, types):
    result = ""
    if tree.val[0].isupper():
        if tree.val in types:
            result += "var({})".format(types[tree.val])
        else:
            print("Variable {} has a unknown type.".format(tree.val))
    else:
        result += tree.val
    if len(tree.children) > 0:
        result += "("
        for i in range(len(tree.children)):
            child = tree.children[i]
            if len(tree.children) >= 2 and i != len(tree.children) - 1:
                result += build_modeh_from_tree(child, types) + ", "
            else:
                result += build_modeh_from_tree(child, types)
        result += ")"
    return result


def build_tree_from_modeh(literal):
    if literal.startswith("var(") and not literal.startswith("var_val("):
        return Variable(literal.split("var(")[1][:-1], "")
    elif literal.startswith("const("):
        return Constant(literal.split("const(")[1][:-1], "")
    else:
        split = literal.split('(', maxsplit=1)
        if len(split) == 1:
            return Node(split[0])
        root = Node(split[0])
        arguments = split[1][:-1]
        children_literals = split_literals(arguments)
        for children_literal in children_literals:
            root.children.append(build_tree_from_modeh(children_literal))
    return root

def print_tree(root):
    print(root)
    for each in root.children:
        print_tree(each)


def generate_possible_head_from_tree_help(root, inverse_dict, constant_dict, possible_head_list, replace_list, index):
    if index == len(replace_list):
        possible_head_list.append(build_predicate(root))
        return
    curr_node = replace_list[index]
    if isinstance(curr_node, Variable):
        if curr_node.type in inverse_dict:
            variable_list = inverse_dict[curr_node.type]
            for literal in variable_list:
                curr_node.val = literal
                index += 1
                generate_possible_head_from_tree_help(root, inverse_dict, constant_dict,
                                                      possible_head_list, replace_list, index)
                index -= 1
                curr_node.val = ""
        else:
            return
    else:
        if curr_node.id in constant_dict:
            constant_list = constant_dict[curr_node.id]
            for literal in constant_list:
                curr_node.val = literal
                index += 1
                generate_possible_head_from_tree_help(root, inverse_dict, constant_dict,
                                                      possible_head_list, replace_list, index)
                index -= 1
                curr_node.val = ""
        else:
            return


def generate_possible_head_from_tree(root, inverse_dict, constant_dict, possible_head_list):
    replace_list = []
    generate_replace_list(root, replace_list)
    generate_possible_head_from_tree_help(root, inverse_dict, constant_dict, possible_head_list, replace_list, 0)


def generate_replace_list(root, replace_list):
    if isinstance(root, Variable) or isinstance(root, Constant):
        replace_list.append(root)
    for child in root.children:
        generate_replace_list(child, replace_list)


def compareTrees(predicate_root, solver_root, union_variables_dict):
    if solver_root.val[0].isupper():
        if solver_root.val not in union_variables_dict:
            union_variables_dict[solver_root.val] = []
        if predicate_root.val not in union_variables_dict[solver_root.val]:
            union_variables_dict[solver_root.val].append(predicate_root.val)
    else:
        for i in range(len(predicate_root.children)):
            compareTrees(predicate_root.children[i], solver_root.children[i], union_variables_dict)
