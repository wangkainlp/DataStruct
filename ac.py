#coding:utf-8
import sys
import trie
from trie import DAT

class AC:
    def __init__(self):
        items, wordMap, id2WordMap = trie.getItems()
        print 'item size:', len(items)
        print 'word size:', len(wordMap)
        # for k, v in wordMap.items():
        #     print k.encode('utf-8'), v
        print items[0].encode('utf-8'), wordMap[items[0][0]]
        print items[1].encode('utf-8'), wordMap[items[1][0]]

        self.items = items
        self.wordMap = wordMap
        self.id2WordMap = id2WordMap

        self.dat = None


    def buildGoto(self):

        self.dat = DAT(self.items, self.wordMap, self.id2WordMap)
        self.dat.build()

    def buildFailure(self):

        self.f = [ 0 ] * self.dat.size
        pass

        depth = 0 

        parent = [ 0 ]
        children = []
        for p in parent:
            _children = self.getChildren(p)
            print _children
            children += _children
        depth += 1
        for i in children:
            self.f[i] = 0
        print children
        print ' '.join([ '%2d' % (it) for it in self.f ])

        parent = children

        # return None

        # while depth <= 2:
        while True:
            print 'failure depth:', depth
            children = []
            for p in parent:
                _children = self.getChildren(p)
                children += _children
                print _children

            if len(children) <= 0:
                break

            for c in children:
                cw = self.dat.state[c]
                for p in parent:
                    n = self.g(p, cw)
                    if n[0] == False:
                        continue
                    else:
                        st = self.f[p]
                        while self.g(st, cw)[0] == False:
                            st = self.f[st]
                        self.f[c] = self.g(st, cw)[1]
                        print 'failure:'
                        print ' '.join([ '%2d' % (it) for it in self.f ])

            '''
            for c in children:
                for p in parent:
                    for w in self.wordMap:
                        n = self.g(p, w)
                        if n[0] == False:
                            continue
                        else:
                            if n[1] != c:
                                # print 'error', p, ':', self.dat.state[p].encode('utf-8'), ' + ', w.encode('utf-8'), ' -> ', c, ' != ', n[1]
                                continue
                            # print 'error', p, ':', self.dat.state[p].encode('utf-8'), ' + ', w.encode('utf-8'), ' -> ', c, ' != ', n[1]

                            st = self.f[p]
                            while self.g(st, w)[0] == False:
                                st = self.f[st]
                            self.f[c] = self.g(st, w)[1]
                            print 'failure:'
                            print ' '.join([ '%2d' % (it) for it in self.f ])
            '''

            parent = children
            depth += 1

        print ' '.join([ '%3d' % (i) for i in range(self.dat.size) ])
        print ' '.join([ '%3d' % (it) for it in self.dat.base ])
        print ' '.join([ '%3d' % (it) for it in self.dat.check ])
        # print ' '.join([ '   ' + (it.encode('utf-8') if it != u'\0' else '++') for it in self.dat.state ][:self.dat.size])
        print ' '.join([ ' ' + ('' + it.encode('utf-8') if it != u'\0' else '++') for it in self.dat.state ][:self.dat.size])
        print ' '.join([ '%3d' % (it) for it in self.f ])

    def g(self, r, a):
        if a not in self.wordMap:
            if r == 0:
                return True, 0
            else:
                return False, None

        p = self.dat.base[r] + self.wordMap[a] + 1
        if self.dat.check[p] != 0 and self.dat.check[p] == self.dat.base[r]:
            # print self.dat.base[r], '+', self.wordMap[a], '+ 1'
            return True, p
        else:
            if r == 0:
                return True, 0
            else:
                return False, None


    def getChildren(self, pidx):
        children = []

        b = self.dat.base[pidx]
        for i in range(self.dat.size):
            if self.dat.check[i] == b:
                children.append(i)

        return children

    def search(self, q):
        print 'search:', q.encode('utf-8')
        rs = []
        idx = 0
        fidx = 0
        print idx
        for i, w in enumerate(q):
            ret = self.g(idx, w)
            if ret[0] == True:
                idx = ret[1]
            else:
                while ret[0] == False:
                    idx = self.f[idx]
                    # print idx
                    ret = self.g(idx, w)
                    '''
                    if ret[1] == None:
                        break
                    '''
                idx = ret[1]
                # if ret[1] != None:
                #     idx = ret[1]

            idx0 = self.dat.base[idx] + 0 + 1
            if self.dat.base[idx0] < 0 and self.dat.check[idx0] == self.dat.base[idx]:
                rs.append(self.items[ -self.dat.base[idx0] - 1 ])

            # output
            _idx = self.f[idx]
            while _idx != 0:
                idx0 = self.dat.base[_idx] + 0 + 1
                if self.dat.base[idx0] < 0 and self.dat.check[idx0] == self.dat.base[_idx]:
                    rs.append(self.items[ -self.dat.base[idx0] - 1 ])
                _idx = self.f[_idx]



            print idx, i, idx0

        '''
        idx0 = self.dat.base[idx] + 0 + 1
        if self.dat.base[idx0] < 0 and self.dat.check[idx0] == self.dat.base[idx]:
            rs.append(self.items[ -self.dat.base[idx0] - 1 ])
        '''


        return rs



if __name__ == '__main__':
    ac = AC()

    print 'build goto'
    ac.buildGoto()

    print 'build failure'
    ac.buildFailure()

    # rs = ac.search(u'熟鸡蛋壳')
    # rs = ac.search(u'清华大学')
    # rs = ac.search(u'ushers')
    rs = ac.search(u'she')

    print len(rs)
    for i in rs:
        print i.encode('utf-8')



