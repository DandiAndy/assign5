import itertools
import io
import glob

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
    
    
def Classify():
    print("...classify...")

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
    print(test_tuples)
    f.close()

    
    #classify the given test data and print to Results.txt
    Classify()
    
    
    
