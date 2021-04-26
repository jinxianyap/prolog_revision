from metarep_encoder.classes import *
from metarep_encoder.helper import *

def parseLiteral(rule_id, literal):
    literal = trim_front_back_whitespace(literal)
    if is_comparator_literal(literal):
        token = ''
        if is_eq_literal(literal): token = Built_in_type.EQ
        elif is_neq_literal(literal): token = Built_in_type.NEQ
        elif is_gt_literal(literal): token = Built_in_type.GT
        elif is_ge_literal(literal): token = Built_in_type.GE
        elif is_lt_literal(literal): token = Built_in_type.LT
        elif is_le_literal(literal): token = Built_in_type.LE

        split = literal.split(token)
        front = trim_front_back_whitespace(split[0])
        back = trim_front_back_whitespace(split[1])
        args = [front, back]
        variables = [x for x in args if is_variable(x)]
        constants = [x for x in args if x not in variables]
        return ProcessingLiteral(rule_id, literal, args), constants, variables
    else:
        split = literal.replace(')', '').split('(')
        if len(split) == 1:
            return ProcessingLiteral(rule_id, split[0].strip(), []), [], []
        else:
            args = [arg.replace(' ', '') for arg in split[1].split(',')]
            variables = [x for x in args if is_variable(x)]
            constants = [x for x in args if x not in variables]

            return ProcessingLiteral(rule_id, literal, args), constants, variables

def parseRule(rule_text, index):
    rule_id = 'r' + str(index + 1)
    rule_text = rule_text[:-1].split(':-')
    head_text = rule_text[0]
    body_text = rule_text[1][1:] if len(rule_text) > 1 else None
    
    constants = []
    variables = []
    
    head_processing_literal, head_constants, head_variables = parseLiteral(rule_id, head_text)
    
    constants = merge_stacks(constants, head_constants)
    variables = merge_stacks(variables, head_variables)
    
    body_processing_literals = []
    if not body_text is None:
        body_text = split_conjunction(body_text)
        for body_literal in body_text:
            body_processing_literal, body_constants, body_variables = parseLiteral(rule_id, body_literal)
            body_processing_literals.append(body_processing_literal)
            constants = merge_stacks(constants, body_constants)
            variables = merge_stacks(variables, body_variables)
            
    var_dict = {}
    for arg in head_processing_literal.args:
        var_dict[arg] = VARIABLE_POOL[len(var_dict)]
    
    for each in body_processing_literals:
        for arg in each.args:
            if not arg in var_dict.keys():
                var_dict[arg] = VARIABLE_POOL[len(var_dict)]
    # print(constants)
    # print(variables)
    # print(var_dict)
    return ProcessingRule(rule_id, head_processing_literal, body_processing_literals, constants, variables, var_dict)
    
def parseText(text):
    rules = [x for x in text.split("\n") if len(x) > 0 and x[0] is not '%' and x[0] is not '#']
    processed = []
    for i in range(len(rules)):
        if len(rules[i]) > 0:
            processed.append(parseRule(rules[i], i))

    # for each in processed:
    #     print(each)
    
    return processed    
    
# f = open("./test.txt", "r")
# parseText(f.read())
# f.close()