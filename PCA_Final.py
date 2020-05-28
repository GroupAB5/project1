#Important importing
import pandas as pd
import numpy as np
import random as rd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt

#Test Dataset
genes = ['gene' + str(i) for i in range(1,101)]
wt = ['wt' + str(i) for i in range(1,6)]
data = pd.DataFrame(columns=[*wt], index=genes)
for gene in data.index:
    data.loc[gene, 'wt1':'wt5'] = np.random.poisson(lam=rd.randrange(10,1000), size =5)

#Prints Dataset and Size of Dataset
print(data.head())
print(data.shape)

#Center and Scale the Data
scaled_data = preprocessing.scale(data.T)

"""
Dataset table should have x,y and z in y axis and stations in x axis
"""

#Create PCA object and do PCA
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)


#Plot
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

#Plot for Influence of Variables (basically percentages of what variables influence the PCA the most)
plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal Component')
plt.title('Scree Plot')
plt.show()

#Actual PCA Plot
pca_df = pd.DataFrame(pca_data, index=[*wt], columns=labels)

plt.scatter(pca_df.PC1, pca_df.PC2)
plt.title('PCA Graph')
plt.xlabel('PC1 - {0}%'.format(per_var[0]))
plt.ylabel('PC2 - {0}%'.format(per_var[1]))

for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))

plt.show()
