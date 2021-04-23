# Report

## Automata Programming Assignment  
By Umang Srivastava  ( 2019101090 )

## Execution
For any problem 'qx' where x = 1,2,3,4
```bash
python3 qx.py <input_file> <output_file>
```


## Video demonstration

[Link](https://drive.google.com/file/d/1hBdp9n3_aH-PEpSfIPycAEJUFFq-d05o/view?usp=sharing) for the video demonstration of execution of all the programs.


## Q1 - Regex to NFA

- We assume that the given regex is valid.  
- Precedence order:  
  '*'  
  '.'  
  '+'
- The given regex is first segregated into valid tokens and then operations are performed as per the symbol. Then the different results are transformed into a NFA.

### NOTE:  
Some states can be eliminated.

## Q2 - NFA to DFA  

Consider an NFA < Q(n) ,q(n), Σ(n), δ(n)  :  Q(n)  x  Σ(n) -->  Q(n),   F(n) >

And its equivalent DFA < Q(d) ,q(d), Σ(d), δ(d)  :  Q(d)  x  Σ(d) -->  Q(d),   F(d) >

Then the following relations exist:
- Q (d) = Power set of Q(n)
- q(d)=q(n)
- Σ(d)=Σ(n)
- Transition matrix is union of all reachable states from a DFA state gives the destination state of DFA.

### NOTE:  
For some outputs, the order maybe different for a particular state. For example, State {"Q0", "Q2"} may be outputted as state {"Q2", "Q0"}. Both will convey the same result.

## Q3 - DFA to Regex

- If there exists any incoming edge to the initial state, then create a new initial state having no incoming edge to it.
- If there exists multiple final states in the DFA, then convert all the final states into non-final states and create a new single final state.
- If there exists any outgoing edge from the final state, then create a new final state having no outgoing edge from it.
- Then we eliminate states one by one.
- Source and destinations are concatenated.
- Kleen star is added for states with self transition.
- For same destination from the same source but on different letters , add a union operator between them.


## Q4 - Minimise DFA

- We minimize DFA using Myphill-Nerode Theorem
- If 2 states have indistinguishible behaviour in the transition matrix, then
they can be reduced to 1 state.
- We consider every state pair not necessarily connected directly and mark them. This is repeated till every state is marked.
- If there is an unmarked pair (Qi, Qj), mark it if the pair {δ (Qi, A), δ (Qi, A)} is marked for some input alphabet.
- Combine all the unmarked pair (Qi, Qj) and make them a single state in the reduced DFA.
