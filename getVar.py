# TODO we do not check if center and a and b are in a line
import random

import numpy as np
import pandas as pd

train_url = "./global.csv"
train = pd.read_csv(train_url, delimiter=',', header=None)
train = train.sample(frac=1)
ytrain = train.iloc[:, -1]
train = train[:-1]
print("data is loaded")

train_temp = train[:40]
MOD_RATE = 15


def hash_train(train, hash_rate):
    hashed_train = []
    print(train.shape[0], train.shape[1])
    for i in range(0, hash_rate):
        random_vector = []
        for j in range(0, train.shape[1]):
            random_vector.append(random.randint(-1, 1))
        hashed_train.append([])
        for index, record in train.iterrows():
            dotted = np.dot(record, random_vector)
            if dotted >= 0:
                hashed_train[i].append(1)
            else:
                hashed_train[i].append(-1)
    print("width1 ", len(hashed_train))
    print("height1 ", len(hashed_train[0]))
    hashed_train = list(map(list, zip(*hashed_train)))
    print("width ", len(hashed_train))
    print("height", len(hashed_train[0]))
    return pd.DataFrame(hashed_train)


train = hash_train(train_temp, 20)
train.to_csv("hash_train.csv", index=False)


def getABOF(vertex, a, b):
    va = a - vertex
    vb = b - vertex
    cosine_angle = np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb))
    angle = np.arccos(cosine_angle)
    angle_degree = np.degrees(angle)
    dista = np.linalg.norm(va)
    distb = np.linalg.norm(vb)
    return angle_degree


def get_ROC(train):
    tp = fn = fp = tn = tpr = fpr = 0
    result = train["ABOF"]
    label = train["label"]
    roc = []
    for tr in range(int(np.min(result)), int(np.max(result))):
        for index, i in train.iterrows():
            if result[index] < tr:  # outlier
                if label[index] == 1:
                    tp += 1
                else:
                    fp += 1
            else:  # normal
                if label[index] == 1:
                    fn += 1
                else:
                    tn += 1
        # print(tp, fn, fp, tn)
        if tp == 0 and fn == 0:
            tpr = 0
        else:
            tpr = tp / (tp + fn)

        if fp == 0 and tn == 0:
            fpr = 0
        else:
            fpr = fp / (fp + tn)
        roc.append((tpr, fpr))
    return roc


varABOF = []
varAvg = []
varModABOF = []
varModAVG = []

for t, center in train.iterrows():
    if t % 10 == 0:
        print(t)
    centerABOF = []
    center = list(center)
    for index, i in train.iterrows():
        if center != list(i):
            for j in range(index, train.shape[0]):
                rowJ = list(train.iloc[j])
                if center != rowJ and list(i) != rowJ:
                    centerABOF.append(getABOF(center, np.array(list(i)), np.array(rowJ)))
    varABOF.append(np.var(centerABOF))
    varAvg.append(np.average(centerABOF))

for record in varABOF:
    varModABOF.append(np.remainder(record, MOD_RATE))

for record in varAvg:
    varModAVG.append(np.remainder(record, MOD_RATE))

train["ABOF"] = varABOF
train["avg"] = varAvg
train["mod_avg"] = varModAVG
train["mod_ABOF"] = varModABOF
train["label"] = ytrain
roc = get_ROC(train)
print(roc)
print("finish")
train.to_csv("mammadAgha.csv", index=False)
