import sys
import itertools
from metarep_encoder.classes import *
from metarep_encoder.parser import *
from metarep_encoder.helper import *

def generateBLRules():
    # body literals
    bl_pbl_rule = Rule([Literal_bl('R', 'P', 'X')], [Literal_pbl('R', 'P', 'X', 'VARS')])
    bl_nbl_rule = Rule([Literal_bl('R', 'P', 'X')], [Literal_nbl('R', 'P', 'X', 'VARS')])

    return [bl_pbl_rule, bl_nbl_rule]

    
def generateVarValRules():
    # var_vals
    var_val_rule = Rule([Literal_var_val('R', 'V', 'T')], [Literal_rule('R'), Literal_variable('V'), Literal_ground('T')])
    is_var_val_rule = Rule([Literal_is_var_val(Literal_var_val('R', 'V', 'T'))], [Literal_rule('R'), Literal_variable('V'), Literal_ground('T')])
    var_val_equal_rule = Rule([Literal_var_val_equal('VVX', 'VVY')], [Literal_is_var_val('VVX'), Literal_is_var_val('VVY'), EqualsLiteral('VVX', Literal_var_val('R', 'V', 'T'), True), EqualsLiteral('VVY', Literal_var_val('R', 'V', 'T'), True)])
    valid_var_val_rule = Rule([Literal_valid_var_val('RULE_NO', Literal_var_val('R', 'V', 'T'), 'VAR')], [Literal_variable('VAR'), Literal_rule('R'), EqualsLiteral('R', 'RULE_NO', True), EqualsLiteral('V', 'VAR', True), Literal_ground('T')])
    
    return [var_val_rule, is_var_val_rule, var_val_equal_rule, valid_var_val_rule]
    
def generateSubsetRules():
    # length
    length_base_rule = Rule([Literal_length('R', 'end', '0', 'MAX', 'end')], [Literal_var_max('MAX'), Literal_rule('R')])
    length_recursive_rule = Rule([Literal_length('R', Literal_var_vals('VV', 'VVS'), 'N', 'MAX', Literal_variables('V', 'VS'))], [Literal_valid_var_val('R', 'VV', 'V'), Literal_length('R', 'VVS', 'N - 1', 'MAX', 'VS'), Literal_var_max('MAX'), LTLiteral('N', 'MAX', True)])
    defined_length_base_rule = Rule([Literal_defined_length('R', 'end', '0')], [Literal_rule('R')])
    defined_length_recursive_rule = Rule([Literal_defined_length('R', 'VVS', 'N')], [Literal_variable_list('VS'), Literal_length('R', 'VVS', 'N', 'MAX', 'VS'), Literal_var_num('N'), Literal_var_num('MAX')])
    check_sets_length_rule = Rule([Literal_check_sets_length('R', 'VVXS', 'VVYS')], [Literal_defined_length('R', 'VVXS', 'NX'), Literal_defined_length('R', 'VVYS', 'NY'), Literal_var_num('NX'), Literal_var_num('NY'), LELiteral('NX', 'NY', True)])
    
    # is_subset
    is_subset_helper_base_rule = Rule([Literal_is_subset_helper('R', 'end', 'VVYS')], [Literal_defined_length('R', 'VVYS', '_')])
    is_subset_helper_recursive_rule_1 = Rule([Literal_is_subset_helper('R', Literal_var_vals('VVX', 'VVXS'), Literal_var_vals('VVY', 'VVYS'))], [Literal_check_sets_length('R', Literal_var_vals('VVX', 'VVXS'), Literal_var_vals('VVY', 'VVYS')), Literal_var_val_equal('VVX', 'VVY'), Literal_is_subset_helper('R', 'VVXS', 'VVYS')])
    is_subset_helper_recursive_rule_2 = Rule([Literal_is_subset_helper('R', Literal_var_vals('VVX', 'VVXS'), Literal_var_vals('VVY', 'VVYS'))], [Literal_check_sets_length('R', Literal_var_vals('VVX', 'VVXS'), Literal_var_vals('VVY', 'VVYS')), NotLiteral(Literal_var_val_equal('VVX', 'VVY')), Literal_is_subset_helper('R', Literal_var_vals('VVX', 'VVXS'), 'VVYS')])
    is_subset_pbl_rule = Rule([Literal_is_subset('R', 'VVXS', 'VVYS')], [Literal_pbl('R', 'PX', 'X', 'VVXS'), Literal_head('R', 'Y', 'VVYS'), Literal_is_subset_helper('R', 'VVXS', 'VVYS')])
    is_subset_nbl_rule = Rule([Literal_is_subset('R', 'VVXS', 'VVYS')], [Literal_nbl('R', 'PX', 'X', 'VVXS'), Literal_head('R', 'Y', 'VVYS'), Literal_is_subset_helper('R', 'VVXS', 'VVYS')])    

    return [length_base_rule, length_recursive_rule, defined_length_base_rule, defined_length_recursive_rule, check_sets_length_rule, is_subset_helper_base_rule, is_subset_helper_recursive_rule_1, is_subset_helper_recursive_rule_2, is_subset_pbl_rule, is_subset_nbl_rule]
    
def generateSeenOrderingRules():
    rule_not_first_rule = Rule([Literal_rule_not_first('R')], [Literal_order('R_OTHER', 'R'), Literal_rule('R'), Literal_rule('R_OTHER')])
    rule_seen_rule_1 = Rule([Literal_seen_rule('R')], [NotLiteral(Literal_rule_not_first('R')), Literal_rule('R'), Literal_in_AS('X', 'R', 'VVXS'), Literal_head('R', 'X', 'VVXS')])
    rule_seen_rule_2 = Rule([Literal_seen_rule('R')], [NotLiteral(Literal_rule_not_first('R')), Literal_rule('R'), NotLiteral(Literal_in_AS('X', 'R', 'VVXS')), Literal_head('R', 'X', 'VVXS')])
    rule_seen_rule_3 = Rule([Literal_seen_rule('R')], [Literal_seen_rule('R_PREV'), Literal_order('R_PREV', 'R'), Literal_rule('R'), Literal_rule('R_PREV'), Literal_in_AS('X', 'R', 'VVXS'), Literal_head('R', 'X', 'VVXS')])
    rule_seen_rule_4 = Rule([Literal_seen_rule('R')], [Literal_seen_rule('R_PREV'), Literal_order('R_PREV', 'R'), Literal_rule('R'), Literal_rule('R_PREV'), NotLiteral(Literal_in_AS('X', 'R', 'VVXS')), Literal_head('R', 'X', 'VVXS')])

    return [rule_not_first_rule, rule_seen_rule_1, rule_seen_rule_2, rule_seen_rule_3, rule_seen_rule_4]

def generateConstraintRules():
    must_have_head_rule = Rule([], [Literal_bl('R', 'P', 'X'), NotLiteral(Literal_head('R', '_', '_'))])
    no_broken_rule = Rule([], [Literal_bl('R', 'P', 'X'), NotEqualsLiteral('P', '1', True), NotLiteral(Literal_bl('R', 'P - 1', '_'))])
    # no_repeated_calls_rule = Rule([], [Literal_bl('R', 'PX', 'X'), Literal_bl('R', 'PY', 'X'), NotEqualsLiteral('PX', 'PY', True)])
        
    return [must_have_head_rule, no_broken_rule]
    # return []
    
def generateSatisfiedRules():
    in_AS_rule = Rule([Literal_in_AS('X', 'R', 'VVXS')], [Literal_head('R', 'X', 'VVXS'), Literal_body_true('R', 'VVXS')])
    
    bl_inbetween_rule = Rule([Literal_bl_inbetween('R', 'PX', 'PY')], [Literal_bl('R', 'PX', 'X'), Literal_bl('R', 'PY', 'Y'), Literal_bl('R', 'PZ', 'Z'), LTLiteral('PX', 'PZ', True), LTLiteral('PZ', 'PY', True)])
    bl_notlast_rule = Rule([Literal_bl_notlast('R', 'PX', 'X')], [Literal_bl('R', 'PX', 'X'), Literal_bl('R', 'PY', 'Y'), LTLiteral('PX', 'PY', True)])
    bl_first_rule = Rule([Literal_bl_first('1')], [])
    
    satisfied_pos_rule = Rule([Literal_satisfied('R', 'PX', 'X', 'VVYS', 'pos')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_pbl('R', 'PX', 'X', 'VVXS'), Literal_in_AS('X', 'R_OTHER', 'VVS_OTHER'), Literal_rule('R_OTHER')])
    satisfied_neg_rule = Rule([Literal_satisfied('R', 'PX', 'X', 'VVYS', 'neg')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_nbl('R', 'PX', 'X', 'VVXS'), NotLiteral(Literal_in_AS('X', '_', '_'))])
    
    # satisfied rules for built-in types - comparators
    satisfied_equals_rule = Rule([Literal_satisfied('R', 'PX', 'equalsLiteral(X, Y)', 'VVYS', 'pos')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_pbl('R', 'PX', 'equalsLiteral(X, Y)', 'VVXS'), 'X = Y'])
    satisfied_not_equals_rule = Rule([Literal_satisfied('R', 'PX', 'notEqualsLiteral(X, Y)', 'VVYS', 'pos')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_pbl('R', 'PX', 'notEqualsLiteral(X, Y)', 'VVXS'), 'X != Y'])
    satisfied_greater_than_rule = Rule([Literal_satisfied('R', 'PX', 'greaterThanLiteral(X, Y)', 'VVYS', 'pos')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_pbl('R', 'PX', 'greaterThanLiteral(X, Y)', 'VVXS'), 'X > Y'])
    satisfied_greater_equals_rule = Rule([Literal_satisfied('R', 'PX', 'greaterEqualsLiteral(X, Y)', 'VVYS', 'pos')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_pbl('R', 'PX', 'greaterEqualsLiteral(X, Y)', 'VVXS'), 'X >= Y'])
    satisfied_lesser_than_rule = Rule([Literal_satisfied('R', 'PX', 'lesserThanLiteral(X, Y)', 'VVYS', 'pos')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_pbl('R', 'PX', 'lesserThanLiteral(X, Y)', 'VVXS'), 'X < Y'])
    satisfied_lesser_equals_rule = Rule([Literal_satisfied('R', 'PX', 'lesserEqualsLiteral(X, Y)', 'VVYS', 'pos')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_pbl('R', 'PX', 'lesserEqualsLiteral(X, Y)', 'VVXS'), 'X <= Y'])
    
    body_true_upto_rule_1 = Rule([Literal_body_true_upto('R', 'PX', 'X', 'VVYS', 'PN')], [Literal_satisfied('R', 'PX', 'X', 'VVYS', 'PN'), Literal_bl_first('PX')])
    body_true_upto_rule_2 = Rule([Literal_body_true_upto('R', 'PX', 'X', 'VVS', 'PNX')], [Literal_satisfied('R', 'PX', 'X', 'VVS', 'PNX'), GTLiteral('PX', 'PY', True), Literal_body_true_upto('R', 'PY', 'Y', 'VVS', 'PNY'), NotLiteral(Literal_bl_inbetween('R', 'PY', 'PX'))])
    
    body_exists_rule = Rule([Literal_body_exists('R')], [Literal_bl('R', 'P', 'X')])
    body_true_rule_1 = Rule([Literal_body_true('R', 'VVS')], [Literal_rule('R'), Literal_head('R', 'X', 'VVS'), NotLiteral(Literal_body_exists('R'))])
    body_true_rule_2 = Rule([Literal_body_true('R', 'VVS')], [Literal_body_true_upto('R', 'P', 'X', 'VVS', 'PN'), NotLiteral(Literal_bl_notlast('R', 'P', 'X'))])
    # satisfied_equals_rule, satisfied_not_equals_rule, satisfied_greater_than_rule, satisfied_lesser_than_rule, satisfied_lesser_equals_rule, 
    return [in_AS_rule, bl_inbetween_rule, bl_notlast_rule, bl_first_rule, satisfied_pos_rule, satisfied_neg_rule, satisfied_equals_rule, satisfied_not_equals_rule, satisfied_greater_than_rule, satisfied_greater_equals_rule,satisfied_lesser_than_rule, satisfied_lesser_equals_rule, body_true_upto_rule_1, body_true_upto_rule_2, body_exists_rule, body_true_rule_1, body_true_rule_2]

def generateVariables(terms):
    if len(terms) == 0:
        return 'end'
    else:
        return Literal_variables(Literal_variable(terms[0]), generateVariables(terms[1:]))
    
def generateVarVals(rule_id, dict_pairs):
    if len(dict_pairs) == 0:
        return 'end'
    else:
        return Literal_var_vals(Literal_var_val(rule_id, dict_pairs[0][0], dict_pairs[0][1]), generateVarVals(rule_id, dict_pairs[1:]))
    
def generateLiteral(literal):
    if is_eq_literal(literal):
        args = [generateLiteral(x) for x in get_arguments(literal, Built_in_type.EQ)]
        return EqualsLiteral(args[0], args[1])
    elif is_neq_literal(literal):
        args = [generateLiteral(x) for x in get_arguments(literal, Built_in_type.NEQ)]
        neq = NotEqualsLiteral(args[0], args[1])
        return neq
    elif is_gt_literal(literal):
        args = [generateLiteral(x) for x in get_arguments(literal, Built_in_type.GT)]
        gt = GTLiteral(args[0], args[1])
        return gt
    elif is_ge_literal(literal):
        args = [generateLiteral(x) for x in get_arguments(literal, Built_in_type.GE)]
        ge = GELiteral(args[0], args[1])
        return ge
    elif is_lt_literal(literal):
        args = [generateLiteral(x) for x in get_arguments(literal, Built_in_type.LT)]
        lt = LTLiteral(args[0], args[1])
        return lt
    elif is_le_literal(literal):
        args = [generateLiteral(x) for x in get_arguments(literal, Built_in_type.LE)]
        le = LELiteral(args[0], args[1])
        return le
    elif '(' in literal:
        name = literal[:-1].split('(', 1)[0]
        args = [generateLiteral(x) for x in get_arguments(literal)]
        return Literal(name, args)
    else:
        # is an atom
        return trim_front_back_whitespace(literal)
    
def generateLiteralRule(rule_id, literal, args, var_dict, index = None):
    args = flatten_args(args)
    dict_pairs = sorted([(var_dict[x], x) for x in var_dict if x in args])
    if index == None:
        head = Literal_head(rule_id, generateLiteral(literal), generateVarVals(rule_id, dict_pairs))
        body = [Literal_ground(x) for x in args if is_variable(x)]
        return Rule([head], body)
    else:
        head = Literal_nbl(rule_id, index, generateLiteral(literal[3:]), generateVarVals(rule_id, dict_pairs)) if literal[:2] == '\+' else Literal_pbl(rule_id, index, generateLiteral(literal), generateVarVals(rule_id, dict_pairs))
        body = [Literal_ground(x) for x in args if is_variable(x)]
        rule = Rule([head], body)
        assign_built_in_type(rule, literal)
        return rule
    
def generateVariableListRules(variables):
    if len(variables) == 0: return ['end']
    ls = ['end']
    for i in range(len(variables)):
        subs = generateVariableListRules(variables[i + 1:])
        for j in subs:
            ls.append(Literal_variables(variables[i], j))
    return ls
    

def generateProgramRules(processed_rules):
    # for each in processed_rules:
    #     print(each)
    program = []
    
    modeh_literals = {}
    rule_ids = []
    rule_lengths = {}
    variables = set()
    var_names = []
    ground_constants = set()
    var_dicts = {}
    
    rules = []
    for rule in processed_rules:
        rule_id = Rule([Literal_rule(rule.rule_id)], [])
        head_rule = None if rule.head is None else generateLiteralRule(rule.rule_id, rule.head.literal, list(rule.var_dict.keys()), rule.var_dict)
        body_rules = [generateLiteralRule(rule.rule_id, x.literal, x.args, rule.var_dict, str(i+1)) for i, x in enumerate(rule.body)]
        rule_lengths[rule.rule_id] = len(body_rules)
        var_dicts[rule.rule_id] = rule.var_dict
        
        rules.append(rule_id)
        if head_rule is not None:
            rules.append(head_rule)
        rules = rules + body_rules
        
        if head_rule is not None:
            head_name, head_arity = get_name_count_arity(head_rule.head[0].literal)
            if head_name not in modeh_literals:
                modeh_literals[head_name] = head_arity

        for each in body_rules:
            if each.built_in_type is not None: 
                continue
            name, arity = get_name_count_arity(each.head[0].literal)
            if name not in modeh_literals:
                modeh_literals[name] = arity
                
        rule_ids.append(rule.rule_id)
        variables.update(rule.variables)
        ground_constants.update(rule.constants)
        for each in rule.var_dict.values():
            if each not in var_names:
                var_names.append(each)
    
    for each in ground_constants:
        program.append(Rule([Literal_ground(each)], []))

    for each in sorted(var_names):
        program.append(Rule([Literal_variable(each)], []))
        
    program = program + rules
    
    for j in range(len(rule_ids)):
        if j < len(rule_ids) - 1:
            program.append(Rule([Literal_order(rule_ids[j], rule_ids[j+1])], []))
    
    var_max = len(var_names) + 1
    program.append(Rule([Literal_var_num(str(var_max), True)], []))
    program.append(Rule([Literal_var_max(str(var_max))], []))
    
    program = program + [Rule([Literal_variable_list(x)], []) for x in generateVariableListRules(sorted(var_names)) if x is not 'end']
    
    return modeh_literals, rule_ids, rule_lengths, var_max, variables, ground_constants, var_dicts, program

def generateStaticRules():
    return generateBLRules() + generateVarValRules() + generateSubsetRules() + generateSeenOrderingRules() + generateConstraintRules() + generateSatisfiedRules()

def encode(text, output):
    f = open(text, 'r')
    dest = open(output, 'w')
    static_rules = generateStaticRules()
    body_literals, rule_ids, rule_lengths, var_max, variables, ground_constants, var_dicts, program = generateProgramRules(parseText(f.read()))
    rules = static_rules + program
    for rule in rules:
        dest.write(rule.__str__() + '\n')
    dest.write('#show in_AS/3.')
    dest.close()
    f.close()
    return body_literals, rule_ids, rule_lengths, var_max, variables, ground_constants, var_dicts, static_rules, program

def main(argv):
    if (len(argv) == 2):
        encode(argv[0], argv[1])
    else:
        print('Please provide an input file and an output destination.')
    
if __name__ == '__main__':
    main(sys.argv[1:])