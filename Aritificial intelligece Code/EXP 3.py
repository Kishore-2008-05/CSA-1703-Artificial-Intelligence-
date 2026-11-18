import itertools

w1,w2,w3=input("Enter the words: ").split()

letters=set(w1+w2+w3)
letters=list(letters)

for p in itertools.permutations(range(10),len(letters)):
    d=dict(zip(letters,p))

    if d[w1[0]]==0 or d[w2[0]]==0 or d[w3[0]]==0:
        continue

    n1=0
    for ch in w1:
        n1=n1*10+d[ch]

    n2=0
    for ch in w2:
        n2=n2*10+d[ch]

    n3=0
    for ch in w3:
        n3=n3*10+d[ch]

    if n1+n2==n3:
        print(w1,"=",n1)
        print(w2,"=",n2)
        print(w3,"=",n3)
        break
else:
    print("No solution")
