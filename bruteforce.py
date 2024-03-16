import sys, os, random, math
from collections import defaultdict, Counter, deque, OrderedDict
from heapq import heapify, heappush, heappop
from functools import cache, reduce
from bisect import bisect_left, bisect_right
from types import GeneratorType
from typing import *

input = lambda : sys.stdin.readline().strip()

debug = lambda *x,**y: 0
if os.environ.get('LOCAL_DEV'): debug = lambda *x,**y: print(*x,y, file=sys.stderr)


class SegmentTree:
    def __init__(self, arr, func = lambda x, y : x + y, defaultvalue = 0) :
        self.n = len(arr)
        self.segmentTree = [0]*self.n + arr
        self.func = func
        self.defaultvalue = defaultvalue
        self.buildSegmentTree(arr)

    def buildSegmentTree(self, arr) :   
        for i in range(self.n -1, 0, -1) :
            self.segmentTree[i] = self.func(self.segmentTree[2*i] , self.segmentTree[2*i+1])         
            
    def query(self, l, r) :
        l += self.n
        r += self.n
        res = self.defaultvalue
        while l < r :
            if l & 1 :   
                res = self.func(res, self.segmentTree[l])
                l += 1
            l >>= 1
            if r & 1 :  
                r -= 1      
                res = self.func(res, self.segmentTree[r]) 
            r >>= 1
        return res

    def update(self, i, value) :
        i += self.n
        self.segmentTree[i] = value  
        while i > 1 :
            i >>= 1         
            self.segmentTree[i] = self.func(self.segmentTree[2*i] , self.segmentTree[2*i+1])


class UnionFind:
    def __init__(self, n):
        self.n = n
        self.parents = list(range(n))
        self.count = [1]*n
    def find(self, x):
        if self.parents[x] == x:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x != y:
            self.parents[x] = y
            self.count[y] += self.count[x]

dire = [0,1,0,-1,0]

def is_prime(n):
    if n==1:
        return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True

def ncr(n, r, p):
    num = den = 1
    for i in range(r):
        num = (num * (n - i)) % p
        den = (den * (i + 1)) % p
    return (num * pow(den,
            p - 2, p)) % p

# For codeforces - hashmap to avoid TLE
RANDOM = random.randrange(2**62)
def mapping_wrapper(x):
  return x ^ RANDOM

class HashMap(dict):
    def __setitem__(self, key, value):
        super().__setitem__(mapping_wrapper(key), value)
    def __getitem__(self, key):
        return super().__getitem__(mapping_wrapper(key))
    def __contains__(self, key):
        return super().__contains__(mapping_wrapper(key))


MOD = 10**9 + 7

def binpow(a, b):
    if b==0:
        return 1
    res = binpow(a,b//2)
    res = pow(res,2,MOD)
    if b%2:
        return (res*a)%MOD
    return res

def mod_inverse(a):
    return binpow(a,MOD-2)

MAX = 2*(10**5)+5

def factors(n): 
    if n==0:
        return set()   
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

# factors = [factors(i) for i in range(MAX)]

# factorial and inverse factorial

# fact = [1]*MAX
# invfact = [1]*MAX
# for i in range(1,MAX):
#     fact[i] = (fact[i-1]*i)%MOD
#     invfact[i] = (invfact[i-1]*mod_inverse(i))%MOD

# recursion limit fix decorator, change 'return' to 'yield' and add 'yield' before calling the function
def bootstrap(f):  
    stack = []
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc

def binary_search(left,right,check,ans):
    minimum_ans = (ans == left)
    while left<=right:
        mid = (left+right)//2
        if minimum_ans:
            if check(mid):
                ans,left = mid, mid+1
            else:
                right = mid-1
        else:
            if check(mid):
                ans,right = mid, mid-1
            else:
                left = mid+1
    return ans

binn = lambda num: bin(num)[2:]

class lazyheap:
    def __init__(self):
        self.heap = []  
        self.count = 0   
        self.sum = 0 
        self.toremove = Counter()
    
    def push(self, item):
        heappush(self.heap, item)
        self.count += 1
        self.sum += item
 
    def remove(self, item):
        self.toremove[item] += 1    
        self.count -= 1
        self.sum -= item
 
    def top(self):
        x = self.heap[0]
        while self.toremove[x] > 0:
            self.toremove[x] -= 1
            heappop(self.heap)
            x = self.heap[0]
        return x
 
    def pop(self):
        x = self.top()
        heappop(self.heap)
        self.count -= 1
        self.sum -= x
        return x

def bit_sum(num):
    b = len(binn(num))
    bs = [0] * b
    c = 2**b - 1
    for i in range(b):
        c -= (1<<i)
        bs[i] = (num & c) // 2
        if num & ((1<<i)):
            bs[i] += (num % (1<<i)) + 1
    return bs

class RollingHash:
    def __init__(self, base = 256, string = "", func = ord):
        self.base = base
        self.hash = 0
        self.length = 0
        self.func = func
        for i in string:
            self.left_add(i)

    def left_add(self, char):
        self.hash =  (self.hash * self.base + self.func(char)) % MOD
        self.length += 1
    
    def right_add(self, char):
        self.hash =  (self.hash + self.func(char) * pow(self.base, self.length, MOD)) % MOD
        self.length += 1


###############################################################################

def solve(case=None):
    pass

###############################################################################

test_cases = int(input())
# test_cases = 1
for t in range(test_cases):
    solve(t+1)