import sys
import subprocess
import functools
from metarep_encoder.encoder import encode, generateVarVals, generateStaticRules
from metarep_encoder.fault_localiser import find_erroneous_rules, get_answer_set
from metarep_encoder.declarations_gen import generate_declarations
from metarep_encoder.rule_mapping import *
from metarep_encoder.constants import *
from tr_ilasp.revision import revise_program, revisableTheory

def generate_revisable_program(file_name, loop):
    correct_body_literals, correct_rule_ids, correct_rule_lengths, correct_var_max, correct_variables, correct_ground_constants, _, _, _, correct_program = encode(file_name, 'correct.las')
    user_body_literals, user_rule_ids, user_rule_lengths, user_var_max, user_variables, user_ground_constants, var_dicts, reorder_naf, static_rules, user_program = encode(file_name.replace('.lp', '_user.lp'), 'user.las')
    
    if reorder_naf:
        return Output_type.REORDER_NAF, REORDER_NAF

    incorrect_arities = find_incorrect_arities(correct_body_literals, user_body_literals)
    if len(incorrect_arities) > 0:
        msg = INCORRECT_ARITIES + '{}.'.format(incorrect_arities)
        print(msg)
        return Output_type.INCORRECT_ARITIES, msg
        
    rule_mapping, syntax_score, correct_rules_grouped, user_rules_grouped = generate_mapping(correct_program, user_program)
    # print(rule_mapping)

    correct_excluded, user_included, errors, revisions_data, answer_set = find_erroneous_rules(rule_mapping, correct_rules_grouped, user_rules_grouped)
    # print(errors)
    # print(revisions_data)
    semantic_errors = sum([len(errors[each][0]) + len(errors[each][1]) for each in errors])
    semantics_score = 1 - (semantic_errors / len(answer_set))
    
    
    if (syntax_score == 1 and semantic_score == 1) or len(errors) == 0:
        msg = 'User program gives expected results. No revision needed.'
        print(msg)
        return Output_type.NO_REVISION, msg
    
    revisable_program, marked_rules, new_rules = generate_declarations(errors, revisions_data, rule_mapping, answer_set, correct_body_literals, correct_rule_ids, correct_var_max, correct_variables, correct_ground_constants, correct_program, user_body_literals, user_rule_ids, user_var_max, user_variables, user_ground_constants, user_program)

    revisable_program = static_rules + revisable_program
    
    dest = open('revisable.las', 'w')
    for each in revisable_program:
        dest.write(each.__str__() + '\n')
    dest.close()    
    
    return Output_type.REVISED, correct_program, user_program, correct_excluded, user_included, (syntax_score, semantics_score), revisable_program, var_dicts, user_rule_lengths, marked_rules, list(errors.keys()), new_rules

# ------------------------------------------------------------------------------
#  Parse Revised Theories        

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
    literals = []
    r_id = None
    pos = None

    for each in heads:
        if each.val == 'head':
            head_elems = each.children
            rule_id = head_elems[0].val
            literal = parse_literal_node(head_elems[1])
            var_vals = parse_var_vals_node(head_elems[2])
            
            head_literal = Literal_head(rule_id, literal, var_vals)
            literals.append(head_literal)
            
            if r_id is None :
                r_id = rule_id
            else:
                assert(r_id == rule_id)
            pos = 'head'   
        else:
            head_elems = each.children
            # assume each.val == pbl or each.val == nbl
            rule_id = head_elems[0].val
            index = head_elems[1].val
            literal = parse_literal_node(head_elems[2])
            var_vals = parse_var_vals_node(head_elems[3])
            
            bl = Literal_pbl(rule_id, index, literal, var_vals) if each.val == 'pbl' else Literal_nbl(rule_id, index, literal, var_vals)
            literals.append(bl)
            if r_id is None and pos is None:
                r_id = rule_id
                pos = index
            else:
                assert(r_id == rule_id)
                assert(pos == index)
                
    return r_id, pos, literals
    
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
    # assert_type_choice(revision, Literal_pbl, Literal_nbl)
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
    
    if isinstance(revision, Literal_head):
        revision.args = [revision.rule_id, revision.literal, revision.var_vals]
    else:
        revision.args = [revision.rule_id, revision.index, revision.literal, revision.var_vals]
    return revision        
    
def interpret_revisions(var_dicts, user_rule_lengths, marked_rules, parsed_revisions):
    # print(var_dicts)
    # print(marked_rules)
    # print(parsed_revisions)
    feedback_text = []

    for rule_id in marked_rules:
        deleted_body = 0

        for index in marked_rules[rule_id]:
            rule, is_extend = marked_rules[rule_id][index]
            head = rule.head[0]
            index = head.index

            if rule_id in parsed_revisions and index in parsed_revisions[rule_id]:
                revision = parsed_revisions[rule_id][index]
                translated = [translate_revision_variables(rule_id, var_dicts[rule_id], x) for x in revision]
                literal = translated[0].literal.__str__()
                
                if isinstance(translated[0], Literal_nbl):
                    literal = '\+ ' + literal
                    
                if len(translated) == 1:
                    text = 'Rule: {}, Index: {} - {} with \'{}\'.'.format(rule_id, index, 'Extend' if is_extend else 'Replace', literal)
                    feedback_text.append(text)
                else:
                    # to be completed
                    text = 'Rule: {}, Index: {} - Replace with \'{}\'.'.format(rule_id, index, literal)
                    feedback_text.append(text)
            else:
                text = 'Rule: {}, Index: {} - Delete body literal.'.format(rule_id, index)
                deleted_body += 1
                feedback_text.append(text)
                
            if deleted_body == user_rule_lengths[rule_id]:
                text = 'Rule: {} - Delete rule.'.format(rule_id)
                feedback_text.append(text)
                
    return feedback_text

def interpret_revisions_new_rule(new_rules):     
    feedback_text = []    
    for rule_id in new_rules:
        rules = new_rules[rule_id]
        for i in range(len(rules)):
            if i == 0:
                # head rule
                text = 'Rule: {} - Add rule with head \'{}\'.'.format(rule_id, (rules[i].head[0].literal).__str__())
                feedback_text.append(text)
            else:
                text = 'Rule: {}, Index: {} - Extend with \'{}\'.'.format(rule_id, str(i), (rules[i].head[0].literal).__str__())
                feedback_text.append(text)
    return feedback_text        

# ------------------------------------------------------------------------------
#  Apply revisions

def remove_revisable_declarations(program):
    for each in program:
        each.make_non_revisable()
        
def find_rule_index(program, rule_id):
    for i, each in enumerate(program):
        if isinstance(each, Rule):
            head = each.head[0]
            if isinstance(head, Literal_rule):
                if head.rule_id == rule_id:
                    return i
                
def generate_grounding(args):
    return [Literal_ground(x) for x in args if is_variable(x)]              
            
def apply_revisions(program, marked_rules, user_rule_lengths, parsed_revisions, new_rule=False):
    for rule_id in parsed_revisions:
        if rule_id is None: continue
        for index in parsed_revisions[rule_id]:
            marked_info = marked_rules[rule_id][index]
            rule_index = find_rule_index(program, rule_id)
            
            if marked_info[1]: # extension of body
                head = parsed_revisions[rule_id][index][0]
                body = generate_grounding(head.literal.args)
                rule = Rule([head], body)
                program.insert(rule_index + 1 + int(index), rule)
            else: # replacement
                head = parsed_revisions[rule_id][index][0]
                body = generate_grounding(head.literal.args)
                rule = Rule([head], body)
                program[rule_index + 1 + int(index)] = rule
            
            marked_rules[rule_id].pop(index)
            if len(marked_rules[rule_id]) == 0:
                marked_rules.pop(rule_id)
                
    for rule_id in marked_rules:
        indexes = sorted(marked_rules[rule_id], reverse=True)
        for index in indexes:
            rule_index = find_rule_index(program, rule_id)
            program.pop(rule_index + 1 + int(index))
            
        # whole rule should be deleted
        if len(indexes) == user_rule_lengths[rule_id]:
            program.pop(rule_index + 1)
            program.pop(rule_index)
            
    save_revised_program(program)
                        
def apply_new_rules_revisions(program, new_rules):
    insertion = []
    for rule_id in new_rules:
        rule_declaration = Rule([Literal_rule(rule_id)], [])
        insertion.append(rule_declaration)
        
        rules = new_rules[rule_id]
        remove_revisable_declarations(rules)
        insertion += rules
        
        prev_id = int(rule_id.split('r')[1]) - 1
        ordering = Rule([Literal_order('r' + str(prev_id), rule_id)], [])
        insertion.append(ordering)    
    
    index = next(i for (i, rule) in enumerate(program) if isinstance(rule.head[0], Literal_order))
    
    for each in insertion:
        program.insert(index, each)
        index += 1
        
    save_revised_program(program)
        
def save_revised_program(program):
    dest = open('revised.las', 'w')
    rules = generateStaticRules() + program
    for rule in rules:
        dest.write(rule.__str__() + '\n')
    dest.write('#show in_AS/3.')
    dest.close()
    
def check_revision_success():
    meta_correct, correct = get_answer_set('correct.las')
    meta_revised, revised = get_answer_set("revised.las")
    
    correct_excluded = [x for x in correct if x not in revised]
    if len(correct_excluded) > 0:
        print('Positive examples not covered:')
        [print(x) for x in correct_excluded]
    user_included = [x for x in revised if x not in correct]
    if len(user_included) > 0:
        print('Negative examples covered:')
        [print(x) for x in user_included]
        
    if len(correct_excluded) == 0 and len(user_included) == 0:
        print('Revision result: Success')
        return True
    else:
        print('Revision result: Failure')
        return False
    
def calculate_similarity_score(syntax, semantics, revisions):
    SYNTAX = 0.2
    SEMANTICS = 0.5
    REVISIONS = 0.3
    
    total = (syntax * SYNTAX) + (semantics * SEMANTICS) + (revisions * REVISIONS)
    return '%.3f' % total
            
# ------------------------------------------------------------------------------
         
def main(argv):
    if argv[0] == '--revise-only':
        revise_program('revisable.las')
        return
    
    loop = True
    
    output = generate_revisable_program(argv[0], loop)
    
    if output[0] == Output_type.REVISED:
        output_type, correct_program, user_program, correct_excluded, user_included, score, revisable, var_dicts, user_rule_lengths, marked_rules, revisable_rule_ids, new_rules = output
        
        remove_revisable_declarations(user_program)

        if len(new_rules) > 0: # if user should add rules, suggest first and have them make changes
            feedback_text = interpret_revisions_new_rule(new_rules)
            
            apply_new_rules_revisions(user_program, new_rules)
            success = check_revision_success() 
            revision_ratio = 1 - len(feedback_text) / sum([x[1] + 1 for x in user_rule_lengths.items()]) 
            similarity_score = calculate_similarity_score(score[0], score[1], revision_ratio)
            
            return Output_type.NEW_RULES, correct_excluded, user_included, similarity_score, revisable_rule_ids, feedback_text, success
        else:
            revised = revise_program('revisable.las')
            
            if revised is None:
                return Output_type.UNSATISFIABLE, UNSATISFIABLE
                        
            parsed_revisions = parse_revised_theories(revised)
            feedback_text = interpret_revisions(var_dicts, user_rule_lengths, marked_rules, parsed_revisions)

            revision_ratio = 1 - len(feedback_text) / sum([x[1] + 1 for x in user_rule_lengths.items()]) 
            similarity_score = calculate_similarity_score(score[0], score[1], revision_ratio)
            
            apply_revisions(user_program, marked_rules, user_rule_lengths, parsed_revisions)
            success = check_revision_success()
            
            return output_type, correct_excluded, user_included, similarity_score, revisable_rule_ids, feedback_text, success
    else:
        return output
 
    
if __name__ == '__main__':
    main(sys.argv[1:])