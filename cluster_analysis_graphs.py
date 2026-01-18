# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 23:01:31 2026

@author: bboyg
"""

import matplotlib.pyplot as plt

def Silhouette_graph(silhouette_avg, range_n_clusters):
    """
    Plots the Silhouette scores for different values of K, showing highest value
    as the optimal cluster numer

    Returns
    -------
    Silhouette Plot.

    """
    print("Optimal number of clusters (Silhouette):", silhouette_avg.index(max(silhouette_avg))+2)
    plt.plot(range_n_clusters, silhouette_avg,'bx-')
    plt.xlabel('Values of K') 
    plt.ylabel('Silhouette Score') 
    plt.title('Silhouette Analysis for Optimal k')
    plt.show()
    
def Calinski_Harabasz_graph(calinski_harabasz_avg, range_n_clusters):
    """
    For completeness, plots Calinski_Harabasz scores for different values of K,
    
    Returns
    -------
    Calinski Harbasz Plot.

    """
    plt.plot(range_n_clusters, calinski_harabasz_avg,'bx-')
    plt.xlabel('Values of K') 
    plt.ylabel('Calinski Harabasz Score') 
    plt.title('Calinski Harabasz Analysis for Optimal k')
    plt.show()
    
def Davies_Bouldin_graph(davies_bouldin_avg, range_n_clusters):
    """
    Plots the Davies Bouldin scores for different values of K, showing lowest value
    as the optimal cluster numer

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

def Elbow_point_graph(elbow_point, wcss, range_n_clusters):
    """
    Plots the WCSS against cluster, and for the point with the greatest rate
    of change, is determined to be the optimal number of clusters

    Returns
    -------
    Eblow Point Plot.

    """
    print("Optimal number of clusters (elbow point):", elbow_point)
    plt.plot(range_n_clusters, wcss, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('WCSS')
    plt.title('Elbow Method for Optimal K')
    plt.grid()
    
    # Mark the elbow point on the graph
    plt.scatter(elbow_point, wcss[elbow_point-2], 
                c='red', marker='x', s=100, label='Elbow Point')
    plt.legend()
    plt.show()