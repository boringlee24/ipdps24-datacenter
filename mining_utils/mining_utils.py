import pandas as pd
import os
from joblib import Parallel, delayed

"""
Rule pruning based on the 4 conditions mentioned in paper
args
    df: the association rule dataframe
    keyword: rule pruning keyword
    cl: C_lift parameter
    cs: C_support parameter
"""
def prune_df(df, keyword, cl, cs): # cl is c_lift, cs is c_support
    df_cp = df.copy()
    drop_list = set()
    for i, row_i in df.iterrows():
        if i in drop_list:
            continue
        if i == len(df):
            return df_cp
        if keyword in row_i['consequents']:
            # find rows with same consequent, with key in consequent
            for j in range(i+1, len(df)):
                if j in drop_list:
                    continue
                row_j = df.iloc[j]
                prune_ind = cond_1(i, j, row_i, row_j, cl, cs)
                if prune_ind is None:
                    prune_ind = cond_3(i, j, row_i, row_j, cl)
                if prune_ind is not None:
                    # prune the row in the dataframe copy
                    if prune_ind not in drop_list:
                        df_cp = df_cp.drop([prune_ind])                       
                        drop_list.add(prune_ind)
        elif keyword in row_i['antecedents']:
            for j in range(i+1, len(df)):
                if j in drop_list:
                    continue
                row_j = df.iloc[j]
                prune_ind = cond_2(i, j, row_i, row_j, cl, cs)
                if prune_ind is None:
                    prune_ind = cond_4(i, j, row_i, row_j, cl)
                if prune_ind is not None:
                    # prune the row in the dataframe copy
                    if prune_ind not in drop_list:
                        df_cp = df_cp.drop([prune_ind])                       
                        drop_list.add(prune_ind)
    return df_cp                   

"""
generate keyword-centric rules from the association rules dataframe
"""
def gen_rule(df, keyword):
    ant_rule, cons_rule = filter_df(df, keyword)
    ant_rule = ant_rule.sort_values(by=['confidence'], ascending=False)
    cons_rule = cons_rule.sort_values(by=['confidence'], ascending=False)
    ant_rule = ant_rule.reset_index(drop=True)
    cons_rule = cons_rule.reset_index(drop=True)
    return ant_rule, cons_rule

"""
prune the antecedent and consequent rules
"""
def prune_rule(ant_df, cons_df, keyword, cl, cs):
    usable_cores = os.sched_getaffinity(0)
    pruned = Parallel(n_jobs=len(usable_cores))(delayed(prune_df)(rule, keyword, cl, cs) for rule in [cons_df, ant_df])
    cons_prune, ant_prune = pruned
    return cons_prune, ant_prune

"""
rule pruning condition 1
"""
def cond_1(i, j, row_i, row_j, cl, cs):
    # return index of pruning
    ant_i = row_i['antecedents']
    con_i = row_i['consequents']
    ant_j = row_j['antecedents']
    con_j = row_j['consequents']
    if con_j == con_i:
        long_ind, short_ind, long_row, short_row = 0, 0, 0, 0
        if ant_i.issubset(ant_j):
            long_row = row_j
            short_row = row_i
            long_ind = j
            short_ind = i
        elif ant_j.issubset(ant_i):
            long_row = row_i
            short_row = row_j
            long_ind = i
            short_ind = j
        if type(long_row) == type(row_i):
            # check support and lift
            if cl * short_row['lift'] >= long_row['lift']:
                return long_ind
            elif cs * long_row['support'] >= short_row['support']:
                return short_ind
            else:
                return None
        else:
            return None
    else:
        return None

"""
rule pruning condition 2
"""
def cond_2(i, j, row_i, row_j, cl, cs):
    # return index of pruning
    ant_i = row_i['antecedents']
    con_i = row_i['consequents']
    ant_j = row_j['antecedents']
    con_j = row_j['consequents']
    if ant_j == ant_i:
        long_ind, short_ind, long_row, short_row = 0, 0, 0, 0
        if con_i.issubset(con_j):
            long_row = row_j
            short_row = row_i
            long_ind = j
            short_ind = i
        elif con_j.issubset(con_i):
            long_row = row_i
            short_row = row_j
            long_ind = i
            short_ind = j
        if type(long_row) == type(row_i):
            # check support and lift
            if cl * long_row['lift'] >= short_row['lift'] and cs * long_row['support'] >= short_row['support']:
                return short_ind
            elif cl * long_row['lift'] < short_row['lift']:
                return long_ind
            else:
                return None
        else:
            return None
    else:
        return None

"""
rule pruning condition 3
"""
def cond_3(i, j, row_i, row_j, cl):
    # return index of pruning
    ant_i = row_i['antecedents']
    con_i = row_i['consequents']
    ant_j = row_j['antecedents']
    con_j = row_j['consequents']
    if ant_j == ant_i:
        long_ind, short_ind, long_row, short_row = 0, 0, 0, 0
        if con_i.issubset(con_j):
            long_row = row_j
            short_row = row_i
            long_ind = j
            short_ind = i
        elif con_j.issubset(con_i):
            long_row = row_i
            short_row = row_j
            long_ind = i
            short_ind = j
        if type(long_row) == type(row_i):
            # check support and lift
            if cl * short_row['lift'] >= long_row['lift']:
                return long_ind
            else:
                return None
        else:
            return None
    else:
        return None

"""
rule pruning condition 4
"""
def cond_4(i, j, row_i, row_j, cl):
    # return index of pruning
    ant_i = row_i['antecedents']
    con_i = row_i['consequents']
    ant_j = row_j['antecedents']
    con_j = row_j['consequents']
    if con_j == con_i:
        long_ind, short_ind, long_row, short_row = 0, 0, 0, 0
        if ant_i.issubset(ant_j):
            long_row = row_j
            short_row = row_i
            long_ind = j
            short_ind = i
        elif ant_j.issubset(ant_i):
            long_row = row_i
            short_row = row_j
            long_ind = i
            short_ind = j
        if type(long_row) == type(row_i):
            # check support and lift
            if cl * short_row['lift'] >= long_row['lift']:
                return long_ind
            else:
                return None
        else:
            return None
    else:
        return None

"""
Filter the dataframe for keyword appearing in antecedents or consequents
"""
def filter_df(rule_df, keyword):
    df_ant = pd.DataFrame(columns=rule_df.columns)
    df_con = pd.DataFrame(columns=rule_df.columns)
    ind_ant = 0
    ind_con = 0
    for df_iter in rule_df.iterrows():
        df_row = df_iter[1]
        if keyword in df_row['antecedents']: 
            df_ant.loc[ind_ant] = df_row
            ind_ant +=1
        if keyword in df_row['consequents']:
            df_con.loc[ind_con] = df_row
            ind_con += 1
    return df_ant, df_con
