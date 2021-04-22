from metarep_encoder.helper import join, assert_type, assert_type_list, assert_type_is_list, assert_type_choice

class Rule:
    def __init__(self, head, body):
        self.head = head
        self.rev_id = None
        self.rev_vars = None
        self.built_in_type = None
        self.body = body
    def __repr__(self):
        return 'Rule()'
    def __str__(self):
        rule = join(self.head) + ('' if len(self.body) == 0 else ' :- ' + join(self.body)) + '.'
        if self.rev_id is not None:
            if self.rev_vars is not None:
                return '#revisable({}, ({}), ({})).'.format(self.rev_id, rule, self.rev_vars)
            else:
                return '#revisable({}, ({})).'.format(self.rev_id, rule)
        else:
            return rule
    def make_revisable(self, rev_id, rev_vars=None):
        self.revisable = True
        assert_type(rev_id, str)
        self.rev_id = rev_id
        self.rev_vars = rev_vars

class Literal:
    def __init__(self, name, args):
            assert_type(name, str)
            assert_type_is_list(args)
            self.name = name
            self.args = args
    def __repr__(self):
        return 'Literal()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    def compare_to(self, other):
        similarity = 0
        differences = 0
        if type(other) != Literal:
            return similarity, differences + 1
        
        if self.name == other.name:
            similarity += 1
        else:
            differences += 1
        if len(self.args) == len(other.args):
            similarity += 1
        else:
            differences += 1
        if set(self.args) == set(other.args):
            similarity += 1
        else: differences += 1
        for i in range(min(len(self.args), len(other.args))):
            if not isinstance(self.args[i], str):
                sim, diff = self.args[i].compare_to(other.args)
                similarity += sim
                differences += diff
            else:
                if self.args[i] == other.args[i]:
                    similarity += 1
                else:
                    differences += 1
        return similarity, differences
        
class EqualsLiteral(Literal):
    def __init__(self, lhs, rhs, literal=False):
        assert_type(lhs, str)
        self.lhs = lhs
        self.rhs = rhs
        self.literal = literal
    def __repr__(self):
        return 'EqualsLiteral()'
    def __str__(self):
        return self.get_rep() if self.literal else 'equalsLiteral({}, {})'.format(self.lhs, self.rhs.__str__())
    def get_rep(self):
        return self.lhs + ' = ' + self.rhs.__str__()
    # def get_weight(self):
    #     lhs_weight = 1
    #     rhs_weight = self.rhs.get_weight() if isinstance(self.rhs, Literal) else 1
    #     return lhs_weight + rhs_weight
    
class NotEqualsLiteral(Literal):
    def __init__(self, lhs, rhs, literal=False):
        assert_type(lhs, str)
        self.lhs = lhs
        self.rhs = rhs
        self.literal = literal
    def __repr__(self):
        return 'NotEqualsLiteral()'
    def __str__(self):
        return self.get_rep() if self.literal else 'notEqualsLiteral({}, {})'.format(self.lhs, self.rhs.__str__())
    def get_rep(self):
        return self.lhs + ' != ' + self.rhs.__str__()
    # def get_weight(self):
    #     lhs_weight = 1
    #     rhs_weight = self.rhs.get_weight() if isinstance(self.rhs, Literal) else 1
    #     return lhs_weight + rhs_weight

class GTLiteral(Literal):
    def __init__(self, lhs, rhs, literal=False):
        assert_type(lhs, str)
        assert_type(rhs, str)
        self.lhs = lhs
        self.rhs = rhs
        self.literal = literal
    def __repr__(self):
        return 'GTLiteral()'
    def __str__(self):
        return self.get_rep() if self.literal else 'greaterThanLiteral({}, {})'.format(self.lhs, self.rhs.__str__())
    def get_rep(self):
        return self.lhs + ' > ' + self.rhs
    # def get_weight(self):
    #     lhs_weight = 1
    #     rhs_weight = self.rhs.get_weight() if isinstance(self.rhs, Literal) else 1
    #     return lhs_weight + rhs_weight
        
class LTLiteral(Literal):
    def __init__(self, lhs, rhs, literal=False):
        assert_type(lhs, str)
        assert_type(rhs, str)
        self.lhs = lhs
        self.rhs = rhs
        self.literal = literal
    def __repr__(self):
        return 'LTLiteral()'
    def __str__(self):
        return self.get_rep() if self.literal else 'lesserThanLiteral({}, {})'.format(self.lhs, self.rhs.__str__())
    def get_rep(self):
        return self.lhs + ' < ' + self.rhs
    
class LELiteral(Literal):
    def __init__(self, lhs, rhs, literal=False):
        assert_type(lhs, str)
        assert_type(rhs, str)
        self.lhs = lhs
        self.rhs = rhs
        self.literal = literal
    def __repr__(self):
        return 'LELiteral()'
    def __str__(self):
        return self.get_rep() if self.literal else 'lesserEqualsLiteral({}, {})'.format(self.lhs, self.rhs.__str__())
    def get_rep(self):
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
        assert_type(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_rule()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_head(Literal):
    def __init__(self, rule_id, literal, var_vals):
        self.name = 'head'
        assert_type(rule_id, str)
        assert_type_choice(literal, str, Literal)
        assert_type_choice(var_vals, str, Literal_var_vals)
        self.rule_id = rule_id
        self.literal = literal
        self.var_vals = var_vals
        self.args = [rule_id, literal, var_vals]
    def __repr__(self):
        return 'Literal_head()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    def compare_to(self, other):
        similarity = 0
        differences = 0
        if type(other) != Literal_head:
            return similarity, differences + 1
        if isinstance(self.literal, Literal):
            sim, diff = self.literal.compare_to(other.literal)
            similarity += sim
            differences += diff
        else:
            if self.literal == other.literal:
                similarity += 1
            else:
                differences += 1
        if isinstance(self.var_vals, Literal_var_vals):
            sim, diff = self.var_vals.compare_to(other.var_vals)
            similarity += sim
            differences += diff
        else:
            if self.var_vals == other.var_vals:
                similarity += 1
            else:
                differences += 1
                
        return similarity, differences
    
class Literal_bl(Literal):
    def __init__(self, rule_id, index, literal):
        self.name = 'bl'
        assert_type(rule_id, str)
        assert_type(index, str)
        assert_type_choice(literal, str, Literal)
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
        assert_type(rule_id, str)
        assert_type(index, str)
        assert_type_choice(literal, str, Literal)
        assert_type_choice(var_vals, str, Literal_var_vals)
        self.rule_id = rule_id
        self.index = index
        self.literal = literal
        self.var_vals = var_vals
        self.args = [rule_id, index, literal, var_vals]
    def __repr__(self):
        return 'Literal_pbl()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    def compare_to(self, other):
        similarity = 0
        differences = 0
        if type(other) != Literal_pbl:
            return similarity, differences + 1
        
        if self.index == other.index:
            similarity += 1
        else:
            differences += 1
        if isinstance(self.literal, Literal):
            sim, diff = self.literal.compare_to(other.literal)
            similarity += sim
            differences += diff
        else:
            if self.literal == other.literal:
                similarity += 1
            else:
                differences += 1
        if isinstance(self.var_vals, Literal_var_vals):
            sim, diff = self.var_vals.compare_to(other.var_vals)
            similarity += sim
            differences += diff
        else:
            if self.var_vals == other.var_vals:
                similarity += 1
            else:
                differences += 1
  
        return similarity, differences
    
class Literal_nbl(Literal):
    def __init__(self, rule_id, index, literal, var_vals):
        self.name = 'nbl'
        assert_type(rule_id, str)
        assert_type(index, str)
        assert_type_choice(literal, str, Literal)
        assert_type_choice(var_vals, str, Literal_var_vals)
        self.rule_id = rule_id
        self.index = index
        self.literal = literal
        self.var_vals = var_vals
        self.args = [rule_id, index, literal, var_vals]
    def __repr__(self):
        return 'Literal_nbl()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    def compare_to(self, other):
        similarity = 0
        differences = 0
        if type(other) != Literal_nbl:
            return similarity, differences + 1
        
        if self.index == other.index:
            similarity += 1
        else:
            differences += 1
        if isinstance(self.literal, Literal):
            sim, diff = self.literal.compare_to(other.literal)
            similarity += sim
            differences += diff
        else:
            if self.literal == other.literal:
                similarity += 1
            else:
                differences += 1
        if isinstance(self.var_vals, Literal_var_vals):
            sim, diff = self.var_vals.compare_to(other.var_vals)
            similarity += sim
            differences += diff
        else:
            if self.var_vals == other.var_vals:
                similarity += 1
            else:
                differences += 1
  
        return similarity, differences   
     
class Literal_variable(Literal):
    def __init__(self, arg):
        self.name = 'variable'
        assert_type(arg, str)
        self.arg = arg
    def __repr__(self):
        return 'Literal_variable()'
    def __str__(self):
        return self.name + '(' + self.arg + ')'
    def compare_to(self, other):
        similarity = 0
        differences = 0
        if type(other) != Literal_variable:
            return similarity, differences + 1
        
        if self.arg == other.arg:
            similarity += 1
        else:
            differences += 1
  
        return similarity, differences
    
class Literal_variables(Literal):
    def __init__(self, arg, others):
        self.name = 'variables'
        assert_type(arg, str)
        assert_type_choice(others, str, Literal_variables)
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
        assert_type_choice(arg, str, Literal_variables)
        self.arg = arg
    def __repr__(self):
        return 'Literal_variable_list()'
    def __str__(self):
        return self.name + '(' + self.arg.__str__() + ')'
    
class Literal_ground(Literal):
    def __init__(self, term):
        self.name = 'ground'
        assert_type(term, str)
        self.term = term
    def __repr__(self):
        return 'Literal_ground()'
    def __str__(self):
        return self.name + '(' + self.term + ')'
    def compare_to(self, other):
        similarity = 0
        differences = 0
        if type(other) != Literal_ground:
            return similarity, differences + 1
        
        if self.term == other.term:
            similarity += 1
        else:
            differences += 1
  
        return similarity, differences

class Literal_var_val(Literal):
    def __init__(self, rule_id, variable, term):
        self.name = 'var_val'
        assert_type(rule_id, str)
        assert_type(variable, str)
        assert_type(term, str)
        self.rule_id = rule_id
        self.variable = variable
        self.term = term
        self.args = [rule_id, variable, term]
    def __repr__(self):
        return 'Literal_var_val()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    def to_metarep(self):
        return 'var_val({}, {}, {})'.format(self.rule_id, self.variable, self.term)
    def compare_to(self, other):
        similarity = 0
        differences = 0
        if type(other) != Literal_var_val:
            return similarity, differences + 1
        
        if self.rule_id == other.rule_id:
            similarity += 1
        else:
            differences += 1
        if self.variable == other.variable:
            similarity += 1
        else:
            differences += 1
        if self.term == other.term:
            similarity += 1
        else:
            differences += 1
  
        return similarity, differences
    
class Literal_var_vals(Literal):
    def __init__(self, arg, others):
        self.name = 'var_vals'
        assert_type_choice(arg, str, Literal_var_val)
        assert_type_choice(others, str, Literal_var_vals)
        self.arg = arg
        self.others = others
        self.args = [arg, others]
    def __repr__(self):
        return 'Literal_var_vals()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    def to_metarep(self):
        arg = self.arg.to_metarep() if isinstance(self.arg, Literal_var_val) else self.arg
        others = self.others.to_metarep() if isinstance(self.others, Literal_var_vals) else self.others
        return 'var_vals({}, {})'.format(arg, others)
    def compare_to(self, other):
        similarity = 0
        differences = 0
        if type(other) != Literal_var_vals:
            return similarity, differences + 1
        
        if isinstance(self.arg, Literal_var_val):
            sim_arg, diff_arg = self.arg.compare_to(other.arg)
            similarity += sim_arg
            differences += diff_arg
        else:
            differences += 1
            
        if isinstance(self.others, Literal_var_vals):
            sim_others, diff_others = self.others.compare_to(other.others)
            similarity += sim_others
            differences += diff_others
        else:
            differences += 1
  
        return similarity, differences
    
class Literal_is_var_val(Literal):
    def __init__(self, var_val):
        self.name = 'is_var_val'
        assert_type_choice(var_val, str, Literal_var_val)
        self.var_val = var_val
    def __repr__(self):
        return 'Literal_is_var_val()'
    def __str__(self):
        return self.name + '(' + self.var_val.__str__() + ')'
    
class Literal_var_val_equal(Literal):
    def __init__(self, var_val_1, var_val_2):
        self.name = 'var_val_equal'
        assert_type_choice(var_val_1, str, Literal_var_val)
        assert_type_choice(var_val_2, str, Literal_var_val)
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
        assert_type(rule_id, str)
        assert_type_choice(var_val, Literal_var_val, str)
        assert_type(variable, str)
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
        assert_type(arg, str)
        self.arg = arg
        self.range = range
    def __repr__(self):
        return 'Literal_var_num()'
    def __str__(self):
        return self.name + ('(1..' if self.range else '(') + self.arg + ')'    
    
class Literal_var_max(Literal):
    def __init__(self, arg):
        self.name = 'var_max'
        assert_type(arg, str)
        self.arg = arg
    def __repr__(self):
        return 'Literal_var_max()'
    def __str__(self):
        return self.name + '(' + self.arg + ')'
    
class Literal_length(Literal):
    def __init__(self, rule_id, var_vals, length, max_length, variables):
        self.name = 'length'
        assert_type(rule_id, str)
        assert_type_choice(var_vals, Literal_var_vals, str)
        assert_type(length, str)
        assert_type(max_length, str)
        assert_type_choice(variables, Literal_variables, str)
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
        assert_type(rule_id, str)
        assert_type_choice(var_vals, Literal_var_vals, str)
        assert_type(length, str)
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
        assert_type(rule_id, str)
        assert_type_choice(var_vals_1, Literal_var_vals, str)
        assert_type_choice(var_vals_2, Literal_var_vals, str)
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
        assert_type(rule_id, str)
        assert_type_choice(var_vals_1, Literal_var_vals, str)
        assert_type_choice(var_vals_2, Literal_var_vals, str)
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
        assert_type(rule_id, str)
        assert_type_choice(var_vals_1, Literal_var_vals, str)
        assert_type_choice(var_vals_2, Literal_var_vals, str)
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
        assert_type(rule_id_1, str)
        assert_type(rule_id_2, str)
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
        assert_type(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_rule_not_first()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_seen_rule(Literal):
    def __init__(self, rule_id):
        self.name = 'seen_rule'
        assert_type(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_seen_rule()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_in_AS(Literal):
    def __init__(self, literal, rule_id, var_vals):
        self.name = 'in_AS'
        assert_type_choice(literal, Literal, str)
        assert_type(rule_id, str)
        assert_type_choice(var_vals, Literal_var_vals, str)
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
        assert_type(rule_id, str)
        assert_type_choice(var_vals, Literal_var_vals, str)
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
        assert_type(rule_id, str)
        self.rule_id = rule_id
    def __repr__(self):
        return 'Literal_body_exists()'
    def __str__(self):
        return self.name + '(' + self.rule_id + ')'
    
class Literal_bl_inbetween(Literal):
    def __init__(self, rule_id, literal_1, literal_2):
        self.name = 'bl_inbetween'
        assert_type(rule_id, str)
        assert_type_choice(literal_1, Literal, str)
        assert_type_choice(literal_2, Literal, str)
        self.rule_id = rule_id
        self.literal_1 = literal_1
        self.literal_2 = literal_2
        self.args = [rule_id, literal_1, literal_2]
    def __repr__(self):
        return 'Literal_bl_inbetween()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_bl_notlast(Literal):
    def __init__(self, rule_id, position, literal):
        self.name = 'bl_notlast'
        assert_type(rule_id, str)
        assert_type_choice(literal, Literal, str)
        self.rule_id = rule_id
        self.position = position
        self.literal = literal
        self.args = [rule_id, position, literal]
    def __repr__(self):
        return 'Literal_bl_notlast()'
    def __str__(self):
        return self.name + '(' + join(self.args) + ')'
    
class Literal_bl_first(Literal):
    def __init__(self, position):
        self.name = 'bl_first'
        assert_type(position, str)
        self.position = position
    def __repr__(self):
        return 'Literal_bl_first()'
    def __str__(self):
        return self.name + '(' + self.position + ')'
    
class Literal_satisfied(Literal):
    def __init__(self, rule_id, index, literal, var_vals, posneg):
        self.name = 'satisfied'
        assert_type(rule_id, str)
        assert_type(index, str)
        assert_type_choice(literal, Literal, str)
        assert_type_choice(var_vals, Literal_var_vals, str)
        assert_type(posneg, str)
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
        assert_type(rule_id, str)
        assert_type(index, str)
        assert_type_choice(literal, Literal, str)
        assert_type_choice(var_vals, Literal_var_vals, str)
        assert_type(posneg, str)
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

class Declaration():
    def __init__(self):
        super.__init__() 
class Declaration_pos_example(Declaration):
    def __init__(self, rev_id, literal):
        self.rev_id = rev_id
        self.literal = literal
    def __repr__(self):
        return 'Declaration_pos_example()'
    def __str__(self):
        return '#pos(p{}, {{{}}}, {{}}, {{}}).'.format(self.rev_id, self.literal)
    
class Declaration_neg_example(Declaration):
    def __init__(self, rev_id, literal):
        self.rev_id = rev_id
        self.literal = literal
    def __repr__(self):
        return 'Declaration_neg_example()'
    def __str__(self):
        return '#neg(n{}, {{{}}}, {{}}, {{}}).'.format(self.rev_id, self.literal)
    
class Declaration_const(Declaration):
    def __init__(self, symbol, constant):
        self.symbol = symbol
        self.constant = constant
    def __repr__(self):
        return 'Declaration_const()'
    def __str__(self):
        return '#constant({}, {}).'.format(self.symbol, self.constant)
    
class Declaration_modeh(Declaration):
    def __init__(self, string):
        self.string = string
    def __repr__(self):
        return 'Declaration_modeh()'
    def __str__(self):
        return '#modeh({}).'.format(self.string)
    
class Declaration_modeb(Declaration):
    def __init__(self, string):
        self.string = string
    def __repr__(self):
        return 'Declaration_modeb()'
    def __str__(self):
        return '#modeb({}).'.format(self.string)