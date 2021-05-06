from metarep_encoder.classes import *
from metarep_encoder.helper import *
# DECAY = 0.8

def compare_terms(a, b):
    # similarity = 0
    # differences = 0
    # if isinstance(a, str) and isinstance(b, str):
    #     similarity += 1
    #     if is_variable(a) and is_variable(b):
    #         similarity += 1
    #         if a == b: 
    #             similarity += 1
    #         else:
    #             differences += 1
    #     elif not is_variable(a) and not is_variable(b):
    #         similarity += 1
    #         if a == b: 
    #             similarity += 1
    #         else:
    #             differences += 1
    #     else:
    #         differences += 1
    if isinstance(a, Literal) and isinstance(b, Literal):
        sim, diff = a.compare_to(b)
        return sim, diff     
    else:
        return 0, 1

def compare_rules(a, b):
    similarity = 0
    differences = 0
    head_similarity, head_differences = compare_terms(a.head[0], b.head[0])
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
        sim, diff = compare_terms(a.body[i], b.body[i])
        similarity += sim
        differences += diff
    
    return similarity, differences

def assign_similarity(a, b):
    similarity = 0
    differences = 0
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

    for each in matrix:
        score = -1
        index = None
        for entry in matrix[each]:
            sim, diff = matrix[each][entry]
            if sim > score:
                score = sim
                index = entry 
            
        mappings[each] = index
        sim, diff = matrix[each][index]
        total_sim += sim
        total_diff += diff
        
    score = '%.3f' % (total_sim / (total_sim + total_diff))
    return mappings, score, correct_rules_grouped, user_rules_grouped
            