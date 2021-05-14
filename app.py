import sys
from flask import Flask, request, jsonify, render_template
from feedback_gen import main as generate_feedback
from metarep_encoder.messages import Output_type
app = Flask(__name__, template_folder='./')

@app.route('/')
def form():
    data = {}
    
    data['model_program_filename'] = app.config.get('model_filename')
    try:
        data['model_program'] = load_program(data['model_program_filename'])
    except:
        return render_template('./error.html', data='Model program file not found.')
    
    data['student_program_filename'] = app.config.get('model_filename').replace('.lp', '_user.lp')
    try:
        data['student_program'] = load_program(data['student_program_filename'], annotate=True)
    except:
        return render_template('./error.html', data='Student program file not found.')
    
    feedback = generate_feedback([data['model_program_filename']])
    
    if feedback[0] == Output_type.REVISED or feedback[0] == Output_type.NEW_RULES:
        _, correct_excluded, user_included, similarity_score, revisable_rule_ids, feedback_text = feedback
        
        data['success'] = True
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
    if len(sys.argv) < 2:
        print('File name for program required')
    else:
        app.config['model_filename'] = sys.argv[1]
        app.run(threaded=False, port=5000)