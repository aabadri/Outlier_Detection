# TODO we do not check if center and a and b are in a line
import random

import numpy as np
import pandas as pd

train_url = "./data1.csv"
train = pd.read_csv(train_url, delimiter=',', header=None)
train = train.sample(frac=1)
ytrain = train[274]
train = train.drop(274, axis=1)
print("data is loaded")

train_temp = train[:100]


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
    print(hashed_train)
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
    return angle_degree / (dista ** 2) * (distb ** 2)


varABOF = []

for t, center in train.iterrows():
    if (t % 10 == 0):
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
train["ABOF"] = varABOF
train["label"] = ytrain
print("finish")
train.to_csv("mammadAgha.csv", index=False)
print(varABOF)
print(train.head())

