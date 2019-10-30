#coding:utf-8
import sys

def getItems():
    items = []
    filename = 'ori_item.m'
    filename = 'ori_item'
    filename = 'name'
    with open(filename) as fp:
        for line in fp:
            line = line.strip('\n')
            it = line.decode('utf-8') + u'\0'
            items.append(it)

    wordMap = {}
    id2WordMap = {}
    idx = 10
    idx = 1
    for it in items:
        # print it.encode('utf-8')
        for w in it:
            if w not in wordMap:
                idx += 1
                wordMap[w] = idx
                id2WordMap[idx] = w

    items = sorted(items, cmp=lambda x, y: _cmp(x, y, wordMap))

    wordMap[u' '] = 1
    id2WordMap[1] = u' '

    wordMap[u'\0'] = 0
    id2WordMap[0] = u'\0'
    return items, wordMap, id2WordMap
    
def _cmp(A, B, wordMap):
    minLen = min(len(A), len(B))
    for i in range(minLen):
        if wordMap[A[i]] > wordMap[B[i]]:
            return 1
        elif wordMap[A[i]] < wordMap[B[i]]:
            return -1

    if len(A) > len(B):
        return 1
    elif len(A) < len(B):
        return -1
    else: 
        return 0


class Node:
    def __init__(self, code, depth, left, right, items):
        self.depth = depth
        self.left = left
        self.right = right
        self.items = items
        self.code = code

class DAT:
    def __init__(self, items, wordMap, id2WordMap):
        # self.size = 100000
        self.size = 10
        self.base  = [0] * self.size
        self.check = [0] * self.size
        self.state = ['__'] * self.size

        self.base[0] = 1
        self.check[0] = 0

        self.nextPos = 1
        self.used = [False] * self.size

        self.items = items
        self.wordMap = wordMap
        self.id2WordMap = id2WordMap

        self.progress = 0

    def resize(self, size):
        print 'resize:', self.size, size
        self.base += [0] * (size - self.size)
        self.check += [0] * (size - self.size)
        self.state += ['__'] * (size - self.size)
        self.used += [False] * (size - self.size)

        self.size = size


    def fetchChildren(self, parent):

        children = []
        preCode = -1
        depth = parent.depth
        for i in range(parent.left, parent.right + 1):
            print parent.items[i].encode('utf-8')
            if len(parent.items[i]) <= depth:
                continue
            ch = parent.items[i][depth]
            # print len(self.wordMap)
            chCode = self.wordMap[ch]

            '''
            if preCode == -1:
                preCode = chCode
            elif preCode == chCode:
                continue
            '''

            if preCode != -1 and preCode == chCode:
                continue

            # node = Node(chCode, depth, i, i, parent.items)
            node = Node(chCode, depth + 1, i, i, parent.items)
            if len(children) > 0:
                children[-1].right = i - 1

            children.append(node)
            preCode = chCode

        if len(children) > 0:
            children[-1].right = parent.right

        if len(children) <= 0:
            print self.id2WordMap[parent.code].encode('utf-8'), '<--', 'null', depth
        else:
            print self.id2WordMap[parent.code].encode('utf-8'), '<--', ' '.join([ self.id2WordMap[it.code].encode('utf-8') for it in children ]), depth
        print '--------------'

        return children


    def insert(self, parent, children):

        if len(children) <= 0:
            return -1

        # pos = (children[0].code + 1 > self.nextPos ? children[0].code + 1 : nextPos) - 1
        pos = self.nextPos - 1
        '''
        pos = self.nextPos
        if children[0].code + 1 > self.nextPos:
            pos = children[0].code + 1
        pos -= 1
        '''

        flag = False
        first = True
        pos = 0
        while flag == False:
            pos += 1
            if self.used[pos] == True:
                continue

            if first == True:
                first = False
                self.nextPos = pos

            if self.size <= pos + children[-1].code + 1:
                print 'pos:', pos, pos + children[-1].code + 1
                self.resize( int(1.0 * len(self.items) / (self.progress + 1) * self.size) )

            flag = True
            for i in range(len(children)):
                if self.check[pos + children[i].code + 1] != 0:
                    flag = False

        begin = pos
        self.used[begin] = True
        # self.nextPos = begin

        print 'begin:', begin
        print 'insert:', parent.code, ':', self.id2WordMap[parent.code].encode('utf-8')
        for i in range(len(children)):
            print '\tinsert:', self.id2WordMap[children[i].code].encode('utf-8'), children[i].code
            self.check[begin + children[i].code + 1] = begin
            self.state[begin + children[i].code + 1] = self.id2WordMap[children[i].code]

        # print 'insert:', parent.code, ':', self.id2WordMap[parent.code].encode('utf-8')

        print ' '.join([ '%2d' % (i) for i in range(50) ])
        print ' '.join([ '%2d' % (it) for it in self.base[:50] ])
        print ' '.join([ '%2d' % (it) for it in self.check[:50] ])
        print ' '.join([ it.encode('utf-8') for it in self.state ][:50])


        for i in range(len(children)):
            _children = self.fetchChildren(children[i])
            if len(_children) <= 0:
                self.base[begin + children[i].code + 1] = -(children[i].left + 1)
                self.progress += 1
            else:
                _begin = self.insert(children[i], _children)
                if _begin > 0:
                    self.base[begin + children[i].code + 1] = _begin
                    print 'father base:', self.id2WordMap[children[i].code].encode('utf-8'), _begin
                else:
                    pass
                    print >> sys.stderr, 'error'

        return begin
    
    def build(self):
        depth = 0
        root = Node(self.wordMap[u' '], depth, 0, len(self.items) - 1, self.items)

        children = self.fetchChildren(root)

        print 'children:', len(children)

        '''
        for it in children:
            print it.code, self.id2WordMap[it.code].encode('utf-8')
        '''

        # '''
        for j in range(len(children)):
            print '----------------------'
            for i in range(children[j].left, children[j].right + 1):
                print self.items[i].encode('utf-8')
        # '''

        begin = self.insert(root, children)

        for it in self.items:
            print it.encode('utf-8')

        for k, v in self.wordMap.items():
            print k.encode('utf-8'), v

        print 'insert:'
        print ' '.join([ '%2d' % (i) for i in range(50) ])
        print ' '.join([ '%2d' % (it) for it in self.base[:50] ])
        print ' '.join([ '%2d' % (it) for it in self.check[:50] ])
        print ' '.join([ it.encode('utf-8') if it != u'\0' else '++' for it in self.state ][:50])





    def search(self, q):
        print 'search:', q.encode('utf-8')

        result = []

        n = 0
        m = n
        for w in q:
            # print n 
            b = self.base[n]
            print n, b
            if b < 0 and self.check[n + 0 + 1] == self.base[m]:
                result.append(-b - 1)

            m = n
            n = b + self.wordMap[w] + 1
            if b == self.check[n]:
                pass
            else:
                return result

        b = self.base[n]
        print n, b
        if b < 0 and self.check[n + 0] == self.base[m]:
            result.append(-b - 1)

        return result

    def commonSearch(self, q):
        print 'search:', q.encode('utf-8')

        result = []

        b = self.base[0]
        p = b
        for w in q:
            p = b
            idx0 = b + 0 + 1
            if self.base[idx0] < 0 and self.check[idx0] == b:
                result.append(-self.base[idx0] - 1)
                print w.encode('utf-8'), -self.base[idx0] - 1, b

            idxn = b + self.wordMap[w] + 1
            if b == self.check[idxn]:
                b = self.base[idxn]
            else:
                return result

        idx0 = b + 0 + 1
        if self.base[idx0] < 0 and self.check[idx0] == b:
            result.append(-self.base[idx0] - 1)

        return result

    def dump(self):

        print ' '.join([ '%5d' % (i) for i in range(self.size) ])
        print ' '.join([ '%5d' % (it) for it in self.base[:self.size] ])
        print ' '.join([ '%5d' % (it) for it in self.check[:self.size] ])
        print ' '.join([ '   ' + (it.encode('utf-8') if it != u'\0' else '++') for it in self.state ][:self.size])

if __name__ == '__main__': 

    items, wordMap, id2WordMap = getItems()
    print 'item size:', len(items)
    print 'word size:', len(wordMap)

    for k, v in wordMap.items():
        print k.encode('utf-8'), v

    print items[0].encode('utf-8'), wordMap[items[0][0]]
    print items[1].encode('utf-8'), wordMap[items[1][0]]

    dat = DAT(items, wordMap, id2WordMap)
    dat.build()

    q = u'清华大学'
    q = u'调料包'

    rs = dat.commonSearch(q)

    dat.dump()

    print rs
    for i in rs:
        print items[i].encode('utf-8')

