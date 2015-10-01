# AVL Trees, by Elizabeth Feicke

class AVLNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = None
        
        
    def height(n):
        if n:
            return 1 + max(height(n.left), height(n.right))
        else:
            return -1
        
    def balance(self):
        if self.right:
            x = height(self.right)
        else:
            x = -1
        if self.left:
            y = height(self.left)
        else:
            y = -1
        return (x - y)
    
    def r_left(self):
        x = self
        y = self.right
        stree = y.left
        
        self = y
        y.left = x
        x.right = stree
        
    def r_right(self):
        x = self
        y = self.left
        stree = y.right
        
        self = y
        y.right = x
        x.left = stree
    
    def sbalance(self):
        if not(self.balance()) in [-1,0,1]:
            if height(self.left) > height(self.right):
                if height(self.left.left) > height(self.left.right):
                    self.r_right()
                    if self.parent:
                        self.parent.sbalance()
                else:
                        self.left.r_left()
                        self.r_right()
                        if self.parent:
                            self.parent.sbalance()
                            if height(self.right) > height(self.left):
                                self.r_left()
                                if self.parent:
                                    self.parent.sbalance()
                            else:
                                self.right.r_right()
                                self.r_left()
                                if self.parent:
                                    self.parent.sbalance()
                                    


    def less_than(x,y):
        return x < y
    
    def g_ancestor(x):
        p = x.parent
        if p and x == p.right:
            return g_ancestor(p)
        else:
            return p
        

    def l_ancestor(x):
        p = x.parent
        if p and x == p.left:
            return l_ancestor(p)
        else:
            return p

    def transp(T, u, v):
        if not u.parent:
            T.root = v
            elif u == u.parent.left:
                u.parent.left = v
                else:
                    u.parent.right = v
                    if v:
                        v.parent = u.parent

class AVLTree:
    def __init__(self, root = None, less=less_than):
        self.root = root
        self.less = less

    # takes value, returns node with key value
    def insert(self, k):
        if self.root:
            n = self.internal_search(k)
            if less_than(n.key, k):
                n1 = AVLNode(k, None, n.right)
                n.right = n1
                n1.parent = n.right
            elif less_than(k, n.key):
                n1 = AVLNode(k, n.left, None)
                n.left = AVLNode(k, n.left, None)
                n1.parent = n
            n.sbalance()
            return n1
        else:
            self.root = AVLNode(k)
            return self.root

    # takes node, returns node
    # return the node with the smallest key greater than n.key
    def successor(self, n):
        if n.right:
            n = n.right
            n2 = n.left
            while n2:
                n = n2
                n2 = n.left
            return n
        elif n.parent == None:
            return None
        else:
            return g_ancestor(n)

    # return the node with the largest key smaller than n.key
    def predecessor(self, n):
        if n.left:
            n = n.left
            n2 = n.right
            while n2:
                n = n2
                n2 = n.right
            return n
        elif n.parent == None:
            return None
        else:
            return l_ancestor(n)
        

    # takes key returns node
    # can return None
    def search(self, k):
        n = self.internal_search(k)
        if n.key == k:
            return n
        else:
            return None
        
    def internal_search(self, k):
        n = self.root
        previous = n
        notFound = True
        while not(n == None) and notFound:
            if k == n.key:
                notFound = False
                return n
            elif less_than(k, n.key):
                previous = n
                n = n.left
            elif less_than(n.key, k):
                previous = n
                n = n.right
        if notFound:
            return previous
            
    # takes node, returns node
    def delete_node(self, n):
        if (n.left == None) and (n.right == None):
            if (n.parent.right == n):
                n.parent.right = None
            else:
                n.parent.left = None

        elif (n.left == None):
            r = n.right
            transp(AVLTree(n.right), n, r)
            r.sbalance()


        elif (n.right == None):
            r = n.left
            transp(AVLTree(n.left), n, r)
            r.sbalance()

        else:
            s = successor(n)
            transp(AVLTree(s,less_than), n, s)
            s.sbalance()

