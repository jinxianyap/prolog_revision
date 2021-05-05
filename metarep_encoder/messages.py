INCORRECT_TYPE = 'Incorrect type assigned.'
INCORRECT_VARS_LENGTH = 'Incorrect number of variables provided.'
INCORRECT_ARITIES = 'Literals used with incorrect number of variables. Please refer to the correct arities: '
UNSATISFIABLE = 'The theory is unsatisfiable. Unable to revise program.'

class Output_type:
    REVISED = 0
    NO_REVISION = 1
    INCORRECT_ARITIES = 2
    UNSATISFIABLE = 3