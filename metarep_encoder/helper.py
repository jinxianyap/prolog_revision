from messages import *

def join(literals):
    strings = (map(lambda x: x.__str__(), literals))
    return ', '.join(strings)
    
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
