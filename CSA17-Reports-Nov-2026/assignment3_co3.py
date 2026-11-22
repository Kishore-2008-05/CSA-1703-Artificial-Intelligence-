"""CSA17 CO3: propositional model checking, unification and chaining."""
from itertools import product

def entails(kb,query,symbols):
    models=0
    for values in product([False,True],repeat=len(symbols)):
        m=dict(zip(symbols,values)); models+=1
        if all(f(m) for f in kb) and not query(m): return False,models
    return True,models

def occurs(v,t,theta):
    if v==t:return True
    if isinstance(t,str) and t in theta:return occurs(v,theta[t],theta)
    if isinstance(t,tuple):return any(occurs(v,x,theta) for x in t[1:])
    return False

def unify(x,y,theta=None):
    theta={} if theta is None else dict(theta)
    def deref(t):
        while isinstance(t,str) and t in theta:t=theta[t]
        return t
    x,y=deref(x),deref(y)
    if x==y:return theta
    if isinstance(x,str) and x.startswith("?"):
        if occurs(x,y,theta):return None
        theta[x]=y;return theta
    if isinstance(y,str) and y.startswith("?"):return unify(y,x,theta)
    if isinstance(x,tuple) and isinstance(y,tuple) and x[0]==y[0] and len(x)==len(y):
        for a,b in zip(x[1:],y[1:]):
            theta=unify(a,b,theta)
            if theta is None:return None
        return theta
    return None

def forward_chain(facts,rules):
    known=set(facts); fired=0; changed=True
    while changed:
        changed=False
        for premises,conclusion in rules:
            if set(premises)<=known and conclusion not in known:
                known.add(conclusion);fired+=1;changed=True
    return known,fired

if __name__=="__main__":
    print("unifier",unify(("parent","?x","alice"),("parent","bob","alice")))
    print("occurs check",unify(("p","?x"),("p",("f","?x"))))
    print("chain",forward_chain({"badge","office"},[(("badge","office"),"allow")]))
