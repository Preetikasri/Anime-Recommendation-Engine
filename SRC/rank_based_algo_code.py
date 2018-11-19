import pandas as pd
import operator
import numpy as np

rating = pd.read_csv('rating.csv/rating.csv')
mask =(rating['user_id'].value_counts() >= 50) & (rating['user_id'].value_counts() <= 100)
users = mask[mask == True].index
rating_2 = rating[rating['user_id'].isin(users)]




def indicator_f(x):
    if(x <0):
        r = 1
    else:
        r = 0
    return r

def Kendall_CC(u_id, v_id, df):
    S = 0
    
    user_anm_rating = pd.merge(df[df['user_id'] == u_id], df[df['user_id'] == v_id], on='anime_id', how='inner', \
                               suffixes={'_U', '_V'})
    if(len(user_anm_rating)>10):
        val = 0
        for a in range(len(user_anm_rating)-1):
            e = (user_anm_rating.loc[a,'rating_U'] - user_anm_rating.loc[a+1,'rating_U'])*(user_anm_rating.loc[a,'rating_V'] - user_anm_rating.loc[a+1,'rating_V'])
            val = val + indicator_f(e)
            #print(val)
        S = 1-4*(val/len(user_anm_rating)*(len(user_anm_rating)-1))
    return S

def preference_func(A, B, user_id, rating):
    neighbs = Neighb(user_id, rating) ## return dictionary
    num = 0.0
    denom = 0.0
    for key, val in neighbs.iteritems():
        prod = rating.loc[((rating['user_id'] == key)&(rating['anime_id'] == A)), 'rating'] - rating.loc[((rating['user_id'] == key)&(rating['anime_id'] == B)), 'rating']
        num = num + prod*val
        denom = denom+val
    return num/denom


def Neighb(user_id, rating, cutoff = 10):
    all_users = list((rating['user_id']).unique())#.remove(user_id)
    all_users.remove(user_id)
    neighb_score = {}
    for u in all_users:
        #print(u)
        neighb_score[u] = Kendall_CC(user_id, u, rating)
    top_10 = sorted(x.items(), key=operator.itemgetter(1), reverse=True)[cutoff]
    return top_10

all_items = rating_2['anime_id'].unique()

def calculate_order_greedy(Item_list, rating, user_id):
    pie = {}
    rank = {}
    for i in Item_list:
        pie[i] = preference_func(i, i+1, user_id, rating) - preference_func(i+1, i, user_id, rating)
    while (len(Item_list) > 0):
        t = max(pie.items(), key = operator.itemgetter(1))[0]
        rank[t] = len(Item_list)
        Item_list.remove(t)
        for k in Item_list:
            pie[k] = pie[k] + preference_func(t,k, user_id, rating) - preference_func(k,t, user_id, rating)
    return rank

all_ranks = calculate_order_greedy(all_items, rating_2, 9112)
