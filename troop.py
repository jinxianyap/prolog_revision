import sys
import argparse
from flask import Flask, request, jsonify, render_template
from feedback_gen.feedback_gen import main as generate_feedback
from feedback_gen.constants import Output_type, ERROR
app = Flask(__name__, template_folder='./')

@app.route('/')
def form():
    data = {}
    
    data['model_program_filename'] = app.config.get('model_filename')
    try:
        data['model_program'] = load_program(data['model_program_filename'])
    except:
        return render_template('./error.html', data='Model program file not found.')
    
    data['student_program_filename'] = app.config.get('student_filename')
    try:
        data['student_program'] = load_program(data['student_program_filename'], annotate=True)
    except:
        return render_template('./error.html', data='Student program file not found.')
    
    feedback = None
    try:
        feedback = generate_feedback([data['model_program_filename'], data['student_program_filename']], timeout=app.config.get('timeout'))
    except:
        feedback = Output_type.ERROR, ERROR
    
    if feedback[0] == Output_type.REVISED or feedback[0] == Output_type.NEW_RULES:
        _, correct_excluded, user_included, similarity_score, revisable_rule_ids, feedback_text, revision_success = feedback

        data['feedback_gen_success'] = True
        data['revision_success'] = revision_success
        data['positive_examples'] = correct_excluded
        data['negative_examples'] = user_included
        data['similarity_score'] = similarity_score
        data['revisable_rule_ids'] = revisable_rule_ids
        data['revisions'] = feedback_text
        
    else:
        _, msg = feedback
        data['success'] = False
        data['message'] = msg
        
    return render_template('./display.html', data=data)

def run_without_interface(model_filename, user_filename, timeout):
    feedback = generate_feedback([model_filename, user_filename], timeout=timeout)
    
    print()
    print('---------------------------------------')
    print('RESULTS:\n')
    
    print('Original Student Program:')
    student_program = load_program(user_filename, annotate=True)
    for each in student_program:
        print('{} - {}'.format(each, student_program[each]))
    print()  
    
    if feedback[0] == Output_type.REVISED or feedback[0] == Output_type.NEW_RULES:
        _, correct_excluded, user_included, similarity_score, revisable_rule_ids, feedback_text, revision_success = feedback
        
        print('Similarity Score:\t\t{}\n'.format(similarity_score))
        print('Erroneous Rule(s):\t\t{}\n'.format(', '.join(revisable_rule_ids)))
        
        if len(correct_excluded) > 0:
            print('Facts not derived:\t\t{}'.format(correct_excluded[0]))
            for each in correct_excluded[1:]:
                print('\t\t\t\t{}'.format(each))
        else:
            print('Facts not derived:\t\tNone')
        print()
            
        if len(user_included) > 0:
            print('Incorrect facts derived:\t{}'.format(user_included[0]))
            for each in user_included[1:]:
                print('\t\t\t\t{}'.format(each))
        else:
            print('Incorrect facts derived:\tNone')
        print()   
        
        if len(feedback_text) > 0: 
            print('Revisions:\t\t\t{}'.format(feedback_text[0]))
            for each in feedback_text[1:]:
                print('\t\t\t\t{}'.format(each))
        else:
            print('Revisions:\t\t\t\tNone')
        print()
        
        print('Revision Success:\t\t{}'.format(revision_success))
    else:
        _, msg = feedback
        print('Revision Success:\t\tFalse')
        print(msg)
    
def load_program(filename, annotate=False):
    f = open(filename, 'r')
    text = f.read()
    lines = [x for x in text.split('\n') if len(x) > 0 and x[0] != '%' and x[0] != '#']
    if annotate:
        rules = {}
        for i in range(len(lines)):
            rules['r'+str(i+1)] = lines[i]
            # lines[i] = 'r{} - {}'.format(str(i+1), lines[i])
        return rules
    return lines     

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Troop - Automated Feedback Generation for Prolog')
    parser.add_argument('-d', action='store_true', help='run without HTML interface')
    parser.add_argument('--timeout', type=int, help='set timeout duration (default: 30s)')
    parser.add_argument('model_filename', type=str, help='model program filename')
    parser.add_argument('user_filename', type=str, help='user program filename')
    args = parser.parse_args()
    
    if args.d:
        run_without_interface(args.model_filename, args.user_filename, args.timeout)
    else:
        app.config['model_filename'] = args.model_filename
        app.config['student_filename'] = args.user_filename
        app.config['timeout'] = args.timeout
        app.run(threaded=False, port=5000)