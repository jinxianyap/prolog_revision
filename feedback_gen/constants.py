INCORRECT_ARITIES = 'Literals used with incorrect number of variables. Please refer to the correct arities: '
UNSATISFIABLE = 'The theory is unsatisfiable. Unable to revise program.'
REORDER_NAF = 'Prolog negation must appear at the end of rules to avoid unbounded NAF.'
ERROR = 'Encountered error during feedback generation.'

class Output_type:
    REVISED = 'REVISED'
    NO_REVISION = 'NO_REVISION'
    INCORRECT_ARITIES = 'INCORRECT_ARITIES'
    UNSATISFIABLE = 'UNSATISFIABLE'
    NEW_RULES = 'NEW_RULES'
    REORDER_NAF = 'REORDER_NAF'
    ERROR = 'ERROR'
    
class Revision_type:
    REPLACE_BODY = 'REPLACE_BODY'
    ADD_BODY = 'ADD_BODY'
    DELETE_BODY = 'DELETE_BODY'
    ADD_RULE = 'ADD_RULE'
    DELETE_RULE = 'DELETE_RULE'
    NEG_BODY = 'NEG_BODY'
    ORDER_BODY = 7
    ORDER_RULE = 8
    LISTS = 9    