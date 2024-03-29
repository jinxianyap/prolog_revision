from .classes import *
from .helper import *

def compare_literals(a, b):
    if isinstance(a, Literal) and isinstance(b, Literal):
        sim, diff = a.compare_to(b)
        return sim, diff     
    else:
        return 0, 1

def compare_rules(a, b):
    similarity = 0
    differences = 0
    head_similarity, head_differences = compare_literals(a.head[0], b.head[0])
    similarity += head_similarity
    differences += head_differences

    if len(a.body) == len(b.body):
        similarity += 1
    else:
        differences += 1
    
    body_lits_a = set([x.name for x in a.body])
    body_lits_b = set([x.name for x in b.body])
    
    similarity += len(body_lits_a.intersection(body_lits_b))
    differences += len(body_lits_a.difference(body_lits_b)) + len(body_lits_b.difference(body_lits_a))
        
    for i in range(min(len(a.body), len(b.body))):
        sim, diff = compare_literals(a.body[i], b.body[i])
        similarity += sim
        differences += diff
    
    return similarity, differences

def assign_similarity(a, b):
    similarity = 0
    differences = 0
    
    if a[0].head[0].literal.name != b[0].head[0].literal.name:
        differences += 1
        return similarity, differences
    
    if len(a) == len(b):
        similarity += 1
    else:
        differences += 1
        
    lits_a = set([x.head[0].literal for x in a if isinstance(x.head[0], Literal_pbl) or isinstance(x.head[0], Literal_nbl)])
    lits_b = set([x.head[0].literal for x in a if isinstance(x.head[0], Literal_pbl) or isinstance(x.head[0], Literal_nbl)])
    
    similarity += len(lits_a.intersection(lits_b))
    differences += len(lits_a.difference(lits_b)) + len(lits_b.difference(lits_a))
    
    for i in range(min(len(a), len(b))):
        sim, diff = compare_rules(a[i], b[i])
        similarity += sim
        differences += diff
        
    return similarity, differences

def identify_rules(program):
    rule_start = {}
    grouped_rules = {}
    curr_rule = None
    for i in range(len(program)):
        rule = program[i].head[0]
        if isinstance(rule, Literal_rule):
            rule_start[rule.rule_id] = (i + 1, None)
            curr_rule = rule.rule_id
        elif (isinstance(rule, Literal_head) or \
            isinstance(rule, Literal_pbl) or \
            isinstance(rule, Literal_nbl)) and \
            curr_rule is not None:
            ori = rule_start[curr_rule]
            rule_start[curr_rule] = (ori[0], i+1)
            
    for each in rule_start:
        (start, end) = rule_start[each]
        grouped_rules[each] = program[start:end]
        
    return rule_start, grouped_rules

def generate_similarity_matrix(correct, correct_indexes, user, user_indexes):
    matrix = {}

    for i in correct_indexes:
        inner = {}
        c_i = correct_indexes[i]
        for j in user_indexes:
            u_i = user_indexes[j]
            inner[j] = assign_similarity(correct[c_i[0]:c_i[1]], user[u_i[0]:u_i[1]])
        matrix[i] = inner
        
    return matrix

def generate_mapping(correct, user):
    correct_indexes, correct_rules_grouped = identify_rules(correct)
    user_indexes, user_rules_grouped = identify_rules(user)
    
    matrix = generate_similarity_matrix(correct, correct_indexes, user, user_indexes)
    mappings = {}
    total_sim = 0
    total_diff = 0
    model_excess = 0

    for each in matrix:
        score = -1
        index = None
        for entry in matrix[each]:
            sim, diff = matrix[each][entry]
            if sim > score and sim > diff:
                score = sim
                index = entry 
        
        if index is None:
            model_excess += 1
            index = 'r' + str(len(user_indexes) + model_excess)
            mappings[each] = index
        else:
            mappings[each] = index
            sim, diff = matrix[each][index]
            total_sim += sim
            total_diff += diff
    
    score = total_sim / (total_sim + total_diff)
    
    # handle unmatched user rules    
    unmatched_user = 0
    for j in user_indexes:
        if j not in mappings.values():
            unmatched_user += 1 
    score -= score * min((unmatched_user + model_excess) / len(correct_indexes), 1)
    # score = '%.3f' % score
            
    return mappings, score, correct_rules_grouped, user_rules_grouped
            