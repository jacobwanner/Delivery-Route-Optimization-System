# Citing source: WGU C950 - Webinar-1 - Let's Go Hashing
# W-1_ChainingHashTable_zyBooks_Key-Value.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.

# Create Hash Map class
class CreateHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table
    def insert(self, key, value):  # does both insert and update
        # get the bucket list where this item will go.
        cell = hash(key) % len(self.table)
        cell_list = self.table[cell]

        # update key if it is already in the cell
        for kv in cell_list:  # O(N) CPU time
            # print (key_value)
            if kv[0] == key:
                kv[1] = value
                return True

        # if not, insert the item to the end of the cell list
        key_value = [key, value]
        cell_list.append(key_value)
        return True

    # Lookup values in hash table and returns it if found. (None if not found)
    def search(self, key):
        cell = hash(key) % len(self.table)
        cell_list = self.table[cell]

        #search for the key in cell list
        for kv in cell_list:
            if key == kv[0]:
                return kv[1]
        return None

    # Removes item from hash table
    def remove(self, key):
        cell = hash(key) % len(self.table)
        cell_list = self.table[cell]

        # If the key is found in the hash table then remove the value
        for kv in cell_list:
            if kv[0] == key:
                cell_list.remove([kv[0], kv[1]])