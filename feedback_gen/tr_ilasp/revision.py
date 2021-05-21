import argparse
import subprocess

from .predicateTree import print_tree, build_tree, build_predicate, build_modeh_from_tree, build_tree_from_modeh, \
    generate_possible_head_from_tree, compareTrees
from .utils import split_literals, type_error, concat_literal, check_paren_literal, paren_error, fullstop_error, \
    variable_literals, build_inverse_dict


class revisableTheory:
    def __init__(self, head, body, types, ground_literals_set, mode_variable_rep, variable_rep, ground_literals_rep,
                 possible_head=None, union_variables_dict=None):
        self.head = head
        self.body = body
        self.types = types
        self.ground_literals_set = ground_literals_set
        self.possible_head = possible_head
        self.mode_variable_rep = mode_variable_rep
        self.variable_rep = variable_rep
        self.ground_literals_rep = ground_literals_rep
        self.union_variables_dict = {}


def parse_input():
    parser = argparse.ArgumentParser(description="Revisable Program")
    parser.add_argument('--solver', nargs=1)
    parser.add_argument('--revise-type', nargs=1)
    parser.add_argument('--max-head', nargs=1)
    parser.add_argument('--nc', action='store_true')
    parser.add_argument('file_name', type=str, help='File name')
    return parser.parse_args()


def read_file(input_file):
    lines = []
    for line in input_file:
        lines.append(line)
    return lines


def write_to_workfile(lines):
    workfile = open("workfile.las", "w")
    revisable_theory = []
    possible_head_list = []
    disjunct_modeh_general, disjunct_modeh_rule, constant_str = [], [], []
    complete_line = True
    curr_line = ""
    for line in lines:
        if revise_type == "disjunctive":
            if line.startswith("#modeh"):
                disjunct_modeh_general.append(line)
                continue
            elif line.startswith("#constant"):
                constant_str.append(line)
                workfile.write(line)
                continue

        if not complete_line or line.startswith("#revisable") or line.startswith("#possible_head") \
                or line.startswith("possible_head_modeh"):
            complete_line = False
            curr_line += line.strip()
        else:
            workfile.write(line)
        if (line.endswith(".\n") or line.endswith(".")) and not complete_line:
            if curr_line.startswith("#revisable"):
                revisable_theory.append(curr_line)
            elif curr_line.startswith("possible_head"):
                possible_head_list.append(curr_line)
            else:
                disjunct_modeh_rule.append(curr_line)
            curr_line = ""
            complete_line = True
    if not complete_line:
        print("Parsing Error: Revisable theory doesn't end with '.', current parsing theory: {}".format(curr_line))
        print("Terminating...")
        exit()
    return workfile, revisable_theory, possible_head_list, disjunct_modeh_general, disjunct_modeh_rule, constant_str


def split_rule(rule):
    rule = rule.strip()

    if rule[0] != '(' or rule[-1] != ')':
        paren_error(rule)
    if rule[-2] != '.':
        fullstop_error(rule)

    rule = rule[1:-2]
    split = rule.split(":-")

    if len(split) != 2:
        print("Wrong format for rule {}".format(rule))
        exit()

    head = split[0].strip()
    head_dict = {}
    head_list = split_literals(head, deliminator=';')
    for predicate in head_list:
        head_dict[concat_literal(predicate)] = build_tree(predicate)

    check_paren_literal(head, rule)

    body_raw = split[1].strip()
    body_split = split_literals(body_raw)

    body_dict = {}
    for body_literal in body_split:
        body_literal = body_literal.strip()
        check_paren_literal(body_literal, rule)
        body_dict[concat_literal(body_literal)] = build_tree(body_literal)

    return head_dict, body_dict


def split_types(types, rule_and_type):
    types = types.strip()

    if types[0] != '(' or types[-1] != ')':
        type_error(types, rule_and_type)
    types = types[1:-1]

    type_dict = {}
    types_split = types.split(",")
    for type in types_split:
        type = type.strip()

        split = type.split(":")
        if len(split) != 2:
            type_error(type, rule_and_type)

        for i in range(len(split)):
            split[i] = split[i].strip()

        type_dict[split[0]] = split[1]

    return type_dict


def check_paren_and_split(rule_and_type):
    if rule_and_type[0] != '(' or rule_and_type[-2] != ')':
        paren_error(rule_and_type)

    rule_and_type = rule_and_type[1:-2]
    split = split_literals(rule_and_type)

    if len(split) != 3 and len(split) != 2:
        paren_error(rule_and_type)

    if len(split) < 2:
        print("Insufficient arguments! Expected: revision name, revision theory, types")
        exit()

    head_dict, body_dict = split_rule(split[1])

    type_dict = {}
    if len(split) == 3:
        type_dict = split_types(split[2], rule_and_type)

    return split[0], head_dict, body_dict, type_dict

# added by jx
def filter_possible_head(head):
    split = head.split('var_vals(')
    variables = []
    
    for each in split:
        if 'var_val' in each:
            variable = [x for x in each if x.isupper()]
            variables += variable
        
    return variables == sorted(variables) and len(variables) == len(set(variables))

def parse_revisable_theories(revisable_theory_str, possible_head_list, disjunct_modeh_general, disjunct_modeh_rule,
                             constant_str):
    revisable_theories = {}

    # Build constant dictionary
    constant_dict = {}
    for line in constant_str:
        line = line.strip()
        split = line.split("#constant(")[1].split(',')
        head = split[0]
        tail = split[1].split(')')[0].strip()
        if head not in constant_dict:
            constant_dict[head] = []
        constant_dict[head].append(tail)

    for string in revisable_theory_str:
        rule_and_type = string.lstrip('#revisable')
        revision_id, head_dict, body_dict, type_dict = check_paren_and_split(rule_and_type)

        ground_literals_set = set()
        for type in type_dict.values():
            ground_literals_set.add(type)

        variable_rep = "v("
        if type_dict:
            for variable in type_dict:
                variable_rep += variable + ", "
            variable_rep = variable_rep[:-2]
        else:
            variable_rep += "null"

        variable_rep += ")"

        mode_variable_rep = "v("
        if type_dict:
            for type in type_dict.values():
                mode_variable_rep += "var(" + type + "), "
            mode_variable_rep = mode_variable_rep[:-2]
        else:
            mode_variable_rep += "null"

        mode_variable_rep += ")"

        ground_literals_rep = ""
        for variable, type in type_dict.items():
            ground_literals_rep += " " + type + "(" + variable + "),"
        ground_literals_rep = ground_literals_rep[1:-1]

        # Build modeh tree and propagate variable for disjunctive mode
        possible_head = {}
        if revise_type == "disjunctive":
            for modeh in disjunct_modeh_general:
                root = build_tree_from_modeh(modeh.split("#modeh(")[1].strip()[:-2])
                # print_tree(root)
                inverse_dict = build_inverse_dict(type_dict)
                # print(type_dict)
                possible_head_raw = []
                generate_possible_head_from_tree(root, inverse_dict, constant_dict, possible_head_raw)
                # print(possible_head_raw)
                for literal in possible_head_raw:
                    # modified by jx
                    if filter_possible_head(literal):
                        possible_head[concat_literal(literal)] = build_tree(literal)

        rv = revisableTheory(head=head_dict, body=body_dict, types=type_dict, ground_literals_set=ground_literals_set,
                             variable_rep=variable_rep, mode_variable_rep=mode_variable_rep,
                             ground_literals_rep=ground_literals_rep, possible_head=possible_head)
        revisable_theories[revision_id] = rv

    # Possible Head rule-specific modeh Generation
    for rule in disjunct_modeh_rule:
        revid_and_head = rule.lstrip('#possible_head_modeh')
        if revid_and_head[0] != '(' or revid_and_head[-2] != ')':
            paren_error(revid_and_head)
        revid_and_head = revid_and_head.strip()[1:-2]
        split = revid_and_head.split(",", maxsplit=1)
        revid = split[0]
        theory = revisable_theories[revid]
        possible_head = split[1].strip()[1:-1]
        possible_head_modeh = split_literals(possible_head)
        if not theory:
            print("Cannot find revisable id in rule {}".format(rule))
            exit()
        for modeh in possible_head_modeh:
            root = build_tree_from_modeh(modeh)
            inverse_dict = build_inverse_dict(theory.types)
            possible_head_raw = []
            generate_possible_head_from_tree(root, inverse_dict, constant_dict, possible_head_raw)
            for literal in possible_head_raw:
                theory.possible_head[concat_literal(literal)] = build_tree(literal)

    # Possible Head Generation
    for string in possible_head_list:
        revid_and_head = string.lstrip('#possible_head')
        if revid_and_head[0] != '(' or revid_and_head[-2] != ')':
            paren_error(revid_and_head)
        revid_and_head = revid_and_head.strip()[1:-2]
        split = revid_and_head.split(",", maxsplit=1)
        revid = split[0]
        possible_head = split[1].strip()[1:-1]
        possible_head_literals = split_literals(possible_head)

        theory = revisable_theories[revid]
        if not theory:
            print("Cannot find revisable id in rule {}".format(string))
            exit()

        for literal in possible_head_literals:
            theory.possible_head[concat_literal(literal)] = build_tree(literal)

    return revisable_theories


def deletion_rule_generation(revisable_theories, output_file):
    output_file.write("%Deletion rules\n\n")
    output_file.write("#modeh(delete(const(revid_type), const(id_type))).\n")

    if solver == "ILASP":
        for revid, theory in revisable_theories.items():
            output_file.write("#constant(revid_type, {}).\n".format(revid))
            for identifier in theory.body:
                output_file.write("#constant(id_type, {}).\n".format(identifier))

        output_file.write("\n")
        output_file.write("#bias(\":- head(delete(_, _)), body(_).\").\n\n")
    else:
        for revid, theory in revisable_theories.items():
            output_file.write("revid_type({}).\n".format(revid))
            for identifier in theory.body:
                output_file.write("id_type({}).\n".format(identifier))

        output_file.write("\n")
        output_file.write("#bias(\":- in_head(delete(_, _)), in_body(_).\").\n\n")


def extension_rule_generation(revisable_theories, output_file):
    output_file.write("%Extension rules and mode declaration\n\n")

    for revid, theory in revisable_theories.items():
        mode = "#modeh(extension({}, {})).\n".format(revid, theory.mode_variable_rep)
        output_file.write(mode)

        """
        if solver == "ILASP":
            output_file.write("0 ~ extension({}, {}) :- {}.\n"
                              .format(revid, theory.variable_rep, theory.ground_literals_rep))
        """


def delete_literal(revid, iden):
    return "delete({}, {})".format(revid, iden)


class literal_wrap:
    def __init__(self, try_literals, extend_literals):
        self.try_literals = try_literals
        self.extend_literals = extend_literals


def possible_head_generate(id2literal, revisable_theories, output_file):
    possible_head_rules, no_constraint_rules, max_head_rules, max_head_choice_rules = [], [], [], []
    empty_head_rules = []
    for revid, theory in revisable_theories.items():
        try_literals = id2literal[revid].try_literals
        extend_literals = id2literal[revid].extend_literals
        max_head_is_heads, possible_heads = [], []
        head_deletes, head_extensions = [], []

        if theory.head:
            for head_id, head_tree in theory.head.items():
                rule_head = "possible_head({}, {}, {})".format(revid, theory.variable_rep, build_predicate(head_tree))
                rule = "{} :-\n".format(rule_head)
                head_delete = "head_delete({}, {})".format(revid, head_id)
                rule += "\tnot {},\n".format(head_delete)
                rule = try_and_extend_literals_generation(extend_literals, rule, try_literals)

                possible_head_rules.append(rule)
                possible_heads.append(rule_head)
                head_deletes.append(head_delete)

                # For max head
                is_head = "is_head({}, {})".format(revid, head_id)
                max_head_is_heads.append(is_head)
                max_head_rules.append("{} :- {}.\n".format(is_head, rule_head))

        if theory.possible_head:
            for possible_head_id, possible_head_literal in theory.possible_head.items():
                rule_head = "possible_head({}, {}, {})" \
                    .format(revid, theory.variable_rep, build_predicate(possible_head_literal))
                rule = "{} :-\n".format(rule_head)
                head_extension = "head_extension({}, {}, {})" \
                    .format(revid, possible_head_id, build_predicate(possible_head_literal))
                rule += "\t{},\n".format(head_extension)
                # modified by jx
                for each in head_deletes:
                    rule += "\t{},\n".format(each)
                rule = try_and_extend_literals_generation(extend_literals, rule, try_literals)

                possible_head_rules.append(rule)
                possible_heads.append(rule_head)
                head_extensions.append(head_extension)

                # For max head
                is_head = "is_head({}, {})".format(revid, possible_head_id)
                max_head_is_heads.append(is_head)
                max_head_rules.append("{} :- {}.\n".format(is_head, rule_head))

        # empty_head generation
        empty_head = "empty_head({})".format(revid)
        rule = "{} :-\n".format(empty_head)
        rule_body = ""
        for head_delete in head_deletes:
            rule_body += "\t{},\n".format(head_delete)
        for head_extension in head_extensions:
            rule_body += "\tnot {},\n".format(head_extension)
        rule += rule_body + "\t" + theory.ground_literals_rep + ".\n\n"
        empty_head_rules.append(rule)

        rule = ":- {},\n".format(empty_head)
        # modified by jx
        rule = try_and_extend_literals_generation(extend_literals, rule, try_literals, True)
        empty_head_rules.append(rule)

        # Empty possible_head generation
        possible_head = "possible_head({}, {}, null)".format(revid, theory.variable_rep)
        possible_head_rules.append(
            "{} :-\n\t{},\n\t{}.\n\n".format(possible_head, empty_head, theory.ground_literals_rep))
        rule = "{} :-\n\tnot {},\n".format(possible_head, empty_head)
        for literal in possible_heads:
            rule += "\tnot {},\n".format(literal)
        rule += "\t" + theory.ground_literals_rep + ".\n\n"
        possible_head_rules.append(rule)

        rule = ":- not {},\n".format(empty_head)
        rule += "\tpossible_head({}, {}, null):".format(revid, theory.variable_rep)

        # Constraint about empty_head and possible_head
        rule = ":- not {},\n\t{}: {}.\n\n".format(empty_head, possible_head, theory.ground_literals_rep)
        empty_head_rules.append(rule)

        if no_constraint:
            no_constraint_rules.append(":- {}.\n\n".format(empty_head))

        if max_head != -1:
            max_head_choice = "0 {"
            for literal in max_head_is_heads:
                max_head_choice += literal + "; "
            max_head_choice = max_head_choice[:-2] + "}}{}.\n\n".format(str(max_head))
            max_head_choice_rules.append(max_head_choice)

    for rule in possible_head_rules:
        output_file.write(rule)

    for rule in empty_head_rules:
        output_file.write(rule)

    if no_constraint:
        output_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        for rule in no_constraint_rules:
            output_file.write(rule)

    if max_head != -1:
        output_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        for rule in max_head_rules:
            output_file.write(rule)
        for rule in max_head_choice_rules:
            output_file.write(rule)

# modified by jx: custom=True to allow deletion of rules
def try_and_extend_literals_generation(extend_literals, rule, try_literals, custom=False):
    for try_literal in try_literals:
        try_literal = try_literal.replace('try', 'delete').replace(', ground(X)', '') if custom else try_literal
        rule += "\t{},\n".format(try_literal)
    for extend_literal in extend_literals:
        rule += "\t{},\n".format(extend_literal)
    rule = rule[:-2] + ".\n\n"
    return rule


def try_rule_generation(revisable_theories, output_file):
    output_file.write("%Try and extension rules\n\n")
    main_rules, try_rules, tried_rules, negate_trieds, negate_extendeds, extended_rules = [], [], [], [], [], []
    id2literal = {}
    for revid, theory in revisable_theories.items():
        lw = literal_wrap([], [])
        head_expansion = ""
        for head_tree in theory.head.values():
            head_expansion += build_predicate(head_tree) + "; "
        head_expansion = head_expansion[:-2] + ":-\n"
        for iden, literal in theory.body.items():
            variables = variable_literals(literal, theory)
            try_literal = "try({}, {}, {})".format(revid, iden, build_predicate(literal))
            lw.try_literals.append(try_literal)

            delete = delete_literal(str(revid), iden)
            try_delete_rule = "{} :- \n\t{}".format(try_literal, delete)
            try_not_delete_rule = "{} :- \n\t{},\n\tnot {}".format(try_literal, build_predicate(literal), delete,
                                                                   variables)

            if variables:
                try_delete_rule += ",\n\t{}\n\n".format(variables)
                try_not_delete_rule += ",\n\t{}\n\n".format(variables)
            else:
                try_delete_rule += ".\n\n"
                try_not_delete_rule += ".\n\n"

            try_rules.append(try_delete_rule)
            try_rules.append(try_not_delete_rule)

            head_expansion += "\t" + try_literal + ",\n"

            # Tried rules
            tried_head = "tried({}, {})".format(revid, iden)
            tried_literal = tried_head + " :- \n\t{}".format(try_literal)
            if variables:
                tried_literal += ",\n\t{}\n\n".format(variables)
            else:
                tried_literal += ".\n\n"

            negate_tried = ":- not {}.\n\n".format(tried_head)
            tried_rules.append(tried_literal)
            negate_trieds.append(negate_tried)

        extend_literal = "\textension({}, {})".format(revid, theory.variable_rep)
        lw.extend_literals.append(extend_literal[1:])

        head_expansion += extend_literal

        main_rules.append(head_expansion + ".\n\n")

        # Extended Rule
        negate_extended = ":- not extended({}).\n\n".format(revid)
        extended_literal = "extended({}) :- \n\t{},\n".format(revid, extend_literal[1:])
        if theory.ground_literals_rep == "":
            extended_literal = extended_literal[:-2] + ".\n\n"
        else:
            extended_literal += "\t" + theory.ground_literals_rep + ".\n\n"
        negate_extendeds.append(negate_extended)
        extended_rules.append(extended_literal)

        id2literal[revid] = lw

    # Printing out results to output file
    if revise_type == "body":
        for rule in main_rules:
            output_file.write(rule)
    else:
        possible_head_generate(id2literal, revisable_theories, output_file)
        output_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

    for rule in try_rules:
        output_file.write(rule)

    for rule in tried_rules:
        output_file.write(rule)

    for rule in extended_rules:
        output_file.write(rule)

    for rule in negate_trieds:
        output_file.write(rule)

    for rule in negate_extendeds:
        output_file.write(rule)


def head_delete_rule_generation(revisable_theories, output_file):
    output_file.write("#modeh(head_delete(const(revid_type), const(hid_type))).\n")
    variable_set = set()
    for theory in revisable_theories.values():
        if theory.head:
            for head_literal in theory.head:
                if head_literal not in variable_set:
                    if solver == "ILASP":
                        output_file.write("#constant(hid_type, {}).\n".format(head_literal))
                    else:
                        output_file.write("hid_type({}).\n".format(head_literal))
                    variable_set.add(head_literal)


def head_extension_rule_generation(revisable_theories, output_file):
    buffer, constant_buffer = [], set()
    for revid, theory in revisable_theories.items():
        for possible_head_id, possible_head_tree in theory.possible_head.items():
            possible_head_modeh = build_modeh_from_tree(possible_head_tree, theory.types)
            constant_buffer.add("#constant(head_extension_type, {}).\n".format(possible_head_id))
            if possible_head_modeh not in buffer:
                output_file.write("#modeh(head_extension({}, const(head_extension_type), {})).\n"
                                  .format(revid, possible_head_modeh))
                buffer.append(possible_head_modeh)
    for constant in constant_buffer:
        output_file.write(constant)
    """
    if solver == "ILASP":
        for revid, theory in revisable_theories.items():
            if theory.possible_head:
                for possible_head_literal in theory.possible_head.values():
                    rule = "1 ~ head_extension({}, {}, {}) :- ".format(revid, theory.variable_rep, possible_head_literal)
                    rule += theory.ground_literals_rep + ".\n"
                    output_file.write(rule)
            output_file.write("\n")
    
    for revid, theory in revisable_theories.items():
        if theory.possible_head:
            for possible_head_literal in theory.possible_head.values():
                split = possible_head_literal.split("(", maxsplit=1)
                modeh_head_literal = split[0]
                if len(split) == 2:
                    modeh_head_literal += "("
                    variables = split[1][:-1]
                    variable_list = split_literals(variables)
                    for v in variable_list:
                        if v[0].islower():
                            modeh_head_literal += v
                        else:
                            if v in theory.types:
                                modeh_head_literal += "var({})".format(theory.types[v])
                            else:
                                print(
                                    "Variable {} in rule {} is not in revisable type.".format(v, possible_head_literal))
                                print("Exiting program...")
                                exit()
                        modeh_head_literal += ", "
                    modeh_head_literal = modeh_head_literal[:-2] + ")"
                output_file.write("#modeh(head_extension({}, {})).\n"
                                  .format(revid, modeh_head_literal))
    """


def prove_rule_generation(revisable_theories, output_file):
    output_file.write("prove(X) : possible_head(R, V, X) :- extension(R, V).\n")
    for theory in revisable_theories.values():
        if theory.head:
            for head_tree in theory.head.values():
                head_literal = build_predicate(head_tree)
                output_file.write("{} :- prove({}).\n".format(head_literal, head_literal))
        if theory.possible_head:
            for possible_head_tree in theory.possible_head.values():
                possible_head_literal = build_predicate(possible_head_tree)
                output_file.write("{} :- prove({}).\n".format(possible_head_literal, possible_head_literal))
    output_file.write("\n")


def generate_revision(revisable_theories, output_file):
    output_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    deletion_rule_generation(revisable_theories, output_file)
    output_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    extension_rule_generation(revisable_theories, output_file)
    output_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

    if revise_type == "disjunctive":
        output_file.write("%Mode for revising heads\n")
        head_delete_rule_generation(revisable_theories, output_file)
        output_file.write("\n")
        head_extension_rule_generation(revisable_theories, output_file)
        output_file.write("\n")
        if solver == "ILASP":
            output_file.write("#bias(\":- head(head_delete(_, _)), body(_).\").\n")
            output_file.write("#bias(\":- head(head_extension(_, _, _)), body(_).\").\n")
        else:
            output_file.write("#bias(\":- in_head(head_delete(_, _)), in_body(_).\").\n")
            output_file.write("#bias(\":- in_head(head_extension(_, _, _)), in_body(_).\").\n")
        output_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

        prove_rule_generation(revisable_theories, output_file)

    try_rule_generation(revisable_theories, output_file)


def delete_revision(delete_list, revisable_theories):
    for line in delete_list:
        line = line.lstrip("delete(")[:-3]
        split = split_literals(line)
        revid = split[0].strip()
        literal_key = split[1].strip()
        theory = revisable_theories[revid]
        theory.body.pop(literal_key)


def replace_variables(root, variable_dict, theory):
    global arbitrary_index
    if root.val[0].isupper():
        if root.val in variable_dict:
            root.val = variable_dict[root.val][0]
        else:
            arb_term = "Arb" + str(arbitrary_index)
            #theory.types[arb_term] = theory.type_dict[root.val]
            root.val = arb_term
            arbitrary_index += 1
    else:
        for child in root.children:
            replace_variables(child, variable_dict, theory)


def extend_revision(extend_list, revisable_theories):
    for line in extend_list:
        line = line[:-1]
        split = line.split(":-")

        if len(split) == 1:
            return

        head = split[0].strip()
        head = head.lstrip("extension(")[:-1]
        head_argument_split = split_literals(head)
        revid = head_argument_split[0]
        theory = revisable_theories[revid]

        variable_set = set()
        for head_tree in theory.head.values():
            variable_set = variable_set.union(extract_variables(head_tree))

        for body_tree in theory.body.values():
            variable_set = variable_set.union(extract_variables(body_tree))

        head_argument_split = head_argument_split[1].strip()
        variable_dict = generate_variable_dict(head_argument_split, theory)

        body = split[1].strip()[:-1]
        body_literals = split_literals(body, deliminator=';')
        for literal in body_literals:
            literal = literal.strip()
            literal_tree = build_tree(literal)
            replace_variables(literal_tree, variable_dict, theory)
            replaced_literal = build_predicate(literal_tree)

            if literal.split("(")[0].strip() in theory.ground_literals_set:
                continue

            theory.body[concat_literal(replaced_literal)] = literal_tree

            """
            flag = False
            for var in literal_variable_set:
                if var in variable_set:
                    flag = True

            if flag:
                theory.body[concat_literal(replaced_literal)] = literal_tree
            """


def generate_variable_dict(variables, theory):
    variable_dict = theory.union_variables_dict
    variables = variables.lstrip("v(")[:-1]
    variables = variables.split(",")
    count = 0
    for variable in theory.types:
        solver_variable = variables[count].strip()
        if solver_variable not in variable_dict:
            variable_dict[solver_variable] = []
        variable_dict[solver_variable].append(variable)
        count += 1
    return variable_dict


def extract_variables(root):
    result = set()
    extract_variables_help(root, result)
    return result


def extract_variables_help(root, result):
    if root.val[0].isupper():
        result.add(root.val)
    else:
        for child in root.children:
            extract_variables_help(child, result)


def ground_theories(revisable_theories):
    for theory in revisable_theories.values():
        if not theory.body:
            for variable, type in theory.types.items():
                theory.body[type + "_" + variable] = type + "(" + variable + ")"


def head_delete_revision(head_delete_list, revisable_theories):
    for line in head_delete_list:
        line = line.lstrip("head_delete(")[:-3]
        split = split_literals(line)
        revid = split[0].strip()
        literal_key = split[1].strip()
        theory = revisable_theories[revid]
        theory.head.pop(literal_key)


def head_extension_revision(head_extension_list, revisable_theories):
    for line in head_extension_list:
        split = line.split(":-")
        body = split[1].strip()[:-1]
        line = split[0].strip()
        line = line.lstrip("head_extension(")
        if line[-1] == '.':
            line = line[:-2]
        else:
            line = line[:-1]
        split = split_literals(line)
        revid = split[0].strip()
        predicate_id = split[1].strip()
        solver_literal = split[2].strip()
        theory = revisable_theories[revid]
        predicate_tree = theory.possible_head[predicate_id]
        solver_tree = build_tree(solver_literal)
        union_variables_dict = theory.union_variables_dict
        # modified by jx
        # print('in predicate_tree', predicate_tree.children[3].children[0].children[2])
        # print('in solver_tree', solver_tree.children[3].children[0].children[2])
        # print('in predicate_tree', predicate_tree.children[3].children[1].children[0].children[2])
        # print('in solver_tree', solver_tree.children[3].children[1].children[0].children[2])
        # print(union_variables_dict)
        # compareTrees(predicate_tree, solver_tree, union_variables_dict)
        # print(union_variables_dict)
        theory.head[predicate_id] = predicate_tree


def generate_solver_type_dict(body_literals):
    type_dict = {}
    for literal in body_literals:
        split = literal.split("(")
        if len(split) == 2:
            type, variable = split[0], split[1][:-1]
            type_dict[variable] = type
    return type_dict


def revise(solver_result, revisable_theories):
    revise_list = []
    for line in solver_result:
        if len(line) > 1:
            revise_list.append(line)

    delete_list = []
    extend_list = []
    head_delete_list = []
    head_extension_list = []
    for line in revise_list:
        if line.startswith("delete"):
            delete_list.append(line)
        elif line.startswith("extension"):
            extend_list.append(line)
        elif line.startswith("head_delete"):
            head_delete_list.append(line)
        else:
            head_extension_list.append(line)

    delete_revision(delete_list, revisable_theories)
    extend_revision(extend_list, revisable_theories)

    if revise_type == "disjunctive":
        head_delete_revision(head_delete_list, revisable_theories)
        head_extension_revision(head_extension_list, revisable_theories)

    ground_theories(revisable_theories)


def generate_ground_terms(variable_set, theory):
    result = ""
    for variable in variable_set:
        result += "{}({}), ".format(theory.types[variable], variable)
    return result[:-2]


def print_result(revisable_theories):
    print("Revised theories are:\n")
    variable_set = set()
    for theory in revisable_theories.values():
        buffer = ""
        for h in theory.head.values():
            buffer += "{}; ".format(build_predicate(h))
            variable_set = variable_set.union(extract_variables(h))
        buffer = buffer[:-2] + " :-\n"
        for b in theory.body.values():
            predicate = build_predicate(b)
            buffer += "\t{},\n".format(predicate)
            if not predicate.startswith("not"):
                variable_set = variable_set.difference(extract_variables(b))

        ground_terms = generate_ground_terms(variable_set, theory)

        if ground_terms == "":
            buffer = buffer[:-2] + ",\n\t"
        else:
            buffer += "\t" + ground_terms + ",\n\t"

        union_variable_dict = theory.union_variables_dict
        duplicate_equal_set = set()
        for list in union_variable_dict.values():
            if len(list) <= 1:
                continue
            first = list[0]
            for i in range(1, len(list)):
                equals_string = "{} = {}".format(first, list[i])
                if equals_string not in duplicate_equal_set:
                    buffer += equals_string + ", "
                duplicate_equal_set.add(equals_string)
                duplicate_equal_set.add("{} = {}".format(list[i], first))

        if buffer.strip()[-1] == ',':
            buffer = buffer.strip()[:-1] + "."
        print(buffer)

# modified by jx
def revise_program(file_name):
    global solver
    global arbitrary_index
    global revise_type
    global max_head
    global no_constraint
    
    solver = 'ILASP'
    arbitrary_index = 1
    revise_type = 'disjunctive'
    max_head = -1
    no_constraint = None
    
    try:
        input_file = open(file_name, "r")
    except IOError:
        print("The file does not exist!")
        print("Terminating...")
        exit()
    lines = read_file(input_file)
    output_file, revisable_theory_str, possible_head_list, disjunct_modeh_general, disjunct_modeh_rule, constant_str = \
        write_to_workfile(lines)

    # Parsing revision rule
    revisable_theories = parse_revisable_theories(revisable_theory_str, possible_head_list, disjunct_modeh_general,
                                                  disjunct_modeh_rule, constant_str)
    # Generate extension and deletion
    generate_revision(revisable_theories, output_file)
    
    input_file.close()
    output_file.close()

    # solver
    print("Running solver...")
    temp_file_name = "temp.txt"

    subprocess.call("rm " + temp_file_name, shell=True)

    version = 4
    subprocess.call(solver + " --version=" + str(version) + " --strict-types -q workfile.las > " + temp_file_name,
                        shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    temp_file = open(temp_file_name, "r")
    solver_result = read_file(temp_file)
    if len(solver_result) == 0 or solver_result[0].startswith("UNSATISFIABLE"):
        print("The theory is unsatisfiable\nExiting...")
        return None
    temp_file.close()

    # Revise according to solver result
    revise(solver_result, revisable_theories)
    
    # Print result
    print_result(revisable_theories)
    
    return revisable_theories

def main():
    global solver
    global arbitrary_index
    global revise_type
    global max_head
    global no_constraint

    arbitrary_index = 1

    args = parse_input()

    if args.solver:
        if args.solver[0] == "ILASP" or args.solver[0] == "FastLAS":
            solver = args.solver[0]
        else:
            print("Incorrect solver type!")
            exit()
    else:
        solver = "ILASP"

    revise_set = {"body", "disjunctive"}
    if args.revise_type:
        if args.revise_type[0] in revise_set:
            revise_type = args.revise_type[0]
        else:
            print("Incorrect revise type!")
            exit()
    else:
        revise_type = "body"

    if revise_type == "full" and solver == "FastLAS":
        print("FastLAS does not support head revision currently, terminating...")
        exit()

    if args.max_head and revise_type == "disjunctive":
        max_head = args.max_head[0]
    else:
        max_head = -1

    no_constraint = args.nc
    if no_constraint and revise_type == "body":
        print("Warning: Revise type body only cannot be used with constraint learning")

    try:
        input_file = open(args.file_name, "r")
    except IOError:
        print("The file does not exist!")
        print("Terminating...")
        exit()
    lines = read_file(input_file)
    output_file, revisable_theory_str, possible_head_list, disjunct_modeh_general, disjunct_modeh_rule, constant_str = \
        write_to_workfile(lines)

    # Parsing revision rule
    revisable_theories = parse_revisable_theories(revisable_theory_str, possible_head_list, disjunct_modeh_general,
                                                  disjunct_modeh_rule, constant_str)
    # Generate extension and deletion
    generate_revision(revisable_theories, output_file)
    
    input_file.close()
    output_file.close()

    # solver
    print("Running solver...")
    temp_file_name = "temp.txt"

    subprocess.call("rm " + temp_file_name, shell=True)

    if solver == "ILASP":
        version = 4
        subprocess.call(solver + " --version=" + str(version) + " --strict-types -q workfile.las > " + temp_file_name,
                        shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.call(solver + " --fl2 workfile.las > " + temp_file_name, shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    temp_file = open(temp_file_name, "r")
    solver_result = read_file(temp_file)
    if len(solver_result) == 0 or solver_result[0].startswith("UNSATISFIABLE"):
        print("The theory is unsatisfiable\nExiting...")
        exit()
    temp_file.close()

    # Revise according to solver result
    revise(solver_result, revisable_theories)
    
    # modified by jx
    # print(revisable_theories['rev1'].head)
    # print(revisable_theories['rev1'].body)
    # print(revisable_theories['rev1'].types)
    # print(revisable_theories['rev1'].ground_literals_set)
    # print(revisable_theories['rev1'].possible_head)
    # print(revisable_theories['rev1'].mode_variable_rep)
    # print(revisable_theories['rev1'].variable_rep)
    # print(revisable_theories['rev1'].ground_literals_rep)
    # print(revisable_theories['rev1'].union_variables_dict)
    # Print result
    print_result(revisable_theories)

    return revisable_theories


if __name__ == "__main__":
    main()
