import sys
import itertools
import json

def minimiseDFA(states, alphabets, t_func, start_st, acc_st):
    l = len(alphabets)
    non_acc_st = list(set(states)-set(acc_st))
    alp_hash = dict((alphabets[i],i) for i in range(l))
    st_hash = dict((states[i],i) for i in range(len(states)))
    tp_mat = [list(itertools.repeat("",l)) for i in range(len(states))]
    l = len(states)
    t_mat = [[0 for i in range(len(states))] for j in range(len(states))]


    tp_st = []
    for t in t_func:
        tp_mat[st_hash[t[0]]][alp_hash[t[1]]] = t[2]

    
    acc_st_2 = []
    for i in range(len(t_mat)):
        for j in range(len(t_mat[i])):
            e = list(st_hash.keys())[list(st_hash.values()).index(j)]
            s = list(st_hash.keys())[list(st_hash.values()).index(i)]
            if s in non_acc_st:
                if e in acc_st:
                    t_mat[i][j] = t_mat[j][i] = 1
            elif s in acc_st:
                if e in non_acc_st:
                    t_mat[i][j] = t_mat[j][i] = 1

    
    while 1>0:
        flag = False
        for i in range(len(t_mat)):
            for j in range(len(t_mat[i])):
                if i==j:
                    continue
                else:
                    if not t_mat[i][j]:
                        for alp in alphabets:
                            if tp_mat[i][alp_hash[alp]] != "":
                                if tp_mat[j][alp_hash[alp]] == "":
                                    continue
                                else:
                                    if t_mat[st_hash[tp_mat[i][alp_hash[alp]]]][st_hash[tp_mat[j][alp_hash[alp]]]]:
                                        t_mat[i][j] = 1
                                        flag = True
                                        break

        if flag == True:
            continue
        else:
            break

    
    for i in range(len(t_mat)):
        for j in range(len(t_mat[i])):
            if i == j:
                continue
            else:
                if not t_mat[i][j]:
                    v_A = list(st_hash.keys())[list(st_hash.values()).index(i)]
                    v_B = list(st_hash.keys())[list(st_hash.values()).index(j)]
                    if not len(tp_st):
                        temp = [v_A,v_B]
                        tp_st.append(temp)
                    else:
                        flag = False
                        for v in range(len(tp_st)):
                            if v_A in tp_st[v]:
                                tp_st[v].extend([v_A,v_B])
                                tp_st[v] = list(dict.fromkeys(tp_st[v]))
                                flag = True
                                break
                            elif v_B in tp_st[v]:
                                tp_st[v].extend([v_A,v_B])
                                tp_st[v] = list(dict.fromkeys(tp_st[v]))
                                flag = True
                                break
                        if flag == False:
                            tp_st.append([v_A,v_B])

    
    start_st_2 = []
    t_func_2 = []

    for s in states:
        flag = False
        for not_same_st in tp_st:
            if s in not_same_st:
                flag = True
                break
        if flag == False:
            tp_st.append([s])

    


    for i in tp_st:
        flag = False
        for s in i:
            for j in acc_st:
                if s in j:
                    flag = True
                    break
                
            if flag == True:
                break
        if flag == True:
            acc_st_2.append(i)
    
    
    for s in tp_st:
        flag = 0
        for not_same_st in start_st:
            if not_same_st in s:
                flag = 1
                start_st_2.append(s)
                break
            else:
                flag = 0
    
    for s in tp_st:
        for alp in alphabets:
            
            v_A = tp_mat[st_hash[s[0]]][alp_hash[alp]]
            flag = 0
            for not_same_st in tp_st:
                if v_A in not_same_st:
                    flag = 1
                else:
                    flag = 0
                if v_A in not_same_st:
                    v_A = not_same_st    
                if flag == 1:
                    break
            t_func_2.append([s, alp, v_A])
    

    return {
        "states": tp_st,
        "letters": alphabets,
        "transition_matrix": t_func_2,
        "start_states": start_st_2,
        "final_states": acc_st_2
    }

def main():
   
    with open(sys.argv[1],'r') as file:
        data = json.load(file)
    states = data['states']
    letters = data['letters']
    t_mat = data['transition_function']
    start_st = data['start_states']
    fin_st =  data['final_states']

    output = minimiseDFA(states, letters, t_mat, start_st, fin_st)
    
    with open(sys.argv[2],"w") as file:
        json.dump(output,file,indent=4)
main()

    