from classes import *

def generateBLRules():
    # body literals
    bl_pbl_rule = Rule([Literal_bl('R', 'P', 'X')], [Literal_pbl('R', 'P', 'X', 'VARS')])
    bl_nbl_rule = Rule([Literal_bl('R', 'P', 'X')], [Literal_nbl('R', 'P', 'X', 'VARS')])
    
    print(bl_pbl_rule)
    print(bl_nbl_rule)
    
def generateVarValRules():
    # var_vals
    var_val_rule = Rule([Literal_var_val('R', 'V', 'T')], [Literal_rule('R'), Literal_variable('V'), Literal_ground('T')])
    is_var_val_rule = Rule([Literal_is_var_val(Literal_var_val('R', 'V', 'T'))], [Literal_rule('R'), Literal_variable('V'), Literal_ground('T')])
    var_val_equal_rule = Rule([Literal_var_val_equal('VVX', 'VVY')], [Literal_is_var_val('VVX'), Literal_is_var_val('VVY'), EqualsLiteral('VVX', Literal_var_val('R', 'V', 'T')), EqualsLiteral('VVY', Literal_var_val('R', 'V', 'T'))])
    valid_var_val_rule = Rule([Literal_valid_var_val('RULE_NO', Literal_var_val('R', 'V', 'T'), 'VAR')], [Literal_variable('VAR'), Literal_rule('R'), EqualsLiteral('R', 'RULE_NO'), EqualsLiteral('V', 'VAR'), Literal_ground('T')])
    
    print(var_val_rule)
    print(is_var_val_rule)
    print(var_val_equal_rule)
    print(valid_var_val_rule)
    
def generateSubsetRules():
    # length
    length_base_rule = Rule([Literal_length('R', 'end', '0', 'MAX', 'end')], [Literal_var_max('MAX'), Literal_rule('R')])
    length_recursive_rule = Rule([Literal_length('R', Literal_var_vals('VV', 'VVS'), 'N', 'MAX', Literal_variables('V', 'VS'))], [Literal_valid_var_val('R', 'VV', 'V'), Literal_length('R', 'VVS', 'N - 1', 'MAX', 'VS'), Literal_var_max('MAX'), LTLiteral('N', 'MAX')])
    defined_length_base_rule = Rule([Literal_defined_length('R', 'end', '0')], [Literal_rule('R')])
    defined_length_recursive_rule = Rule([Literal_defined_length('R', 'VVS', 'N')], [Literal_variable_list('VS'), Literal_length('R', 'VVS', 'N', 'MAX', 'VS'), Literal_var_num('N'), Literal_var_num('MAX')])
    
    
    # is_subset
    
    print(length_base_rule)
    print(length_recursive_rule)
    print(defined_length_base_rule)
    print(defined_length_recursive_rule)    
    
    
generateBLRules()
generateVarValRules()
generateSubsetRules()