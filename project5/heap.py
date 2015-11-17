from swap import swap

def less(x, y):
    return x < y

def less_key(x, y):
    return x.key < y.key

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * (i + 1)

def parent(i):
    return (i-1) / 2

# Student code -- fill in all the methods that have pass as the only statement
class Heap:
    def __init__(self, data, 
                 less = less):
        self.data = data
        self.less = less
        self.build_min_heap()
        
    def __repr__(self):
        return repr(self.data)
    
    def minimum(self):
        return self.data[0]

    def insert(self, obj):
        self.data.append(obj)
        self.build_min_heap()

    def extract_min(self):
        n = self.minimum()
        self.data.pop(0)
        self.build_min_heap()
        return n
        
    def min_heapify(self, i):
        n = len(self.data)
        
        if left(i) < n and self.less(self.data[left(i)],self.data[i]):
            mini = left(i)
        else:
            mini = i
        if right(i) < n and self.less(self.data[right(i)],self.data[i]):
            mini = right(i)
        if mini != i:
            swap(self.data,i,mini)
            self.min_heapify(mini)
    
    def build_min_heap(self):
        last_parent = (len(self.data)-1)
        for i in range(last_parent,-1,-1):
            self.min_heapify(i)
    
class PriorityQueue:
    def __init__(self, less=less_key):
        self.heap = Heap([], less)

    def __repr__(self):
        return repr(self.heap)

    def push(self, obj):
        self.heap.insert(obj)

    def pop(self):
        return self.heap.extract_min()

if __name__ == "__main__":
    # unit tests here
    heap = PriorityQueue(less)
    heap.push(6)
    heap.push(1)
    heap.push(3)
    heap.push(2)
    heap.push(4)
    print heap
    print heap.pop()
    # unit tests here
    print heap.pop()
    print heap