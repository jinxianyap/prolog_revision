import sys
import os
import csv
from feedback_gen.feedback_gen import main as generate_feedback
from feedback_gen.constants import Output_type
from evaluation_pkg.generate_random import main as generate_random_programs

RANDOM_FOLDER = 'random_programs'
EVAL_DATA_FILE = 'eval_data.csv'

class TestProgram:
    def __init__(self, filename, output_type, similarity_score, program_data, revision_tags, success):
        self.filename = filename
        self.output_type = output_type
        self.similarity_score = similarity_score
        self.program_data = program_data
        self.revision_tags = revision_tags
        self.success = success

def run_evaluation(model_filename, random_programs):
    test_programs = []
    successes = 0
    failures = 0
    not_applicables = 0
    
    for i, each in enumerate(random_programs):
        print(i)
        result = generate_feedback([model_filename, each], True)
        if result[0] in [Output_type.NO_REVISION, Output_type.INCORRECT_ARITIES, Output_type.REORDER_NAF]:
            test_programs.append(TestProgram(each, result[0], None, None, None, True))
            not_applicables += 1
        else:
            output_type, similarity_score, program_data, revision_tags, success = result
            test_programs.append(TestProgram(each, output_type, similarity_score, program_data, revision_tags, success))
            if success: 
                successes += 1
            else:
                failures += 1            
        
    return test_programs, successes, failures, not_applicables
    
def write_results(model_filename, test_programs, successes, failures, not_applicables):
    with open(EVAL_DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(["MODEL FILENAME", "FILENAME", "OUTPUT TYPE", "SIMILARITY SCORE", "RULES", "MAX_BODY_LENGTH", "VARIABLES", "REVISIONS", "SUCCESS"])
        for each in test_programs:
            rules = None if each.program_data is None else each.program_data[0]
            max_body_length = None if each.program_data is None else each.program_data[1]
            variables = None if each.program_data is None else each.program_data[2]
            revision_tags = None if each.revision_tags is None else ','.join([x for x in each.revision_tags])
            
            writer.writerow([model_filename, each.filename, each.output_type, each.similarity_score, rules, max_body_length, variables, revision_tags, each.success])         

def main(argv):
    if len(argv) < 2:
        print('Please provide a model program and a spec file.')
        return
    
    model_filename = argv[0]
    spec_filename = argv[1]
    
    generate_random_programs([spec_filename])
    
    random_programs = sorted([os.path.join(RANDOM_FOLDER, f) for f in os.listdir(RANDOM_FOLDER) if os.path.isfile(os.path.join(RANDOM_FOLDER, f))])
    
    test_programs, successes, failures, not_applicables = run_evaluation(model_filename, random_programs)
    print('Successes:', successes, 'out of', successes + failures)

    write_results(model_filename, test_programs, successes, failures, not_applicables)
    
    

if __name__ == '__main__':
    main(sys.argv[1:])