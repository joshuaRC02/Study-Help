def varReplace(s):
    s = s.split("'")
    for _ in range(len(s)):
        if s[_] in list(varDict.keys()):
            s[_] = "varDict['{}']".format(s[_])

    return ''.join(s)

def qGetter(q):
    import random as rand
    import math
    from names import get_first_name
    # randomly selecting a question and setting it as the question
    qList = list(q.keys())
    question = q[qList[rand.randint(0, len(qList) - 1)]]
    global varDict 
    varDict = {}

    # dealing with evalulate questions
    if question['type'] == 'evalulate':
        # generating all the variables in the expression
        varDict['operands'] = []
        for _ in range(0, question['operands']):
            # getting rid of 0 and making a smart way to get negative or positive
            var = rand.randint(5, 10) * (rand.randint(0, 1) * 2 - 1)
            single_operators = []
            single_operators+= question['single operators']
            # removing all the operator types that wont work with negative numbers
            if var < 0:
                single_operators.remove("math.factorial('x')")
                single_operators.remove("('x'**'y')")
            # adding single_operators to confuse people
            single = 0
            while rand.randint(1, 2) == 1 or single > 10:
                # getting a random single operator
                operator = rand.choice(single_operators)
                # making sure to get rid of factorial if the new result could be not a whole number
                if operator in ["(1/'x')", "math.cos('x')", "math.sin('x')", "math.tan('x')", "('x'**'y')"] and "math.factorial('x')" in single_operators:
                    single_operators.remove("math.factorial('x')")
                elif operator == "math.factorial('x')":
                    single_operators.remove("math.factorial('x')")
                # adding the var to the single operator
                var = operator.replace("'x'", str(var))
                # if there is a second var involved with the operator then it will be generated and filled in
                if "'y'" in operator:
                    y = rand.randint(-3,3)
                    var = var.replace("'y'", str(y))
                single+=1
            varDict['operands'].append(var)
        # setting up the equation
        seperating_operators = question['seperating operators']
        equation = ""
        while len(varDict['operands']) > 1:
            equation+= rand.choice(seperating_operators).format(varDict['operands'].pop())
        equation+= str(varDict['operands'].pop())

        # getting the answer
        qAnswer = round(eval(equation), question['round'])

        # setting up the question
        qString = ''
        qString+= question['question']
        qString+= '(round {}) '.format(question['round'])
        if any(func in equation for func in ['sin', 'cos', 'tan']):
            qString+= '(rad)'
        qString+= ': ' + equation.replace('math.', '').replace('**', '^').replace(' / ', ' ÷ ')
        return {'type':question['type'], 'answer':qAnswer, 'question':qString}

    elif question['type'] == 'equation':
        for var in question['variables']:
            # getting var integer values 
            if var[1] == 'int':
                varDict[var[0]] = rand.randint(int(var[2][0]), int(var[2][1]))
            # getting var based on var values values
            elif var[1] == 'var':
                if not var[2][0].isnumeric():
                    low = eval(varReplace(var[2][0]))
                else:
                    low = int(var[2][0])
                if not var[2][1].isnumeric():
                    high = eval(varReplace(var[2][1]))
                else:
                    high = int(var[2][1])
                varDict[var[0]] = rand.randint(low, high)  
            # getting random names
            elif var[1] == 'names':
                for _ in range(1, int(var[2][0]) + 1):
                    name = 'name' + str(_)
                    varDict[name] = get_first_name()
            # adding incase of weird stuff like float
            else:
                varDict[var[0]] = rand.uniform(var[2][0], var[2][1])
        

        # getting the equation variables generated
        for var in question['equation_vars']:
            # generating what the equation_var equals and adding it to the var dict
            varDict[var[0]] = eval(varReplace(var[1]))

        # getting question according to vars
        qString = []
        qString = question['question']
        
        # setting each var in the question to its corresponding var
        for _  in varDict:
            # making it so you can throw the leading 0s on a var by adding '~~' to it
            if '~~' in _:
                lead = str(eval(varReplace(_))).zfill(2)
                qString = qString.replace("'{}'".format(_), lead)
            else:
                qString = qString.replace("'{}'".format(_), str(eval(varReplace(_))))
            

        # getting question according to vars
        reasoning = []
        reasoning = question['reasoning']
        # setting each var in the reasoning to its corresponding var
        for _  in varDict:
            reasoning = reasoning.replace("'{}'".format(_), str(eval(varReplace(_))))
        # rounding the answer and fixing weird things
        qAnswer = round(varDict['answer'], question['round'])
        qString = qString + ' (Round to {} digits)'.format(str(question['round']))
        # making it so 0 rounding is actually integer rounding
        if question['round'] < 1:
            try:
                if qAnswer.is_integer():
                    qAnswer = int(qAnswer)
            except:
                qAnswer = qAnswer
        
        # giving all important info on a question back
        return {'type':question['type'], 'question':qString, 'answer':qAnswer, 'hint':question['hint'], 'reasoning':reasoning}
    
    elif question['type'] == 'multiple_choice':
        import os
        # getting the list of options for the other places
        path = os.getcwd()
        path = path + '/lists/{}.txt'.format(question['name_list'])
        f = open(path, 'r')
        option_list = list(f.readlines())
        f.close()

        # striping the \n off the end of each list entry
        option_list = [option.rstrip() for option in option_list]

        # removing the answer choice from the options to avoid two right answers
        option_list.remove(question['answer'])
        options = []

        # gets x options and sets adds them to the list and removes the from option list
        x = 5
        for _ in range(x):
            option = rand.choice(option_list)
            options.append(option.replace(' ', '_'))
            option_list.remove(option)

        
        # changes a random option to the correct answer
        options[rand.randrange(0, len(options))] = question['answer'].replace(' ', '_')
        return {'type':question['type'], 'question':question['question'], 'answer':question['answer'], 'options':options}
    
# # checking to make sure the question does not go too high
# from qSetup import qSetup
# q = qSetup('order of operations')
# answer = 0
# n = 0
# while answer < 100000000000000 and n < 3000:
#     question = qGetter(q)
#     answer = question['answer']
#     n+=1
# print(question['answer'])
# print(question['question'])

# # checking to make sure the question actually works
# from qSetup import qSetup
# q = qSetup('evaluating 2 speeds')
# print(qGetter(q))