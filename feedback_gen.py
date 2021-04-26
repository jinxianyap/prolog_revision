import sys
from metarep_encoder.encoder import encode
from metarep_encoder.fault_localiser import find_erroneous_rules
from metarep_encoder.declarations_gen import generate_declarations
from metarep_encoder.rule_mapping import *

def main(argv):
    correct_body_literals, correct_rule_ids, correct_variables, correct_ground_constants, _, correct_program = encode(argv[0], 'correct.las')
    user_body_literals, user_rule_ids, user_variables, user_ground_constants, static_rules, user_program = encode(argv[0].replace('.lp', '_user.lp'), 'user.las')

    incorrect_arities = find_incorrect_arities(correct_body_literals, user_body_literals)
    
    if len(incorrect_arities) > 0:
        print('Literals used with incorrect number of variables. Please refer to the correct arities: {}.'.format(incorrect_arities))
        return incorrect_arities
        
    rule_mapping, score = generate_mapping(correct_program, user_program)
    print('Similarity score: %s' % str(score))
    errors, answer_set = find_erroneous_rules(rule_mapping)

    if str(score) == '1.000' or len(errors) == 0:
        print('User program gives expected results. No revision needed.')
        return
    
    revisable = generate_declarations(errors, answer_set, correct_body_literals, correct_rule_ids, correct_variables, correct_ground_constants, correct_program, user_body_literals, user_rule_ids, user_variables, user_ground_constants, user_program)
    
    revisable = static_rules + revisable
    
    dest = open('revisable.las', 'w')
    for each in revisable:
        dest.write(each.__str__() + '\n')
    dest.close()    
    
    return revisable  
    
if __name__ == '__main__':
    main(sys.argv[1:])