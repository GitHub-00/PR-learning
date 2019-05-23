
from __future__ import division
import operator
import sys

sys.path.append('../util')
import util.readdata as read

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

if __name__=='__main__':
    get_one_user_recom()