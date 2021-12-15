import mysql.connector
from flask import Flask,request

app = Flask(__name__)

# Connecting with the MYSQL local server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="algodynamics-BTP-2021",
    database="algodynamics_quiz"
)
cursor = mydb.cursor()


@app.route('/submit',methods=['POST'])
def submit():
    request_data = request.get_json()
    UserId = request_data['uuid']
    Responses = request_data['responses']
    l = len(Responses)
    s = "insert into user_response(uuid,qid,answer) values (%s,%s,%s)"
    try:
        for i in range(l):
            val = (UserId,str(Responses[i]['qid']),Responses[i]['answer'])
            cursor.execute(s, val)
            mydb.commit()
        return "Records entered successfully",200
    except:
        return "Database Error",404


@app.route('/addquiz',methods=['POST'])
def addquiz():
    request_data = request.get_json()
    quiz_name = request_data['quiz_name']
    s = "insert into quiz(quiz_name) values (%s)"
    try:
        cursor.execute(s,(quiz_name,))
        mydb.commit()
        return "Record entered successfully",200
    except:
        return "Database Error",404


@app.route('/<path:pars>/',methods=['POST'])
def modify_quizquestions(pars):
    par1 = '/'.join(pars.split("/",2)[:1])
    par2 = pars.split("/",2)[1:][0]

    i = 0
    while(i < len(par1)):
        if (par1[i] == '='):
            break
        i += 1
    par1 = par1[i+1:]
    request_data = request.get_json()
    
    if (par2 == 'addquestions'):
        Questions = request_data['questions']
        s = "insert into questions values (%s,%s,%s,%s,%s,%s)"
        l = len(Questions)
        try:
            for i in range(l):
                val = (str(Questions[i]['qid']),Questions[i]['question'],Questions[i]['question_type'],Questions[i]['options'],Questions[i]['answer'],par1)
                cursor.execute(s,val)
                mydb.commit()
            return "Records entered successfully",200
        except:
            return "Database Error",404
    
    elif (par2 == 'delete'):
        try:
            cursor.execute("delete from questions where quizid=%s",(par1,))
            mydb.commit()
            return "Record deleted successfully",200
        except:
            return "Database Error",404


@app.route('/all',methods=['GET'])
def all():
    try:
        cursor.execute("select * from quiz")
        res = cursor.fetchall()
        D = {}
        for x in res:
            D[x[0]] = x[1]
        return D,200
    except:
        return "Database Error",404
    
    
@app.route('/<path:pars>/',methods=['GET'])
def get_quiz(pars):
    par1 = '/'.join(pars.split("/",2)[:1])
    par2 = pars.split("/",2)[1:][0]
    
    i = 0
    while(i < len(par1)):
        if (par1[i] == '='):
            break
        i += 1
    par1 = par1[i+1:]
    quiz_id = (par1,)
    questions = []  
    
    try:
        cursor.execute("select * from questions where quizid=%s",quiz_id)
        content = cursor.fetchall()
        if (len(content) == 0):
            return "No entries for given Quiz_Id",404  
    except:
        return "Database Error",404

    if ord(par2[0])>=48 and ord(par2[0])<=57:
        num = int(par2) 
        if (num == 0):
            return "Invalid number of questions",404
        elif (len(content) < num):
            return "Not enough questions for given Quiz_Id",404
        i = 0
        while(i < num):
            D = {}
            D['qid'] = content[i][0]
            D['question'] = content[i][1]
            D['Q_type'] = content[i][2]
            D['options'] = content[i][3]
            D['answer'] = content[i][4]
            questions.append(D)
            i += 1
        return {'Quiz_Id':quiz_id,'questions':questions},200
    
    elif (par2 == 'all'):
        for x in content:
            D = {}
            D['qid'] = x[0]
            D['question'] = x[1]
            D['Q_type'] = x[2]
            D['options'] = x[3]
            D['answer'] = x[4]
            questions.append(D)
        return {'Quiz_Id':quiz_id,'questions':questions},200
        




if __name__ == "__main__":
    app.run(debug=True,port=5000)         
        
    