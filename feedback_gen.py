import sys
import subprocess
from metarep_encoder.encoder import encode, generateVarVals
from metarep_encoder.fault_localiser import find_erroneous_rules
from metarep_encoder.declarations_gen import generate_declarations
from metarep_encoder.rule_mapping import *
from metarep_encoder.messages import *
from tr_ilasp.revision import revise_program, revisableTheory

def generate_revisable_program(file_name):
    correct_body_literals, correct_rule_ids, correct_var_max, correct_variables, correct_ground_constants, _, _, correct_program = encode(file_name, 'correct.las')
    user_body_literals, user_rule_ids, user_var_max, user_variables, user_ground_constants, var_dicts, static_rules, user_program = encode(file_name.replace('.lp', '_user.lp'), 'user.las')

    incorrect_arities = find_incorrect_arities(correct_body_literals, user_body_literals)
    if len(incorrect_arities) > 0:
        msg = INCORRECT_ARITIES + '{}.'.format(incorrect_arities)
        print(msg)
        return Output_type.INCORRECT_ARITIES, msg
        
    rule_mapping, score, correct_rules_grouped, user_rules_grouped = generate_mapping(correct_program, user_program)
    print('Similarity score: %s' % str(score))
    correct_excluded, user_included, errors, revisions_data, answer_set = find_erroneous_rules(rule_mapping, correct_rules_grouped, user_rules_grouped)
    # print(errors)
    # print(revisions_data)
    if str(score) == '1.000' or len(errors) == 0:
        msg = 'User program gives expected results. No revision needed.'
        print(msg)
        return Output_type.NO_REVISION, msg
    
    revisable_program, marked_rules = generate_declarations(errors, revisions_data, rule_mapping, answer_set, correct_body_literals, correct_rule_ids, correct_var_max, correct_variables, correct_ground_constants, correct_program, user_body_literals, user_rule_ids, user_var_max, user_variables, user_ground_constants, user_program)
    
    revisable_program = static_rules + revisable_program
    
    dest = open('revisable.las', 'w')
    for each in revisable_program:
        dest.write(each.__str__() + '\n')
    dest.close()    
    
    return Output_type.REVISED, correct_excluded, user_included, score, revisable_program, var_dicts, marked_rules, list(errors.keys())

def parse_revised_theories(theories):
    parsed = {}
    for each in theories.values():
        rule_id, index, revisions = parse_theory(each)
        if rule_id in parsed:
            temp = parsed[rule_id]
            temp[index] = revisions
        else:
            temp = {}
            temp[index] = revisions
            parsed[rule_id] = temp
            
    return parsed

def parse_theory(theory):
    assert_type(theory, revisableTheory)
    heads = theory.head.values()
    bls = []
    r_id = None
    pos = None

    for each in heads:
        head_elems = each.children
        # assume each.val == pbl or each.val == nbl
        rule_id = head_elems[0].val
        index = head_elems[1].val
        literal = parse_literal_node(head_elems[2])
        var_vals = parse_var_vals_node(head_elems[3])
        
        bl = Literal_pbl(rule_id, index, literal, var_vals) if each.val == 'pbl' else Literal_nbl(rule_id, index, literal, var_vals)
        bls.append(bl)
        if r_id is None and pos is None:
            r_id = rule_id
            pos = index
        else:
            assert(r_id == rule_id)
            assert(pos == index)
            
    return r_id, pos, bls
    
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
    
def translate_revision_variables(rule_id, var_dict, revision):
    assert_type_choice(revision, Literal_pbl, Literal_nbl)
    vv = revision.var_vals
    replacements = {}
    updated_var_pairs = []

    while vv != 'end':
        arg = vv.arg
        for each in var_dict:
            if var_dict[each] == arg.variable:
                updated_var_pairs.append((arg.variable, each))
                replacements[arg.term] = each   
        vv.arg = arg
        vv = vv.others
    revision.var_vals = generateVarVals(rule_id, updated_var_pairs)    

    literal = revision.literal
    for i in range(len(literal.args)):
        arg = literal.args[i]
        if arg in replacements:
            literal.args[i] = replacements[arg]
    revision.literal = literal
    
    revision.args = [revision.rule_id, revision.index, revision.literal, revision.var_vals]
    return revision        
    
def interpret_revisions(var_dicts, marked_rules, parsed_revisions):
    # print(var_dicts)
    # print(marked_rules)
    # print(parsed_revisions)
    feedback_text = []

    for rule_id in marked_rules:
        for index in marked_rules[rule_id]:
            rule, extension = marked_rules[rule_id][index]
            head = rule.head[0]
            index = head.index
            
            if rule_id in parsed_revisions and index in parsed_revisions[rule_id]:
                revision = parsed_revisions[rule_id][index]
                translated = [translate_revision_variables(rule_id, var_dicts[rule_id], x) for x in revision]
                literal = translated[0].literal.__str__()
                
                if isinstance(translated[0], Literal_nbl):
                    literal = '\+ ' + literal
                    
                if len(translated) == 1:
                    text = 'Rule: {}, Index: {} - {} with \'{}\'.'.format(rule_id, index, 'Extend' if extension else 'Replace', literal)
                    feedback_text.append(text)
                else:
                    # to be completed
                    text = 'Rule: {}, Index: {} - Replace with \'{}\'.'.format(rule_id, index, literal)
                    feedback_text.append(text)
            else:
                text = 'Rule: {}, Index: {} - Delete body literal.'.format(rule_id, index)
                feedback_text.append(text)
    return(feedback_text)            

def main(argv):
    if argv[0] == '--revise-only':
        revise_program('revisable.las')
        return
    
    output = generate_revisable_program(argv[0])
    
    if output[0] == Output_type.REVISED:
        output_type, correct_excluded, user_included, score, revisable, var_dicts, marked_rules, revisable_rule_ids = output
        revised = revise_program('revisable.las')
        
        if revised is None:
            return Output_type.UNSATISFIABLE, UNSATISFIABLE
                    
        parsed_revisions = parse_revised_theories(revised)
        feedback_text = interpret_revisions(var_dicts, marked_rules, parsed_revisions)
                
        return output_type, correct_excluded, user_included, score, revisable_rule_ids, feedback_text
    else:
        return output
 
    
if __name__ == '__main__':
    main(sys.argv[1:])