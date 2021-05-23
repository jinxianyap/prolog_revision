import os
import sys
import glob
import random

FOLDER_NAME = 'random_programs'
PROGRAMS = 50
VARIABLES = ['X', 'Y', 'Z', 'A', 'B']
JOIN_ELEMS = ', '
JOIN_RULES = '\n'

def generatePredicate(name, arity, variables, head=False):
    args = random.sample(variables, arity)
    if head:
        args = sorted(args)
    pred_string = '{}({})'.format(name, JOIN_ELEMS.join(args))
    return pred_string, args

def generateRule(objective, max_body_length, max_variables, predicates):
    variables = VARIABLES[0:max_variables]
    head_string, head_args = generatePredicate(objective, predicates[objective], variables, head=True)
        
    body_length = random.randint(1, max_body_length)
    body = []
    variables_used = set(head_args)
    
    while len(body) < body_length:
        pred_name, arity = random.choice(list(predicates.items()))
        
        pred_string, args = generatePredicate(pred_name, arity, variables)
        if pred_string not in body and pred_string != head_string:
            body.append(pred_string)
            variables_used.update(args)       

    rule = '{} :- {}.'.format(head_string, JOIN_ELEMS.join(body))
    
    return rule, len(body), variables_used

def generateProgram(objective, max_rules, max_body_length, max_variables, predicates, background):
    prog_length = random.randint(1, max_rules)
    prog = []
    body_length = 0
    variables = set()
    
    while len(prog) < prog_length:
        rule, body_used, variables_used = generateRule(objective, max_body_length, max_variables, predicates)
        
        if rule not in prog:
            prog.append(rule)
            body_length = max(body_length, body_used)
            variables.update(variables_used)
    
    program_data = (len(prog), body_length, len(variables))
    full_program = JOIN_RULES.join(prog + background)
    
    return full_program, prog, program_data

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
        full_program, program, program_data = generateProgram(objective, max_rules, max_body_length, max_variables, predicates, background)
        prog_trace = ''.join(program)

        if not prog_trace in traces:
            f = open('{}/random_{}.lp'.format(FOLDER_NAME, str(len(traces) + 1)), 'w')
            f.write(full_program)
            f.write('\n')
            f.write('${}-{}-{}'.format(program_data[0], program_data[1], program_data[2]))
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