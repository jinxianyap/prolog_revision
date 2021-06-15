import sys
import os
import csv
import time
import subprocess
from feedback_gen.feedback_gen import main as generate_feedback
from feedback_gen.constants import Output_type
from evaluation_pkg.generate_random import main as generate_random_programs

RANDOM_FOLDER = 'random_programs'
EVAL_DATA_FILE = 'eval_data.csv'

class TestProgram:
    def __init__(self, number, output_type, similarity_score=None, program_data=None, revision_tags=None, success=None, duration=None):
        self.number = number
        self.output_type = output_type
        self.similarity_score = similarity_score
        self.program_data = program_data
        self.revision_tags = revision_tags
        self.success = success
        self.duration = duration

def run_evaluation(model_filename, random_programs):
    test_programs = []
    successes = 0
    failures = 0
    not_applicables = 0
    
    for i, each in enumerate(random_programs):
        subprocess.run(['killall', 'clingo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['killall', 'ILASP'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(i)
        print(random_programs[i])
        start_time = time.time()
        result = generate_feedback([model_filename, each], is_eval=True)
        test_program = None
        if result[0] in [Output_type.NO_REVISION, Output_type.INCORRECT_ARITIES, Output_type.REORDER_NAF]:
            test_program = TestProgram(i, result[0], success=True)
            not_applicables += 1
        else:
            output_type, similarity_score, program_data, revision_tags, success = result
            duration = time.time() - start_time
            test_program = TestProgram(i, output_type, similarity_score, program_data, revision_tags, success, duration)
            if success: 
                successes += 1
            else:
                failures += 1            
        write_result(model_filename, test_program)
        test_programs.append(test_program)
        
    return test_programs, successes, failures, not_applicables
    
def write_result(model_filename, test_program):
    with open(EVAL_DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        
        syntax_score = None
        semantics_score = None
        revisions_score = None
        
        if test_program.similarity_score is not None:
            syntax_score = test_program.similarity_score[0]
            semantics_score = test_program.similarity_score[1]
            revisions_score = test_program.similarity_score[2]
        
        rules = None if test_program.program_data is None else test_program.program_data[0]
        max_body_length = None if test_program.program_data is None else test_program.program_data[1]
        variables = None if test_program.program_data is None else test_program.program_data[2]
        revision_tags = None if test_program.revision_tags is None else ','.join(test_program.revision_tags)
        
        writer.writerow([model_filename, test_program.number, test_program.output_type, syntax_score, semantics_score, revisions_score, rules, max_body_length, variables, revision_tags, test_program.success, test_program.duration])         

def main(argv):
    if len(argv) < 2:
        print('Please provide a model program and a spec file.')
        return
    
    model_filename = argv[0]
    spec_filename = argv[1]
    
    try:
        generate_random_programs([spec_filename])
    except:
        print('Failed to generate random programs')
        return
    
    random_programs = sorted([os.path.join(RANDOM_FOLDER, f) for f in os.listdir(RANDOM_FOLDER) if os.path.isfile(os.path.join(RANDOM_FOLDER, f))])
    
    with open(EVAL_DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(["MODEL FILENAME", "NUMBER", "OUTPUT TYPE", "SYNTAX SCORE", "SEMANTICS SCORE", "REVISIONS SCORE", "RULES", "MAX_BODY_LENGTH", "VARIABLES", "REVISIONS", "SUCCESS", "DURATION"])
        
    test_programs, successes, failures, not_applicables = run_evaluation(model_filename, random_programs)
    print('Successes:', successes, 'out of', successes + failures)

    # write_results(model_filename, test_programs, successes, failures, not_applicables)
    
    

if __name__ == '__main__':
    main(sys.argv[1:])