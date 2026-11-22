"""Assignment 4 CO4: reproducible learning demonstrations.
Dependencies: numpy, scikit-learn, matplotlib (plots optional).
Run: python learning_lab.py
"""
import numpy as np
from collections import Counter

# Task 1: evaluation protocol and explicit baseline
def split_indices(n, test_fraction=0.2, seed=17):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    cut = int(n * (1-test_fraction))
    return idx[:cut], idx[cut:]

def majority_baseline(y_train, y_test):
    majority = Counter(y_train).most_common(1)[0][0]
    return float(np.mean(np.asarray(y_test) == majority)), majority

# Task 2: decision tree from scratch, numeric features
class Node:
    def __init__(self, prediction, feature=None, threshold=None, left=None, right=None):
        self.prediction, self.feature, self.threshold = prediction, feature, threshold
        self.left, self.right = left, right

def entropy(y):
    if len(y) == 0: return 0.0
    _, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    return float(-np.sum(p * np.log2(p)))

def gini(y):
    if len(y) == 0: return 0.0
    _, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    return float(1 - np.sum(p*p))

def best_split(X, y, criterion="entropy"):
    impurity = entropy if criterion == "entropy" else gini
    parent = impurity(y)
    best = (0.0, None, None)
    for j in range(X.shape[1]):
        values = np.unique(X[:, j])
        for t in (values[:-1] + values[1:]) / 2:
            mask = X[:, j] <= t
            if not mask.any() or mask.all(): continue
            gain = parent - (mask.mean()*impurity(y[mask]) + (~mask).mean()*impurity(y[~mask]))
            if gain > best[0]: best = (gain, j, float(t))
    return best

def fit_tree(X, y, criterion="entropy", max_depth=None, min_samples=2, depth=0):
    prediction = Counter(y.tolist()).most_common(1)[0][0]
    if len(np.unique(y)) == 1 or len(y) < min_samples or (max_depth is not None and depth >= max_depth):
        return Node(prediction)
    gain, feature, threshold = best_split(X, y, criterion)
    if feature is None or gain <= 1e-12: return Node(prediction)
    mask = X[:, feature] <= threshold
    return Node(prediction, feature, threshold,
                fit_tree(X[mask], y[mask], criterion, max_depth, min_samples, depth+1),
                fit_tree(X[~mask], y[~mask], criterion, max_depth, min_samples, depth+1))

def predict_one(node, row):
    while node.feature is not None:
        node = node.left if row[node.feature] <= node.threshold else node.right
    return node.prediction

def predict_tree(node, X):
    return np.array([predict_one(node, row) for row in X])

def tree_stats(node):
    if node.feature is None: return 1, 1
    dl, ll = tree_stats(node.left); dr, lr = tree_stats(node.right)
    return 1+max(dl,dr), ll+lr

# Task 3: 1-D Gaussian mixture EM; faulty version intentionally omits normalisation.
def gaussian_pdf(x, mu, var):
    var = max(float(var), 1e-9)
    return np.exp(-0.5*(x-mu)**2/var) / np.sqrt(2*np.pi*var)

def gmm_em(X, K=2, iterations=50, seed=0, faulty=False):
    X = np.asarray(X, dtype=float).ravel()
    rng = np.random.default_rng(seed)
    means = rng.choice(X, K, replace=False).astype(float)
    variances = np.full(K, max(np.var(X), 0.1))
    weights = np.full(K, 1/K)
    ll_trace, weight_trace = [], []
    for _ in range(iterations):
        joint = np.column_stack([weights[k]*gaussian_pdf(X, means[k], variances[k]) for k in range(K)])
        denom = joint.sum(axis=1, keepdims=True)
        resp = joint if faulty else joint / np.maximum(denom, 1e-300)
        if faulty:
            # The defect: responsibilities are unnormalised and Nk is not a component's expected count.
            resp = np.clip(resp, 0, 1)
        Nk = resp.sum(axis=0) + 1e-12
        means = (resp*X[:,None]).sum(axis=0)/Nk
        variances = (resp*(X[:,None]-means)**2).sum(axis=0)/Nk
        weights = Nk/Nk.sum()
        ll_trace.append(float(np.sum(np.log(np.maximum(denom.ravel(), 1e-300)))))
        weight_trace.append(float(weights.sum()))
    return weights, means, variances, np.array(ll_trace), np.array(weight_trace)

# Task 4: NumPy 2-2-1 network and XOR
def sigmoid(z): return 1/(1+np.exp(-np.clip(z,-40,40)))
def xor_forward(X, W1, b1, W2, b2):
    h = sigmoid(X@W1+b1)
    return sigmoid(h@W2+b2), h

def xor_train(seed=4, epochs=12000, lr=1.0):
    rng = np.random.default_rng(seed)
    X = np.array([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
    y = np.array([[0.],[1.],[1.],[0.]])
    W1 = rng.normal(0,1,(2,4)); b1=np.zeros(4)
    W2 = rng.normal(0,1,(4,1)); b2=np.zeros(1)
    for _ in range(epochs):
        pred,h = xor_forward(X,W1,b1,W2,b2)
        d2 = (pred-y)*pred*(1-pred)/len(X)
        gW2=h.T@d2; gb2=d2.sum(axis=0)
        d1=(d2@W2.T)*h*(1-h)
        gW1=X.T@d1; gb1=d1.sum(axis=0)
        W2-=lr*gW2; b2-=lr*gb2; W1-=lr*gW1; b1-=lr*gb1
    pred,_=xor_forward(X,W1,b1,W2,b2)
    return pred.ravel(), (W1,b1,W2,b2)

# Task 5: categorical Naive Bayes with Laplace smoothing
class CategoricalNB:
    def __init__(self, alpha=1.0): self.alpha=alpha
    def fit(self, X, y):
        self.classes_=np.unique(y); self.prior={}; self.tables=[]; self.values=[]
        for c in self.classes_:
            self.prior[c]=(np.sum(y==c)+self.alpha)/(len(y)+self.alpha*len(self.classes_))
        for j in range(X.shape[1]):
            vals=np.unique(X[:,j]); self.values.append(vals); table={}
            for c in self.classes_:
                subset=X[y==c,j]; denom=len(subset)+self.alpha*len(vals)
                table[c]={v:(np.sum(subset==v)+self.alpha)/denom for v in vals}
            self.tables.append(table)
        return self
    def predict(self, X):
        out=[]
        for row in X:
            scores=[]
            for c in self.classes_:
                s=np.log(self.prior[c])
                for j,v in enumerate(row): s+=np.log(self.tables[j][c].get(v, self.alpha/(self.alpha+1)))
                scores.append(s)
            out.append(self.classes_[int(np.argmax(scores))])
        return np.array(out)

# Task 6: tabular energy controller, Q-learning vs fixed rule
ACTIONS=("Off","Low","High")
def energy_step(state, action, rng):
    # state = (occupancy 0/1, temperature bucket 0=cool,1=warm,2=hot, price bucket 0/1)
    occ,temp,price=state
    cooling={"Off":0,"Low":1,"High":2}[action]
    next_temp=int(np.clip(temp + (1 if temp==2 else 0) - cooling + int(rng.random()<0.25),0,2))
    comfort_violation=int(occ and next_temp==2)
    kwh={"Off":0.0,"Low":0.7,"High":1.5}[action]
    cost=kwh*(1.0 if price==0 else 2.0)
    reward=-cost-3.0*comfort_violation
    next_occ=int(rng.random()<0.65)
    next_price=int(rng.random()<0.35)
    return (next_occ,next_temp,next_price), reward, kwh, comfort_violation

def q_learning(episodes=300, steps=48, seed=0, alpha=.15, gamma=.95, epsilon=.15):
    rng=np.random.default_rng(seed); Q=np.zeros((2,3,2,3)); returns=[]; energy=[]; violations=[]
    for ep in range(episodes):
        s=(0,1,0); total=used=bad=0
        for _ in range(steps):
            if rng.random()<epsilon: a=int(rng.integers(3))
            else: a=int(np.argmax(Q[s]))
            ns,r,k,v=energy_step(s,ACTIONS[a],rng)
            Q[s][a]+=alpha*(r+gamma*np.max(Q[ns])-Q[s][a])
            s=ns; total+=r; used+=k; bad+=v
        returns.append(total); energy.append(used); violations.append(bad)
    return Q,np.array(returns),np.array(energy),np.array(violations)

def demo():
    # Task 2 toy decision tree
    X=np.array([[95,1,85],[90,1,78],[60,0,40],[55,0,35],[80,1,65],[45,0,30]],float)
    y=np.array([1,1,0,0,1,0])
    tree=fit_tree(X,y,"entropy",max_depth=3)
    print("Decision tree depth/leaves:",tree_stats(tree),"predictions:",predict_tree(tree,X).tolist())
    # Task 3 repaired/faulty EM checks
    data=np.array([-2.2,-2.0,-1.8,2.0,2.2,2.4])
    repaired=gmm_em(data,seed=2); faulty=gmm_em(data,seed=2,faulty=True)
    print("EM repaired weight sum / final loglik:",repaired[0].sum(),repaired[3][-1])
    print("EM faulty weight sum / final loglik:",faulty[0].sum(),faulty[3][-1])
    # Task 4 XOR
    pred,_=xor_train()
    print("XOR predictions:",np.round(pred,3).tolist())
    # Task 5 Naive Bayes toy data
    nb=CategoricalNB(alpha=1).fit(np.array([["normal","low"],["hazard","high"],["normal","high"],["hazard","high"]]),np.array([0,1,0,1]))
    print("Naive Bayes:",nb.predict(np.array([["hazard","high"],["normal","low"]])).tolist())
    # Task 6 RL
    _,ret,en,vio=q_learning(episodes=100,seed=7)
    print("Q-learning last-20 mean return/energy/violations:",round(ret[-20:].mean(),2),round(en[-20:].mean(),2),round(vio[-20:].mean(),2))

if __name__ == "__main__":
    demo()
