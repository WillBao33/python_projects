'''
Build a k-means clustering model from scratch
'''
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

class KMeansClustering:
    def __init__(self, k = 3):
        self.k = k
        self.centroids = None

    @staticmethod
    def euclidean_distance(data_points, centroids):
        return np.sqrt(np.sum((data_points - centroids)**2, axis=1))
    
    def fit(self, X, max_iteration=200):
        self.centroids = np.random.uniform(np.amin(X, axis=0), np.amax(X, axis=0), size=(self.k, X.shape[1]))

        for _ in range(max_iteration):
            y = []
            
            for data_points in X:
                distance = KMeansClustering.euclidean_distance(data_points, self.centroids)
                cluster_num = np.argmin(distance)
                y.append(cluster_num)

            y = np.array(y)
            cluster_inidicies = []

            for i in range(self.k):
                cluster_inidicies.append(np.argwhere(y == i))

            cluster_centers = []

            for i, indicies in enumerate(cluster_inidicies):
                if len(indicies) == 0:
                    cluster_centers.append(self.centroids[i])
                else:
                    cluster_centers.append(np.mean(X[indicies], axis=0)[0])

            if np.max(self.centroids - np.array(cluster_centers)) < 0.0001:
                break
            else:
                self.centroids = np.array(cluster_centers)

        return y
    
# test
data = make_blobs(n_samples=100, n_features=2, centers=3) # 100 2D points with 3 centers
data_points = data[0] # only keep the data, remove the labels
kmeans = KMeansClustering(k=3)
labels = kmeans.fit(data_points)

plt.scatter(data_points[:,0], data_points[:,1], c=labels)
plt.scatter(kmeans.centroids[:,0], kmeans.centroids[:,1], c=range(len(kmeans.centroids)), marker='*', s=200)
plt.show()
