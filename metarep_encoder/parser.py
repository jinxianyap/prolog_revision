from classes import *
from helper import *

def generateVarVals(constants, rule_id, variables):
    if len(constants) == 0:
        return 'end'
    else:
        return 'var_vals(var_val(' + ', '.join([rule_id, variables[0], constants[0]]) + '),' + generateVarVals(constants[1:], rule_id, variables[1:]) + ')'

def parseLiteral(rule_id, literal):
    literal = literal.replace(' ', '')
    split = literal.replace(')', '').split('(')
    args = split[1].split(',')
    constants = [x for x in args if x[0].islower()]
    variables = [x for x in args if x not in constants]

    return ProcessingLiteral(rule_id, literal, args), constants, variables

def parseRule(rule_text, index):
    rule_id = 'r' + str(index + 1)
    rule_text = rule_text[:-1].split(':-')
    head_text = rule_text[0]
    body_text = rule_text[1][1:] if len(rule_text) > 1 else None
    
    constants = []
    variables = []
    
    head_processing_literal, head_constants, head_variables = parseLiteral(rule_id, head_text)
    
    constants = mergeStacks(constants, head_constants)
    variables = mergeStacks(variables, head_variables)
    
    body_processing_literals = []
    if not body_text is None:
        body_text = splitConjunction(body_text)
        for body_literal in body_text:
            body_processing_literal, body_constants, body_variables = parseLiteral(rule_id, body_literal)
            body_processing_literals.append(body_processing_literal)
            constants = mergeStacks(constants, body_constants)
            variables = mergeStacks(variables, body_variables)
            
    var_dict = {}
    for arg in head_processing_literal.args:
        var_dict[variable_pool[len(var_dict)]] = arg
    
    for each in body_processing_literals:
        for arg in each.args:
            if not arg in var_dict.values():
                var_dict[variable_pool[len(var_dict)]] = arg
    # print(constants)
    # print(variables)
    # print(var_dict)
    return ProcessingRule(rule_id, head_processing_literal, body_processing_literals, constants, variables, var_dict)
    
def parseText(text):
    rules = text.split("\n")
    processed = []
    for i in range(len(rules)):
        processed.append(parseRule(rules[i], i))

    for each in processed:
        print(each)
        
    
f = open("./test.txt", "r")
parseText(f.read())
f.close()