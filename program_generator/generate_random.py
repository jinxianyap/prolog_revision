import sys
import random

PROGRAMS = 3
VARIABLES = ['X', 'Y', 'Z', 'A', 'B']
JOIN_ELEMS = ', '
JOIN_RULES = '\n'

def generatePredicate(name, arity, variables):
    args = random.sample(variables, arity)
    pred_string = '{}({})'.format(name, JOIN_ELEMS.join(args))
    return pred_string

def generateRule(objective, max_body_length, max_variables, predicates):
    variables = VARIABLES[0:max_variables]
    head_string = generatePredicate(objective, predicates[objective], variables)
        
    body_length = random.randint(1, max_body_length)
    body = []
    
    while len(body) < body_length:
        pred_name, arity = random.choice(list(predicates.items()))
        
        pred_string = generatePredicate(pred_name, arity, variables)
        if pred_string not in body and pred_string != head_string:
            body.append(pred_string)
        

    rule = '{} :- {}.'.format(head_string, JOIN_ELEMS.join(body))
    
    return rule

def generateProgram(i, objective, max_rules, max_body_length, max_variables, predicates, background):
    prog_length = random.randint(1, max_rules)
    prog = []
    
    while len(prog) < prog_length:
        rule = generateRule(objective, max_body_length, max_variables, predicates)
        prog.append(rule)
        
    program = JOIN_RULES.join(prog + background)
    f = open('random_{}.lp'.format(i), 'w')
    f.write(program)
    f.close()

def parseSpecFile(file_text):
    if file_text is None:
        return
    
    background = []
    objective = None
    max_rules = None
    max_body_length = None
    max_variables = None
    predicates = {}
    
    bg = False
    pred = False

    for each in file_text:
        if len(each) == 0: continue
        
        if each.startswith('# BG:'):
            bg = True
        elif each.startswith('# OBJ:'):
            bg = False
            objective = each[6:].strip()
        elif each.startswith('# MAX_RULES:'):
            max_rules = int(each[12:].strip())
        elif each.startswith('# MAX_BODY_LENGTH:'):
            max_body_length = int(each[18:].strip())
        elif each.startswith('# MAX_VARIABLES:'):
            max_variables = int(each[16:].strip())
        elif each.startswith('# PREDICATES:'):
            pred = True
        elif bg:
            background.append(each.strip())
        elif pred:
            split = each.split(':')
            predicates[split[0].strip()] = int(split[1].strip())

    # print(background)
    # print(max_rules)
    # print(max_body_length)
    # print(max_variables)
    # print(predicates)
    
    for i in range(PROGRAMS):
        generateProgram(str(i + 1), objective, max_rules, max_body_length, max_variables, predicates, background)
    
def main(argv):
    if (len(argv) == 1):
        text = None
        try:
            f = open(argv[0], 'r')
            text = f.read().split('\n')
            f.close()
        except:
            print('Spec file not found.')
        
        parseSpecFile(text)
    else:
        print('Please provide a spec file.')
    
if __name__ == '__main__':
    main(sys.argv[1:])