import sys
import itertools
from classes import *
from parser import *
from helper import *

def generateBLRules():
    # body literals
    bl_pbl_rule = Rule([Literal_bl('R', 'P', 'X')], [Literal_pbl('R', 'P', 'X', 'VARS')])
    bl_nbl_rule = Rule([Literal_bl('R', 'P', 'X')], [Literal_nbl('R', 'P', 'X', 'VARS')])
    
    # print(bl_pbl_rule)
    # print(bl_nbl_rule)
    return [bl_pbl_rule, bl_nbl_rule]

    
def generateVarValRules():
    # var_vals
    var_val_rule = Rule([Literal_var_val('R', 'V', 'T')], [Literal_rule('R'), Literal_variable('V'), Literal_ground('T')])
    is_var_val_rule = Rule([Literal_is_var_val(Literal_var_val('R', 'V', 'T'))], [Literal_rule('R'), Literal_variable('V'), Literal_ground('T')])
    var_val_equal_rule = Rule([Literal_var_val_equal('VVX', 'VVY')], [Literal_is_var_val('VVX'), Literal_is_var_val('VVY'), EqualsLiteral('VVX', Literal_var_val('R', 'V', 'T')), EqualsLiteral('VVY', Literal_var_val('R', 'V', 'T'))])
    valid_var_val_rule = Rule([Literal_valid_var_val('RULE_NO', Literal_var_val('R', 'V', 'T'), 'VAR')], [Literal_variable('VAR'), Literal_rule('R'), EqualsLiteral('R', 'RULE_NO'), EqualsLiteral('V', 'VAR'), Literal_ground('T')])
    
    # print(var_val_rule)
    # print(is_var_val_rule)
    # print(var_val_equal_rule)
    # print(valid_var_val_rule)
    return [var_val_rule, is_var_val_rule, var_val_equal_rule, valid_var_val_rule]
    
def generateSubsetRules():
    # length
    length_base_rule = Rule([Literal_length('R', 'end', '0', 'MAX', 'end')], [Literal_var_max('MAX'), Literal_rule('R')])
    length_recursive_rule = Rule([Literal_length('R', Literal_var_vals('VV', 'VVS'), 'N', 'MAX', Literal_variables('V', 'VS'))], [Literal_valid_var_val('R', 'VV', 'V'), Literal_length('R', 'VVS', 'N - 1', 'MAX', 'VS'), Literal_var_max('MAX'), LTLiteral('N', 'MAX')])
    defined_length_base_rule = Rule([Literal_defined_length('R', 'end', '0')], [Literal_rule('R')])
    defined_length_recursive_rule = Rule([Literal_defined_length('R', 'VVS', 'N')], [Literal_variable_list('VS'), Literal_length('R', 'VVS', 'N', 'MAX', 'VS'), Literal_var_num('N'), Literal_var_num('MAX')])
    check_sets_length_rule = Rule([Literal_check_sets_length('R', 'VVXS', 'VVYS')], [Literal_defined_length('R', 'VVXS', 'NX'), Literal_defined_length('R', 'VVYS', 'NY'), Literal_var_num('NX'), Literal_var_num('NY'), LELiteral('NX', 'NY')])
    
    # is_subset
    is_subset_helper_base_rule = Rule([Literal_is_subset_helper('R', 'end', 'VVYS')], [Literal_defined_length('R', 'VVYS', '_')])
    is_subset_helper_recursive_rule_1 = Rule([Literal_is_subset_helper('R', Literal_var_vals('VVX', 'VVXS'), Literal_var_vals('VVY', 'VVYS'))], [Literal_check_sets_length('R', Literal_var_vals('VVX', 'VVXS'), Literal_var_vals('VVY', 'VVYS')), Literal_var_val_equal('VVX', 'VVY'), Literal_is_subset_helper('R', 'VVXS', 'VVYS')])
    is_subset_helper_recursive_rule_2 = Rule([Literal_is_subset_helper('R', Literal_var_vals('VVX', 'VVXS'), Literal_var_vals('VVY', 'VVYS'))], [Literal_check_sets_length('R', Literal_var_vals('VVX', 'VVXS'), Literal_var_vals('VVY', 'VVYS')), NotLiteral(Literal_var_val_equal('VVX', 'VVY')), Literal_is_subset_helper('R', Literal_var_vals('VVX', 'VVXS'), 'VVYS')])
    is_subset_pbl_rule = Rule([Literal_is_subset('R', 'VVXS', 'VVYS')], [Literal_pbl('R', 'PX', 'X', 'VVXS'), Literal_head('R', 'Y', 'VVYS'), Literal_is_subset_helper('R', 'VVXS', 'VVYS')])
    is_subset_nbl_rule = Rule([Literal_is_subset('R', 'VVXS', 'VVYS')], [Literal_nbl('R', 'PX', 'X', 'VVXS'), Literal_head('R', 'Y', 'VVYS'), Literal_is_subset_helper('R', 'VVXS', 'VVYS')])    
    
    # print(length_base_rule)
    # print(length_recursive_rule)
    # print(defined_length_base_rule)
    # print(defined_length_recursive_rule)  
    # print(check_sets_length_rule)  
    # print(is_subset_helper_base_rule)
    # print(is_subset_helper_recursive_rule_1)
    # print(is_subset_helper_recursive_rule_2)
    # print(is_subset_pbl_rule)
    # print(is_subset_nbl_rule)
    return [length_base_rule, length_recursive_rule, defined_length_base_rule, defined_length_recursive_rule, check_sets_length_rule, is_subset_helper_base_rule, is_subset_helper_recursive_rule_1, is_subset_helper_recursive_rule_2, is_subset_pbl_rule, is_subset_nbl_rule]
    
def generateSeenOrderingRules():
    rule_not_first_rule = Rule([Literal_rule_not_first('R')], [Literal_order('R_OTHER', 'R'), Literal_rule('R'), Literal_rule('R_OTHER')])
    rule_seen_rule_1 = Rule([Literal_seen_rule('R')], [NotLiteral(Literal_rule_not_first('R')), Literal_rule('R'), Literal_in_AS('X', 'R', 'VVXS'), Literal_head('R', 'X', 'VVXS')])
    rule_seen_rule_2 = Rule([Literal_seen_rule('R')], [NotLiteral(Literal_rule_not_first('R')), Literal_rule('R'), NotLiteral(Literal_in_AS('X', 'R', 'VVXS')), Literal_head('R', 'X', 'VVXS')])
    rule_seen_rule_3 = Rule([Literal_seen_rule('R')], [Literal_seen_rule('R_PREV'), Literal_order('R_PREV', 'R'), Literal_rule('R'), Literal_rule('R_PREV'), Literal_in_AS('X', 'R', 'VVXS'), Literal_head('R', 'X', 'VVXS')])
    rule_seen_rule_4 = Rule([Literal_seen_rule('R')], [Literal_seen_rule('R_PREV'), Literal_order('R_PREV', 'R'), Literal_rule('R'), Literal_rule('R_PREV'), NotLiteral(Literal_in_AS('X', 'R', 'VVXS')), Literal_head('R', 'X', 'VVXS')])
    
    # print(rule_not_first_rule)
    # print(rule_seen_rule_1)
    # print(rule_seen_rule_2)
    # print(rule_seen_rule_3)
    # print(rule_seen_rule_4)
    return [rule_not_first_rule, rule_seen_rule_1, rule_seen_rule_2, rule_seen_rule_3, rule_seen_rule_4]
    
def generateSatisfiedRules():
    in_AS_rule = Rule([Literal_in_AS('X', 'R', 'VVXS')], [Literal_head('R', 'X', 'VVXS'), Literal_body_true('R', 'VVXS')])
    
    bl_inbetween_rule = Rule([Literal_bl_inbetween('R', 'X', 'Y')], [Literal_bl('R', 'PX', 'X'), Literal_bl('R', 'PY', 'Y'), Literal_bl('R', 'PZ', 'Z'), LTLiteral('PX', 'PZ'), LTLiteral('PZ', 'PY')])
    bl_notlast_rule = Rule([Literal_bl_notlast('R', 'X')], [Literal_bl('R', 'PX', 'X'), Literal_bl('R', 'PY', 'Y'), LTLiteral('PX', 'PY')])
    bl_notfirst_rule = Rule([Literal_bl_notfirst('R', 'X')], [Literal_bl('R', 'PX', 'X'), GTLiteral('PX', '1')])
    
    satisfied_pos_rule = Rule([Literal_satisfied('R', 'PX', 'X', 'VVYS', 'pos')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_pbl('R', 'PX', 'X', 'VVXS'), Literal_in_AS('X', 'R_OTHER', 'VVS_OTHER'), Literal_rule('R_OTHER')])
    satisfied_neg_rule = Rule([Literal_satisfied('R', 'PX', 'X', 'VVYS', 'neg')], [Literal_is_subset('R', 'VVXS', 'VVYS'), Literal_nbl('R', 'PX', 'X', 'VVXS'), NotLiteral(Literal_in_AS('X', '_', '_'))])
    
    body_true_upto_rule_1 = Rule([Literal_body_true_upto('R', 'PX', 'X', 'VVYS', 'PN')], [Literal_satisfied('R', 'PX', 'X', 'VVYS', 'PN'), NotLiteral(Literal_bl_notfirst('R', 'X'))])
    body_true_upto_rule_2 = Rule([Literal_body_true_upto('R', 'PX', 'X', 'VVS', 'PNX')], [Literal_satisfied('R', 'PX', 'X', 'VVS', 'PNX'), GTLiteral('PX', 'PY'), Literal_body_true_upto('R', 'PY', 'Y', 'VVS', 'PNY'), NotLiteral(Literal_bl_inbetween('R', 'Y', 'X'))])
    
    body_exists_rule = Rule([Literal_body_exists('R')], [Literal_bl('R', 'P', 'X')])
    body_true_rule_1 = Rule([Literal_body_true('R', 'VVS')], [Literal_rule('R'), Literal_head('R', 'X', 'VVS'), NotLiteral(Literal_body_exists('R'))])
    body_true_rule_2 = Rule([Literal_body_true('R', 'VVS')], [Literal_body_true_upto('R', 'P', 'X', 'VVS', 'PN'), NotLiteral(Literal_bl_notlast('R', 'X'))])
    
    # print(in_AS_rule)
    # print(bl_inbetween_rule)
    # print(bl_notlast_rule)
    # print(bl_notfirst_rule)
    # print(satisfied_pos_rule)
    # print(satisfied_neg_rule)
    # print(body_true_upto_rule_1)
    # print(body_true_upto_rule_2)
    # print(body_exists_rule)
    # print(body_true_rule_1)
    # print(body_true_rule_2)
    return [in_AS_rule, bl_inbetween_rule, bl_notlast_rule, bl_notfirst_rule, satisfied_pos_rule, satisfied_neg_rule, body_true_upto_rule_1, body_true_upto_rule_2, body_exists_rule, body_true_rule_1, body_true_rule_2]
    
def generateVariables(terms):
    if len(terms) == 0:
        return 'end'
    else:
        return Literal_variables(Literal_variable(terms[0]), generateVariables(terms[1:]))
    
def generateVarVals(rule_id, terms, var_dict):
    if len(terms) == 0:
        return 'end'
    else:
        return Literal_var_vals(Literal_var_val(rule_id, var_dict[terms[0]], terms[0]), generateVarVals(rule_id, terms[1:], var_dict))
    
def generateLiteralRule(rule_id, literal, args, var_dict, index = None):
    if index == None:
        head = Literal_head(rule_id, literal, generateVarVals(rule_id, args, var_dict))
        body = [Literal_ground(x) for x in args if is_variable(x)]
        return Rule([head], body)
    else:
        head = Literal_nbl(rule_id, index, literal[4:], generateVarVals(rule_id, args, var_dict)) if literal[:3] == 'not' else Literal_pbl(rule_id, index, literal, generateVarVals(rule_id, sorted(args), var_dict))
        body = [Literal_ground(x) for x in args if is_variable(x)]
        return Rule([head], body)
    
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
    
    rule_ids = []
    variables = set()
    ground_constants = set()
    
    rules = []
    for rule in processed_rules:
        rule_id = Rule([Literal_rule(rule.rule_id)], [])
        head_rule = generateLiteralRule(rule.rule_id, rule.head.literal, list(rule.var_dict.keys()), rule.var_dict)
        body_rules = [generateLiteralRule(rule.rule_id, x.literal, x.args, rule.var_dict, str(i+1)) for i, x in enumerate(rule.body)]
        
        rules.append(rule_id)
        rules.append(head_rule)
        rules = rules + body_rules
        rule_ids.append(rule.rule_id)
        variables.update(rule.variables)
        ground_constants.update(rule.constants)
        
    for each in ground_constants:
        program.append(Rule([Literal_ground(each)], []))
        
    for i in range(len(variables)):
        program.append(Rule([Literal_variable(variable_pool[i])], []))
        
    program = program + rules
    
    for j in range(len(rule_ids)):
        if j < len(rule_ids) - 1:
            program.append(Rule([Literal_order(rule_ids[j], rule_ids[j+1])], []))
            
    program.append(Rule([Literal_var_num(str(len(variables) + 1), True)], []))
    program.append(Rule([Literal_var_max(str(len(variables) + 1))], []))
    
    program = program + [Rule([Literal_variable_list(x)], []) for x in generateVariableListRules(sorted(list(rule.var_dict.values()))) if x is not 'end']
    
    return program

def generateStaticRules():
    return generateBLRules() + generateVarValRules() + generateSubsetRules() + generateSeenOrderingRules() + generateSatisfiedRules()

def encode(text, output):
    f = open('../examples/' + text, 'r')
    dest = open(output, 'w')
    rules = generateStaticRules()
    rules = rules + generateProgramRules(parseText(f.read()))
    # rules.append('#show in_AS/3.')
    for rule in rules:
        dest.write(rule.__str__() + '\n')
    dest.close()
    f.close()

def main(argv):
    if (len(argv) == 2):
        encode(argv[0], argv[1])
    else:
        print('Please provide an input file and an output destination.')
    
if __name__ == '__main__':
    main(sys.argv[1:])