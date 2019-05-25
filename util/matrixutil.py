
from __future__ import division
from scipy.sparse import coo_matrix
import numpy as np
import sys
import util.readdata as read


def graph_to_matrix(graph):
    '''
    Args:
        graph: user item graph
    Retrun:
        a coo_matrix, sparse matrix m
        a list, total user item point
        a dict, map all the point to row index
    '''

    vertex = list(graph.keys())
    address_dict = {}
    total_len = len(vertex)
    for idx in range(total_len):
        address_dict[vertex[idx]] = idx

    row = []
    col = []
    data = []
    for element_i in graph:
        weight = round(1/len(graph[element_i]),3)
        row_index = address_dict[element_i]
        for element_j in graph[element_i]:
            col_index = address_dict[element_j]
            row.append(row_index)
            col.append(col_index)
            data.append(weight)

    row = np.array(row)
    col = np.array(col)
    data = np.array(data)

    matrix = coo_matrix((data,(row,col)), shape = (total_len,total_len))
    return matrix, vertex, address_dict


def get_matrix_all_point(matrix, vertex, alpha):
    '''
    Args:
        matrix:
        vertex: total user and item point
        alpha: the prob for random walk
    Return:
        a sparse matrix
    '''
    total_len = len(vertex)
    row = []
    col = []
    data = []
    #print(total_len)
    for index in range(total_len):
        row.append(index)
        col.append(index)
        data.append(1)

    row = np.array(row)
    col = np.array(col)
    data = np.array(data)

    eye_t = coo_matrix((data,(row,col)), shape = (total_len,total_len))

    return eye_t.tocsr() - alpha * matrix.tocsr().transpose()



if __name__ == '__main__':
    graph = read.get_graph_from_data('../data/log.txt')
    m, vertex, address_dict = graph_to_matrix(graph)
    #print(address_dict)
    #print(m.todense())
    #print(vertex)

    print(get_matrix_all_point(m, vertex, 0.8).todense())