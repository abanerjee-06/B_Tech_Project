from flask import Flask, request
import pandas as pd

app = Flask(__name__)

# user response
users_path = './user_response.csv'
# questions
questions_path = './questions.csv'
# quiz names
quiz_path = './quiz.csv'


@app.route('/submit',methods=['POST'])
def submit():
    request_data = request.get_json()
    data = pd.read_csv(users_path)

    Response_id = data.iat[-1,0]
    UserId = request_data['uuid']
    Responses = request_data['responses']
    l = len(Responses)
    for i in range(l):
        data = data.append({
            'response_id': Response_id+i+1,
            'uuid': UserId,
            'qid': Responses[i]['qid'],
            'answer': Responses[i]['answer']
        },ignore_index=True)
    
    data.to_csv(users_path,index=False)
    return {'Success':'true'},200


@app.route('/addquiz',methods=['POST'])
def addquiz():
    request_data = request.get_json()
    data = pd.read_csv(quiz_path)

    quiz_id = data.iat[-1,0]
    quiz_name = request_data['quiz_name']
    data = data.append({
        'quiz_id': quiz_id+1,
        'quiz_name':quiz_name
    },ignore_index=True)
    
    data.to_csv(quiz_path,index=False)
    return {'Success':'true'},200


@app.route('/all',methods=['GET'])
def all():
    data = pd.read_csv(quiz_path)
    D = {}
    L1 = data['quiz_id'].values.tolist()
    L2 = data['quiz_name'].values.tolist()
    for i in range(len(L1)):
        D[L1[i]] = L2[i]
    return D,200


@app.route('/<path:pars>/',methods=['GET'])
def get_quiz(pars):
    data = pd.read_csv(questions_path)
    par1 = '/'.join(pars.split("/",2)[:1])
    par2 = pars.split("/",2)[1:][0]
    
    i = 0
    while(i < len(par1)):
        if (par1[i] == '='):
            break
        i += 1
    par1 = par1[i+1:]
    quiz_id = int(par1)
    df = data.loc[(data.quiz_id == quiz_id)]
    questions = []

    if ord(par2[0])>=48 and ord(par2[0])<=57:
        num = int(par2) 
        print(num)
        if (df.shape[0] < num):
            return {'Success':'false'},404
        else:
            for index,rows in df.iterrows():
                if num == 0:
                    break
                D = {}
                D['qid'] = rows['qid']
                D['question'] = rows['question']
                D['question_type'] = rows['q_type']
                D['options'] = rows['options']
                D['answer'] = rows['answer']
                questions.append(D)
                num -= 1

            return {'quiz_id':quiz_id,'questions':questions},200
            
    elif (par2 == 'all'):    
        for index,rows in df.iterrows():
            D = {}
            D['question_id'] = rows['qid']
            D['question'] = rows['question']
            D['question_type'] = rows['q_type']
            D['options'] = rows['options']
            D['answer'] = rows['answer']
            questions.append(D)
        return {'quiz_id':quiz_id,'questions':questions},200


@app.route('/<path:pars>/',methods=['POST'])
def modify_quizquestions(pars):
    data = pd.read_csv(questions_path)
    par1 = '/'.join(pars.split("/",2)[:1])
    par2 = pars.split("/",2)[1:][0]

    i = 0
    while(i < len(par1)):
        if (par1[i] == '='):
            break
        i += 1
    par1 = par1[i+1:]
    quiz_id = int(par1)
    request_data = request.get_json()
    
    if (par2 == 'addquestions'):
        qid = data.iat[-1,0]
        Questions = request_data['questions']
        l = len(Questions)
        for i in range(l):
            data = data.append({
                'qid': qid+i+1,
                'question': Questions[i]['question'],
                'q_type': Questions[i]['question_type'],
                'options': Questions[i]['options'],
                'answer': Questions[i]['answer'],
                'quiz_id': quiz_id
            },ignore_index=True)
        data.to_csv(questions_path,index=False)
        return {'Success':'true'},200
    
    elif (par2 == 'delete'):
        data = data[data['quiz_id'] != quiz_id]
        
        data.to_csv(questions_path,index=False)
        return {'Success':'true'},200
        
                  
        


if __name__ == "__main__":
    app.run(debug=True,port=5000) 