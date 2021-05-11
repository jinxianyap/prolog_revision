import random
from metarep_encoder.classes import *
from metarep_encoder.helper import *
from metarep_encoder.encoder import generateVarVals, generateVariableListRules
from metarep_encoder.fault_localiser import DerivableFact

def make_rule_revisable(rule_id, program, counter, revisions_data):
    found = False
    revisable_rules = {}
    for i, each in enumerate(program):
        if isinstance(each.head[0], Literal_rule):
            if each.head[0].rule_id == rule_id and not found:
                found = True
            elif found:
                break
        elif found and (isinstance(each.head[0], Literal_pbl) or isinstance(each.head[0], Literal_nbl)):
            if rule_id in revisions_data and each.head[0].index not in revisions_data[rule_id].keys():
                continue     
            else:
                head = each.head[0]
                revise_vars = join([x + ': ground' for x in var_vals_to_revisable_variables(head.var_vals)])
                each.make_revisable('rev' + str(counter), revise_vars)
                counter += 1
                revisable_rules[head.index] = (each, False)
    return counter, revisable_rules
  
def find_head_literal_name_and_arity(program, rule_id):
    for each in program:
        if isinstance(each.head[0], Literal_head) and each.head[0].rule_id == rule_id:
            return (rule_id, each.head[0].literal.name, len(each.head[0].literal.args))
        
def filter_example(example, revisables):
    relevant = False
    for rev in revisables:
        if rev[1] in example.fact.original_str:
            relevant = True
            break
    return relevant

def variables_dict_to_var_vals(rule_id, variables_dict):
    if len(variables_dict) == 0:
        return 'end'
    else:
        return Literal_var_vals(Literal_var_val(rule_id, variables_dict[0][0], variables_dict[0][1]), variables_dict_to_var_vals(rule_id, variables_dict[1:]))

def generate_negative_examples(rule_id, literal_name, arity, ground_constants, term_combos, max_num):
    tries = max_num * 2
    negs = []
    print(term_combos)
    while len(negs) < max_num and tries > 0:
        tries -= 1
        terms = []
        variables_dict = {}
        
        while len(terms) < arity:
            i = random.randint(0, len(ground_constants) - 1)
            term = ground_constants[i]
            terms.append(term)
            variables_dict[VARIABLE_POOL[len(terms)]] = term

        if tuple(terms) not in term_combos:
            print(tuple(terms))
            literal = Literal(literal_name, terms)
            var_vals = variables_dict_to_var_vals(rule_id, list(variables_dict.items()))
            original_str = 'in_AS(' + ', '.join([rule_id, literal.__str__(), var_vals.__str__()]) + ')'
            negs.append(Declaration_neg_example('_{}_{}'.format(rule_id, len(negs)), DerivableFact(rule_id, literal, variables_dict, original_str)))
            term_combos.add(tuple(terms))

    return negs
    
def generate_declarations(errors, revisions_data, answer_set, correct_body_literals, correct_rule_ids, correct_var_max, correct_variables, correct_ground_constants, correct_program, user_body_literals, user_rule_ids, user_var_max, user_variables, user_ground_constants, user_program):
    declarations = []
    
    const_rule_ids = user_rule_ids + [x for x in correct_rule_ids if x not in user_rule_ids]
    const_variables = list(user_variables.union(correct_variables))
    ground_constants = list(user_ground_constants.union(correct_ground_constants))

    const_rule_ids = [Declaration_const(RULE_ID_SYMBOL, x) for x in const_rule_ids if x in errors]
    const_variables = [Declaration_const(VARIABLE_SYMBOL + x[-2:], x) for x in VARIABLE_POOL[:len(const_variables)]] 
    const_ground_constants = [Declaration_const(GROUND_CONSTANT_SYMBOL, x) for x in ground_constants]
    const_positions = set()
    for each in revisions_data:
        const_positions.update(revisions_data[each].keys())
    const_positions = [Declaration_const(POS_SYMBOL, x) for x in sorted(const_positions)]
    const_var_vals_end = [Declaration_const(VAR_VALS_END_SYMBOL, 'end')]
        
    declarations += const_rule_ids + const_variables + const_ground_constants + const_positions + const_var_vals_end
    
    literal_arities = correct_body_literals
    for each in user_body_literals:
        if each not in literal_arities:
            literal_arities[each] = user_body_literals[each]
            
    const_variable_symbols = [x.symbol for x in const_variables]
    positive_examples = [Declaration_pos_example(i, x) for i, x in enumerate(answer_set)]
    negative_examples = []
           
    revise_counter = 1
    revisable_rules = {} # collects all #revisable declarations for each rule_id for each index
    revisable_literals = [] # list of affected literals where there is an error in the answer set
    modehs = []     
    
    for each in sorted(errors.keys()):
        revisable_literals.append(find_head_literal_name_and_arity(user_program, each))
        for neg in errors[each][1]:
            negative_examples.append(Declaration_neg_example(len(negative_examples), neg))
        revise_counter, rules_to_revise = make_rule_revisable(each, user_program, revise_counter, revisions_data)
        revisable_rules[each] = rules_to_revise
        
        if each in revisions_data:
            modeh_literals = [(x[0].name, x[1]) for x in revisions_data[each].values() if x is not None]
            for x in modeh_literals:
                literal_name = x[0]
                is_pbl = x[1]
                arity = literal_arities[literal_name]
                literal = literal_name + '(' + join(['var(ground)' for x in range(arity)]) + ')'
                var_vals = generate_var_vals_declarations(sorted(const_variable_symbols), arity)
                for vv in var_vals:
                    if vv == 'const({})'.format(VAR_VALS_END_SYMBOL): continue
                    if is_pbl is None:
                        pbl_string = 'pbl(const({}), const({}), {}, {})'.format(RULE_ID_SYMBOL, POS_SYMBOL, literal, vv)
                        modehs.append(Declaration_modeh(pbl_string))
                        nbl_string = 'nbl(const({}), const({}), {}, {})'.format(RULE_ID_SYMBOL, POS_SYMBOL, literal, vv)
                        modehs.append(Declaration_modeh(nbl_string))
                    elif is_pbl:
                        pbl_string = 'pbl(const({}), const({}), {}, {})'.format(RULE_ID_SYMBOL, POS_SYMBOL, literal, vv)
                        modehs.append(Declaration_modeh(pbl_string))
                    else:
                        nbl_string = 'nbl(const({}), const({}), {}, {})'.format(RULE_ID_SYMBOL, POS_SYMBOL, literal, vv)
                        modehs.append(Declaration_modeh(nbl_string))
                    
    for rule_id in revisions_data:
        for index in revisions_data[rule_id]:
            # generating #revisable declarations for new rules
            if index not in revisable_rules[rule_id].keys():
                literal = revisions_data[rule_id][index][0]
                # create dict pairs for Literal_var_vals generation
                dict_pairs = [(VARIABLE_POOL[i], x) for i, x in enumerate(literal.args)]
                var_vals = generateVarVals(rule_id, dict_pairs)             
                pbl = Literal_pbl(rule_id, index, literal, var_vals)
                rule = Rule([pbl], [Literal_ground(x) for x in literal.args])
                
                revise_vars = join([x + ': ground' for x in var_vals_to_revisable_variables(var_vals)])
                rule.make_revisable('rev' + str(revise_counter), revise_vars)
                revise_counter += 1
                revisable_rules[rule_id][index] = (rule, True)
                user_program.append(rule)          
            
    declarations += modehs
    positive_examples = list(filter(lambda x: filter_example(x, revisable_literals), positive_examples))
    negative_examples = list(filter(lambda x: filter_example(x, revisable_literals), negative_examples))   
    declarations += positive_examples + negative_examples
    
    # generate more negative examples, given ground_constants, revisable_literals, its arity and term_combos
    term_combos = set()  
    for each in positive_examples:
        term_combos.add(tuple(each.fact.literal.args))
    for each in negative_examples:
        term_combos.add(tuple(each.fact.literal.args))
    for each in revisable_literals:
        declarations += generate_negative_examples(each[0], each[1], each[2], ground_constants, term_combos, 5)
        
    declarations.append(Declaration_modeb('ground(var(ground))'))
    declarations.append(Declaration_maxv(max(literal_arities.values())))
    
    # var_max additions
    if user_var_max != correct_var_max:
        i = len(user_program) - 1
        while i > 0:
            if isinstance(user_program[i].head[0], Literal_var_num):
                break
            else:
                i -= 1
        user_program = user_program[:i]
    
        var_names_extensions = []
        
        var_num_rule = Rule([Literal_var_num(str(correct_var_max), True)], [])
        var_max_rule = Rule([Literal_var_max(str(correct_var_max))], [])
        variable_list_rules = [Rule([Literal_variable_list(x)], []) for x in generateVariableListRules(sorted(VARIABLE_POOL[:correct_var_max-1])) if x is not 'end']
        
        var_names_extensions.append(var_num_rule)
        var_names_extensions.append(var_max_rule)
        var_names_extensions += variable_list_rules
        
        for i in range(user_var_max - 1, correct_var_max - 1):
            var_names_extensions.append(Rule([Literal_variable(VARIABLE_POOL[i])], []))
        
        user_program += var_names_extensions
    
    user_program += declarations
        
    # for each in user_program:
    #     print(each)
    return user_program, revisable_rules

def main():
    generate_declarations()
    
    
if __name__ == '__main__':
    main()