import math
import operator
import collections
import random
import sys


train_file, test_file, type_of_classification, stump_count = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
R = {}
G = {}
B = {}
orientation = {}
weight = {}
R_test = {}
G_test = {}
B_test = {}
orientation_test = {}


#ADABOST LOGIC

# We have implemented simple classifiers i.e. R>B, R>G and G>B on randomly selected pixels. 
# We select the best classifier according to the max correct predictions of the simple classifier.
#This function is called when adaboost is choosen as a classifer
#this method accepts all the files and call all the functions related to Adaboost.
def start_adaboost():
        global train_file, test_file, type_of_classification, stump_count, R, G, B, orientation, weight, R_test, G_test, B_test, orientation_test
        content = {}
        R = {}
        G = {}
        B = {}
        orientation = {}
        weight = {}

		#Reading train file in temp variable.
        with open(train_file, 'r+') as f:
                temp = f.readlines()
				
        for item in temp:
                words = item.split()
				#orientation dictionary has all the actual orientations.
                orientation[words[0]+words[1]] = int(words[1])
				#R dictionary has all the R components of the image.
                R[words[0]+words[1]] = map(int, words[2::3])
				#G dictionary has all the R components of the image.
                G[words[0]+words[1]] = map(int, words[3::3])
				#B dictionary has all the R components of the image.
                B[words[0]+words[1]] = map(int, words[4::3])
				#weights has all the weights which are initialised to 1/no_of_files in the training set.
                weight[words[0]+words[1]] = float(1) / len(temp)
		
		#Reading train file in temp variable
        with open(test_file, 'r+') as f:
                temp1 = f.readlines()

        R_test = {}
        G_test = {}
        B_test = {}
        orientation_test = {}
		
		#Test data is also gathered as training data is gathered but in different variables.
        for item in temp1:
                words = item.split()
                orientation_test[words[0]+words[1]] = int(words[1])
                R_test[words[0]+words[1]] = map(int, words[2::3])
                G_test[words[0]+words[1]] = map(int, words[3::3])
                B_test[words[0]+words[1]] = map(int, words[4::3])

		#Ensemble for 0 oreintation
        model0 = ensemble(0, stump_count)
		#Ensemble for 90 oreintation
        model90 = ensemble(90, stump_count)
		#Ensemble for 180 oreintation
        model180 = ensemble(180, stump_count)
		#Ensemble for 270 oreintation
        model270 = ensemble(270, stump_count)

        cor_count = 0
	confusion_matrix = {}
	predicted_orientation = {}
        for item in R_test.keys():
                temp = test_model(item, R_test, model0, model90, model180, model270)
		predicted_orientation[item] = temp
                if orientation_test[item] == temp:
                        cor_count = cor_count + 1
                if orientation_test[item] in confusion_matrix.keys():
                        confusion_matrix[orientation_test[item]].append(temp)
                else:
                        confusion_matrix[orientation_test[item]] = [temp]
	print("Writing contentes to adaboost_output.txt")
	with open("adaboost_output.txt", "w") as f:
		f.write("To each file name I have appended its actual orientation just for reference. \n")
		for item in predicted_orientation.keys():
        		f.write(str(item) + "\t" + str(predicted_orientation[item]) + "\n")


        for item in confusion_matrix.keys():
                confusion_matrix[item] = dict(collections.Counter(confusion_matrix[item]))

        print ("Accuracy: ", float(cor_count)/len(R_test.keys())*100)

        print ("Confusion Matrix: ")
        res_keys = map(int, confusion_matrix.keys())
        for i in res_keys:
                for j in res_keys:
                        if j in confusion_matrix[i].keys():
                                print(confusion_matrix[i][j]),
                        else:
                                print (0),
                print

# This function is used for initializing the weights.				
def initialize_weights():
        global weight, R
        for item in R.keys():
        	weight[item] = float(1) / len(R.keys())

# Adjust the weight after each stump. 			
def adjust_weight(best_fit, pixel, orient, e_m):
        global weight, R, G, orientation
        error_list = []
        if best_fit == 'R_G':
                for item in R.keys():
                        if R[item][pixel] > G[item][pixel] and orientation != orient:
                                weight[item] = weight[item] * math.sqrt((1-e_m)/(e_m))
                        else:
                                weight[item] = weight[item] * math.sqrt(e_m/(1-e_m))
        elif best_fit == 'G_B':
                for item in R.keys():
                        if G[item][pixel] > B[item][pixel] and orientation != orient:
                                weight[item] = weight[item] * math.sqrt((1-e_m)/e_m)
                        else:
                                weight[item] = weight[item] * math.sqrt(e_m/(1-e_m))
        else:
                for item in R.keys():
                        if R[item][pixel] > B[item][pixel] and orientation != orient:
                                weight[item] = weight[item] * math.sqrt((1-e_m)/e_m)
                        else:
                                weight[item] = weight[item] * math.sqrt(e_m/(1-e_m))

# Find the most suitable stump so that the max wrongly predicted elements in the previous stump 
# are correctly predicted in this stump.								
def stump(pixel, orient):
        global weight, R, G, B, orientation
        error = []
        R_B = 0
        G_B = 0
        R_G = 0
        for item, value in R.iteritems():
                if R[item][pixel] > G[item][pixel] and orientation[item] == orient:
                        R_G = R_G + weight[item]
                if G[item][pixel] > B[item][pixel] and orientation[item] == orient:
                        G_B = G_B + weight[item]
                if R[item][pixel] > B[item][pixel] and orientation[item] == orient:
                        R_B = R_B + weight[item]

        e_m = min(R_G, G_B, R_B)/len(R.keys())

        probs = {'R_G': R_G, 'G_B': G_B, 'R_B': R_B}

        best_fit = max(probs, key = probs.get)
        adjust_weight(best_fit, pixel, orient, e_m)
        return ([pixel, best_fit])

# This function creates the ensemle for the given orientation.		
def ensemble(orient, num_of_stumps):
        model = []
        initialize_weights()
        for i in range(num_of_stumps):
                pixel = random.randint(0, 60)
                model.append(stump(pixel, orient))
        return model

# Test the ensemble on test data and find the correctly predicted elements.		
def test_ensemble(orient, item, model):
        global R_test, G_test, B_test, orientation_test
        count = 0
        for i in model:
                if i[1] == 'R_G':
                        if R_test[item][i[0]] > G_test[item][i[0]] and orientation_test[item] == orient:
                                count = count + 1
                elif i[1] == 'G_B':
                        if G_test[item][i[0]] > B_test[item][i[0]] and orientation_test[item] == orient:
                                count = count + 1
                else:
                        if R_test[item][i[0]] > B_test[item][i[0]] and orientation_test[item] == orient:
                                count = count + 1
        return (float(count)/len(R_test.keys())*100)

# Find the ensemble with max correct rate.		
def test_model(item, R_test, model0, model90, model180, model270):
        probs = {0: test_ensemble(0, item, model0), 90: test_ensemble(90, item, model90), 180: test_ensemble(180, item, model180), 270: test_ensemble(270, item, model270)}
        return max(probs, key = probs.get)

# k nearest neighbor type_of_classification
#execution-time maximum 25 minutes
def nearest(stump_count):
    def dataprocessing(fname, data):
        with open(fname) as f:
            for line in f:
                data.append([n if '.jpg' in n else int(n) for n in line.strip().split(' ')])
    #Applying Euclidean distance
    def heuristic_function(image1, image2):
        euc_distance = 0
        for m in range(2, len(image1)):
            euc_distance += abs(((image1[m]) - (image2[m])))
        return (euc_distance)
    #type_of_classification
    def k_nearest_neighbors(traindata, testinput, k):
        euc_distances = []
        for m in range(len(traindata)):
            dist = heuristic_function(testinput, traindata[m])
            euc_distances.append((traindata[m][1], dist))
        euc_distances.sort(key=operator.itemgetter(1))
        nearest_neighbors = []
        for m in range(k):
            nearest_neighbors.append(euc_distances[m][0])
        return nearest_neighbors
    #assigning label
    def assigning_label(knearestneighbors):
        counter = collections.Counter(knearestneighbors)
        assigned_label = counter.most_common(1)[0][0]
        return assigned_label

    def accuracy(testdata):
        right = 0
        for m in range(len(testdata)):
            try:
                if testdata[m][1] == testdata[m][len(testdata[m])-1]:
                    right += 1
            except ValueError:
                print "ERROR"

        return (right/float(len(testdata))) * 100

    def update_c_matrix(class_label, assigned_label, c_matrix):
        if class_label == 0:
            if assigned_label ==0:
                c_matrix[0][0] += 1
            if assigned_label ==90:
                c_matrix[0][1] += 1
            if assigned_label ==180:
                c_matrix[0][2] += 1
            if assigned_label ==270:
                c_matrix[0][3] += 1
        if class_label == 90:
            if assigned_label ==0:
                c_matrix[1][0] += 1
            if assigned_label ==90:
                c_matrix[1][1] += 1
            if assigned_label ==180:
                c_matrix[1][2] += 1
            if assigned_label ==270:
                c_matrix[1][3] += 1

        if class_label == 180:
            if assigned_label ==0:
                c_matrix[2][0] += 1
            if assigned_label ==90:
                c_matrix[2][1] += 1
            if assigned_label ==180:
                c_matrix[2][2] += 1
            if assigned_label ==270:
                c_matrix[2][3] += 1

        if class_label == 270:
            if assigned_label ==0:
                c_matrix[3][0] += 1
            if assigned_label ==90:
                c_matrix[3][1] += 1
            if assigned_label ==180:
                c_matrix[3][2] += 1
            if assigned_label ==270:
                c_matrix[3][3] += 1

        return c_matrix


    def nearest_basic(stump_count):
        traindata, testdata, c_matrix = [], [], [[0,0,0,0], [0,0,0,0],[0,0,0,0], [0,0,0,0]]

        dataprocessing(train_file, traindata)
        dataprocessing(test_file, testdata)

        target = open('nearest_output.txt', 'w')
        k = stump_count
        for i in range(len(testdata)):
            nearest_neigbors = k_nearest_neighbors(traindata, testdata[i], int(k))
            label_assigned = assigning_label(nearest_neigbors)
            testdata[i].append(label_assigned)
            target.write(testdata[i][0] + ' ' +str(label_assigned))
            target.write("\n")
            c_matrix = update_c_matrix(testdata[i][1], label_assigned, c_matrix)
        accuracy_value = accuracy(testdata)
        print ('Accuracy: ' + str(accuracy_value) + '%')
        print "Confusion_Matrix"
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in c_matrix]))
        target.close()
    nearest_basic(stump_count)

#improved k nearest neighbor type_of_classification
#execution time reduced to 10-12minutes from 25 minutes
def nearest_improved(stump_count):
    def dataprocessing(fname, data):
        with open(fname) as f:
            for line in f:
                data.append([n if '.jpg' in n else int(n) for n in line.strip().split(' ')])

    def heuristic_function(image1, image2):
        euc_distance = 0
        for m in range(2, len(image1)):
            euc_distance += abs(((image1[m]) - (image2[m])))
        return (euc_distance)

    def k_nearest_neighbors(traindata, testinput, k):
        euc_distances = []
        for m in range(len(traindata)):
            dist = heuristic_function(testinput, traindata[m])
            euc_distances.append((traindata[m][1], dist))
        euc_distances.sort(key=operator.itemgetter(1))
        nearest_neighbors = []
        for x in range(k):
            nearest_neighbors.append(euc_distances[x][0])
        return nearest_neighbors

    def assigning_label(knearestneighbors):
        counter = collections.Counter(knearestneighbors)
        assigned_label = counter.most_common(1)[0][0]
        return assigned_label

    def accuracy(testdata):
        right = 0
        for x in range(len(testdata)):
            try:
                if testdata[x][1] == testdata[x][len(testdata[x])-1]:
                    right += 1
            except ValueError:
                print "ERROR"

        return (right/float(len(testdata))) * 100

    def normalizing(data):
        max_value = 0
        min_value = 1000000
        for i in ((data)):
            for j in range(2, len(i)):
                if i[j] > max_value:
                    max_value = i[j]
                if i[j] < min_value:
                    min_value = i[j]

        for i in ((data)):
            for j in range(2, len(i)):
                i[j] = (i[j] - min_value) / (max_value - min_value)

    def update_c_matrix(class_label, assigned_label, c_matrix):
        if class_label == 0:
            if assigned_label ==0:
                c_matrix[0][0] += 1
            if assigned_label ==90:
                c_matrix[0][1] += 1
            if assigned_label ==180:
                c_matrix[0][2] += 1
            if assigned_label ==270:
                c_matrix[0][3] += 1
        if class_label == 90:
            if assigned_label ==0:
                c_matrix[1][0] += 1
            if assigned_label ==90:
                c_matrix[1][1] += 1
            if assigned_label ==180:
                c_matrix[1][2] += 1
            if assigned_label ==270:
                c_matrix[1][3] += 1

        if class_label == 180:
            if assigned_label ==0:
                c_matrix[2][0] += 1
            if assigned_label ==90:
                c_matrix[2][1] += 1
            if assigned_label ==180:
                c_matrix[2][2] += 1
            if assigned_label ==270:
                c_matrix[2][3] += 1

        if class_label == 270:
            if assigned_label ==0:
                c_matrix[3][0] += 1
            if assigned_label ==90:
                c_matrix[3][1] += 1
            if assigned_label ==180:
                c_matrix[3][2] += 1
            if assigned_label ==270:
                c_matrix[3][3] += 1

        return c_matrix

    def reduced_time(stump_count):
        traindata, testdata, traindata_before, testdata_before, c_matrix = [], [], [], [], [[0,0,0,0], [0,0,0,0],[0,0,0,0], [0,0,0,0]]

        dataprocessing(train_file, traindata_before)
        dataprocessing(test_file, testdata_before)
        for y in range(len(traindata_before)):
            temp = []
            x = 0
            while x < len(traindata_before[y]):
                if x == 0:
                    temp.append(traindata_before[y][x])
                    temp.append(traindata_before[y][x+1])
                else:
                    temp.append(0.2989*traindata_before[y][x] + 0.5870*traindata_before[y][x+1] + 0.1140*traindata_before[y][x+2])
                if x == 0:
                    x += 2
                else:
                    x += 3
            traindata.append(temp)
        x = 0
        for y in range(len(testdata_before)):
            temp = []
            x = 0
            while x < len(testdata_before[y]):
                if x == 0:
                    temp.append(testdata_before[y][x])
                    temp.append(testdata_before[y][x+1])
                else:
                    temp.append(0.2989*testdata_before[y][x] + 0.5870*testdata_before[y][x+1] + 0.1140*testdata_before[y][x+2])
                if x == 0:
                    x += 2
                else:
                    x += 3
            testdata.append(temp)
        normalizing(testdata)
        normalizing(traindata)
        target = open('nearest_output_improved.txt', 'w')
        k = stump_count
        for i in range(len(testdata)):
            nearest_neigbors = k_nearest_neighbors(traindata, testdata[i], int(k))
            label_assigned = assigning_label(nearest_neigbors)
            testdata[i].append(label_assigned)
            target.write(testdata[i][0] + ' ' + str(label_assigned))
            target.write("\n")
            c_matrix = update_c_matrix(testdata[i][1], label_assigned, c_matrix)
        accuracy_value = accuracy(testdata)
        print "Confusion_Matrix"
        print ('Accuracy: ' + str(accuracy_value) + '%')
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in c_matrix]))
        target.close()
    reduced_time(stump_count)

LEARNING_RATE=.6

def multiply_matrix(X, Y):
    result = [[sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]
    return result


def create_matrix(mat, row, column,val):
    for i in range(row):
        mat.append([val] * column)


def read_input(file_name, input_data,img_names):
    for line in open(file_name, "r"):
        temp = line.rstrip("\n").split(" ")
        if len(temp)==0:
            continue

        p = [0, 0, 0, 0]
        if int(temp[1]) == 0:
            p[3] = 1
        elif int(temp[1]) == 90:
            p[2] = 1
        elif int(temp[1]) == 180:
            p[1] = 1
        elif int(temp[1]) == 270:
            p[0] = 1
        img_names.append(temp[0])
        t = map(float, temp[2:])
        t.append(1)
        for i in range(0, len(t)):
             t[i] /= 255.00000

        map((lambda x: x/255.0), t)
        q = [t, p]
        input_data.append(q)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

#Implemented feedforward to classify image-orientation
def feedforward(input_data, weight_level1, weight_level2, hidden_nodes_count):

    aj = multiply_matrix([input_data], weight_level1)
    
    for i in range(len(aj[0])):
        aj[0][i] = sigmoid(aj[0][i])
    aj[0][hidden_nodes_count] = 0.001
    aj2 = multiply_matrix(aj, weight_level2)
    for i in range(len(aj2[0])):
        aj2[0][i] = sigmoid(aj2[0][i])
    return aj, aj2


def train_nn(train_data, weight_level1, weight_level2, input_node_count, hidden_nodes_count, output_node_count,img_names):
    one_matrix=[]
    create_matrix(one_matrix,1,output_node_count,1)
    one_matrix2=[]
    create_matrix(one_matrix2,1,hidden_nodes_count+1,1)
    matrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    target_file_nn3=open('weight_layer1.txt','w')
    target_file_nn2=open('weight_layer2.txt','w')
    for m in range(0,1):
        correct=0.0
        counter=0
        for example in train_data:
            input_data = example[0]
            expected_output = example[1]
            hidden_layer_output, main_output = feedforward(input_data, weight_level1, weight_level2,
                                                                 hidden_nodes_count)
            #code to
            #this is expected-actual output
            main_index=main_output[0].index(max(main_output[0]))
            actual_index=expected_output.index(1)
            matrix[actual_index][main_index]+=1
            counter+=1
            if main_index==actual_index:
                correct+=1
            delta_main_output=[a_i - b_i for a_i, b_i in zip(expected_output, main_output[0])]
            #this is 1 is actual output
            one_minus_original_output=[a_i - b_i for a_i, b_i in zip(one_matrix[0],main_output[0])]
            mult_term1=[a_i * b_i for a_i, b_i in zip(main_output[0],one_minus_original_output)]
            error_output_node=[a_i * b_i for a_i, b_i in zip(mult_term1,delta_main_output)]
            one_minus_hidden_output=[a_i - b_i for a_i, b_i in zip(one_matrix2[0],hidden_layer_output[0])]
            mult_term12=[a_i * b_i for a_i, b_i in zip(hidden_layer_output[0],one_minus_hidden_output)]
            error_hidden_node=[]
            for hidden_node_w in range(len(weight_level2)):
                summation=0.0
                for output_node__w in range(len(weight_level2[hidden_node_w])):
                    summation+=weight_level2[hidden_node_w][output_node__w]*error_output_node[output_node__w]
                    weight_level2[hidden_node_w][output_node__w]+= LEARNING_RATE*error_output_node[output_node__w]*hidden_layer_output[0][hidden_node_w]
                summation*=mult_term12[hidden_node_w]
                error_hidden_node.append(summation)

            for input_node in range(len(weight_level1)-1):
                for hidden_node_w in range(len(weight_level1[input_node])):
                    weight_level1[input_node][hidden_node_w]+= LEARNING_RATE*input_data[input_node]*error_hidden_node[hidden_node_w]
            #print str(hidden_layer_output)
        for input_node in range(len(weight_level1)):
            t=""
            for hidden_node_w in range(len(weight_level1[input_node])):
               t+=" "+str(+weight_level1[input_node][hidden_node_w])
            t=t.lstrip(" ")
            t=t+"\n"
            target_file_nn3.write(t)
        target_file_nn3.close()
        for hidden_node_w in range(len(weight_level2)):
            t=""
            for output_node__w in range(len(weight_level2[hidden_node_w])):
                t+=" "+str(+weight_level1[input_node][hidden_node_w])
            t=t.lstrip(" ")
            t=t+"\n"

            target_file_nn2.write(t)
        target_file_nn2.close()
        print "Train Accuracy: " + str(correct/len(train_data) *100)
        print "Output_Matrix:"
        print('\n'.join([''.join(['{:10}'.format(item) for item in row]) for row in matrix]))
       
def predict(test_data, weight_level1, weight_level2, input_node_count, hidden_nodes_count, output_node_count,img_names,isbest):
    correct=0.0
    matrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    counter=1
    if isbest:
        target_file_nn=open('best_output.txt','w')
    if not isbest:
        target_file_nn=open('nnet_output.txt','w')
    for example in test_data:
        input_data = example[0]
        expected_output = example[1]
        hidden_layer_output, main_output = feedforward(input_data, weight_level1, weight_level2,
                                                             hidden_nodes_count)

        #this is expected-actual output
        main_index=main_output[0].index(max(main_output[0]))
        actual_index=expected_output.index(1)
        matrix[actual_index][main_index]+=1
        if main_index==0:
            target_file_nn.write(str(img_names[counter])+" 270\n")
        elif main_index==1:
            target_file_nn.write(str(img_names[counter])+" 180\n")
        elif main_index==2:
            target_file_nn.write(str(img_names[counter])+" 90\n")
        elif main_index==3:
            target_file_nn.write(str(img_names[counter])+" 0\n")
        counter+=1
        if main_index==actual_index:
                correct+=1
    target_file_nn.close()
    print "Test Accuracy: " + str(correct/len(test_data) *100)
    print "Output_Matrix:"
    print('\n'.join([''.join(['{:10}'.format(item) for item in row]) for row in matrix]))

def initialize_weight(weight_level1, weight_level2, input_node_count, hidden_nodes_count, output_node_count):
    create_matrix(weight_level1,input_node_count,hidden_nodes_count+1,0.0)
    create_matrix(weight_level2,hidden_nodes_count+1,output_node_count,0.0)
    epsilon1 = math.sqrt(6) / math.sqrt(input_node_count + hidden_nodes_count + 1);
    epsilon2 = math.sqrt(6) / math.sqrt(hidden_nodes_count + output_node_count + 1);
    for i in range(input_node_count):
        for j in range((hidden_nodes_count + 1)):
            weight_level1[i][j] = random.uniform(-.1, .1)
    for i in range((hidden_nodes_count + 1)):
        for j in range(output_node_count):
            weight_level2[i][j] = random.uniform(-.1, .1)

#Step3 
def NN(stump_count):
    weight_level1 = []
    weight_level2 = []
    train_data = []
    test_data=[]
    img_names=[]
    input_node_count = 193
    hidden_nodes_count = stump_count
    output_node_count = 4
    initialize_weight(weight_level1, weight_level2, input_node_count, hidden_nodes_count, output_node_count)
    print "Weight Initialized for Neural Network"
    read_input(train_file, train_data,img_names)
    read_input(test_file, test_data,img_names)
    print "Input Data read"
    train_nn(train_data, weight_level1, weight_level2, input_node_count, hidden_nodes_count, output_node_count,img_names)
    predict(test_data, weight_level1, weight_level2, input_node_count, hidden_nodes_count, output_node_count,img_names,False)
    print "Matrix  each row and column corresponds to 270 180 90 0 respectively"

def read_weight(weight_level1,weight_level2):

    for line in open("weight_layer1.txt", "r"):
        temp = line.rstrip("\n").split(" ")
        if len(temp)==0:
            continue
        temp=map(float, temp)
        weight_level1.append(temp)
    for line in open("weight_layer2.txt", "r"):
        temp = line.rstrip("\n").split(" ")
        if len(temp)==0:
            continue
        temp=map(float, temp)
        weight_level2.append(temp)
#Step 4
def NN_Best(stump_count):
    weight_level1 = []
    weight_level2 = []
    train_data = []
    test_data=[]
    img_names=[]
    input_node_count = 193
    hidden_nodes_count = stump_count
    output_node_count = 4
    print "Weight Initialized for Neural Network Best type_of_classification"
    read_weight(weight_level1,weight_level2)
    read_input(train_file, train_data,img_names)
    read_input(test_file, test_data,img_names)
    print "Input Data read"
    train_nn(train_data, weight_level1, weight_level2, input_node_count, hidden_nodes_count, output_node_count,img_names)
    best=True
    predict(test_data, weight_level1, weight_level2, input_node_count, hidden_nodes_count, output_node_count,img_names,best)
    print "Matrix  each row and column corresponds to 270 180 90 0 respectively"

#Selection of type_of_classification
if type_of_classification == 'nearest_improved':
    nearest_improved(int(stump_count))
if type_of_classification == 'nearest':
    nearest(int(stump_count))
if type_of_classification == 'nnet':
    NN(int(stump_count))
if type_of_classification == 'best':
    NN_Best(30)
if type_of_classification == 'adaboost':
    start_adaboost()
    #NN_Best(int(stump_count))
