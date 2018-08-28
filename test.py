a= [(1,2),(3,4)]
b=[5,6]
c=list(map(lambda x,y: x+tuple([y]),a,b))
print(c)