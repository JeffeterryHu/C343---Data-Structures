from stack import ArrayStack

class BSTNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = None
        
    def msmall(self):
        if self.left != None:
            return self.left.msmall()
        else:
            return self
        
    def msmall2(self):
        if self.right != None:
            return self.right.msmall2()
        else:
            return self
        
    def l_successor(self):
        if self.parent != None:
            if self == self.parent.left:
                return self.parent
            else:
                self.parent.l_successor()
        else:
            return self
        
    def l_predecessor(self):
        if self.parent != None:
            if self == self.parent.right:
                return self.parent
            else:
                self.parent.l_predecessor()
        else:
            return self
            
def less_than(x,y):
    return x < y

class BinarySearchTree:
    def __init__(self, root = None, less=less_than):
        self.root = root
        self.parents = True
        self.less = less

    # takes value, returns node with key value
    def insert(self, k):
        if self.root == None:
            third_node = BSTNode(k)
            self.root = third_node
        elif k <= self.root.key:
            if self.root.left != None:
                self.root.left.insert(k)
            else:
                first_node = BSTNode(k)
                self.root.left = first_node
                first_node.parent = self.root
        else:
            if self.root.right != None:
                self.root.right.insert(k)
            else:
                second_node = BSTNode(k)
                self.root.right = second_node
                second_node.parent = self.root
            

    # takes node, returns node
    # return the node with the smallest key greater than n.key
    def successor(self, n):
        if n.right != None:
            return n.right.msmall()
        else:
            return n.l_successor()

    # return the node with the largest key smaller than n.key
    def predecessor(self, n):
        if n.left != None:
            return n.left.msmall2()
        else:
            return n.l_predecessor()

    # takes key returns node
    # can return None
    def search(self, k):
        if self.root.key == k:
            return self.root
        elif self.root.key < k:
            if self.root.left != None:
                self.root.left.search(k)
            else:
                return None
        else:
            if self.root.right != None:
                self.root.right.search(k)
            else:
                return None
            
    # takes node, returns node
    def delete_node(self, n):
        if self.left == None and self.right == None:
            if self.parent == None:
                return self
            elif self.parent.right == self:
                self.parent.right = None
                self.parent = None
                return self
            else:
                self.parent.left = None
                self.parent = None
                return self

