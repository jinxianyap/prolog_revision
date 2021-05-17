INCORRECT_TYPE = 'Incorrect type assigned.'
INCORRECT_VARS_LENGTH = 'Incorrect number of variables provided.'
INCORRECT_ARITIES = 'Literals used with incorrect number of variables. Please refer to the correct arities: '
UNSATISFIABLE = 'The theory is unsatisfiable. Unable to revise program.'
REORDER_NAF = 'Prolog negation must appear at the end of rules to avoid unbounded NAF.'
ERROR = 'Encountered error during feedback generation.'

class Output_type:
    REVISED = 0
    NO_REVISION = 1
    INCORRECT_ARITIES = 2
    UNSATISFIABLE = 3
    NEW_RULES = 4
    REORDER_NAF = 5
    ERROR = -1