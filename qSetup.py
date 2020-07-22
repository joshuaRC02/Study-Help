def qSetup(subject):
    # grabbing the questions from a seperate document
    import os
    try :
        path = os.getcwd()
        path = path + "\\questions\\" + subject + '.txt'
        f = open(path, 'r')
        qDoc = list(f.readlines())
        f.close()
    except:
        print(subject + " is not a subject!")
        return {}
            

    # making the question list usable
    questions = {}
    for _ in qDoc:
        temp = _.split(':', 1)
        # checking if it is an empty line
        if temp[0] == '\n':
            continue
        # getting rid of \n at the end of statements
        temp[1] = temp[1].rstrip()
        # checking to see if it is a new question
        if temp[0] == 'title':
            questions[temp[1]] = {}
            title = temp[1]
            continue
        
        # question, type, and reasoning clean up
        if temp[0] in ['question', 'type', 'reasoning', 'hint']:
            temp[1] = temp[1].split('"')[1]

        # variables and equationvar clean up
        if temp[0] in ["variables", "equation_vars"]:
            temp[1] = temp[1].replace(' ','').split(',')
            # variables clean up
            if temp[0] == "variables":
                for _ in range(len(temp[1])):
                    temp[1][_] = temp[1][_].split(':')
                    temp[1][_][2] = temp[1][_][2].split('<')  
            # equation_vars cleanup
            else:
                for _ in range(len(temp[1])):
                    temp[1][_] = temp[1][_].split('=')

        # round clean up
        if temp[0] == 'round':
            temp[1] = int(temp[1])
        # adding the parameter once everything has been verified
        questions[title][temp[0]] = temp[1]

    return questions




# q = qSetup('sequences')
# print(q[set(q.keys()).pop()])