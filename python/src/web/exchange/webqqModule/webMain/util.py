#coding=utf-8
__author__ = 'zhouyi1'

import PyV8

def hashJs(q,ptwebqq):
    encryptionJs = open('mq_comm.js')
    encryptionJsCode = encryptionJs.read()
    ctxt = PyV8.JSContext()
    ctxt.enter()
    jsCode = encryptionJsCode
    encryptionJsFun = ctxt.eval(jsCode)
    hashCode = encryptionJsFun.u(q,ptwebqq)
    return hashCode

# u = function (x, K) {
#     x += "";
#     for (var N = [], T = 0; T < K.length; T++)N[T % 4] ^= K.charCodeAt(T);
#     var U = ["EC", "OK"], V = [];
#     V[0] = x >> 24 & 255 ^ U[0].charCodeAt(0);
#     V[1] = x >> 16 & 255 ^ U[0].charCodeAt(1);
#     V[2] = x >> 8 & 255 ^ U[1].charCodeAt(0);
#     V[3] = x & 255 ^ U[1].charCodeAt(1);
#     U = [];
#     for (T = 0; T < 8; T++)U[T] = T % 2 == 0 ? N[T >> 1] : V[T >> 1];
#     N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
#     V = "";
#     for (T = 0; T < U.length; T++) {
#         V += N[U[T] >> 4 & 15];
#         V += N[U[T] & 15]
#     }
#     return V
# }

def hash(q,ptwebqq):
    q += ""
    N = [0]*len(ptwebqq)
    for T in range(len(ptwebqq)):
        N[T%4] ^= ord(ptwebqq[T])
    U = ["EC","OK"]
    V = [0 for i in range(4)]
    V[0] = int(q)>>24 & 255 ^ ord(U[0][0])
    V[1] = int(q)>>16 & 255 ^ ord(U[0][1])
    V[2] = int(q)>>8 & 255 ^ ord(U[1][0])
    V[3] = int(q) & 255 ^ ord(U[1][1])
    U = [0 for i in range(8)]
    for T in range(8):
        U[T] = N[T>>1] if T%2==0 else V[T>>1]
    N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    V = ""
    for T in range(len(U)):
        V += N[U[T] >> 4 & 15]
        V += N[U[T] & 15]
    return V



def hashOld(q,ptwebqq):
    N=ptwebqq + "password error"
    T=""
    V=[]
    while(1):
        if(len(T) <= len(N)):
            T += q
            if(len(T) == len(N)):
                break
        else:
            T = T[:len(N)]
            break

    for u in range(len(T)):
        V.append(ord(T[u]) ^ ord(N[u]))

    N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    T = ""
    for u in range(len(V)):
        T += N[V[u] >> 4 & 15]
        T += N[V[u] & 15]
    return T

        #老版
        # u = function (x, K) {
        #     for (var N = K + "password error",
        #     T = "",
        #     V = [];;) if (T.length <= N.length) {
        #         T += x;
        #         if (T.length == N.length) break
        #     } else {
        #         T = T.slice(0, N.length);
        #         break
        #     }
        #     for (var U = 0; U < T.length; U++) V[U] = T.charCodeAt(U) ^ N.charCodeAt(U);
        #     N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
        #     T = "";
        #     for (U = 0; U < V.length; U++) {
        #         T += N[V[U] >> 4 & 15];
        #         T += N[V[U] & 15]
        #     }
        #     return T
        # }();