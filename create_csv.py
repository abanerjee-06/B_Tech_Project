import pandas as pd


quiz_id = [1,2,3]
quiz_name = ['Sorting Algorithms(General)','Quick Sort','Time Complexity of Algorithms']

D = {'quiz_id':quiz_id,'quiz_name':quiz_name}
df = pd.DataFrame(D)
df.to_csv('quiz.csv')