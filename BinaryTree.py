#coding:utf-8
import numpy as np


class Node:
    def __init__(self):
        self.value = float(np.inf)
        self.left = None
        self.right = None
        self.color = None
        self.parent = None

def insert(root, value):

    p = root
    f = None
    while p != None:
        f = p
        if value < p.value:
            p = p.left
        elif value > p.value:
            p = p.right
        else:
            return

    add = Node()
    add.parent = f
    add.value = value

    if f == None:
        root = add
    elif value < f.value:
        f.left = add
    else:
        f.right = add

    add.left = None
    add.right = None
    add.color = "R"
    insert_fixup(root, add)

def insert_fixup(root, add):



def traverse(root):

    if root != None:
        traverse(root.left)
        print root.value,
        traverse(root.right)




if __name__ == "__main__":

    root = Node()
    root.value = 5
    root.color = "B"

    insert(root, 9)
    insert(root, 3)
    insert(root, 3)
    insert(root, 8)

    print "done"

    traverse(root)
    print ""
