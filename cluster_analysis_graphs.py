# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 23:01:31 2026

@author: bboyg
"""

import numpy as np
import sklearn.metrics
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

def Davies_Bouldin_graph(davies_bouldin_avg, range_n_clusters):
    """
    Plots the Davies Bouldin scores for different values of K, showing the lowest value
    as the optimal cluster number

    Returns
    -------
    Davies Bouldin Plot.

    """
    print("Optimal number of clusters (Davies Bouldin):", davies_bouldin_avg.index(min(davies_bouldin_avg))+2)
    plt.plot(range_n_clusters,davies_bouldin_avg,'bx-')
    plt.xlabel('Values of K', fontsize = 12) 
    plt.ylabel('Davies Bouldin Score', fontsize = 12) 
    plt.title('Davies Bouldin Analysis for Optimal k')
    plt.show()
    
def perform_cluster_analysis(range_n_clusters, telecoords):
    """
    For the map, it assigns k-means between 2-40 clusters. How well do these fit
    are judged on a score using the Davies Bouldin index to determine the 
    number of clusters. 

    Returns
    -------
    cluster_centers, cluster_labels

    """
    # Assuming you have relevant data for clustering (e.g., significant coordinates)
    # Define a range of cluster numbers to evaluate
    # Initialise lists to store evaluation metrics
    davies_bouldin_avg = []
    for num_clusters in range_n_clusters:
        # Initialise K-means clustering with a specific number of clusters
        kmeans = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10)
        kmeans.fit(telecoords)
        cluster_labels = kmeans.labels_

        # Calculate Davies-Bouldin score
        davies_bouldin_avg.append(sklearn.metrics.davies_bouldin_score(telecoords, cluster_labels))
    
    wcss = []
    for i in (range_n_clusters):
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
        kmeans.fit(telecoords)
        wcss.append(kmeans.inertia_)

    # Determine the optimal number of clusters based on evaluation metrics
    num_clusters = davies_bouldin_avg.index(min(davies_bouldin_avg)) + 2

    # Initialize K-means clustering with the chosen number of clusters
    kmeans = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10)
    kmeans.fit(telecoords)

    # Get cluster labels and cluster centres
    cluster_labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    
    return davies_bouldin_avg, wcss, cluster_labels, cluster_centers
