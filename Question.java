import java.io.*;
import java.util.*;
class Variable{

    public String name;
    public String varType;
    // generated numbers uses these vars range = [floor,numCeil] \ noNos
    // int, double, depended
    public String floor; // least val allowed
    public String ceil; // max val allowed 
    public String[] noNos; // numbers that break stuff 1/x -> x != 0
    // equation
    public String equation;

    // given string of info
    Variable(String info){
        final String VARIABLE_INFO_SEPERATOR = "~";
        String[] infoBits = info.split(VARIABLE_INFO_SEPERATOR);
        this.name = infoBits[0];
        this.varType = infoBits[1];
        // dealing with different types of variables
        switch(this.varType){
            case "int":
            case "dep":
                this.setupNum(infoBits);
                break;
            case "equation":
                this.setupEquation(infoBits);
                break;

        }
    }

    // given the stored var info
    // sets up the number part of the variable
    public void setupNum(String[] infoBits){
        // getting the bounds
        String[] bounds = infoBits[2].split("<");
        this.floor = bounds[0];
        this.ceil = bounds[1];

        // getting the no no numbers
        if(infoBits.length > 3){
            String[] noNosInfo = infoBits[3].split(",");
            int numNoNos = noNosInfo.length;
            String[] noNos = new String[numNoNos];
            for(int index = 0; index < numNoNos; index++){
                noNos[index] = noNosInfo[index];
            }
            this.noNos = noNos;
        }
    }

    // given the stored var info
    // sets up the equation part of the variable
    public void setupEquation(String[] infoBits){
        // fixes all the equation shorthand
        String equation = infoBits[2];
        equation = equation.replace("m.", "Math.");
        this.equation = equation;
    }


    @Override
    public String toString(){
        StringBuilder output = new StringBuilder();
        output.append(name + " " + varType + " ");
        switch(varType){
            case "int":
            case "dep":
                output.append(floor + " ");
                output.append(ceil + " ");
                if(noNos != null){
                    for(String valueNoNo : noNos){
                        output.append(valueNoNo + " ");
                    }
                }
                break;
            case "equation":
                output.append(equation);
        } 
        return output.toString().trim();
    }
    

    // given line of variables
    // returns a variable array
    public static Variable[] parseVariables(String info, String INFO_SEPERATOR){
        // setting up variables
        String[] variablesInfo = info.split(INFO_SEPERATOR);
        int VarDepiables = variablesInfo.length;
        Variable[] variables = new Variable[VarDepiables];
        // setting up all the variables and adding them
        for(int index = 0; index < VarDepiables; index++){
            String variableInfo = variablesInfo[index];
            Variable variable = new Variable(variableInfo);
            variables[index] = variable;
        }
        return variables;
    }
}



public class Question{
    public static final String TOPIC_FOLDER = "/topics/";
    public static final String FIELD_SEPERATOR = ":";
    public static final String INFO_SEPERATOR = "  ";

    public String title;
    public String type;
    // question type equation
    public String question;
    public String hint;
    public String reasoning;
    public int precision;
    public Variable[] variables;
    public String[] equations;


    // creates the reader for the topic file
    public static BufferedReader getReader(String topic) throws FileNotFoundException{
        String path = System.getProperty("user.dir");
        File topicFile = new File(path + TOPIC_FOLDER + topic + ".txt");
        BufferedReader reader = new BufferedReader(new FileReader(topicFile));
        return reader;
    }
    
    public static Question[] readFile(BufferedReader reader) throws IOException{
        ArrayList<Question> questions = new ArrayList<Question>();
        String line;
        Question currentQuestion = null;
        while((line = reader.readLine()) != null){
            // skipping empty lines
            if(line.trim().isEmpty()){
                continue;
            }

            // formatting the line
            String[] split = line.split(FIELD_SEPERATOR,2);
            String field = split[0].toLowerCase();
            if(field.equals("title")){// title has be first for this to work
                currentQuestion = new Question();
                questions.add(currentQuestion);
            }
            String info = "";
            if(split.length == 2){
                info = split[1].trim();
            }

            // adding the info to the current question
            currentQuestion.addInfo(field, info);
        }
        return questions.toArray(new Question[0]);
    }

    // gets all the questions in a topic
    public static Question[] getTopicQuestions(String topic) throws IOException{
        // getting the doc
        BufferedReader reader = getReader(topic);
        
        // reading from the file and setting up all the questions
        Question[] questions = readFile(reader);
        
        return questions;
    }

    // given the field it fills info is formatted and put into its respective field
    public void addInfo(String field, String info){
        switch(field){
            case "title":
                this.title = info;
                break;
            case "type":
                this.type = info;
                break;
            case "question":
                this.question = info;
                break;
            case "hint":
                this.hint = info;
                break;
            case "reasoning":
                this.reasoning = info;
                break;
            case "precision":
                this.precision = Integer.parseInt(info);
                break;
            case "variables":
                this.variables = Variable.parseVariables(info, INFO_SEPERATOR);
                break;
        }
    }

    @Override
    public String toString(){
        StringBuilder output = new StringBuilder();
        output.append("Title: " + this.title + "\n");
        output.append("Question: " + this.question + "\n");
        output.append("Hint: " + this.hint + "\n");
        output.append("Reasoning: " + this.reasoning + "\n");
        output.append("Precision: " + this.precision + "\n");
        output.append("Variables: " + "\n");
        if(variables != null){
            for(Variable var: this.variables){
                output.append("    " + var.toString() + "\n");
            }
        }

        return output.toString();
    }

    public static void main(String[] args) throws IOException{
        String topic = "evaluating 2 speeds";
        Question[] questions = getTopicQuestions(topic);
        System.out.println(questions[0]);
    }
}