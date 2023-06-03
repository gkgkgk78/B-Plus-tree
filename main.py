# -*- coding: utf-8 -*-
import sys
import csv
import pickle

sys.setrecursionlimit(1000000000)
import math
import random
from random import *


# 각 노드를 만들기 위한 부분
# 이부분은 리프노드가 아닙니다.
class NODE:
    def __init__(self, degree):
        self.m = []
        self.value = []
        self.degree = degree
        # self.p = []
        self.parent = None
        self.r = []  # 가장 오른쪽 child node를 가리키는 것을 의미
        # self.type="node"

    def split(self):  # 리프 노드들이 아닌 노드들이 위로 올라갈때 처리과정임
        key_1 = (self.degree // 2)  # 해당 되는 인덱스가 이제 쪼갤때 위로 올라갈 노드임!
        mid = self.m[key_1]
        # print("hi",self.value)
        # print(self.m,self.p)
        # 왼,가,오
        topleft = NODE(self.degree)
        topleft.m = self.m[0:key_1]
        topleft.value = self.value[0:key_1 + 1]
        # topleft.p = self.p[0:key_1]
        topleft.r = topleft.value[key_1]
        topright = NODE(self.degree)
        topright.m = self.m[key_1 + 1:]
        topright.value = self.value[key_1 + 1:]

        topright.r = topright.value[len(topright.value) - 1]
        top = NODE(self.degree)
        top.value = [topleft, topright]
        top.m = [mid]
        top.r = topright

        topright.parent = top
        topleft.parent = top
        return top


# 리프 노드가 되는 부분 이제 리프 노드가 되어서 처리를 하여줍니다
class LEAFNODE():
    def __init__(self, degree):
        self.m = []
        self.value = []
        self.degree = degree
        self.parent = None

        self.right = None
        # self.type="leaf"

    def split(self):
        key_1 = (self.degree // 2)  # 해당 되는 인덱스가 이제 쪼갤때 위로 올라갈 노드임!

        left = LEAFNODE(self.degree)
        RL = LEAFNODE(self.degree)
        RL.value = self.value[key_1:]
        RL.m = self.m[key_1:]

        mid = NODE(self.degree)
        ind = self.value[key_1]
        mid.m.append(self.m[key_1])
        mid.value = [self, RL]
        mid.r = RL
        # print(self.value[key_1])

        left.m = self.m[0:key_1]
        left.value = self.value[0:key_1]
        self.m = left.m
        self.value = left.value

        RL.right = self.right
        self.right = RL
        self.parent = mid
        RL.parent = mid

        return mid


class plustree:

    # 우선 삽입 되는 노드는 리프노드로 써 처리가 된다
    def __init__(self, degree):
        no = LEAFNODE(degree)
        self.root = no  # 처음 노드는 리프노드형태로 저장이 되어야 함.
        self.degree = degree

    def insert(self, key, value):
        node = self.root
        # 삽입은 어차피 리프 노드에서만 일어나는데
        # 루트 노드에서부터 차례대로 하나 하나씩 찾아나가 보자
        while (True):
            if type(node) == LEAFNODE:  # 리프 노드일시 탐색을 멈추게 됨
                break
            else:
                hi = node
                node = self.find(node, key)  # 리프노드를 찾을때까지 찾아가는 형식
                # 쭉 타고 내려가면서 찾아갑니다
                if type(node) == LEAFNODE:
                    break
        # 이제 탐색을 마치고 찾아낸 리프노드에 삽입을 시켜줘야함
        key1 = [key]
        value1 = [[value]]
        if len(node.m) == 0:  # 가장 처음에 삽입을 하는 경우를 나타냄
            # print(node.m)
            node.m += key1
            # print(node.m,key)
            node.value += value1
            h = node.m.index(key)


        else:  # 리프노드에서 처음 삽입하는게 아님
            index = 0
            for i in node.m:
                if key < i:  # 지금 입력하려는 키값이 원래 있던 값보다 작을경우
                    pre = node.m[0:index]
                    nex = node.m[index:]
                    final = pre + key1 + nex
                    node.m = final
                    pre = node.value[0:index]
                    nex = node.value[index:]
                    final = pre + value1 + nex
                    node.value = final
                    t = node.m.index(key)
                    break
                index = index + 1
            if index == len(node.m):  # 이제는 넣을곳은 맨 마지막 에 넣어줘야함,그전까지의 위치에서 찾지못함
                node.m += key1
                node.value += value1
                t = node.m.index(key)

        # 삽입을 한후에 크기가 꽉차게 되었으면 분할과정을 통해
        # 부모로 올리고 부모조차 가득찼으면 계속 반복해야함

        if len(node.m) >= node.degree:  # 이제 가득 차게 된것이니 위로 올라가면서 쭉 분할을 해야 하는 과정
            # 분할을 할시에 키값이 변경이 되는 지점도 생각을 해야함
            # 분할을 한다라....

            while (len((node.m)) >= node.degree):
                if type(node) == LEAFNODE:  # 분할이 일어나는 노드가 리프노드라면
                    # 걍 부모노드로 올림
                    pi = node.parent
                    # print(type(node.parent))
                    ki = node.split()  # 을 통해서 리프노드에서 부모노드로 올릴 것을 찾아냄
                    # print(ki.value,ki.m)
                    if pi == None:  # 초기분할이 일어나야 하는 상태로 리프 노드들의 집합임
                        pi = NODE(node.degree)
                        pi.m = ki.m
                        pi.value = ki.value
                        pi.r = pi.value[len(pi.value) - 1]
                        node = pi
                        for i in pi.value:
                            if i.parent != pi:
                                i.parent = pi
                        self.root = node


                    else:  # 이때는 리프노드인데 부모가 존재하는 경우
                        # 들어갈 위치를 찾아야 함, 그후 데이터 값을 넣어줌
                        # 찾아낸 부모 노드를 다 parent로 지정해주어야 함
                        hi = pi
                        nono = self.find(pi, ki.m[0])
                        j = hi.value.index(nono)
                        tag = j
                        # 이제 노드가 들어갈 위치를 찾았는데....
                        # 부모노드의 어느 부분에 들어가야 하는지 확인해보고 알맞게 넣어주자

                        for i in ki.value:
                            if i.parent != pi:
                                i.parent = pi  # 이제 올라간 노드의 자식들이 부모 노드에 해당 되어야 함
                        # 이제 올라온 노드를 알맞은 위치에 넣어 주어야 함.

                        # !!이제 부모 노드에 넣어줄때 키와 인덱스 처리 과정은 어떻게 되야할지 생각해보자.
                        # 원래있던 key와 value 들을 지워야 하나?....->
                        if tag == 0:  # 맨 처음 부분에 들어감
                            # print("처음 리프")
                            pi.m = ki.m + pi.m
                            pi.value = ki.value + pi.value[tag + 1:]
                            pi.r = pi.value[len(pi.value) - 1]

                            node = pi

                        elif tag == len(pi.m):  # 맨 마지막에 들어감
                            # print("마지막 리프")
                            pi.m = pi.m + ki.m
                            pi.value = pi.value[0:tag] + ki.value
                            pi.r = pi.value[len(pi.value) - 1]
                            node = pi

                        else:  # 걍 중간에 들어감, 이때는 해당 인덱스에 추가 되야 하는 부분임
                            del pi.value[tag]  # 후에 넣으려는 노드 추가 위해 제거 ,key는 제거하면 안됨!
                            # print("중간 리프")
                            pi.m = pi.m[0:tag] + ki.m + pi.m[tag:]
                            pi.value = pi.value[0:tag] + ki.value + pi.value[tag:]
                            pi.r = pi.value[len(pi.value) - 1]
                            node = pi
                    if node.parent == None:
                        self.root = node

                else:  # 여기는 분할하려는데 리프노드 형태가 아닌 그냥 노드일경우를 처리
                    # 여기는 내부 노드이기도 하며 / 루트 노드가 해당 되기도 함
                    pi = node.parent
                    ki = node.split()
                    if pi == None:
                        node = ki
                        for i in ki.value:
                            for j in i.value:
                                if j.parent != i:
                                    j.parent = i
                        self.root = node
                    else:  # 여기는 그냥 상위 루트 노드가 아닌 내부 노드 들 처리를 위한 곳
                        hi = node.parent
                        nono = self.find(node.parent, ki.m[0])
                        j = hi.value.index(nono)
                        tag = j
                        for i in ki.value:
                            if i.parent != pi:
                                i.parent = pi
                            for j in i.value:
                                if j.parent != i:
                                    j.parent = i

                        if tag == 0:  # 맨 처음 부분에 들어감
                            # print("처음 노드")
                            pi.m = ki.m + pi.m
                            pi.value = ki.value + pi.value[tag + 1:]
                            pi.r = pi.value[len(pi.value) - 1]
                            node = pi


                        elif tag == len(pi.m):  # 맨 마지막에 들어감
                            # print("마지막 노드")
                            pi.m = pi.m + ki.m
                            pi.value = pi.value[0:tag] + ki.value
                            pi.r = pi.value[len(pi.value) - 1]
                            node = pi

                        else:  # 걍 중간에 들어감, 이때는 해당 인덱스에 추가 되야 하는 부분임
                            del pi.value[tag]  # 후에 넣으려는 노드 추가 위해 제거 ,key는 제거하면 안됨!
                            # print("중간 노드")
                            pi.m = pi.m[0:tag] + ki.m + pi.m[tag:]
                            pi.value = pi.value[0:tag] + ki.value + pi.value[tag:]
                            pi.r = pi.value[len(pi.value) - 1]
                            node = pi
                        if pi == None:
                            node = ki
                            self.root = node

    def merge_left_node(self, left_t, node, parent):

        hk = parent.value.index(node)  # 부모 노드에서 병합 진행 하려는 노드가리키는 인덱스 찾기
        parent.value.pop(hk)
        # 부모 노드 값 들 왼쪽 노드에 다 넣어줌
        left_t.m.append(parent.m[hk - 1])
        nk = parent.m.pop(hk - 1)
        # 오른쪽 노드 값들을 왼쪽 노드에 넣어줌
        left_t.m += node.m
        # 합칠 오른쪽 노드들의 부모를 왼쪽 노드로 모두 변경
        for i in node.value:
            i.parent = left_t
        left_t.value += node.value
        left_t.r = left_t.value[-1]

        if len(self.root.m) == 0:  # 부모노드의 키값이 존재 하지 않는다면
            self.root = left_t  # 루트노드 변경

        return left_t

    def merge_right_node(self, right_t, node, parent):
        hk = parent.value.index(node)  # 부모 노드에서 병합 진행 하려는 노드가리키는 인덱스 찾기
        parent.value.pop(hk)
        if hk >= len(parent.value):
            nk1 = parent.m[-1]
            right_t.m.insert(0, nk1)
            nk = parent.m.pop(-1)
        # 부모 노드 값 들 오른쪽 노드에 다 넣어줌
        else:
            nk1 = parent.m[hk]
            right_t.m.insert(0, nk1)
            nk = parent.m.pop(hk)
        chj = 0
        hkn = -2.5
        right_t.m = node.m + right_t.m
        # 합칠 오른쪽 노드들의 부모를 왼쪽 노드로 모두 변경
        for i in node.value:
            i.parent = right_t
        right_t.value = node.value + right_t.value
        right_t.r = right_t.value[-1]
        # 부모노드의 부모노드가 존재한다면 자식노드 바뀐 left 노드로 지정해주고
        if len(self.root.m) == 0:  # 부모노드의 키값이 존재 하지 않는다면
            self.root = right_t  # 루트노드 변경

        return right_t

    def merge_left_leaf(self, left_t, node, parent, key):

        node_p = parent
        jk = 0
        # left_t가 위치하는 인덱스와 node가 위치하는 인덱스를 찾기 위한 코드
        for i in node_p.value:
            if i == left_t:
                break
            jk = jk + 1

        up_to = -1.4
        key_1 = node.m.index(key)  # 병합 시킬  노드에서 KEY가 있는 인덱스 찾기
        del node.m[key_1]  # 원래 노드에서 삭제하고자 한값 지움
        if len(node.m) > 0:
            up_to = node.m[0]
        nk_1 = parent.value.index(node)  # 지금 가리키는 노드를 찾아내서

        change_out = parent.m[nk_1 - 1]
        if len(node.m) > 0:
            parent.m[nk_1 - 1] = up_to  # 올려야할 값으로 바꿔줌
        ch = 0
        # 왼쪽노드로 옮기기전에 정리 node의 value 삭제해주자.
        node.value.pop(key_1)
        ch = 0

        # 왼쪽 노드에서 처리해 주는 과정
        left_t.m += node.m
        left_t.value += node.value

        key_hi = left_t.m[0]  # 나중에 내부 노드로 올릴 값
        left_t.right = node.right  # node의 오른쪽 포인터는 사라질 노드가 가리키던 오른쪽 포인터로지정
        # 부모노드 처리
        parent.value.pop(nk_1)
        lm = parent.m.pop(nk_1 - 1)
        node_p.r = node_p.value[-1]

        if len(self.root.m) == 0 and len(left_t.parent.m) == 0:  # 부모노드의 키값이 존재 하지 않는다면
            if self.root == left_t.parent:
                self.root = left_t  # 루트노드 변경
                left_t.parent = None

        return key_hi

    def merge_right_leaf(self, right_t, node, parent, key):
        # 이제 이상황은 오른쪽 노드와 병합을 진행하여야 하는 상황임!
        # 그렇담, 상대측 노드에서 빌려줄수 있는것 또한 최소의 키 개수를 가진 상태임!
        node_p = parent

        bright = 0
        for i in node_p.value:
            if right_t == i:
                break
            bright = bright + 1  # 이렇게 해서 부모 노드에서 right_t의 인덱스 순서를 알아내고 node의 순서도 알수있음

        # 오른쪽 노드에서 처리해 주는 과정
        node.m += right_t.m
        node.value += right_t.value

        # 이거 지울때 우리가 삭제하고자 했던 값이 나타내던 것만 지우자
        key_1 = node.m.index(key)
        del node.m[key_1]
        del node.value[key_1]
        value = node.value[key_1]

        key1 = node.m[0]  # 나중에 내부 노드로 올릴 값
        node.right = right_t.right  # node의 오른쪽 포인터는 사라질 노드가 가리키던 오른쪽 포인터로지정

        # 이제 부모 노드 처리과정
        help = node_p.m.pop(bright - 1)

        node_p.value.pop(bright)  # 지우게 될 노드 가리키던 포인터 지움
        node_p.r = node_p.value[-1]  # 맨 오른쪽 가리키던 포인터 갱신

        if len(self.root.m) == 0 and len(node.parent.m) == 0:  # 부모노드의 키값이 존재 하지 않는다면
            if self.root == node.parent:
                self.root = node  # 루트노드 변경
                node.parent = None
        return key1

    def borrow_left_node(self, left_t, node, parent):
        borrowleft_key = left_t.m[-1]
        borrowleft_value = left_t.value[-1]
        borrowleft_index = 0
        borrowleft_pair = []
        for i in parent.value:
            if i == left_t:
                break
            borrowleft_index = borrowleft_index + 1  # 왼쪽 노드에 해당하는 인덱스 값을 알아둠
        # 부모노드 변경과정
        change_to_parent_key = parent.m[borrowleft_index]  # 바꿔야할 부모노드 키값
        parent.m[borrowleft_index] = left_t.m[-1]  # 부모 키값 변경

        left_t.m.pop(-1)
        # value
        left_t.value.pop(-1)
        node.value.insert(0, borrowleft_value)
        node.value[0].parent = node
        nnn = node.value[1]
        nnn = nnn.m[0]
        node.m.insert(0, nnn)

        node.r = node.value[-1]
        left_t.r = left_t.value[-1]
        parent.r = parent.value[-1]

    def borrow_right_node(self, right_t, node, parent):
        borrowright_value = right_t.value[0]
        borrowright_index = 0
        for i in parent.value:
            if i == right_t:
                break
            borrowright_index = borrowright_index + 1  # 왼쪽 노드에 해당하는 인덱스 값을 알아둠
        # 부모노드 변경과정
        change_to_parent_key = parent.m[borrowright_index - 1]  # 바꿔야할 부모노드 키값
        parent.m[borrowright_index - 1] = right_t.m[0]  # 부모 키값 변경

        right_t.m.pop(0)
        # value
        right_t.value.pop(0)

        # 빌려줄 노드에 삽입하는 과정 어차피 맨 뒤에 다 삽입 시켜주면됨
        node_insert_key = node.value[-1]
        node.m.append(change_to_parent_key)  # 맨뒤에 삽입
        node.value.append(borrowright_value)
        node.value[-1].parent = node

        node.r = node.value[-1]
        right_t.r = right_t.value[-1]
        parent.r = parent.value[-1]

    def borrow_left_leaf(self, left_t, node, parent, key):
        # 이제 왼쪽 리프노드에서 빌려오는 경우를 상정해서 시작해보자
        # 이때는 삭제하고자 하는 값을 그저 가져올거임
        borrow_left_key = left_t.m[-1]  # 이제 빌려올 키 값을 우선 알아두고
        borrow_left_value = left_t.value[-1]
        node_p = parent  # 부모 노드에서 지우려는 값이 위치하는 키 인덱스를 알아두고
        control = 0
        for i in parent.m:  # 부모 노드 키값 조정을 위한 인덱스 찾는 과정
            if key < i:
                break
            control = control + 1
        if i == len(parent.m):
            control = i
        don = []

        # 부모노드 수정하는 과정
        node_p.m[control - 1] = left_t.m[-1]  # 빌려올 키값을 부모노드에 올림
        # 빌려온 오른쪽 노드 값들 수정하는 과정
        del left_t.m[-1]  # 빌려온 key 삭제

        don = []
        del left_t.value[-1]  # 왼쪽 노드에서 오른쪽으로 빌려주니 가장 오른쪽 에있는거 제거해주면됨

        jkjk = node.m.index(key)
        node.m[jkjk] = borrow_left_key
        node.value[jkjk] = borrow_left_value
        parent.r = parent.value[-1]

        if parent.parent == None:
            self.root = parent

    def borrow_right_leaf(self, right_t, node, parent, key):
        borrow_left_key = right_t.m[0]  # 이제 빌려올 키 값을 우선 알아두고
        borrow_left_value = right_t.value[0]
        node_p = parent  # 부모 노드에서 지우려는 값이 위치하는 키 인덱스를 알아두고
        control = 0
        for i in parent.m:  # 부모 노드 키값 조정을 위한 인덱스 찾는 과정
            if key <= i:
                break
            control = control + 1
        nk = control
        ch = 0
        for i in node_p.m:  # 부모 노드의 키값 수정, 빌린 오른쪽 노드의 값의 오른쪽 값을 올려줌
            if i == borrow_left_key:
                node_p.m[ch] = right_t.m[1]
                break
            ch = ch + 1
        node.m.remove(key)
        ik = -5.5
        if len(node.m) > 0:  # 텅빈 노드 일수도 있으니 이렇게 처리
            ik = node.m[0]
        node.m.append(key)
        if ik != -5.5:
            if ch > 0:
                node_p.m[ch - 1] = ik

        # 빌려온 오른쪽 노드 값들 수정하는 과정
        del right_t.m[0]  # 빌려온 key 삭제
        don = []
        # del right_t.value[right_t.value.index([borrow_left_key])]  # 빌려온 value삭제
        del right_t.value[0]  # 빌려온 value삭제
        l = 0

        # 맨 뒤에 있을 key를 빌려온 값을 넣어줌
        jhkjk = node.m.index(key)
        # hkhk = node.value.index([key])
        node.value[jhkjk] = borrow_left_value
        node.m[jhkjk] = borrow_left_key

        parent.r = parent.value[-1]
        if parent.parent == None:
            self.root = parent

    def delete(self, key):
        node = self.root
        while (True):
            if type(node) == LEAFNODE:  # 리프 노드일시 탐색을 멈추게 됨
                break
            else:
                hi = node
                node = self.find(node, key)  # 리프노드를 찾을때까지 찾아가는 형식
                j = hi.value.index(node)
                tag = j
                # 쭉 타고 내려가면서 찾아갑니다
                if type(node) == LEAFNODE:
                    break

        # 삭제하려는 값이 리프노드가 아닌 내부노드에 존재하는지 탐색하는 과정
        node2 = self.root
        while (True):
            if node2 == None or key in node2.m:  # 리프 노드일시 탐색을 멈추게 됨
                break
            else:
                node2 = self.find_internal(node2, key)  # 리프노드를 찾을때까지 찾아가는 형식
                # 쭉 타고 내려가면서 찾아갑니다
                if node2 == None or key in node2.m:
                    break
        '''
        찾고자 하는 키가 있는 상태임! 
        우선 리프 노드에서 제거를 하고자 함.(node는 리프노드)    
        1. 찾은 노드에 최소 키보다 많은 키가 존재하는가?
        2. 노드에 삭제 해야 하는데 최소키 만큼의 수가 있다면.....,
           키를 삭제하고 형제로부터 키를 빌리자!, 그후 부모에 형제노드의 중앙값키 추가    
        '''
        right_t = None
        left_t = None
        angel = node.parent
        if angel != None:
            gosibling = self.find(angel, key)
            goindex = angel.value.index(gosibling)  # 형제 노드 찾기 위한 인덱스부터 설정 , 우선 부모노드에서 나부터 설정 하는거로
            left_index = goindex - 1
            right_index = goindex + 1
            # print(left_index,right_index)
            # 형제 노드는 부모 노드를 통해서만 찾아야 함! 그게 형제임

            # key값이 있는 노드의 왼쪽과 오른쪽노드를 찾았으니
            # 찾아낸 인덱스가 부모노드가 가진 인덱스를 넘어섰을수도 있음!
            # 그거 판별하자
            if left_index >= 0 and left_index <= len(node.parent.value):
                left_t = node.parent.value[left_index]

            if right_index >= 0 and right_index > left_index and right_index <= len(node.parent.value) - 1:
                right_t = node.parent.value[right_index]

        node_counter = len(node.m)
        check_minimum = math.ceil(node.degree / 2) - 1
        # 이때는 키가 리프노드에만 존재할 경우라고 가정하자
        if type(node2) == LEAFNODE and node2 == self.root:
            ok_left = 0
            ok_right = 0
            # 우선 삭제하려는 노드의 양쪽 노드가 존재 하는지 안하는지 부터 살펴보자!...
            if left_t != None:
                ok_left = 1  # 1 이라는 숫자의 의미는 해당 되는 형제 노드가 존재함을 의미한다.
            if right_t != None:
                ok_right = 1
            # 왼쪽 형제와 오른쪽 형제 노드가 빌려줄수 있는 상황인지 판단해보자.
            ok_left_borrow = 0
            ok_right_borrow = 0
            if ok_left == 1:
                if len(left_t.m) - 1 >= check_minimum:
                    ok_left_borrow = 1
            if ok_right == 1:
                if len(right_t.m) - 1 >= check_minimum:
                    ok_right_borrow = 1
            '''
            부모 key를 조정 할필요 없이 가져오는 경우를 생각하여 보자.                
            '''
            if node.m[0] != key:  # 삭제하려는 노드가 리프노드의 맨앞에 위치하면 위의
                if (node_counter - 1 >= check_minimum):  # 삭제하려는 노드에서 삭제가 가능할때
                    inin = node.m.index(key)
                    # print(inin,node.m,node.m[inin],key)
                    node.m.remove(key)  # 해당 되는 키값 삭제
                    node.value.pop(inin)  # 해당 되는 키값에 해당하는 value삭제
                    inin = 0
                    intex = 0

                else:
                    if ok_left_borrow == 1:  # 왼쪽 형제 에게서 빌려올수 있음,우선 현재 리프 노드일 경우임
                        # 빌려올 왼쪽 노드와 부모노드 키값을 조정하는 과정
                        self.borrow_left_leaf(left_t, node, node.parent, key)  # 왼쪽 리프노드, 지워야할 노드, 노드의 부모 를 넘겨줌
                    elif ok_right_borrow == 1:  # 왼쪽 형제 에게서 빌려올수 있음,우선 현재 리프 노드일 경우임
                        # 빌려올 왼쪽 노드와 부모노드 키값을 조정하는 과정
                        self.borrow_right_leaf(right_t, node, node.parent, key)  # 오른쪽 리프노드, 지워야할 노드, 노드의 부모 를 넘겨줌
                    else:  # 오른쪽과 병합
                        '''
                        !!! 이쪽도 left, right borrow하는거 만들어 놓자

                        '''
                        if ok_left == 1:  # 왼쪽 노드와 병함

                            kij = self.merge_left_leaf(left_t, node, node.parent, key)
                        else:
                            #
                            kij = self.merge_right_leaf(right_t, node, node.parent, key)
                            # 얘는 키가 내부 노드에 존재 안하니 추가조정 필요는 없음

            # 키가 리프노드에만 존재하는데 삭제하려는 리프노드의 개수가 삭제할시 최소 수만큼 존재해서 형제로부터 키를 빌려야 하는 상황!
            else:
                if (node_counter - 1 >= check_minimum or node == self.root):  # 삭제하려는 노드에서 삭제가 가능할때
                    inin = node.m.index(key)
                    # print(inin,node.m,node.m[inin],key)
                    node.m.remove(key)  # 해당 되는 키값 삭제
                    node.value.pop(inin)  # 해당 되는 키값에 해당하는 value삭제
                    inin = 0
                    intex = 0
                else:
                    if ok_left_borrow == 1:  # 왼쪽 형제 에게서 빌려올수 있음,우선 현재 리프 노드일 경우임
                        # 빌려올 왼쪽 노드와 부모노드 키값을 조정하는 과정
                        self.borrow_left_leaf(left_t, node, node.parent, key)  # 왼쪽 리프노드, 지워야할 노드, 노드의 부모 를 넘겨줌
                    elif ok_right_borrow == 1:  # 왼쪽 형제 에게서 빌려올수 있음,우선 현재 리프 노드일 경우임
                        # 빌려올 왼쪽 노드와 부모노드 키값을 조정하는 과정
                        self.borrow_right_leaf(right_t, node, node.parent, key)  # 오른쪽 리프노드, 지워야할 노드, 노드의 부모 를 넘겨줌
                    else:  # 오른쪽과 병합
                        if ok_left == 1:  # 왼쪽 노드와 병함

                            kij = self.merge_left_leaf(left_t, node, node.parent, key)
                        else:
                            #
                            kij = self.merge_right_leaf(right_t, node, node.parent, key)
                            # 얘는 키가 내부 노드에 존재 안하니 추가조정 필요는 없음


        # 이제 키가 리프노드에만 존재하는 경우가 아님
        else:  # 키가 맨앞에 위치하는데 부모노드에 키가 존재하지않고 더 상위 노드에 지우고자 하는 키값이 존재하는경우

            if (node_counter - 1 >= check_minimum):
                # 삭제하려는 노드에서 삭제가 가능할때임, 삭제하려는 키값은 상위 노드에 존재하는 것을 찾아서 알맞게 지워주자.
                inin = node.m.index(key)

                node.m.remove(key)  # 해당 되는 키값 삭제
                node.value.pop(inin)  # 해당 되는 키값에 해당하는 value삭제

                # 부모 노드에서의 키값을 수정해주어야 함
                jkjk = node2
                # print("너와나 지금 여기")
                if key in jkjk.m:  # 삭제하려는 키값이 자식 노드의 첫번째 값이었지만 부모 노드에 존재 하지 않을수도 있어서 놔둔거임
                    gosibling_1 = self.find(jkjk, key)  # 부모 노드에서 해당 키값을 가리키는 키값의 인덱스 찾기위해 진행
                    goindex_1 = jkjk.value.index(gosibling_1)  # 부모노드에서 우리가 조정하고 싶은 키값을 찾아낸거임
                    mmm = jkjk.m[goindex_1 - 1]  # 그후 찾아낸 인덱스에 맞는 부모노드의 키값을 지정해주고

                    jkjk.m[goindex_1 - 1] = node.m[0]  # 바뀐 자식 노드의 첫 key값을 바껴야 할 부모 노드의 키값으로 변경~


            else:  # 이상태는 내가 있는 노드를 삭제하기 힘든 상황이어서, 형제노드에서 빌림, 무조건
                # 부모 노드에 키값이 있는게 아니라 빌릴수 없는 상황은 존재하지 않을것
                ok_left = 0
                ok_right = 0
                # 우선 삭제하려는 노드의 양쪽 노드가 존재 하는지 안하는지 부터 살펴보자!........후
                if left_t != None:
                    ok_left = 1  # 1 이라는 숫자의 의미는 해당 되는 형제 노드가 존재함을 의미한다.
                if right_t != None:
                    ok_right = 1
                # 왼쪽 형제와 오른쪽 형제 노드가 빌려줄수 있는 상황인지 판단해보자.
                ok_left_borrow = 0
                ok_right_borrow = 0
                if ok_left == 1:
                    if len(left_t.m) - 1 >= check_minimum:
                        ok_left_borrow = 1
                if ok_right == 1:
                    if len(right_t.m) - 1 >= check_minimum:
                        ok_right_borrow = 1

                if ok_left_borrow == 1:  # 왼쪽 형제 에게서 빌려올수 있음,우선 현재 리프 노드일 경우임
                    # 빌려올 왼쪽 노드와 부모노드 키값을 조정하는 과정
                    # print("너와나 지금 left borrow")
                    self.borrow_left_leaf(left_t, node, node.parent, key)
                    if node.parent != node2:
                        jkjk = node2
                        if key in jkjk.m:  # 삭제하려는 키값이 자식 노드의 첫번째 값이었지만 부모 노드에 존재 하지 않을수도 있어서 놔둔거임
                            gosibling_1 = self.find(jkjk, key)  # 부모 노드에서 해당 키값을 가리키는 키값의 인덱스 찾기위해 진행
                            goindex_1 = jkjk.value.index(gosibling_1)  # 부모노드에서 우리가 조정하고 싶은 키값을 찾아낸거임
                            mmm = jkjk.m[goindex_1 - 1]  # 그후 찾아낸 인덱스에 맞는 부모노드의 키값을 지정해주고

                            jkjk.m[goindex_1 - 1] = node.m[0]  # 바뀐 자식 노드의 첫 key값을 바껴야 할 부모 노드의 키값으로 변경~


                elif ok_right_borrow == 1:

                    # 오른쪽 형제에게서 키를 빌려올수 있는경우를 의미
                    self.borrow_right_leaf(right_t, node, node.parent, key)
                    # print("너와나 지금 right borrow")
                    if node.parent != node2:
                        jkjk = node2

                        if key in jkjk.m:  # 삭제하려는 키값이 자식 노드의 첫번째 값이었지만 부모 노드에 존재 하지 않을수도 있어서 놔둔거임
                            gosibling_1 = self.find(jkjk, key)  # 부모 노드에서 해당 키값을 가리키는 키값의 인덱스 찾기위해 진행
                            goindex_1 = jkjk.value.index(gosibling_1)  # 부모노드에서 우리가 조정하고 싶은 키값을 찾아낸거임
                            mmm = jkjk.m[goindex_1 - 1]  # 그후 찾아낸 인덱스에 맞는 부모노드의 키값을 지정해주고
                            jkjk.m[goindex_1 - 1] = node.m[0]  # 바뀐 자식 노드의 첫 key값을 바껴야 할 부모 노드의 키값으로 변경~


                elif ok_right_borrow == 0 or ok_left_borrow == 0:

                    if ok_left == 1:  # 왼쪽 노드와 병함
                        kij = self.merge_left_leaf(left_t, node, node.parent, key)
                    elif ok_right == 1:  # 오른쪽 노드와 병합
                        kij = self.merge_right_leaf(right_t, node, node.parent, key)
                        # intex = node2.m.index(key)
                        # node2.m[intex] = kij  # 내부 노드 키값 변경 시켜줌
        # 여기서 상황을 봐서 노드의 borrow, node의 merge을 해야할것을 정해야 함
        # 쭉쭉 위로 올라가자!
        node = node.parent
        if node == None:
            return
        while (len(node.m) < (math.ceil(node.degree / 2) - 1) or len(node.value) < (len(node.m) + 1)):
            if node == self.root or node == None:  # 루트 노드일때는 다르게 처리
                break
            else:
                angel = node.parent
                if (len(node.m)) == 0:  # 차수가 낮을때는 그냥 지워져 버리면 비어 있는 상황도 존재
                    key = angel.value.index(node)  # 현재 노드를 가리키고 있는 포인터를 알아냄
                    goindex = key

                else:
                    key = node.m[0]
                    gosibling = self.find(angel, key)
                    goindex = angel.value.index(gosibling)  # 형제 노드 찾기 위한 인덱스부터 설정 , 우선 부모노드에서 나부터 설정 하는거로

                left_index = goindex - 1
                right_index = goindex + 1

                # 형제 노드는 부모 노드를 통해서만 찾아야 함! 그게 형제임
                right_t = None
                left_t = None
                # key값이 있는 노드의 왼쪽과 오른쪽노드를 찾았으니
                # 찾아낸 인덱스가 부모노드가 가진 인덱스를 넘어섰을수도 있음!
                # 그거 판별하자
                if left_index >= 0 and left_index <= len(node.parent.value):
                    left_t = node.parent.value[left_index]

                if right_index >= 0 and right_index > left_index and right_index <= len(node.parent.value) - 1:
                    right_t = node.parent.value[right_index]

                node_counter = len(node.m)
                check_minimum = math.ceil(node.degree / 2) - 1

                ok_left = 0
                ok_right = 0
                # 우선 삭제하려는 노드의 양쪽 노드가 존재 하는지 안하는지 부터 살펴보자!........후
                if left_t != None:
                    ok_left = 1  # 1 이라는 숫자의 의미는 해당 되는 형제 노드가 존재함을 의미한다.
                if right_t != None:
                    ok_right = 1
                # 왼쪽 형제와 오른쪽 형제 노드가 빌려줄수 있는 상황인지 판단해보자.
                ok_left_borrow = 0
                ok_right_borrow = 0
                if ok_left == 1:
                    if len(left_t.m) - 1 >= check_minimum:
                        ok_left_borrow = 1
                if ok_right == 1:
                    if len(right_t.m) - 1 >= check_minimum:
                        ok_right_borrow = 1

                if ok_left_borrow == 1:  # 왼쪽 형제 에게서 빌려올수 있음,우선 현재 리프 노드일 경우임
                    # 빌려올 왼쪽 노드와 부모노드 키값을 조정하는 과정
                    self.borrow_left_node(left_t, node, node.parent)
                elif ok_right_borrow == 1:
                    # 오른쪽 형제에게서 키를 빌려올수 있는경우를 의미
                    self.borrow_right_node(right_t, node, node.parent)

                elif ok_right_borrow == 0 or ok_left_borrow == 0:
                    if ok_left == 1:  # 왼쪽 노드와 병함
                        # print("merge left")
                        hi = self.merge_left_node(left_t, node, node.parent)
                        node = hi  # 리턴시 이제 node는 없어졌으니 바뀐 왼쪽노드가 node가 됨

                    elif ok_right == 1:  # 오른쪽 노드와 병합
                        hi = self.merge_right_node(right_t, node, node.parent)
                        node = hi
            if node == self.root or node == None:  # 루트 노드일때는 다르게 처리
                break
            node = node.parent  # 부모노드로 올려버려~

    def find(self, ro, fin):  # 노드, 키값: 주어진 값에 따라 알맞은 곳을 찾아나가는 과정
        nj = ro.m  # ni는 찾고자 하는 노드가 입력이 되는 상황입니다.
        ni = ro.value
        tag = 0
        for i in nj:
            if fin < i:  # 탐색시 작지 않으면 다음 인덱스로 가서 탐색
                return ni[tag]
            tag = tag + 1
        if tag == len(nj):  # 지금 이제 더이상 찾을수 없음
            # 즉 현재 노드에 있는 값보다 입력된 키값이 더큰경우임
            return ni[tag]  # 해당되는 리프노드의 리스트 리턴시켜줌

    def find_internal(self, ro, fin):  # 찾고자 하는 키값이 내부인터널 노드에 존재하는지 탐색하는 함수.
        while (True):
            if type(ro) == LEAFNODE:
                return None
            if fin in ro.m:
                return ro
            else:
                tag = 0
                for i in ro.m:
                    if fin < i:  # 중복값은 입력이 되지 않으니 <= 으로 하지 말자, 작지 않으면 다음 인덱스로 가서 탐색
                        # 작아야 오름차순으로 들어갈 자리가 정해지니 이렇게 해야함.
                        ro = ro.value[tag]
                        return ro
                    tag = tag + 1
                if tag == len(ro.m):  # 지금 이제 더이상 찾을수 없음
                    # 즉 현재 노드에 있는 값보다 입력된 키값이 더큰경우임
                    ro = ro.value[tag]  # 해당되는 리프노드의 리스트 리턴시켜줌
                    return ro

    def singlesearch_key(self, key):
        node_s = self.root
        while type(node_s) != LEAFNODE:
            ican = self.find(node_s, key)
            node_s = ican

        if key in node_s.m:  # 키가있음을 알림
            return 1
        else:
            return 0

    def singlesearch(self, key):
        node_s = self.root
        ghgh = []
        ghgh.append(node_s)
        while type(node_s) != LEAFNODE:
            ican = self.find(node_s, key)
            ghgh.append(ican)
            node_s = ican
        ghgh.pop(-1)
        ghgh_1 = []
        for i in ghgh:
            for j in i.m:
                ghgh_1.append(j)
        for i in ghgh_1:
            if i == ghgh_1[-1]:
                print("{0}".format(i), end="")
            else:
                print("{0}".format(i), end=",")
        print()
        if key in node_s.m:
            jk = node_s.m.index(key)
            jks = (node_s.value[jk])
            print("{0}".format(*jks))
        else:
            print("NOT FOUND")

    def rangesearch(self, start, end):
        node_s = self.root
        ghgh = []

        while type(node_s) != LEAFNODE:
            ican = self.find(node_s, start)
            ghgh.append(ican)
            node_s = ican
        node_s1 = self.root
        ghgh = []
        while type(node_s1) != LEAFNODE:
            ican = self.find(node_s1, end)
            ghgh.append(ican)
            node_s1 = ican
        if node_s == node_s1:
            for i in range(0, len(node_s.m)):
                if node_s.m[i] >= start and node_s.m[i] <= end:
                    print("{0},{1}".format(node_s.m[i], *node_s.value[i]))
        else:
            while node_s != node_s1:
                for i in range(0, len(node_s.m)):
                    if node_s.m[i] >= start:
                        print("{0},{1}".format(node_s.m[i], *node_s.value[i]))
                node_s = node_s.right
            for i in range(0, len(node_s1.m)):
                if node_s.m[i] <= end:
                    print("{0},{1}".format(node_s.m[i], *node_s.value[i]))


# 걍 다 저장해보려고 함
get = sys.argv[1]
dat = sys.argv[2]
fourth = sys.argv[3]
if get == "-c":
    with open(dat, 'w') as file:
        file.write('{0}\n'.format(fourth))
elif get == "-i":
    with open(dat, 'r') as f:
        line = f.readline()
        line = line.split()  # 차수입력
        b = plustree(int(line[0]))
        while 1:
            read = f.readline()
            if not read:
                break
            else:
                read = read.split()
                if read[0] == "i":
                    test = b.singlesearch_key(int(read[1]))
                    if test == 0:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                        b.insert(int(read[1]), int(read[2]))
                elif read[0] == "d":
                    test = b.singlesearch_key(int(read[1]))
                    if test == 1:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                        # duplicate.append(j)
                        b.delete(int(read[1]))
        string = []
        with open(fourth, 'r') as file:
            read = csv.reader(file, delimiter=',')
            for row in read:
                test = b.singlesearch_key(int(row[0]))
                if test == 0:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                    # duplicate.append(j)
                    b.insert(int(row[0]), int(row[1]))
                    string.append('i {0} {1}\n'.format(row[0], row[1]))

        with open(dat, 'a') as file:
            for i in string:
                file.write(i)

elif get == "-d":
    with open(dat, 'r') as f:
        line = f.readline()
        line = line.split()  # 차수입력
        b = plustree(int(line[0]))

        while 1:
            read = f.readline()
            if not read:
                break
            else:
                read = read.split()
                if read[0] == "i":
                    test = b.singlesearch_key(int(read[1]))
                    if test == 0:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                        b.insert(int(read[1]), int(read[2]))
                elif read[0] == "d":
                    test = b.singlesearch_key(int(read[1]))
                    if test == 1:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                        b.delete(int(read[1]))
        string = []
        with open(fourth, 'r') as file:
            read = csv.reader(file, delimiter=',')
            for row in read:
                test = b.singlesearch_key(int(row[0]))
                if test == 1:  # 이미 들어가 있는 키가 있으니 삭제가 가능함
                    # duplicate.append(j)

                    b.delete(int(row[0]))
                    string.append('d {0}\n'.format(row[0]))
        with open(dat, 'a') as file:
            for i in string:
                file.write(i)
elif get == "-s":
    with open(dat, 'r') as f:
        line = f.readline()
        line = line.split()  # 차수입력
        b = plustree(int(line[0]))
        while 1:
            read = f.readline()
            if not read:
                break
            else:
                read = read.split()
                if read[0] == "i":

                    test = b.singlesearch_key(int(read[1]))
                    if test == 0:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                        # duplicate.append(j)
                        b.insert(int(read[1]), int(read[2]))
                elif read[0] == "d":
                    test = b.singlesearch_key(int(read[1]))
                    if test == 1:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                        b.delete(int(read[1]))
        b.singlesearch(int(fourth))

elif get == "-r":
    fifth = sys.argv[4]
    with open(dat, 'r') as f:
        line = f.readline()
        line = line.split()  # 차수입력
        b = plustree(int(line[0]))
        while 1:
            read = f.readline()
            if not read:
                break
            else:
                read = read.split()
                if read[0] == "i":
                    test = b.singlesearch_key(int(read[1]))
                    if test == 0:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                        # duplicate.append(j)
                        b.insert(int(read[1]), int(read[2]))
                elif read[0] == "d":
                    test = b.singlesearch_key(int(read[1]))
                    if test == 1:  # 이미 들어가 있는 키가 없으니 삽입이 가능함
                        b.delete(int(read[1]))
        b.rangesearch(int(fourth), int(fifth))
