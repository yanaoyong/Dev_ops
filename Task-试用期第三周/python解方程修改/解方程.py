import math

a=int(input("请输入方程a项的值"))
b=int(input("请输入方程b项的值"))
c=int(input("请输入方程c项的值"))
d=b*b-4*a*c
def quadratic(a,b,c,d):
    if a==0:
        x1=-c/b
        return ("此一元一次方程的解为"),x1
    elif d<0:
        return ("此一元二次方程无解")
    else:
        d=math.sqrt(d)
        x1=-(b+d)/(2*a)
        x2=-(b-d)/(2*a)
        return ("此一元二次方程的解为"),x1,x2
print(quadratic(a,b,c,d))  