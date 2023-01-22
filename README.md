# Hash-Map

## SCHashMap.py


To implement the Hash Map we Use a dynamic array to store our hash table,and
implement chaining for collision resolution using a singly linked list using the following methods:

### put()
Method updates the key/value pair in the hash map.
If given key already exists in the hash map,
associated value is replaced with the new value.
If given key is not in the hash map, new key/value pair is added

## get()
Method returns the value associated with the given key. 
If the key is not in the hash map, the method returns None.

## remove()
Method removes the given key and its associated value from the hash map. If the key
is not in the hash map, the method does nothing

## contains_key()
Method returns True if the given key is in the hash map, 
otherwise it returns False. An empty hash map does not contain any keys.

## clear()
Method clears the contents of the hash map. 
It does not change the underlying hash map capacity.

## empty_buckets()
Method returns the number of empty buckets in the hash table.

## resize_table()
Method changes the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map, and all hash table links must be rehashed.

## table_load()
Method returns the current hash table load factor.

## get_keys()
Method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter.