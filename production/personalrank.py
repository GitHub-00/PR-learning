
from __future__ import division
from scipy.sparse.linalg import gmres
import operator
import sys
import numpy as np

sys.path.append('../util')
import util.readdata as read
import util.matrixutil as mat_util


def personal_rank(graph, root, alpha, iter_num, recom_num=10 ):
    '''
    Args:
        graph: user item graph
        root: for user recom
        alpha: the prob to go to random walk
        iter_num: iteration number
        recom_num: recom item number
    Return:
        a dict key:itemid value pr
    '''

    rank = {}
    rank = {point:0 for point in graph}
    rank[root] = 1
    recom_result = {}

    for iter_index in range(iter_num):
        tmp_rank = {}
        tmp_rank = {point:0 for point in graph}
        for out_point, out_dict in graph.items():
            for inner_point, value in graph[out_point].items():
                #print(alpha*rank[out_point]/len(out_dict))
                tmp_rank[inner_point] += round(alpha*rank[out_point]/len(out_dict),4)
                if inner_point == root:
                    tmp_rank[inner_point] += round(1-alpha,4)
        if tmp_rank==rank:
            #print('out'+str(iter_index))
            break

        rank = tmp_rank

    right_num = 0
    for zuhe in sorted(rank.items(),key=operator.itemgetter(1), reverse=True):
        point, pr_score = zuhe[0],zuhe[1]
        if len(point.split('_'))<2:
            continue
        if point in graph[root]:
            continue
        recom_result[point] = pr_score
        right_num += 1
        if right_num>recom_num:
            break
    return  recom_result

def personal_rank_matrix(graph, root, alpha, recom_num=10):
    '''
    Args:
        graph: user and item graph
        root: fix user to recom
        alpha: the prob to random walk
        recom_num: recom item number
    Return:
        a dic: key: itemid, value: pr score
    '''
    m, vertex, address_dict = mat_util.graph_to_matrix(graph)
    if root not in address_dict:
        return {}

    print(vertex)
    score_dict = {}
    recom_dict = {}
    mat_all = mat_util.get_matrix_all_point(m, vertex, graph)
    index = address_dict[root]
    initial_list = [[0] for row in range(len(vertex))]
    initial_list[index] = 1
    r_zero = np.array(initial_list)
    res = gmres(mat_all, r_zero, tol=1e-8)[0]

    for index in range(len(res)):
        point = vertex[index]
        if len(point.strip().split('_'))<2:
            continue
        if point in graph[root]:
            continue

        score_dict[point] = round(res[index],3)

    for zuhe in sorted(score_dict.items(),key=operator.itemgetter(1), reversed=True)[:recom_num]:
        point, score = zuhe[0], zuhe[1]
        recom_dict[point] = score

    return recom_dict


def get_one_user_recom():
    '''
    user = 'A'
    alpha = 0.6
    graph = read.get_graph_from_data('../data/log.txt')
    #graph = read.get_graph_from_data('../data/ratings.csv')
    iter_num = 10
    print(personal_rank(graph,user,alpha,iter_num))
    '''
    user = '32'
    alpha = 0.8
    graph = read.get_graph_from_data('../data/ratings.csv')
    iter_num = 100
    recom_result = personal_rank(graph, user, alpha, iter_num)
    item_info = read.get_item_info('../data/movies.csv')
    for itemid in graph[user]:
        item = itemid.split('_')[1]
        print(item_info[item])
    print('---------------------------------result-----------------------')
    for itemid in recom_result:
        item = itemid.split('_')[1]
        print(item_info[item])
        print(recom_result[itemid])

def get_one_user_by_matrix():
    '''
    test one user recom
    '''
    user = '32'
    alpha = 0.8
    iter_num = 100
    graph = read.get_graph_from_data('../data/ratings.csv')
    recom_result = personal_rank_matrix(graph,user,alpha,iter_num)

if __name__=='__main__':
    #get_one_user_recom()
    recom_result_ori = get_one_user_recom()
    recom_result_mat = get_one_user_by_matrix()
    num = 0
    for ele in recom_result_ori:
        if ele in recom_result_mat:
            num += 1
    print(num)
