import subprocess
import clingo
from .encoder import *

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
        return 'in_AS(' + ', '.join([self.literal.__str__(), self.rule_id, self.variables.__str__()]) + ')'   
    def equal_to(self, other):
        sim, diff = self.literal.compare_to(other.literal)
        return sim > 0 and diff == 0 and self.variables == other.variables

def variables_to_dict(variables):
    variables = [x.split(')')[0] for x in variables.split('var_val(')[1:]]
    var_dict = {}
    for each in variables:
        split = each.split(',')
        var_dict[split[1]] = split[2]
    return var_dict

def transform(ori, mapping=None):
    args = ori[6:-1]
    literal = None
    rule_id = None
    variables = None
    ori_str = None
    stack = []
    ptr = 0

    while literal is None:
        if args[ptr] == ',' and len(stack) == 0:
            literal_found = True
            literal = args[:ptr]
            name = literal.split('(')[0]
            lit_args = literal.split('(')[1][:-1].split(',')
            literal = Literal(name, lit_args)
        elif args[ptr] == '(':
            stack.append(args[ptr])
        elif args[ptr] == ')' and len(stack) > 0:
            stack.pop()
        ptr += 1
    
    args = args[ptr:]
    ptr = 0
    
    while rule_id is None:
        if args[ptr] == ',':
            ori_rule_id = args[:ptr]
            rule_id = mapping[ori_rule_id] if mapping is not None else ori_rule_id
            ori_str = ori.replace(ori_rule_id, rule_id)
            variables = args[ptr + 1:]
            break
        ptr += 1
        
    return DerivableFact(rule_id, literal, variables_to_dict(variables), ori_str)    

def get_answer_set(filename, mapping=None):
    raw_answer_set = []
    
    ctl = clingo.Control(logger=lambda x, y: x)
    ctl.load(filename)
    ctl.ground([("base", [])])
    solving_result = ctl.solve(on_model=lambda m: raw_answer_set.extend(map(lambda x: x.__str__(), m.symbols(shown=True))))
        
    if not solving_result.satisfiable:
        raise Exception('Failed to solve answer set for {}.'.format(filename))
    
    meta_answer_set = []
    answer_set = []
    for each in raw_answer_set:
        if each[:5] == 'in_AS':
            fact_obj = transform(each, mapping)
            meta_answer_set.append(fact_obj)
            answer_set.append(fact_obj.literal.__str__())
    return meta_answer_set, answer_set

def group_by_rule_id(answer_set):
    groups = {}
    for each in answer_set:
        if not each.rule_id in groups:
            groups[each.rule_id] = set()
        groups[each.rule_id].add(each)
    return groups    

def identify_discrepancies(index, actual_AS, model_AS=None, user_AS=None):
    if model_AS is None:
        correct_excluded = list(set(user_AS[index]))
        correct_excluded = [x for x in correct_excluded if x.literal.__str__() not in actual_AS]
        return [], correct_excluded
    elif user_AS is None:
        return list(set(model_AS[index])), []
    else:
        set_a = model_AS[index] if index in model_AS else set()
        set_b = user_AS[index] if index in user_AS else set()
        
        for i in set_a:
            for j in set_b:
                if i.equal_to(j):
                    i.match_exists = True
                    j.match_exists = True

        set_a = [x for x in set_a if not x.match_exists]  
        set_b = [x for x in set_b if not x.match_exists and x.literal not in actual_AS]      

        return set_a, set_b

def identify_rule_discrepancies(index, model_rules=None, user_rules=None, mapping=None):
    # also enforces ordering of literals
    # position number of literals - literal names to use in modehs
    to_revise = {}
    i = 0
    # returns at each index of to_revise (literal, is_pbl, needs to be marked revisable)
    # for now tuple[2] is redundant
    if model_rules is None and user_rules is not None:
        user_rule = user_rules[index]
        while i < len(user_rule):
            if isinstance(user_rule[i].head[0], Literal_head):
                i += 1
                continue
            to_revise[str(i)] = (user_rule[i].head[0].literal, isinstance(user_rule[i].head[0], Literal_pbl), True)
            i += 1
    elif model_rules is not None and user_rules is not None:
        model_rule = model_rules[get_dict_key(mapping, index)]
        if index not in user_rules:
            while i < len(model_rule):
                if isinstance(model_rule[i].head[0], Literal_head):
                    i += 1
                    continue
                to_revise[str(i)] = (model_rule[i].head[0].literal, isinstance(model_rule[i].head[0], Literal_pbl), True)
                i += 1
        else:
            user_rule = user_rules[index]
            while i < max(len(model_rule), len(user_rule)):
                if i >= len(user_rule) and not isinstance(model_rule[i].head[0], Literal_head):
                    to_revise[str(i)] = (model_rule[i].head[0].literal, isinstance(model_rule[i].head[0], Literal_pbl), True)
                elif i >= len(model_rule) and not isinstance(user_rule[i].head[0], Literal_head):
                    to_revise[user_rule[i].head[0].index] = (user_rule[i].head[0].literal, isinstance(user_rule[i].head[0], Literal_pbl), True)
                else:
                    head_a = model_rule[i].head[0]
                    head_b = user_rule[i].head[0]
                    
                    if isinstance(head_a, Literal_head) or isinstance(head_b, Literal_head):
                        i += 1
                        continue
                    else:
                        sim, diff = head_a.compare_to(head_b)
                        if diff > 0:
                            to_revise[head_b.index] = (head_a.literal, isinstance(head_a, Literal_pbl), diff > 0)
                i += 1
    
    return to_revise

def find_erroneous_rules(mapping, correct_rules_grouped, user_rules_grouped):
    meta_correct, correct = get_answer_set('correct.las', mapping)
    print('Generated AS for correct program.')
    meta_user, user = get_answer_set("user.las")
    print('Generated AS for user program.')
    # print('.\n.\n.')
    
    # print(correct)
    # print(user)
    
    # Semantic checking
    correct_excluded = [x for x in correct if x not in user]
    # if len(correct_excluded) > 0:
    #     print('Positive examples not covered:')
    #     [print(x) for x in correct_excluded]
    user_included = [x for x in user if x not in correct]
    # if len(user_included) > 0:
    #     print('Negative examples covered:')
    #     [print(x) for x in user_included]
    
    # Syntactic/Declarative checking
    # remember that meta_correct rule ids have already been mapped!
    grouped_correct = group_by_rule_id(meta_correct)
    grouped_user = group_by_rule_id(meta_user)

    AS_discrepancies = {}
    revisions_data = {}

    for each in grouped_correct.keys():
        rem_correct, rem_user = identify_discrepancies(each, correct, grouped_correct, grouped_user)  
        if len(rem_correct) > 0 or len(rem_user) > 0:
            AS_discrepancies[each] = (rem_correct, rem_user)
            # print('Consider modifying rule {}:'.format(each))
            # print('-- {} positive example(s) not covered: {}'.format(len(rem_correct), '  '.join([x.literal.__str__() for x in rem_correct])))
            # print('-- {} negative example(s) included: {}'.format(len(rem_user), '  '.join([x.literal.__str__() for x in rem_user])))

            rule_discrepancies = identify_rule_discrepancies(each, correct_rules_grouped, user_rules_grouped, mapping)
            if len(rule_discrepancies) > 0:
                    revisions_data[each] = rule_discrepancies
                    
    # unmatched user rules
    for each in grouped_user.keys():
        if each not in mapping.values():
            rem_correct, rem_user = identify_discrepancies(each, correct, user_AS=grouped_user)
            if len(rem_correct) > 0 or len(rem_user) > 0:
                AS_discrepancies[each] = (rem_correct, rem_user)
                # print('Consider modifying rule {}:'.format(each))
                # print('-- {} negative example(s) included: {}'.format(len(rem_user), '  '.join([x.__str__() for x in rem_user])))
                
                rule_discrepancies = identify_rule_discrepancies(each, user_rules=user_rules_grouped)
                if len(rule_discrepancies) > 0:
                    revisions_data[each] = rule_discrepancies

    return correct_excluded, user_included, AS_discrepancies, revisions_data, meta_correct

# def main():
#     find_erroneous_rules()
    
    
# if __name__ == '__main__':
#     main()