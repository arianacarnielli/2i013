import operator

l = {(1,2):5, (3,4):48, (0,5):12, (1,0):154, (1,1):154}

maxi=0

for cle in l.keys():
    if l[cle] >= maxi:
        maxi = l[cle]
print(maxi)
for a in l.keys():
    if l[a] == maxi:
        print(a)

        
        
