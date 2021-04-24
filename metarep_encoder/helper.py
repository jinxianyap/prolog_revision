from metarep_encoder.messages import *

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
                args.append(rem[i:j])
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
        
        args.append(rem[i:j])

    return args        

def get_name_count_arity(literal):
    return literal.name, len(literal.args)

def assign_built_in_type(rule, literal):
    if is_eq_literal(literal):
        rule.built_in_type = Built_in_type.EQ
    elif is_neq_literal(literal):
        rule.built_in_type = Built_in_type.NEQ

# ------------------------------------------------------------------------------
#  Built-in predicates

class Built_in_type:
    EQ = '='
    NEQ = '!='

def is_eq_literal(literal):
    return '=' in literal and '!=' not in literal

def is_neq_literal(literal):
    return '!=' in literal

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

variable_pool = ['var_x', 'var_y', 'var_z', 'var_p', 'var_q', 'var_r', 'var_s']

def is_variable(text):
    return text[0].isupper()

def split_conjunction(text):
    return text.replace('),', ')*').split('* ')

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
