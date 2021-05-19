import re
from metarep_encoder.constants import *

def find_incorrect_arities(correct, user):
    incorrect = {}
    for each in user:
        if each in correct and user[each] != correct[each]:
            incorrect[each] = correct[each]
    return incorrect

# ------------------------------------------------------------------------------
#  Fault Localiser
    
def get_dict_key(dictionary, value):
    for each in dictionary:
        if dictionary[each] == value:
            return each
    return None
# ------------------------------------------------------------------------------
#  Declarations Generator

RULE_ID_SYMBOL = 'rule_id'
VARIABLE_SYMBOL = 'variable'
GROUND_CONSTANT_SYMBOL = 'ground_constant'
POS_SYMBOL = 'position'
VAR_VALS_END_SYMBOL = 'var_vals_end'
MAX_POS = 4
    
def var_vals_to_revisable_variables(var_vals):
    if var_vals == 'end':
        return []

    if is_variable(var_vals.arg.term):
        return [var_vals.arg.term] + var_vals_to_revisable_variables(var_vals.others)
    else:
        return var_vals_to_revisable_variables(var_vals.others)

def generate_var_vals_declaration(n):
    if n == 0: return 'const({})'.format(VAR_VALS_END_SYMBOL)
    else:
        return 'var_vals(var_val(const({}), const({}), var(ground)), {})'.format(RULE_ID_SYMBOL, VARIABLE_SYMBOL, generate_var_vals_declaration(n-1))
    
def generate_var_vals_declarations(symbols, arity):
    if len(symbols) < arity or arity < 0: return []
    ls = ['const({})'.format(VAR_VALS_END_SYMBOL)] if arity == 0 else []
    for i in range(len(symbols)):
        subs = generate_var_vals_declarations(symbols[i + 1:], arity-1)
        for j in subs:
            ls.append('var_vals(var_val(const({}), const({}), var(ground)), {})'.format(RULE_ID_SYMBOL, symbols[i], j))
    return ls
    
# ------------------------------------------------------------------------------
#  Encoder

def join(literals):
    strings = (map(lambda x: x.__str__(), literals))
    return ', '.join(strings)

def flatten_args(args):
    final_args = []
    for each in args:
        if isinstance(each, ProcessingLiteral):
            final_args += sum([flatten_args(x) for x in each.args], [])
        else:
            assert_type(each, str)
            final_args.append(each)
    return final_args

def get_arguments(literal, built_in_type=None): 
    args = []
    if built_in_type is not None:
        args = [trim_front_back_whitespace(x) for x in literal.split(built_in_type)]
    else:
        literal = literal[:-1].split('(', 1)
        rem = literal[1]
        
        stack = []
        i = 0
        j = 0
        
        while j < len(rem):
            if rem[j] == ',' and len(stack) == 0:
                args.append(trim_front_back_whitespace(rem[i:j]))
                j += 1
                i = j
            elif rem[j] == '(':
                stack.append(i + 1)
                j += 1
            elif rem[j] == ')':
                start = stack.pop()
                args.append(rem[start:j+1])
                j += 1
                i = j
            else:
                j += 1
        
        if i != j and not rem[i:j].isspace():
            args.append(trim_front_back_whitespace(rem[i:j]))
    return args        

def get_name_count_arity(literal):
    return literal.name, len(literal.args)

def assign_built_in_type(rule, literal):
    if is_eq_literal(literal):
        rule.built_in_type = Built_in_type.EQ
    elif is_neq_literal(literal):
        rule.built_in_type = Built_in_type.NEQ
    elif is_gt_literal(literal):
        rule.built_in_type = Built_in_type.GT
    elif is_ge_literal(literal):
        rule.built_in_type = Built_in_type.GE
    elif is_lt_literal(literal):
        rule.built_in_type = Built_in_type.LT
    elif is_le_literal(literal):
        rule.built_in_type = Built_in_type.LE
    elif is_plus_literal(literal):
        rule.built_in_type = Built_in_type.PLUS
    elif is_minus_literal(literal):
        rule.built_in_type = Built_in_type.MINUS
    elif is_mult_literal(literal):
        rule.built_in_type = Built_in_type.MULT
    

# ------------------------------------------------------------------------------
#  Built-in predicates

class Built_in_type:
    EQ = '='
    NEQ = '!='
    GT = '>'
    LT = '<'
    LE = '<='
    GE = '>='
    PLUS = '+'
    MINUS = '-'
    MULT = '*'

def is_arithmetic_literal(literal):
    matches = re.findall('^[A-Za-z0-9_]+\(.*\)$', literal)
    if len(matches) > 0:
        return False
    return is_eq_literal(literal) or is_neq_literal(literal) or \
        is_gt_literal(literal) or is_ge_literal(literal) or \
        is_lt_literal(literal) or is_le_literal(literal) or \
        is_plus_literal(literal) or is_minus_literal(literal) or \
        is_mult_literal(literal)

def is_eq_literal(literal):
    return '=' in literal and not is_neq_literal(literal) and \
        not is_ge_literal(literal) and not is_le_literal(literal)

def is_neq_literal(literal):
    return '!=' in literal

def is_gt_literal(literal):
    return '>' in literal and '>=' not in literal

def is_ge_literal(literal):
    return '>=' in literal

def is_lt_literal(literal):
    return '<' in literal and '<=' not in literal

def is_le_literal(literal):
    return '<=' in literal

def is_plus_literal(literal):
    return '+' in literal and not is_naf_literal(literal)

def is_minus_literal(literal):
    return '-' in literal

def is_mult_literal(literal):
    return '*' in literal

def is_naf_literal(literal):
    return '\+' in literal

# ------------------------------------------------------------------------------
#  Parser
class ProcessingLiteral:
    def __init__(self, rule_id, literal, args):
        self.rule_id = rule_id
        self.literal = literal
        self.args = args
    def __repr__(self):
        return 'ProcessingLiteral()'
    def __str__(self):
        return 'ProcessingLiteral(' + join([self.rule_id, self.literal, self.args]) + ')'
        
class ProcessingRule:
    def __init__(self, rule_id, head, body, constants, variables, var_dict):
        self.rule_id = rule_id
        self.head = head
        self.body = body
        self.constants = constants
        self.variables = variables
        self.var_dict = var_dict
    def __repr__(self):
        return 'ProcessingRule()'
    def __str__(self):
        return 'ProcessingRule(' + join([self.rule_id, self.head, list(map(lambda x: x.__str__(), self.body)), self.constants, self.variables, self.var_dict]) + ')'

VARIABLE_POOL = ['var_1', 'var_2', 'var_3', 'var_4', 'var_5', 'var_6', 'var_7']

def is_variable(text):
    return text[0].isupper()

def split_conjunction(text):
    body = []
    stack = []
    i = 0
    j = 0
    
    for j in range(len(text)):
        if text[j] == '(':
            stack.append(text[j])
        elif text[j] == ')':
            stack.pop()
        elif text[j] == ',' and len(stack) == 0:
            body.append(trim_front_back_whitespace(text[i:j]))
            i = j + 1
       
    body.append(trim_front_back_whitespace(text[i:j+1]))
    
    return body

def merge_stacks(a, b):
    # merges b into a
    for each in b:
        if not each in a:
            a.append(each)
    return a

def trim_front_back_whitespace(text):
    if text[0].isspace():
        text = text[1:]
    if text[-1].isspace():
        text = text[:-1]
    return text

# ------------------------------------------------------------------------------
#  Assertions
    
def assert_type(object, target):
    assert isinstance(object, target), INCORRECT_TYPE
    
def assert_type_choice(object, target1, target2):
    assert isinstance(object, target1) or isinstance(object, target2), INCORRECT_TYPE
    
def assert_type_is_list(object):
    assert isinstance(object, list), INCORRECT_TYPE
    
def assert_type_list(object, target):
    assert type(object) is list, INCORRECT_TYPE
    for each in object:
        assert isinstance(each, target), INCORRECT_TYPE
        
def assert_type_list_choice(object, target1, target2):
    assert type(object) is list, INCORRECT_TYPE
    for each in object:
        assert isinstance(each, target1) or isinstance(each, target2), INCORRECT_TYPE

def assert_vars_number(object, number):
    assert len(object) == number, INCORRECT_VARS_LENGTH
