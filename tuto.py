def newlist(a,b):
    return [a*b for a,b in zip(a,b)]

def sizeofwords(a):
    for i in a:
        print(i,len(i))

def swap(temp):
    return temp[-1:] + temp[1:-1] + temp[:1]

arr=[1,2,3,4]
brr=[5,6,7,8]
print(newlist(arr,brr))
print(sizeofwords(["car","bike"]))
print(swap("siddharth"))

marks=list(map(int,input().split()))
print(sum(marks)/len(marks))
