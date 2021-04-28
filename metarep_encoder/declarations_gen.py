from metarep_encoder.classes import *
from metarep_encoder.helper import *

def make_rule_revisable(rule_id, program, counter, revisions_data):
    found = False
    for i, each in enumerate(program):
        if isinstance(each.head[0], Literal_rule):
            if each.head[0].rule_id == rule_id and not found:
                found = True
            elif found:
                break
        elif found and (isinstance(each.head[0], Literal_pbl) or isinstance(each.head[0], Literal_nbl)):
            if rule_id in revisions_data and each.head[0].index not in revisions_data[rule_id][0]:
                continue     
            else:
                head = each.head[0]
                revise_vars = join([x + ': ground' for x in var_vals_to_revisable_variables(head.var_vals)])
                each.make_revisable('rev' + str(counter), revise_vars)
                counter += 1
    return counter
  
def find_head_literal_name(program, rule_id):
    for each in program:
        if isinstance(each.head[0], Literal_head) and each.head[0].rule_id == rule_id:
            return each.head[0].literal.name
        
def filter_example(example, revisables):
    relevant = False
    for rev in revisables:
        if rev in example.literal:
            relevant = True
            break
    return relevant
    
def generate_declarations(errors, revisions_data, answer_set, correct_body_literals, correct_rule_ids, correct_variables, correct_ground_constants, correct_program, user_body_literals, user_rule_ids, user_variables, user_ground_constants, user_program):
    declarations = []
    
    const_rule_ids = user_rule_ids + [x for x in correct_rule_ids if x not in user_rule_ids]
    const_variables = list(user_variables.union(correct_variables))
    const_ground_constants = list(user_ground_constants.union(correct_ground_constants))
    
    const_rule_ids = [Declaration_const(RULE_ID_SYMBOL, x) for x in const_rule_ids if x in errors]
    const_variables = [Declaration_const(VARIABLE_SYMBOL + x[-2:], x) for x in VARIABLE_POOL[:len(const_variables)]] 
    const_ground_constants = [Declaration_const(GROUND_CONSTANT_SYMBOL, x) for x in const_ground_constants]
    const_positions = set()
    for each in revisions_data:
        const_positions.update(revisions_data[each][0])
    const_positions = [Declaration_const(POS_SYMBOL, x) for x in sorted(const_positions)]
    const_var_vals_end = [Declaration_const(VAR_VALS_END_SYMBOL, 'end')]
        
    declarations += const_rule_ids + const_variables + const_ground_constants + const_positions + const_var_vals_end
    
    literal_arities = correct_body_literals
    for each in user_body_literals:
        if each not in literal_arities:
            literal_arities[each] = user_body_literals[each]
            
    revise_counter = 1
    revisable_literals = []
    modehs = []    
    const_variable_symbols = [x.symbol for x in const_variables]    
    positive_examples = [Declaration_pos_example(i, x.original_str) for i, x in enumerate(answer_set)]
    negative_examples = [] 
    
    for each in sorted(errors.keys()):
        revisable_literals.append(find_head_literal_name(user_program, each))
        for neg in errors[each][1]:
            negative_examples.append(Declaration_neg_example(len(negative_examples), neg.original_str))
        revise_counter = make_rule_revisable(each, user_program, revise_counter, revisions_data)
        
        if each in revisions_data:
            modeh_literals = revisions_data[each][1]
            for each in modeh_literals:
                arity = literal_arities[each]
                literal = each + '(' + join(['var(ground)' for x in range(arity)]) + ')'
                var_vals = generate_var_vals_declarations(sorted(const_variable_symbols), arity)
                for vv in var_vals:
                    if vv == 'const({})'.format(VAR_VALS_END_SYMBOL): continue
                    pbl_string = 'pbl(const({}), const({}), {}, {})'.format(RULE_ID_SYMBOL, POS_SYMBOL, literal, vv)
                    # nbl_string = 'nbl(const({}), const({}), {}, {})'.format(RULE_ID_SYMBOL, POS_SYMBOL, literal, var_vals)
                    modehs.append(Declaration_modeh(pbl_string))
                    # modehs.append(Declaration_modeh(nbl_string))   
    
    # for each in literal_arities:
    #     arity = literal_arities[each]
    #     literal = each + '(' + join(['var(ground)' for x in range(arity)]) + ')'
    #     var_vals = generate_var_vals_declarations(sorted(const_variable_symbols), arity)
    #     for vv in var_vals:
    #         if vv == 'const({})'.format(VAR_VALS_END_SYMBOL): continue
    #         pbl_string = 'pbl(const({}), const({}), {}, {})'.format(RULE_ID_SYMBOL, POS_SYMBOL, literal, vv)
    #         # nbl_string = 'nbl(const({}), const({}), {}, {})'.format(RULE_ID_SYMBOL, POS_SYMBOL, literal, var_vals)
    #         modehs.append(Declaration_modeh(pbl_string))
    #         # modehs.append(Declaration_modeh(nbl_string))
            
    declarations += modehs
    positive_examples = list(filter(lambda x: filter_example(x, revisable_literals), positive_examples))
    negative_examples = list(filter(lambda x: filter_example(x, revisable_literals), negative_examples))   
    declarations += positive_examples + negative_examples
    
    declarations.append(Declaration_modeb('ground(var(ground))'))
    declarations.append(Declaration_maxv(max(literal_arities.values())))
    
    user_program += declarations
        
    # for each in user_program:
    #     print(each)
    return user_program

def main():
    generate_declarations()
    
    
if __name__ == '__main__':
    main()