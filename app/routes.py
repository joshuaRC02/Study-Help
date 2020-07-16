# sets up how the website flows
from flask import render_template, flash, redirect, request, url_for, session, send_file
from app import app
from os import getcwd
# home page stuff
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    # initalizing all the vars for the session
    path = getcwd()
    path = path + "/questions/subjects.txt"
    f = open(path, 'r')
    subjects = list(f.readlines())
    f.close()
    subjects = [_.replace('\n', '').replace(" ", "_") for _ in subjects]
    session['question_num'] = 1
    session['correct'] = 0
    session['incorrect'] = 0
    session['streak'] = 0
    session['accuracy'] = 'None wrong so far, good job!'
    if  request.method == 'POST':
        subjects = request.form.getlist('subjects')
        if subjects == []:
            return redirect(url_for('index'))
        session['subjects'] = [_.replace("_", " ") for _ in subjects]
        return redirect(url_for('questions'))
    # renders the given template and then defines vars
    return render_template('index.html', title='Home', subjects=subjects)

@app.route('/question/setup')
def questions():
    from qSetup import qSetup
    subjects = session['subjects']
    session['questions'] = {}
    for _ in subjects:
        _ = _.replace('_', ' ')
        session['questions'].update(qSetup(_))
    return redirect(url_for('testing'))



@app.route('/testing', methods = ['GET', 'POST'])
def testing():
    from timeit import default_timer as timer
    if  request.method == 'POST':
        session['question_num'] = session['question_num'] + 1
        if  session.get('answer') in request.form['answer']:
            session['last_result'] = "Correct, good job!"
            session['correct'] = session['correct'] + 1
            session['streak'] = session['streak'] + 1
        else:
            session['last_result'] = "Incorrect, try again next time."
            session['incorrect'] = session['incorrect'] + 1
            session['streak'] = 0
        if session['incorrect'] != 0:
            session['accuracy'] = session['correct'] / session['incorrect']
        session['last_answer'] = session.pop('answer')
        session['last_hint'] = session.pop('hint')
        session['last_question'] = session.pop('question')
        session['last_reasoning'] = session.pop('reasoning')
        session['last_time'] =  round(timer() - session.pop('time'))
        session['last_answered'] = True
        return redirect(url_for('testing'))

    
    from qGetter import qGetter
    q = list(map(str, qGetter(session['questions'])))
    session['question'] = q[0]
    session['answer'] = q[1]
    session['hint'] = q[2]
    session['reasoning'] =q[3]
    session['time'] = timer()
    return render_template('testing.html', title='Trainer')

@app.route('/submit', methods = ['GET', 'POST'])
def submit():
    if request.method == 'POST':
        path = getcwd()
        path = path + "submitted questions.txt"
        f = open(path, 'a')        
        # adding all the different vars to the new question file
        f.write('subject: "{}'.format(request.form['subject']))
        f.write('title: "{}"\n'.format(request.form['title']))
        f.write('question: "{}"\n'.format(request.form['question']))
        f.write('type: "{}"\n'.format(request.form['type']))
        f.write('variables: {}\n'.format(request.form['variables']))
        f.write('equation_vars: {}\n'.format(request.form['equation_vars']))
        f.write('round: {}\n'.format(request.form['round']))
        f.write('hint: "{}"\n'.format(request.form['hint']))
        f.write('reasoning: "{}"\n'.format(request.form['reasoning']))
        f.close()
        return redirect(url_for('submit'))
    return render_template('submit.html', title='Submit')

@app.route('/submit/download')
def download():
    path = getcwd()
    path = "submitted_questions.txt"
    return send_file(path, as_attachment=True)

@app.route('/new_session')
def new_session():
    session.clear()
    return redirect(url_for('index'))

@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'