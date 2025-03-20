# n=5
# for i in range(n):
#     for j in range(n-i):
#         print(" ",end="")
#     for j in range(i):
#         print(chr(i+65-1),end=" ")
#     print()
# for i in range(n,0,-1):
#     for j in range(n-i):
#         print(" ",end="")
#     for j in range(i):
#         print(chr(i+65-1),end=" ")
#     print()

# n=10
# a,b=0,1
# for i in range(n):
#     c=a+b
#     a=b
#     b=c
#     print(b,end=" ")
    

m=153
n=str(m)
result=""
for i in n:
    rem=m%2
    result+=rem**3
    m=m//2
if n==result:
    print("armstrong")
else:
    print("Not armstrong")