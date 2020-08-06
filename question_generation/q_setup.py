def q_setup(subject):
    import os,sys
    

    # grabbing the questions from the topic document
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    path = path + '/topics/' + subject + '.txt'
    

    # getting the doc
    f = open(path, 'r')
    qDoc = list(f.readlines())
    f.close()


    # getting the question into a useable format from the doc
    questions = {}
    for line in qDoc:
        # getting rid of empty lines
        if line == '\n':
            continue
        

        # formatting each line into something understandable
        temp = line.split(':', 1)
        part = temp[0]
        meat = temp[1].rstrip()


        # if it is a title it will make a new question dict
        if part == 'title':
            title = meat
            questions[title] = {}
            continue
        

        # cleaning the meats that only require exact formatting
        elif part in ['question', 'type', 'reasoning', 'hint', 'options_list', 'answer']:
            meat = meat.split('<>')[1]
        

        # cleaning up the meats that have multiple items
        elif part in ["variables", "equation_vars", 'seperating operators', 'single operators']:
            meat = meat.split(',,')


            # vars clean up
            if part == "variables":
                for _ in range(len(meat)):                                                              
                    meat[_] = meat[_].replace(' ','').split(':')
                    meat[_][2] = meat[_][2].split('<')


            # equation_vars cleanup
            elif part == "equation_vars":
                meat = [equation.replace(' ','').split('=') for equation in meat]


            # operators cleanup
            elif part in ['seperating operators', 'single operators']:
                meat = [operator.split('<>')[1] for operator in meat]


        # cleaing up number parts
        elif part in ['round', 'operands']:
            meat = int(meat)

        # adding the part once it has been formated
        questions[title][part] = meat


    return questions



# # test to make sure no errors from the setup 
# import os,sys
# path = os.path.abspath(os.path.dirname(sys.argv[0]))
# path = path + '/topics/'
# topics = os.listdir(path)
# topics = [topic.replace('.txt', '') for topic in topics]
# topics.remove('submitted_questions')
# for topic in topics:
#     questions = q_setup(topic)
# print(':) No errors(that would stopping them from running)')