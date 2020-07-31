def qSetup(subject):
    # grabbing the questions from a seperate document
    import os,sys
    try :
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = path + '/questions/' + subject + '.txt'
        f = open(path, 'r')
        qDoc = list(f.readlines())
        f.close()
    except:
        print(subject + " is not a subject!")
        return {}
            

    # making the question list usable
    questions = {}
    for line in qDoc:
        temp = line.split(':', 1)
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
        elif temp[0] in ['question', 'type', 'reasoning', 'hint', 'name_list', 'answer']:
            temp[1] = temp[1].split('<>')[1]

        # variables and equationvar clean up
        elif temp[0] in ["variables", "equation_vars"]:
            temp[1] = temp[1].replace(' ','').split(',,')
            # variables clean up
            if temp[0] == "variables":
                for _ in range(len(temp[1])):
                    temp[1][_] = temp[1][_].split(':')
                    temp[1][_][2] = temp[1][_][2].split('<')  
            # equation_vars cleanup
            else:
                temp[1] = [equation.split('=') for equation in temp[1]]

        # round and operators clean up
        elif temp[0] in ['round', 'operands']:
            temp[1] = int(temp[1])

        elif temp[0] in ['seperating operators', 'single operators']:
            temp[1] = temp[1].split(',')
            temp[1] = [thing.split('<>')[1] for thing in temp[1]]

        # adding the parameter once everything has been verified
        questions[title][temp[0]] = temp[1]

    return questions




# q = qSetup('order of operations')
# print(q[set(q.keys()).pop()])