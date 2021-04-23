import sys
import itertools
import json

message = ''

def execution_of_star(st,t_mat,tr):
    global message
    l = len(t_mat)
    idx = t_mat.index(tr)
    alphabets = tr[1]
    for i in range(l):
        if t_mat[i][2] == st:
            if t_mat[i][0] != st:
                t_mat[i][1]+=alphabets+"*"
    ret = [idx]
    message = message + "\n star executed"
    return ret

def execute_concatenation(pre_trans,suc_trans, t_mat):
    for i in range(0,len(pre_trans)):
        for j in range(len(suc_trans)):
            alphabet = "(" + pre_trans[i][1] + suc_trans[j][1] + ")"
            t_mat.append([pre_trans[i][0],alphabet,suc_trans[j][2]])
    
    for i in range(0,len(pre_trans)):
        idx = t_mat.index(pre_trans[i])
        if idx>=0:
            t_mat.pop(idx)

    for i in range(0,len(suc_trans)):
        idx = t_mat.index(suc_trans[i])
        if idx>=0:
            t_mat.pop(idx)

    return t_mat

def dfaToRegex(states, letters, t_mat, start_st, fin_st):
    global message
    ans_start_st = ["Q"]
    n = len(states)
    ans_fin_st = "Q"+str(n)
    message = ''

    for i in range(0,len(start_st)):
        t_mat.append([ans_start_st[0],"$",start_st[i]])

    for i in range(0,len(fin_st)):
        t_mat.append([fin_st[i], "$", ans_fin_st])

    for s in states:
        pre_trans = [tr for tr in t_mat if tr[2]==s]
        suc_trans = [tr for tr in t_mat if tr[0]==s]
        pre_idx = suc_idx = star_idx = []
        for i in range(0,len(pre_trans)):
            for j in range(0,len(suc_trans)):
                if pre_trans[i][0] == suc_trans[j][2]:
                    if suc_trans[j][2] == s:
                        star_idx.extend(execution_of_star(s,t_mat,pre_trans[i]))
                        pre_idx.append(i)
                        suc_idx.append(j)
        idxs = []
        l = len(t_mat)
        pre_trans = [pre_trans[i] for i in range(len(pre_trans)) if i not in pre_idx]
        suc_trans = [suc_trans[i] for i in range(len(suc_trans)) if i not in suc_idx]
        message = message + "\nStarting concatenation"
        t_mat = [t_mat[i] for i in range(l) if i not in star_idx]
        t_mat = execute_concatenation(pre_trans,suc_trans,t_mat)


        for i in range(len(t_mat)):
            for j in range(i):
                if i not in idxs:
                    if j not in idxs:
                        if t_mat[i][0] == t_mat[j][0]:
                            if t_mat[i][2] == t_mat[j][2]:
                                c1 = t_mat[i][1]
                                c2 = t_mat[j][1]
                                v = "(" + c1+'+'+c2 + ")"
                                t_mat[i][1] = v
                                idxs.append(j)
                                
        message = message + "\n doing union"
        t_mat = [t_mat[i] for i in range(len(t_mat)) if i not in idxs]

    regex = t_mat[0][1]
    # print(message)
    return regex
    

def main():
   
    with open(sys.argv[1],'r') as file:
        data = json.load(file)
    states = data['states']
    letters = data['letters']
    t_mat = data['transition_function']
    start_st = data['start_states']
    fin_st =  data['final_states']
    
    regex = dfaToRegex(states, letters, t_mat, start_st, fin_st)

    output = {
        "regex": str(regex)
    }

    # print(regex)
    
    with open(sys.argv[2],"w") as file:
        json.dump(output,file,indent=4)
main()
    