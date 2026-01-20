import ast

def cool(n):
    for i in range(1,n):
        print(i * '*')

    for i in range(n,1,-1):
        print(i * '*')      
x = 0