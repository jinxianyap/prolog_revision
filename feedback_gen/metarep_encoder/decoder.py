from .classes import *
from .parser import *
from .helper import *
import random

def generate_clause(clause):
    if len(clause.body) == 0:
        return clause.head + '.'
    else:
        return '{} :- {}.'.format(clause.head, join(clause.body))
            

def decode(program):
    rules = {}
    ordering_tuples = []
    orderings = []
    ordered_rules = []
    random.shuffle(program)
    
    for each in program:
        head = each.head[0]
        
        if isinstance(head, Literal_order):
            ordering_tuples.append((head.rule_id_1, head.rule_id_2))
            continue
        
        if not (isinstance(head, Literal_head) or isinstance(head, Literal_pbl) or isinstance(head, Literal_nbl)):
            continue
            
        rule_id = head.rule_id
        
        if rule_id not in rules:
            rules[rule_id] = ProcessingRule(rule_id, None, [], None, None, None)
            
        if isinstance(head, Literal_head):
            rule = rules[rule_id]
            rule.head = head.literal.__str__()
        elif isinstance(head, Literal_pbl):
            rule = rules[rule_id]
            body = rule.body
            if int(head.index) - 1 > len(body):
                body.append(head.literal.__str__())
            else:
                body.insert(int(head.index) - 1, head.literal.__str__())
            rule.body = body
        elif isinstance(head, Literal_nbl):
            rule = rules[rule_id]
            body = rule.body
            body_string = '\+ ' + head.literal.__str__()
            body.insert(int(head.index) - 1, body_string)
            rule.body = body
            
    # determining the ordering of rules
    while len(ordering_tuples) > 0:
        (fst, snd) = ordering_tuples.pop(0)
        
        if len(orderings) == 0:
            orderings = [fst, snd]
        else:
            if fst in orderings and snd not in orderings:
                idx = orderings.index(fst)
                orderings.insert(idx + 1 , snd)
            elif fst not in orderings and snd in orderings:
                idx = orderings.index(snd)
                orderings.insert(idx, fst)
            else:
                ordering_tuples.append((fst, snd))
                  
    for each in orderings:
        if each not in rules:
            continue
        ordered_rules.append(generate_clause(rules[each]))

    return ordered_rules