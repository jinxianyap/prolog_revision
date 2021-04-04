from messages import *

# ------------------------------------------------------------------------------
#  Encoder

def join(literals):
    strings = (map(lambda x: x.__str__(), literals))
    return ', '.join(strings)

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

def isGroundConstant(text):
    return text[0].islower()

def splitConjunction(text):
    return text.replace('), ', ') ').replace(', ', ',').split(' ')

def mergeStacks(a, b):
    # merges b into a
    for each in b:
        if not each in a:
            a.append(each)
    return a

# ------------------------------------------------------------------------------
#  Assertions
    
def assertType(object, target):
    assert isinstance(object, target), INCORRECT_TYPE
    
def assertTypeChoice(object, target1, target2):
    assert isinstance(object, target1) or isinstance(object, target2), INCORRECT_TYPE
    
def assertTypeIsList(object):
    assert isinstance(object, list), INCORRECT_TYPE
    
def assertTypeList(object, target):
    assert type(object) is list, INCORRECT_TYPE
    for each in object:
        assert isinstance(each, target), INCORRECT_TYPE
        
def assertTypeListChoice(object, target1, target2):
    assert type(object) is list, INCORRECT_TYPE
    for each in object:
        assert isinstance(each, target1) or isinstance(each, target2), INCORRECT_TYPE

def assertVarsNumber(object, number):
    assert len(object) == number, INCORRECT_VARS_LENGTH
