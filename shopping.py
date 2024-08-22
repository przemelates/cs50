import csv
import sys
import copy
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    evidence = []
    labels = []
    with open (filename) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            evidence1 = list()
            evidence1.append(int(row[0]))
            evidence1.append(float(row[1]))
            evidence1.append(int(row[2]))
            evidence1.append(float(row[3]))
            evidence1.append(int(row[4]))
            evidence1.append(float(row[5]))
            evidence1.append(float(row[6]))
            evidence1.append(float(row[7]))
            evidence1.append(float(row[8]))
            evidence1.append(float(row[9]))
            months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"June":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
            evidence1.append(months[row[10]])
            evidence1.append(int(row[11]))
            evidence1.append(int(row[12]))
            evidence1.append(int(row[13]))
            evidence1.append(int(row[14]))
            evidence1.append(1) if row[15] == "Returning_Visitor" else evidence1.append(0)
            evidence1.append(0) if row[16] == "FALSE" else evidence1.append(1) 
            evidence.append(evidence1)


            if row[-1] == "FALSE":
                labels.append(0)
            else:
                labels.append(1)
                
    return (evidence,labels)

    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    raise NotImplementedError


def train_model(evidence, labels):
    model = KNeighborsClassifier()
    model.fit(evidence,labels)
    return model

    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    raise NotImplementedError


def evaluate(labels, predictions):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for n in range(len(labels)):
        if labels[n] == 1 and predictions[n] == 1:
            tp+=1
        elif labels[n] == 0 and predictions[n] == 1:
            fp+=1
        elif labels[n] == 0 and predictions[n] == 0:
            tn+=1
        else:
            fn+=1
    sensitivity = tp/(tp+fn)
    specificity = tn/(tn+fp)
    return(sensitivity,specificity)
    



    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
