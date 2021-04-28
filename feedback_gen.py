import sys
import subprocess
from metarep_encoder.encoder import encode
from metarep_encoder.fault_localiser import find_erroneous_rules
from metarep_encoder.declarations_gen import generate_declarations
from metarep_encoder.rule_mapping import *
from tr_ilasp.revision import revise_program, revisableTheory

def generate_revisable_program(file_name):
    correct_body_literals, correct_rule_ids, correct_variables, correct_ground_constants, _, correct_program = encode(file_name, 'correct.las')
    user_body_literals, user_rule_ids, user_variables, user_ground_constants, static_rules, user_program = encode(file_name.replace('.lp', '_user.lp'), 'user.las')

    incorrect_arities = find_incorrect_arities(correct_body_literals, user_body_literals)
    if len(incorrect_arities) > 0:
        print('Literals used with incorrect number of variables. Please refer to the correct arities: {}.'.format(incorrect_arities))
        return incorrect_arities
        
    rule_mapping, score, correct_rules_grouped, user_rules_grouped = generate_mapping(correct_program, user_program)
    print('Similarity score: %s' % str(score))
    errors, revisions_data, answer_set = find_erroneous_rules(rule_mapping, correct_rules_grouped, user_rules_grouped)
    
    if str(score) == '1.000' or len(errors) == 0:
        print('User program gives expected results. No revision needed.')
        return
    
    revisable = generate_declarations(errors, revisions_data, answer_set, correct_body_literals, correct_rule_ids, correct_variables, correct_ground_constants, correct_program, user_body_literals, user_rule_ids, user_variables, user_ground_constants, user_program)
    
    revisable = static_rules + revisable
    
    dest = open('revisable.las', 'w')
    for each in revisable:
        dest.write(each.__str__() + '\n')
    dest.close()    
    
    return revisable

def parse_theory(theory):
    assert_type(theory, revisableTheory)
    heads = theory.head.values()
    bls = []
    
    for each in heads:
        head_elems = each.children
        # assume each.val == pbl or each.val == nbl
        rule_id = head_elems[0].val
        index = head_elems[1].val
        literal = parse_literal_node(head_elems[2])
        var_vals = parse_var_vals_node(head_elems[3])
        
        bl = Literal_pbl(rule_id, index, literal, var_vals) if each.val == 'pbl' else Literal_nbl(rule_id, index, literal, var_vals)
        bls.append(bl)
        
    return bls
    
def parse_literal_node(literal):
    if len(literal.children) == 0:
        return literal.val
    else:
        return Literal(literal.val, [parse_literal_node(x) for x in literal.children])
    
def parse_var_vals_node(var_vals):
    if len(var_vals.children) == 0 and var_vals.val == 'end':
        return 'end'
    elif len(var_vals.children) == 3 and var_vals.val == 'var_val':
        children = var_vals.children
        return Literal_var_val(children[0].val, children[1].val, children[2].val)
    else:   
        children = var_vals.children
        vv = parse_var_vals_node(children[0])
        others = parse_var_vals_node(children[1])
        return Literal_var_vals(vv, others)

def main(argv):
    revisable = generate_revisable_program(argv[0])
    revised = revise_program('revisable.las')
    parsed_revisions = [parse_theory(x) for x in revised.values()]
    for each in parsed_revisions:
        for head in each:
            print(head)  
 
    
if __name__ == '__main__':
    main(sys.argv[1:])