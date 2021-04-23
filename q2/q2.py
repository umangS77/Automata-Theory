import sys
import json

def check_2_power(n):
    f = True
    while (n > 1):
        if (n % 2 != 0):
            f = False
            break
        n = n // 2
    return f

def convert_to_binary(nfa,n):
    binary = ""
    while(n>0):
        k = n%2
        binary = binary + str(k)
        n = n // 2
    while(len(binary)!=(len(nfa.index)-1)):
        binary = binary + "0"
    return binary

def convert_list_to_hash(nfa,lst):
    if len(lst)==0:
        return 0
    v = 0
    for i,j in nfa.index.items():
        if(j in lst):
            v = v + 2**(i-1)
    return v

def convert_hash_to_list(nfa,hash):
    if hash==0:
        return []
    req_lst = []
    x = convert_to_binary(nfa,hash)
    l = len(nfa.index) - 1
    for j in range(l):
        if(x[j]=='1'):
            req_lst.append(nfa.index[j+1])
    return req_lst



class NFA():
    def __init__(self,nfa):
        self.index = dict()
        no_of_states = len(nfa["states"])
        self.index[0] = ''
        for i in range(1,no_of_states+1):
            # print(i)
            self.index[i] = nfa["states"][i-1]

        self.states = []
        for i in range(0,2**no_of_states):
            self.states.append(convert_hash_to_list(self,i))

        self.t_func = dict()
        self.start_st = []
        for st in nfa["start_states"]:
            self.start_st.append([''.join(tuple(st))])

        self.final_st = []
        for st in nfa["final_states"]:
            self.final_st.append([''.join(tuple(st))])

        self.trans_mat = []
        self.eliminated_states = set()
        self.alphabets = []
        self.alphabets = nfa["letters"]
  
    def nfaToDfa(self,nfa):
        no_of_states = len(nfa["states"])


        for st in self.states:
            s = convert_list_to_hash(self,st)
            self.t_func[s] = dict()
            for a in self.alphabets:
                self.t_func[s][a] = set()
        
        for t in nfa["transition_function"]:
            self.t_func[convert_list_to_hash(self,[''.join(tuple(t[0]))])][t[1]].add(''.join(tuple(t[2])))
        
        for i in range(2**no_of_states):
            if(check_2_power(i) == False):
                lst = convert_hash_to_list(self,i)
                for l in self.alphabets:
                    x = set()
                    for a in lst:
                        for b in self.t_func[convert_list_to_hash(self,[a])][l]:
                            x.add(b)
                    self.t_func[i][l] = x

        final_states = set()
        dfa = dict()
        dfa["states"] = self.states
        dfa["letters"] = list(self.alphabets)
        
        for a,t in self.t_func.items():
            for v,b in t.items():
                self.trans_mat.append([convert_hash_to_list(self,a),v,list(b)])
        
        for a in nfa["final_states"]:
            for s in self.states:
                if a in s:
                    final_states.add(convert_list_to_hash(self,s))
                

        
        
        dfa["transition_function"] = self.trans_mat
        dfa["start_states"] = [[a] for a in nfa["start_states"]]
        dfa["final_states"] = [convert_hash_to_list(self,a) for a in final_states]
        return dfa

def main():
    with open(sys.argv[1], 'r') as file:
        data = json.load(file)
    NFA_ans = NFA(data)
    dfa = NFA_ans.nfaToDfa(data)

    with open(sys.argv[2], 'w') as file:
        json.dump(dfa,file,indent = 4)

main()