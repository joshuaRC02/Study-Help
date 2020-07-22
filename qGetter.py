def varReplace(s):
    s = s.split("'")
    for _ in range(len(s)):
        if s[_].isalnum():
            s[_] = "varDict['{}']".format(s[_])

    return ''.join(s)

def qGetter(q):
    import random as rand
    import math
    from names import get_first_name
    # randomly selecting a question and setting it as the question
    qList = list(q.keys())
    question = q[qList[rand.randint(0, len(qList) - 1)]]

    # getting the the range variables generated
    varDict = {}
    for var in question['variables']:
        # getting var integer values 
        if var[1] == 'int':
            varDict[var[0]] = rand.randint(int(var[2][0]), int(var[2][1]))
        # getting var based on var values values
        elif var[1] == 'var':
            low = varReplace(var[2][0])
            high = varReplace(var[2][1])
            varDict[var[0]] = rand.randint(eval(low), eval(high))  
        # getting random names
        elif var[1] =='names':
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
    qString = question['question']
    
    # setting each var in the question to itss corresponding var
    for _  in varDict:
        qString = qString.replace("'{}'".format(_), str(eval(varReplace(_))))

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
    return {'question':qString, 'answer':qAnswer, 'hint':question['hint'], 'reasoning':question['reasoning']}
    

# from qSetup import qSetup
# q = qSetup('ratios')
# print(qGetter(q))