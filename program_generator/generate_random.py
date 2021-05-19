import os
import sys
import glob
import random

FOLDER_NAME = 'random_programs'
PROGRAMS = 20
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

def generateProgram(objective, max_rules, max_body_length, max_variables, predicates, background):
    prog_length = random.randint(1, max_rules)
    prog = []
    
    while len(prog) < prog_length:
        rule = generateRule(objective, max_body_length, max_variables, predicates)
        
        if rule not in prog:
            prog.append(rule)
        
    full_program = JOIN_RULES.join(prog + background)
    
    return full_program, prog

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

    traces = set()
    max_tries = PROGRAMS * 3
    
    while len(traces) < PROGRAMS and max_tries > 0:
        max_tries -= 1
        full_program, program = generateProgram(objective, max_rules, max_body_length, max_variables, predicates, background)
        prog_trace = ''.join(program)

        if not prog_trace in traces:
            f = open('{}/random_{}.lp'.format(FOLDER_NAME, str(len(traces) + 1)), 'w')
            f.write(full_program)
            f.close()
            traces.add(prog_trace)
            
    
def main(argv):
    if (len(argv) == 1):
        text = None
        try:
            f = open(argv[0], 'r')
            text = f.read().split('\n')
            f.close()
                        
            if not os.path.exists(FOLDER_NAME):
                os.makedirs(FOLDER_NAME)
                
            existing_files = glob.glob(FOLDER_NAME + '/*')
            for each in existing_files:
                os.remove(each)
                
            parseSpecFile(text)
        except Exception as e:
            print(e)
    else:
        print('Please provide a spec file.')
    
if __name__ == '__main__':
    main(sys.argv[1:])