import os
from metarep_encoder.encoder import *

class DerivableFact:
    def __init__(self, rule_id, literal, variables_dict, original):
        self.rule_id = rule_id
        self.literal = literal
        self.variables = variables_dict
        self.original_str = original
        self.match_exists = False
    def __repr__(self):
        return 'DerivableFact()'
    def __str__(self):
        return 'in_AS(' + ', '.join([self.literal, self.rule_id, self.variables.__str__()]) + ')'   
    def equal_to(self, other):
        return self.rule_id == other.rule_id and self.literal == other.literal and self.variables == other.variables

def variables_to_dict(variables):
    variables = [x.split(')')[0] for x in variables.split('var_val(')[1:]]
    var_dict = {}
    for each in variables:
        split = each.split(',')
        var_dict[split[1]] = split[2]
    return var_dict

def transform(ori):
    args = ori[6:-1]
    literal = None
    rule_id = None
    variables = None
    stack = []
    ptr = 0

    while literal is None:
        if args[ptr] == ',' and len(stack) == 0:
            literal_found = True
            literal = args[:ptr]
        elif args[ptr] == '(':
            stack.append(args[ptr])
        elif args[ptr] == ')' and len(stack) > 0:
            stack.pop()
        ptr += 1
    
    args = args[ptr:]
    ptr = 0
    
    while rule_id is None:
        if args[ptr] == ',':
            rule_id = args[:ptr]
            variables = args[ptr + 1:]
            break
        ptr += 1
        
    return DerivableFact(rule_id, literal, variables_to_dict(variables), ori)
    

def get_answer_set(filename):
    stream = os.popen('clingo ' + filename)
    output = stream.read()
    lines = output.split(' ')
    meta_answer_set = []
    answer_set = []
    for each in lines:
        if each[:5] == 'in_AS':
            fact_obj = transform(each)
            meta_answer_set.append(fact_obj)
            answer_set.append(fact_obj.literal)
    return meta_answer_set, answer_set

def group_by_rule_id(answer_set):
    groups = {}
    for each in answer_set:
        if not each.rule_id in groups:
            groups[each.rule_id] = set()
        groups[each.rule_id].add(each)
    return groups
        

def identify_discrepancies(set_a, set_b):
    for i in set_a:
        for j in set_b:
            if i.equal_to(j):
                i.match_exists = True
                j.match_exists = True
    
    set_a = [x for x in set_a if not x.match_exists]  
    set_b = [x for x in set_b if not x.match_exists]            
    
    return set_a, set_b

def find_erroneous_rules():
    meta_correct, correct = get_answer_set('correct.las')
    meta_user, user = get_answer_set("user.las")
    
    # Semantic checking
    correct_excluded = [x for x in correct if x not in user]
    if len(correct_excluded) > 0:
        print('Positive examples not covered:')
        [print(x) for x in correct_excluded]
    user_included = [x for x in user if x not in correct]
    if len(user_included) > 0:
        print('Negative examples covered:')
        [print(x) for x in user_included]
    
    # Syntactic/Declarative checking
    # cannot just check with rule id, need some measure of similarity between rules
    grouped_correct = group_by_rule_id(meta_correct)
    grouped_user = group_by_rule_id(meta_user)
    
    discrepancies = {}
    for each in grouped_correct.keys():
        rem_correct, rem_user = identify_discrepancies(grouped_correct[each], grouped_user[each])  
        if len(rem_correct) > 0 or len(rem_user) > 0:
            discrepancies[each] = (rem_correct, rem_user)
            print('Consider modifying rule {}:'.format(each))
            print('-- {} positive example(s) not covered: {}'.format(len(rem_correct), '  '.join([x.__str__() for x in rem_correct])))
            print('-- {} negative example(s) included: {}'.format(len(rem_user), '  '.join([x.__str__() for x in rem_user])))
    
    return discrepancies, meta_correct

# def main():
#     find_erroneous_rules()
    
    
# if __name__ == '__main__':
#     main()