# Zackery Ayscue 000901676

# HashTable class using chaining.
class ChainingHashTable(object):
    # Constructor with optional inital capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, inital_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(inital_capacity):
            self.table.append([])
    
    # Inserts a new item into the hash table.
    def insert(self, item):
        # get the bucket list where this item will go.
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]

        # insert the item to the end of the bucket list.
        bucket_list.append(item)

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        if key in bucket_list:
            # find the item's index and return the item that is in the bucket list.
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            # the key is not found.
            return None

    # Remove an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        if key in bucket_list:
            bucket_list.remove(key)

    # Overloaded string conversion method to create a string
    # representation of the entire hash table. Each bucket is shown
    # as a pointer to a list object.
    def __str__(self):
        index = 0
        s =  "   --------\n"
        for bucket in self.table:
            s += "%2d:|   ---|-->%s\n" % (index, bucket)
            index += 1
        s += "   --------"
        return s