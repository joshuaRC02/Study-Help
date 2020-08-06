def var_replace(string):
    # replacing each var in the dict to its actual var
    for true_var in var_dict:                                                                           
        var = '{}__'.format(true_var)
        string = string.replace(var, str(eval("var_dict['{}']".format(true_var))))
    return string

def q_getter(questions):
    # initalization
    from random import choice
    global var_dict
    var_dict = {}
    question = questions[choice(list(questions.keys()))]


    # dealing with each type of question
    if question['type'] == 'evalulate':
        # checking to make sure the questions answer isn't too large 
        limit = 2 ** 38
        ans_check = limit + 1
        while abs(ans_check) > limit:
            temp_q = q_evalulate(question)
            ans_check = temp_q['answer']
        return temp_q

    elif question['type'] == 'equation':
        return q_equation(question)
    
    elif question['type'] == 'multiple_choice':
        return q_multiple_choice(question)

def q_evalulate(question):
    from random import randint, choice
    import math


    # setting up the operands
    var_dict['operands'] = []
    for _ in range(0, question['operands']):
        # initializing
        var = randint(3, 15) * (randint(0, 1) * 2 - 1)
        single_operators = []
        single_operators+= question['single operators']


        # removing all the operator types that wont work with negative numbers
        if var < 0:                                                                         
            single_operators.remove("math.factorial(x__)")
            single_operators.remove("(x__**y__)")


        # adding single_operators to confuse people
        single = 0
        while randint(1, 2) == 1 or single > 10:
            operator = choice(single_operators)
            single+=1

            if operator in ["(1/x__)", "math.cos(x__)", "math.sin(x__)", "math.tan(x__)", "(x__**y__)"] and "math.factorial(x__)" in single_operators:
                single_operators.remove("math.factorial(x__)")
            elif operator in ["math.factorial(x__)"]:
                single_operators.remove(operator)

            var = operator.replace("x__", str(var))


            # generating a second var if it is required
            if "y__" in operator:
                y = randint(-3,3)
                var = var.replace("y__", str(y))

        var_dict['operands'].append(var)


    # setting up the equation
    seperating_operators = question['seperating operators']
    equation = ""
    while len(var_dict['operands']) > 1:
        equation+= choice(seperating_operators).format(var_dict['operands'].pop())
    equation+= str(var_dict['operands'].pop())

    q_answer = round(eval(equation), question['round'])


    # setting up the question
    q_string = ''
    q_string+= question['question']
    q_string+= '(round {}) '.format(question['round'])
    if any(func in equation for func in ['sin', 'cos', 'tan']):
        q_string+= '(rad)'
    q_string+= ': ' + equation.replace('math.', '').replace('**', '^').replace(' / ', ' ÷ ')


    return {'type':question['type'], 'answer':q_answer, 'question':q_string}

def q_equation(question):
    import random as rand
    import math
    from names import get_first_name


    # generating all the variables
    for var in question['variables']:
        if var[1] == 'int':
            var_dict[var[0]] = rand.randint(int(var[2][0]), int(var[2][1]))


        # var vars (that can also use ints)
        elif var[1] == 'var':                                                                          
            if not str(var[2][0]).isnumeric():
                low = eval(var_replace(var[2][0]))
            else:
                low = int(var[2][0])

            if not str(var[2][1]).isnumeric():
                high = eval(var_replace(var[2][1]))
            else:
                high = int(var[2][1])
            var_dict[var[0]] = rand.randint(low, high)
        

        # getting random names
        elif var[1] == 'names':
            for number in range(1, int(var[2][0]) + 1):
                name = 'name' + str(number)
                var_dict[name] = get_first_name()
    


    # getting the equation variables solved
    for var in question['equation_vars']:
        var_dict[var[0]] = eval(var_replace(var[1]))


    # getting question according to vars
    q_string = ''
    q_string+= question['question']
    q_string = var_replace(q_string)


    # getting reasoning according to vars
    reasoning = []
    reasoning = question['reasoning']
    reasoning = var_replace(reasoning)


    # rounding the answer
    q_answer = round(var_dict['answer'], question['round'])
    q_string = q_string + ' (Round to {} digits)'.format(str(question['round']))


    return {'type':question['type'], 'question':q_string, 'answer':q_answer, 'hint':question['hint'], 'reasoning':reasoning}
     
def q_multiple_choice(question):
    from random import choice, randrange
    import os,sys


    # getting the list of options for the other places
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    path = path + '/lists/{}.txt'.format(question['options_list'])
    f = open(path, 'r')
    options_list = list(f.readlines())
    f.close()


    # setting up the options
    options_list = [option.rstrip() for option in options_list]
    options_list.remove(question['answer'])
    options = []
    x = 5
    for _ in range(x):
        option = choice(options_list)
        options.append(option.replace(' ', '_'))
        options_list.remove(option)    
    options[randrange(0, len(options))] = question['answer'].replace(' ', '_')


    return {'type':question['type'], 'question':question['question'], 'answer':question['answer'], 'options':options}


# # checking to make sure the all the questions actually work
# import os,sys
# from q_setup import q_setup
# path = os.path.abspath(os.path.dirname(sys.argv[0]))
# path = path + '/topics/'
# topics = os.listdir(path)
# topics = [topic.replace('.txt', '') for topic in topics]
# topics.remove('submitted_questions')
# for topic in topics:
#     questions = q_setup(topic)
#     for _ in range(0, 1):
#         print(q_getter(questions))
# print(':) No errors(that would stopping them from running)')