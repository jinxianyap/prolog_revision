from metarep_encoder.classes import *
from metarep_encoder.helper import *

def parseLiteral(rule_id, literal):
    literal = trim_front_back_whitespace(literal)

    if is_arithmetic_literal(literal):
        token = ''
        if is_eq_literal(literal): token = Built_in_type.EQ
        elif is_neq_literal(literal): token = Built_in_type.NEQ
        elif is_gt_literal(literal): token = Built_in_type.GT
        elif is_ge_literal(literal): token = Built_in_type.GE
        elif is_lt_literal(literal): token = Built_in_type.LT
        elif is_le_literal(literal): token = Built_in_type.LE
        elif is_plus_literal(literal): token = Built_in_type.PLUS
        elif is_minus_literal(literal): token = Built_in_type.MINUS
        elif is_mult_literal(literal): token = Built_in_type.MULT

        args = get_arguments(literal, token)
        parsed_args = [parseLiteral(rule_id, x) for x in args]
        final_args = []
        variables = []
        constants = []
        
        for each in parsed_args:
            if isinstance(each, str):
                final_args.append(each)
                if is_variable(each):
                    variables.append(each)
                else:
                    constants.append(each)
            else:
                final_args.append(each[0])
                constants += each[1]
                variables += each[2]

        return ProcessingLiteral(rule_id, literal, final_args), constants, variables
    else:
        if '(' not in literal:
            # literal is an atom
            return literal
        
        args = get_arguments(literal)
        parsed_args = [parseLiteral(rule_id, x) for x in args]
        final_args = []
        variables = []
        constants = []
        
        for each in parsed_args:
            if isinstance(each, str):
                final_args.append(each)
                if is_variable(each):
                    variables.append(each)
                else:
                    constants.append(each)
            else:
                final_args.append(each[0])
                constants += each[1]
                variables += each[2]

        return ProcessingLiteral(rule_id, literal, final_args), constants, variables

def parseRule(rule_text, index):
    rule_id = 'r' + str(index + 1)
    rule_text = rule_text[:-1].split(':-')
    head_text = rule_text[0]
    body_text = rule_text[1][1:] if len(rule_text) > 1 else None
    
    constants = []
    variables = []

    head_processing_literal, head_constants, head_variables = (None, [], []) if len(head_text) == 0 else parseLiteral(rule_id, head_text)
    
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
    
    for each in variables + constants:
        var_dict[each] = VARIABLE_POOL[len(var_dict)]
                
    # if head_processing_literal is not None:
    #     for arg in head_processing_literal.args:
    #         if not isinstance(arg, ProcessingLiteral):
    #             var_dict[arg] = VARIABLE_POOL[len(var_dict)]
    
    # for each in body_processing_literals:
    #     for arg in each.args:
    #         if not arg in var_dict.keys() and not isinstance(arg, ProcessingLiteral):
    #             var_dict[arg] = VARIABLE_POOL[len(var_dict)]
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