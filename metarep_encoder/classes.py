from helper import *
 
class Rule:
    def __init__(self, head, body):
        assertTypeList(head, Literal)
        self.head = head
        if body is None:
            self.body = None
        else:
            assertTypeList(body, Literal)
            self.body = body
    def __repr__(self):
        return 'Rule()'
    def __str__(self):
        return join(self.head) + ('' if self.body is None else ' :- ' + join(self.body)) + '.'

class Literal:
    def __init__(self, name, args):
            assertType(name, str)
            assertTypeIsList(args)
            self.name = name
            self.args = args
    def __repr__(self):
        return 'Literal()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
        
class EqualsLiteral(Literal):
    def __init__(self, lhs, rhs):
        assertType(lhs, str)
        self.lhs = lhs
        self.rhs = rhs
    def __repr__(self):
        return 'EqualsLiteral()'
    def __str__(self):
        return self.lhs + ' = ' + self.rhs.__str__()
    
class LTLiteral(Literal):
    def __init__(self, lhs, rhs):
        assertType(lhs, str)
        assertType(rhs, str)
        self.lhs = lhs
        self.rhs = rhs
    def __repr__(self):
        return 'LTLiteral()'
    def __str__(self):
        return self.lhs + ' < ' + self.rhs
    
class Literal_rule(Literal):
    def __init__(self, rule_id):
        self.name = 'rule'
        assertType(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_rule()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_bl(Literal):
    def __init__(self, rule_id, index, literal):
        self.name = 'bl'
        assertType(rule_id, str)
        assertType(index, str)
        assertTypeChoice(literal, str, Literal)
        self.rule_id = rule_id
        self.index = index
        self.literal = literal
        self.args = [rule_id, index, literal]
    def __repr__(self):
        return 'Literal_bl()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_pbl(Literal):
    def __init__(self, rule_id, index, literal, var_vals):
        self.name = 'pbl'
        assertType(rule_id, str)
        assertType(index, str)
        assertTypeChoice(literal, str, Literal)
        assertTypeChoice(var_vals, str, Literal_var_vals)
        self.rule_id = rule_id
        self.index = index
        self.literal = literal
        self.var_vals = var_vals
        self.args = [rule_id, index, literal, var_vals]
    def __repr__(self):
        return 'Literal_pbl()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_nbl(Literal):
    def __init__(self, rule_id, index, literal, var_vals):
        self.name = 'nbl'
        assertType(rule_id, str)
        assertType(index, str)
        assertTypeChoice(literal, str, Literal)
        assertTypeChoice(var_vals, str, Literal_var_vals)
        self.rule_id = rule_id
        self.index = index
        self.literal = literal
        self.var_vals = var_vals
        self.args = [rule_id, index, literal, var_vals]
    def __repr__(self):
        return 'Literal_nbl()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_variable(Literal):
    def __init__(self, arg):
        self.name = 'variable'
        assertType(arg, str)
        self.arg = arg
    def __repr__(self):
        return 'Literal_variable()'
    def __str__(self):
        return self.name + '(' + self.arg + ')'
    
class Literal_variables(Literal):
    def __init__(self, arg, others):
        self.name = 'variables'
        assertTypeChoice(arg, str, Literal_variable)
        assertTypeChoice(others, str, Literal_variables)
        self.args = [arg, others]
    def __repr__(self):
        return 'Literal_variables()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_variable_list(Literal):
    def __init__(self, arg):
        self.name = 'variable_list'
        assertTypeChoice(arg, str, Literal_variables)
        self.arg = arg
    def __repr__(self):
        return 'Literal_variable_list()'
    def __str__(self):
        return self.name + '(' + self.arg.__str__() + ')'
    
class Literal_ground(Literal):
    def __init__(self, term):
        self.name = 'ground'
        assertType(term, str)
        self.term = term
    def __repr__(self):
        return 'Literal_ground()'
    def __str__(self):
        return self.name + '(' + self.term + ')'

class Literal_var_val(Literal):
    def __init__(self, rule_id, variable, term):
        self.name = 'var_val'
        assertType(rule_id, str)
        assertType(variable, str)
        assertType(term, str)
        self.rule_id = rule_id
        self.variable = variable
        self.term = term
        self.args = [rule_id, variable, term]
    def __repr__(self):
        return 'Literal_var_val()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_var_vals(Literal):
    def __init__(self, arg, others):
        self.name = 'var_vals'
        assertTypeChoice(arg, str, Literal_var_val)
        assertTypeChoice(others, str, Literal_var_vals)
        self.args = [arg, others]
    def __repr__(self):
        return 'Literal_var_vals()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_is_var_val(Literal):
    def __init__(self, var_val):
        self.name = 'is_var_val'
        assertTypeChoice(var_val, str, Literal_var_val)
        self.var_val = var_val
    def __repr__(self):
        return 'Literal_is_var_val()'
    def __str__(self):
        return self.name + '(' + self.var_val.__str__() + ')'
    
class Literal_var_val_equal(Literal):
    def __init__(self, var_val_1, var_val_2):
        self.name = 'var_val_equal'
        assertTypeChoice(var_val_1, str, Literal_var_val)
        assertTypeChoice(var_val_2, str, Literal_var_val)
        self.args = [var_val_1, var_val_2]
    def __repr__(self):
        return 'Literal_var_val_equal()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_valid_var_val(Literal):
    def __init__(self, rule_id, var_val, variable):
        self.name = 'valid_var_val'
        assertType(rule_id, str)
        assertTypeChoice(var_val, Literal_var_val, str)
        assertType(variable, str)
        self.args = [rule_id, var_val, variable]
    def __repr__(self):
        return 'Literal_valid_var_val()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_var_num(Literal):
    def __init__(self, arg, range=False):
        self.name = 'var_num'
        assertType(arg, str)
        self.arg = arg
        self.range = range
    def __repr__(self):
        return 'Literal_var_num()'
    def __str__(self):
        return self.name + ('(1..' if self.range else '(') + self.arg + ')'    
    
class Literal_var_max(Literal):
    def __init__(self, arg):
        self.name = 'var_max'
        assertType(arg, str)
        self.arg = arg
    def __repr__(self):
        return 'Literal_var_max()'
    def __str__(self):
        return self.name + '(' + self.arg + ')'
    
class Literal_length(Literal):
    def __init__(self, rule_id, var_vals, length, max_length, variables):
        self.name = 'length'
        assertType(rule_id, str)
        assertTypeChoice(var_vals, Literal_var_vals, str)
        assertType(length, str)
        assertType(max_length, str)
        assertTypeChoice(variables, Literal_variables, str)
        self.args = [rule_id, var_vals, length, max_length, variables]
    def __repr__(self):
        return 'Literal_length()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_defined_length(Literal):
    def __init__(self, rule_id, var_vals, length):
        self.name = 'defined_length'
        assertType(rule_id, str)
        assertTypeChoice(var_vals, Literal_var_vals, str)
        assertType(length, str)
        self.args = [rule_id, var_vals, length]
    def __repr__(self):
        return 'Literal_defined_length()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
# test1 = Literal('animal', ['X'])
# test2 = Literal('haha', [test1, 'B'])

# print(test1)
# print(test2)