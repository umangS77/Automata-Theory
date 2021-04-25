import sys
import json 

letters = None


class NFA: 
    def __init__(self, states, alphabets, trans_func, start, final):
        self.states = states
        self.start_st = start
        self.final_st = final
        fin_stat = False
        self.letters = alphabets
        self.t_func = trans_func
        

data = ''

def oneState(c):
    return NFA(2, letters, [(0, c, 1)], [0], [1])

def precedenceOf(c):
    if c == '*':
        return 4
    elif c == '.':
        return 3
    elif c == '+':
        return 2
    else:
        return 1

def join_encounter(char_A, char_B):
    f = False
    if char_A.isalnum():
        f = True
    elif char_A == ')':
        f = True
    elif char_A == '*':
        f = True
    elif char_A == '$':
        f = True

    if f == True:
        if char_B.isalnum():
            f = True
        elif char_B == '(':
            f = True
        elif char_B == '$':
            f = True
        else:
            f = False
    return f

def insert_concat_opt(reg_expression):
        l = len(reg_expression)
        temp_regex = ''
        for i in range(0,l):
            if i <= l - 2:
                if join_encounter(reg_expression[i], reg_expression[i+1]) == False:
                    temp_regex += (reg_expression[i])                    
                else:
                    temp_regex += (reg_expression[i] + '.')
            else:
                temp_regex += (reg_expression[i])
        return temp_regex

def inToPost(reg_expression):
    new_RE = []
    st = []
    v = ''
    l = len(reg_expression)
    for i in range(l):
        if reg_expression[i].isalnum():
            new_RE.append(reg_expression[i])
        elif reg_expression[i] == ')':
            while reg_expression[i] == ')' and st[-1] != '(':
                new_RE.append(st.pop())
            st.pop()
        elif reg_expression[i] == '$':
            new_RE.append(reg_expression[i])
        elif reg_expression[i] == '(':
            st.append(reg_expression[i])
        
        else:
            while (len(st) >= 1 and st[-1] != '(' and precedenceOf(reg_expression[i]) <= precedenceOf(st[-1])):
                new_RE.append(st.pop())
            st.append(reg_expression[i])

    while len(st) >= 1:
        new_RE.append(st.pop())

    v = ''.join(new_RE)
    return v

def add_letter_Q(state: int):
        s = 'Q'
        s = s + str(state)
        return s

def regexToNFA(reg_expression):

    global letters
    v = set()
    message = ''
    for c in reg_expression:
        if c == '$':
            v.add(c)
        elif c.isalnum():
            v.add(c)
        

    letters = list(v)
    reg_expression = inToPost(insert_concat_opt(reg_expression))
    stack = []
    for c in reg_expression:
        if c.isalnum():
            stack.append(oneState(c))
        elif c== '$':
            stack.append(oneState(c))
        elif c == '*':
            nfa = stack.pop()
            new_state = nfa.states
            nfa.states += 1
            message = message + "\nStar"
            for s in nfa.start_st:
                nfa.t_func.append((new_state, '$', s))
            nfa.fin_stat = True
            for f in nfa.final_st:
                nfa.t_func.append((f, '$', new_state))
            message = message + "\nadded to trans"
            nfa.start_st = [new_state]
            nfa.final_st = [new_state]
            message = message + "\nnewstates" + str(nfa.start_st) + " " + str(nfa.final_st)
            stack.append(nfa)
        elif c == '+' or c == '.':
            nfa_B = stack.pop()
            nfa_A = stack.pop()
            if c == '+':
                nfa_B.final_st = [nfa_A.states + i for i in nfa_B.final_st]
                nfa_B.start_st = [nfa_A.states + i for i in nfa_B.start_st]
                nfa_B.t_func = [ (nfa_A.states + t[0], t[1], nfa_A.states + t[2])
                                                for t in nfa_B.t_func]
                message = message + "\nUnion"
                new_nfa = NFA(None,None,None,None,None)
                new_nfa.states =  nfa_A.states + nfa_B.states + 1
                new_nfa.letters = letters
                new_nfa.start_st = [new_nfa.states - 1]
                new_nfa.final_st = nfa_A.final_st + nfa_B.final_st
                new_nfa.fin_stat = True
                new_nfa.t_func = nfa_A.t_func + nfa_B.t_func
                message = message + "\nAdded nfaA" 
                for st in nfa_A.start_st:
                    new_nfa.t_func.append((new_nfa.start_st[0], '$', st))
                message = message + "\nAdded nfaB"
                for st in nfa_B.start_st:
                    new_nfa.t_func.append((new_nfa.start_st[0], '$', st))
                
                stack.append(new_nfa)
            else:
                nfa_B.start_st = [nfa_A.states + i for i in nfa_B.start_st]
                nfa_B.final_st = [nfa_A.states + i for i in nfa_B.final_st]
                nfa_B.t_func = [ (nfa_A.states + t[0], t[1], nfa_A.states + t[2])
                                                for t in nfa_B.t_func]
                message = message + "\nconcat"
                new_nfa = NFA(nfa_A.states + nfa_B.states,letters,None,None,None)
                new_nfa.start_st = nfa_A.start_st
                new_nfa.final_st = nfa_B.final_st
                new_nfa.t_func = nfa_A.t_func + nfa_B.t_func
                new_nfa.fin_stat = True
                for st1 in nfa_A.final_st:
                    for st2 in nfa_B.start_st:
                        new_nfa.t_func.append((st1, '$', st2))

                stack.append(new_nfa)
    
    assert len(stack) == 1
    # print(message)
    return stack[0]


def main():
    with open(sys.argv[1], 'r') as file:
        data = json.load(file)
    regex = data['regex']
    regex = str(regex)
    # print(regex)
    nfa_ans = regexToNFA(regex)
    t_func = [(add_letter_Q(t[0]), t[1], add_letter_Q(t[2])) 
                                        for t in nfa_ans.t_func]


    output = dict()
    output['states'] = [add_letter_Q(st) for st in range(nfa_ans.states)]
    output['letters'] = [alp for alp in nfa_ans.letters]
    output['transition_function'] = [(add_letter_Q(t[0]), t[1], add_letter_Q(t[2])) 
                                        for t in nfa_ans.t_func]
    output['start_states'] = [add_letter_Q(st) for st in nfa_ans.start_st]
    output['final_states'] = [add_letter_Q(st) for st in nfa_ans.final_st]
    # print(output)
    with open(sys.argv[2], 'w') as file:
        json.dump(output,file,indent = 4)

main()
