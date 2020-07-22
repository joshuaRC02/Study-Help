# sets up how the website flows
from flask import render_template, flash, redirect, request, url_for, session, send_file
from app import app
from os import getcwd
# home page stuff
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    # initalizing all the vars for the session
    session['topic'] = 'subjects'
    question_type = 'checkbox'
    path = getcwd()
    path = path + "/questions/subjects.txt"
    f = open(path, 'r')
    subjects = list(f.readlines())
    f.close()
    subjects = [_.rstrip().replace(" ", "_") for _ in subjects]
    session['question_num'] = 1
    session['correct'] = 0
    session['incorrect'] = 0
    session['streak'] = 0
    session['accuracy'] = 'None wrong so far, good job!'
    if  request.method == 'POST':
        subjects = request.form.getlist('options')
        if subjects == []:
            return redirect(url_for('index'))
        session['subjects'] = [_.replace("_", " ") for _ in subjects]
        return redirect(url_for('question_setup'))
    # renders the given template and then defines vars
    return render_template('index.html', title='Home', options=subjects, question_type=question_type)

@app.route('/question/setup')
def question_setup():
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
        session['question_num']+=1
        if  session.get('answer') in request.form['answer']:
            session['last_result'] = "Correct, good job!"
            session['correct']+= 1
            session['streak']+= 1
        else:
            session['last_result'] = "Incorrect, try again next time."
            session['incorrect']+=1
            session['streak'] = 0
        session['accuracy'] = session['correct'] / session['question_num']
        session['last_answer'] = session.pop('answer')
        session['last_hint'] = session.pop('hint')
        session['last_question'] = session.pop('question')
        session['last_reasoning'] = session.pop('reasoning')
        session['last_time'] =  round(timer() - session.pop('time'))
        session['last_answered'] = True
        return redirect(url_for('testing'))

    
    from qGetter import qGetter
    q = qGetter(session['questions'])
    session['question'] = str(q['question'])
    session['answer'] = str(q['answer'])
    session['hint'] = str(q['hint'])
    session['reasoning'] = str(q['reasoning'])
    session['time'] = timer()
    return render_template('testing.html', title='Trainer')

@app.route('/submit', methods = ['GET', 'POST'])
def submit():
    if request.method == 'POST':
        path = getcwd()
        path = path + "/submitted_questions.txt"
        f = open(path, 'a')        
        # adding all the different vars to the new question file
        f.write('\nsubject: "{}"\n'.format(request.form['subject']))
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

@app.route('/submit_download')
def download():
    path = getcwd()
    path = path + "/submitted_questions.txt"
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

@app.route('/UIL_tests', methods = ['GET', 'POST'])
def UIL_index():
    session['topic'] = 'UIL test'
    question_type = 'radio'
    path = getcwd()
    path = path + "/UIL/UIL_tests.txt"
    f = open(path, 'r')
    tests = list(f.readlines())
    f.close()
    tests = [_.rstrip().replace(" ", "_") for _ in tests]
    if  request.method == 'POST':
        test = request.form['options']
        if test == []:
            return redirect(url_for('UIL_index'))
        session['test_name'] = test
        return redirect(url_for('test_setup'))
    return render_template('index.html', title='UIL Tests', options=tests, question_type=question_type)


@app.route('/test_setup')
def test_setup():
    from qSetup import qSetup
    from qGetter import qGetter
    path = getcwd()
    path = path + "/UIL/{}_UIL.txt".format(session['test_name'])
    f = open(path, 'r')
    test_questions = list(f.readlines())
    f.close()
    question_num = 0
    test = []
    for subjects in test_questions:
        question_num+=1 
        # getting the avaliable subjects to be put in that spot and the question that come with them
        subjects_list = subjects.split(',')
        questions = {}
        for subject in subjects_list:
            questions.update(qSetup(subject.rstrip()))
        # getting a random question from the list 
        question = qGetter(questions)
        # adding the question number to the question
        question['number'] = question_num
        test.append(question)
    session['test'] = test
    return redirect(url_for('UIL_tester'))

@app.route('/UIL_tester', methods = ['GET', 'POST'])
def UIL_tester():
    if request.method == 'POST':
        session['correct'] = session['incorrect'] = session['questions'] = 0
        answerlist = request.form.getlist('answer')
        for q in session['test']:
            answer = answerlist.pop(0)
            q['your_answer'] = answer 
            session['questions']+=1
            if q['answer'] == answer:
                q['result'] = 'Correct'
                session['correct']+=1
            else:
                q['result'] = 'Incorrect'
        session['accuracy'] = session['correct'] / session['questions']
        return redirect(url_for('UIL_results'))
    return render_template('test.html', title='Trainer')

@app.route('/UIL_results', methods = ['GET', 'POST'])
def UIL_results():
    return render_template('test_results.html')
