# worked with friends

class Hashtable:
    def __init__(self, dic, setSize = 2):
        self.used = 0
        self.size = setSize
        self.slots = [ [] for x in range(0, self.size)]
        for key in dic:
            self[key] = dic[key]

    def __getitem__(self, key):
        hashSlot = self.h(key)
        for pair in self.slots[hashSlot]:
            pKey = pair[0]
            if pKey == key:
                return pair[1]
        return None

    def __setitem__(self, key, value):
        self.slots[self.h(key)].append((key,value))
        self.used += 1
        if (self.used * 2) >= self.size:
            self.tableDouble()


    def __delitem__(self, key):
        hashSlot = self.slots[self.h(key)]
        print 'hashSlot length: ' + str(len(hashSlot))
        worked = False
        for i in range(0, len(hashSlot)):
            print i
            pair = hashSlot[i]
            if key == pair[0]:
                hashSlot.pop(i)
                used -= 1
                worked = True
        if used < (.25 * self.size):
            self.tableHalf()
        return worked



    def keys(self):
        ls = []
        for s in self.slots:
            for pair in s:
                ls.append(pair[0])
        return ls

    def h(self, key):
        return ord(key) % self.size

    def countKeys(self):
        count = 0
        for s in slots:
            for pair in s:
                count += 1
        return count

    def tableDouble(self):
        newTable = Hashtable({}, self.size*2)
        for key in self.keys():
            newTable[key] = self[key]
        self = newTable

    def tableHalf(self):
        self.size /= 2
        newSlots = [ [] for x in range(0, self.size)]
        for key in self.keys():
            newSlots[self.h(key)].append((key, value))
        self.slots = newSlots

