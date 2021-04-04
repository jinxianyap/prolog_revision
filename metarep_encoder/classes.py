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

class GTLiteral(Literal):
    def __init__(self, lhs, rhs):
        assertType(lhs, str)
        assertType(rhs, str)
        self.lhs = lhs
        self.rhs = rhs
    def __repr__(self):
        return 'GTLiteral()'
    def __str__(self):
        return self.lhs + ' > ' + self.rhs
        
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
    
class LELiteral(Literal):
    def __init__(self, lhs, rhs):
        assertType(lhs, str)
        assertType(rhs, str)
        self.lhs = lhs
        self.rhs = rhs
    def __repr__(self):
        return 'LELiteral()'
    def __str__(self):
        return self.lhs + ' <= ' + self.rhs
    
class NotLiteral(Literal):
    def __init__(self, literal):
        self.literal = literal
    def __repr__(self):
        return 'NotLiteral()'
    def __str__(self):
        return 'not ' + self.literal.__str__()

class Literal_rule(Literal):
    def __init__(self, rule_id):
        self.name = 'rule'
        assertType(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_rule()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_head(Literal):
    def __init__(self, rule_id, literal, var_vals):
        self.name = 'head'
        assertType(rule_id, str)
        assertTypeChoice(literal, str, Literal)
        assertTypeChoice(var_vals, str, Literal_var_vals)
        self.rule_id = rule_id
        self.literal = literal
        self.var_vals = var_vals
        self.args = [rule_id, literal, var_vals]
    def __repr__(self):
        return 'Literal_head()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
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
        self.arg = arg
        self.others = others
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
        self.arg = arg
        self.others = others
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
        self.var_val_1 = var_val_1
        self.var_val_2 = var_val_2
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
        self.rule_id = rule_id
        self.variable = variable
        self.var_val = var_val
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
        self.rule_id = rule_id
        self.var_vals = var_vals
        self.length = length
        self.max_length = max_length
        self.variables = variables
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
        self.rule_id = rule_id
        self.var_vals = var_vals
        self.length = length
        self.args = [rule_id, var_vals, length]
    def __repr__(self):
        return 'Literal_defined_length()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_check_sets_length(Literal):
    def __init__(self, rule_id, var_vals_1, var_vals_2):
        self.name = 'check_sets_length'
        assertType(rule_id, str)
        assertTypeChoice(var_vals_1, Literal_var_vals, str)
        assertTypeChoice(var_vals_2, Literal_var_vals, str)
        self.rule_id = rule_id
        self.var_vals_1 = var_vals_1
        self.var_vals_2 = var_vals_2
        self.args = [rule_id, var_vals_1, var_vals_2]
    def __repr__(self):
        return 'Literal_check_sets_length()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'

class Literal_is_subset_helper(Literal):
    def __init__(self, rule_id, var_vals_1, var_vals_2):
        self.name = 'is_subset_helper'
        assertType(rule_id, str)
        assertTypeChoice(var_vals_1, Literal_var_vals, str)
        assertTypeChoice(var_vals_2, Literal_var_vals, str)
        self.rule_id = rule_id
        self.var_vals_1 = var_vals_1
        self.var_vals_2 = var_vals_2
        self.args = [rule_id, var_vals_1, var_vals_2]
    def __repr__(self):
        return 'Literal_is_subset_helper()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_is_subset(Literal):
    def __init__(self, rule_id, var_vals_1, var_vals_2):
        self.name = 'is_subset'
        assertType(rule_id, str)
        assertTypeChoice(var_vals_1, Literal_var_vals, str)
        assertTypeChoice(var_vals_2, Literal_var_vals, str)
        self.rule_id = rule_id
        self.var_vals_1 = var_vals_1
        self.var_vals_2 = var_vals_2
        self.args = [rule_id, var_vals_1, var_vals_2]
    def __repr__(self):
        return 'Literal_is_subset()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_order(Literal):
    def __init__(self, rule_id_1, rule_id_2):
        self.name = 'order'
        assertType(rule_id_1, str)
        assertType(rule_id_2, str)
        self.rule_id_1 = rule_id_1
        self.rule_id_2 = rule_id_2
        self.args = [rule_id_1, rule_id_2]
    def __repr__(self):
        return 'Literal_order()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_rule_not_first(Literal):
    def __init__(self, rule_id):
        self.name = 'rule_not_first'
        assertType(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_rule_not_first()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_seen_rule(Literal):
    def __init__(self, rule_id):
        self.name = 'seen_rule'
        assertType(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_seen_rule()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_in_AS(Literal):
    def __init__(self, literal, rule_id, var_vals):
        self.name = 'in_AS'
        assertTypeChoice(literal, Literal, str)
        assertType(rule_id, str)
        assertTypeChoice(var_vals, Literal_var_vals, str)
        self.literal = literal
        self.rule_id = rule_id
        self.var_vals = var_vals
        self.args = [literal, rule_id, var_vals]
    def __repr__(self):
        return 'Literal_in_AS()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_body_true(Literal):
    def __init__(self, rule_id, var_vals):
        self.name = 'body_true'
        assertType(rule_id, str)
        assertTypeChoice(var_vals, Literal_var_vals, str)
        self.rule_id = rule_id
        self.var_vals = var_vals
        self.args = [rule_id, var_vals]
    def __repr__(self):
        return 'Literal_body_true()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_body_exists(Literal):
    def __init__(self, rule_id):
        self.name = 'body_exists'
        assertType(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_body_exists()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_bl_inbetween(Literal):
    def __init__(self, rule_id, literal_1, literal_2):
        self.name = 'bl_inbetween'
        assertType(rule_id, str)
        assertTypeChoice(literal_1, Literal, str)
        assertTypeChoice(literal_2, Literal, str)
        self.rule_id = rule_id
        self.literal_1 = literal_1
        self.literal_2 = literal_2
        self.args = [rule_id, literal_1, literal_2]
    def __repr__(self):
        return 'Literal_bl_inbetween()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_bl_notlast(Literal):
    def __init__(self, rule_id, literal):
        self.name = 'bl_notlast'
        assertType(rule_id, str)
        assertTypeChoice(literal, Literal, str)
        self.rule_id = rule_id
        self.literal = literal
        self.args = [rule_id, literal]
    def __repr__(self):
        return 'Literal_bl_notlast()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_bl_notfirst(Literal):
    def __init__(self, rule_id, literal):
        self.name = 'bl_notfirst'
        assertType(rule_id, str)
        assertTypeChoice(literal, Literal, str)
        self.rule_id = rule_id
        self.literal = literal
        self.args = [rule_id, literal]
    def __repr__(self):
        return 'Literal_bl_notfirst()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_satisfied(Literal):
    def __init__(self, rule_id, index, literal, var_vals, posneg):
        self.name = 'satisfied'
        assertType(rule_id, str)
        assertType(index, str)
        assertTypeChoice(literal, Literal, str)
        assertTypeChoice(var_vals, Literal_var_vals, str)
        assertType(posneg, str)
        self.rule_id = rule_id
        self.index = index
        self.literal = literal
        self.var_vals = var_vals
        self.posneg = posneg
        self.args = [rule_id, index, literal, var_vals, posneg]
    def __repr__(self):
        return 'Literal_satisfied()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_body_true_upto(Literal):
    def __init__(self, rule_id, index, literal, var_vals, posneg):
        self.name = 'body_true_upto'
        assertType(rule_id, str)
        assertType(index, str)
        assertTypeChoice(literal, Literal, str)
        assertTypeChoice(var_vals, Literal_var_vals, str)
        assertType(posneg, str)
        self.rule_id = rule_id
        self.index = index
        self.literal = literal
        self.var_vals = var_vals
        self.posneg = posneg
        self.args = [rule_id, index, literal, var_vals, posneg]
    def __repr__(self):
        return 'Literal_body_true_upto()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
        
# test1 = Literal('animal', ['X'])
# test2 = Literal('haha', [test1, 'B'])

# print(test1)
# print(test2)