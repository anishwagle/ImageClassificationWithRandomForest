import csv
import pickle
import random

training_data=[]
Random_Training_Data=[]
#this code take imput from training1.csv so uncomment if you wanna train the system with new data
'''
Training_Data_Set=[]
with open('Training1.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
            training_data.append(row)
f.close()
for i in range(100):
    for j in range(60):
        Random_Training_Data.append(training_data[random.randint(0,59)])
    
    Training_Data_Set.append(Random_Training_Data)
    Random_Training_Data=[]
'''
header = ["Gray","Saturation","Entropy","Width", "Height","Item"]

def unique_vals(rows, col):
    """Find the unique values for a column in a dataset."""
    return set([row[col] for row in rows])

def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        return val >= self.value


    def __repr__(self):
        condition = ">="
def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

def find_best_split(rows):
    best_gain = 0 
    best_question = None 
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1 
    for col in range(n_features): 
        values = set([row[col] for row in rows]) 
        for val in values:  
            question = Question(col, val)
            true_rows, false_rows = partition(rows, question)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue
            gain = info_gain(true_rows, false_rows, current_uncertainty)
            if gain > best_gain:
                best_gain, best_question = gain, question
    return best_gain, best_question
class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)

class Decision_Node:
    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

def build_tree(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(question, true_branch, false_branch)

def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return
    print ( str(node.question))
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")
def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)
def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs
def random_tree():
#if __name__ == "__main__":
    Random_Tree=[]
    #uncomment if you are training the random tree
    '''
    for i in range(99):
        my_tree = build_tree(Training_Data_Set[i])
        Random_Tree.append(my_tree)
        
    
    with open ("Random_Tree.pkl",'wb')as output:
        pickle.dump(Random_Tree,output,pickle.HIGHEST_PROTOCOL)
        '''
    #returning trained random tree
    with open ("Random_Tree.pkl",'rb')as input:
        unpickler=pickle.Unpickler(input)
        Random_Tree=unpickler.load()
    testing_data=[]
    #testing_data.append(data)
    #this take input from testing1.csv 
    #i used this for testing data
    
    with open('unknown.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            testing_data.append(row)
    f.close()
    

    #little lazy here :p
    iteam = ["dict_keys(['Mobile'])","dict_keys(['Pant'])","dict_keys(['TShirt'])"]
    #again used this for testing purpose
    
    for row in testing_data:
        for i in range(99):
            mobile=0
            pant=0
            tshirt=0
            my_tree=Random_Tree[i]
            Predection = str(classify(row, my_tree).keys())
            if Predection == iteam[0]:
                mobile +=1
            if Predection == iteam[1]:
                pant +=1
            if Predection == iteam[2]:
                tshirt +=1
        if mobile>pant and mobile >  tshirt:
            print ("Mobile")
            return
        elif pant>tshirt:
            print("Pant")
            return
        else:
            print("TShirt")
            return
