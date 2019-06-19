import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

def getPredictedStage(extractedFeatures):

    extractedFeaturesValues = list(extractedFeatures.values())

    dataset = pd.read_csv('F:\\BEProject\\ImgTuts\\mysite\\trialapp\\newFeatures.csv',sep=',',header= None)

    x = dataset.values[:,0:8]
    y = dataset.values[:,8]

    X_train, X_test, y_train, y_test = train_test_split( x, y, test_size = 0.3, random_state = 100)

    clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,
                                    min_samples_leaf=5)

    abc = clf_entropy.fit(X_train, y_train)

    y_pred_val = clf_entropy.predict(X_test)

    datapoint=[[44,250,500,46,0,0,36,0.5]]

    extractedFeaturesValues = [extractedFeaturesValues]

    newpred = clf_entropy.predict(extractedFeaturesValues)

    stageDict = {0:"Stage-0", 1: "Stage-1", 2: "Stage-2", 3: "Stage-3", 4: "Satge-4"}

    return stageDict[int(newpred[0])]