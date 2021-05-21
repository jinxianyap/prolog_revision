import sys
import os
from feedback_gen.feedback_gen import main as generate_feedback
from evaluation_pkg.generate_random import main as generate_random_programs

RANDOM_FOLDER = 'random_programs'

def main(argv):
    if len(argv) < 2:
        print('Please provide a model program and a spec file.')
        return
    
    model_filename = argv[0]
    spec_filename = argv[1]
    
    generate_random_programs([spec_filename])
    
    random_programs = sorted([os.path.join(RANDOM_FOLDER, f) for f in os.listdir(RANDOM_FOLDER) if os.path.isfile(os.path.join(RANDOM_FOLDER, f))])
    
    successes = 0
    for i, each in enumerate(random_programs):
        result = generate_feedback([model_filename, each], True)
        print(i, result)
        
    print('Successes:', successes)
    
    

if __name__ == '__main__':
    main(sys.argv[1:])