from __future__ import division
import itertools
import io
import glob
from math import log

def CleanData(f, filename):
    print("...clean data...")
    
    #to clean the data we change every string to be lowercase
    lines = [l.lower() for l in f]
    with open(filename, 'w') as out:
        out.writelines(lines)
    
def BuildClassifier(tuples, class_vals,  attr_vals, class_index, attributes):
    print("...naive bayes...")
    for t in tuples:
        #get count of class index values
        if class_vals.has_key(t[class_index]):
            class_vals.update({t[class_index]:class_vals.get(t[class_index])+1})
        else:
            class_vals.update({t[class_index]:1})
        
        #get attr values given the class value
        i = 0
        for a in t:
            if i != class_index:
                cur_key ="{} {} {}".format(t[class_index], attributes[i], a)
                if attr_vals.has_key(cur_key):
                    attr_vals.update({cur_key:attr_vals.get(cur_key)+1})
                else:
                    attr_vals.update({cur_key: 1})
            i += 1
    #print("Class Values:\n{}\nAttribute Values:\n{}".format(class_vals, attr_vals))
    
    
def Classify(tuples, class_attr, attr_vals, attributes, class_index):
    print("...classify...")
    for a in attributes:
        print("{} ".format(a)),
    print("Classification")
    count = sum(class_attr.values())
    m = 0.2
    print(attr_vals)
    #create ditionary for p values to avoid lack of label
    temp = attr_vals.keys()
    p_list = {}
    check = {}
    for attr in temp:
            if p_list.has_key(attr.split()[1]):
                if attr.split()[2] not in p_list.get(attr.split()[1]):
                    p_list.update({attr.split()[1] : p_list.get(attr.split()[1]) + [attr.split()[2]]})
            else:
                p_list.update({attr.split()[1] : list([attr.split()[2]])})
    #print(p_list)

    #run through tuples and and attribute to create the scores for each of the classes attribute values to determine the prediction
    for t in tuples:
        key_list = class_attr.keys()
        class_val = ""
        b = True
        key_val = 0.0
        for key in key_list:
            nb_value = class_attr.get(key)/count
            #print("nb: {}, class count: {}".format(nb_value, class_attr.get(key)))
            i = 0
            for a in t:
                attr_key_list = attr_vals.keys()
                for k in attr_key_list:
                    #print("{} {} {}".format(key, attributes[i], a))
                    if key in k.split() and attributes[i] in k.split() and a in k.split():
                        attr_count = (attr_vals.get(k)+ m*len(p_list.get(attributes[i])))/(class_attr.get(key) + m)
                        #attr_count = (attr_vals.get(k)/count)
                        nb_value *= attr_count
                        #print(nb_value)
                if b:
                    print("{}\t\t".format(a)),
                i += 1
            #print("{} : {}".format(key, nb_value))
            if key_val < nb_value:
                key_val = float(nb_value)
                class_val = str(key)
            #print("{} {}".format(key_val, nb_value))
            b = False
        print("{}".format(class_val))



if __name__ == "__main__":
    print("...main...")

    #open training file
    filename = raw_input("Please enter the training data's filename: ")
    f = None
    try:
        f = open(filename, 'r')
    except IOError:
        print("Cannot open {}. Check if it exists.".format(filename))
        sys.exit()

    #find if target attribute exists in file
    attribute_line = f.readline()
    attributes = attribute_line.split()
    print("Please choose the classifying attribute (by number):")
    i = 1
    for a in attributes:
        print("{}. {}".format(i, a))
        i += 1
    
    #repeat until user selects an attibute that exists
    b = True
    class_index = 0
    while b:
        class_index = input("Please select a target attribute for classification: ")
        if class_index <= i-1 and class_index > 0:
            b = False
        else:
            print("Please select an attribute within the given number range (by number).")
    class_index -= 1
    
    #get the tuples
    train_tuples = []
    for line in f:
        if len(line.split()) > 0:
            train_tuples.append(line.split())
    f.close()
    
    #Create the classifier
    class_attr_vals = {}
    attr_vals = {}
            
    BuildClassifier(train_tuples, class_attr_vals, attr_vals, class_index, attributes)
    print("Class Values:\n{}\nAttribute Values:\n{}".format(class_attr_vals, attr_vals))
    #open testing file
    filename = raw_input("Please enter the testing data's filename (Make sure that the file has the same # of attributes and the same attribute values as the training set): ")
    f = None
    try:
        f = open(filename, 'r')
    except IOError:
        print("Cannot open {}. Check if it exists.".format(filename))
        sys.exit()
    
    #clean the testing data to match the training data
    CleanData(f, filename)
    
    #get the test tuples
    f.seek(0)
    f.readline()
    test_tuples = []
    for line in f:
        if len(line.split()) > 0:
            test_tuples.append(line.split())
    #print(test_tuples)
    f.close()

    
    #classify the given test data and print to Results.txt
    Classify(test_tuples, class_attr_vals, attr_vals, attributes, class_index)
    
    
    
