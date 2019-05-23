
import os

def get_graph_from_data(input_file):
    '''
    Args:
        input_file: user item rating file
    Retrun:
        a dict: {userA:{itemb:1, itemc:1}, itemB:{userA:1}}
    '''

    if not os.path.exists(input_file):
        return {}

    graph = {}
    linenum=0
    score_threshold = 3.0
    f = open(input_file)
    for line in f:
        if linenum == 0:
            linenum+=1
            continue
        item = line.strip().split(',')
        if len(item)<3:
            continue
        userid, itemid, rating = item[0], 'item_'+item[1], item[2]
        if float(rating)< score_threshold:
            continue

        if userid not in graph:
            graph[userid] = {}
        graph[userid][itemid] = 1

        if itemid not in graph:
            graph[itemid] = {}
        graph[itemid][userid] = 1
    f.close()
    return graph

def get_item_info(input_file):
    '''
    get item info:[title, genre]
    args:
        input_file: item info file
    return:
        a dict key itemid, value[title, genre]
    '''
    if not os.path.exists(input_file):
        return {}
    item_info = {}
    linenum = 0

    f = open(input_file, encoding='utf-8')
    for line in f:
        if linenum==0:
            linenum+=1
            continue
        item = line.strip().split(',')
        if len(item)<3:
            continue
        if len(item)==3:
            itemid, title, genre = item[0], item[1], item[2]
        if len(item)>3:
            itemid = item[0]
            genre = item[-1]
            title = ','.join(item[1:-1])

        item_info[itemid] = [title,genre]

    f.closed
    return item_info

if __name__=='__main__':
    #print(get_graph_from_data('../data/log.txt'))
    graph = get_graph_from_data('../data/ratings.csv')
    print(graph['30'])