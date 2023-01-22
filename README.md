# Hash-Map

## SCHashMap.py
To implement the Hash Map we use a dynamic array to store our hash table,and
implement chaining for collision resolution using a singly linked list using the following methods:

### 1. put()
Method updates the key/value pair in the hash map.
If given key already exists in the hash map,
associated value is replaced with the new value.
If given key is not in the hash map, new key/value pair is added

### 2. get()
Method returns the value associated with the given key. 
If the key is not in the hash map, the method returns None.

### 3. remove()
Method removes the given key and its associated value from the hash map. If the key
is not in the hash map, the method does nothing

### 4. contains_key()
Method returns True if the given key is in the hash map, 
otherwise it returns False. An empty hash map does not contain any keys.

### 5. clear()
Method clears the contents of the hash map. 
It does not change the underlying hash map capacity.

### 6. empty_buckets()
Method returns the number of empty buckets in the hash table.

### 7. resize_table()
Method changes the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map, and all hash table links must be rehashed.

### 8. table_load()
Method returns the current hash table load factor.

### 9. get_keys()
Method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter.

## 10. find_mode()
Implemented a standalone function "find_mode()" outside of the HashMap class
that receives a dynamic array (that is not guaranteed to be sorted).
This function will return a tuple containing, in this order,
a dynamic array comprising the mode (most occurring) value/s of the array,
and an integer that represents the highest frequency (how many times they appear).

## OAHashMap.py
To implement the Hash Map we use a dynamic array to store our hash table,and
implement open addressing with Quadratic Probing for collision resolution inside that dynamic array. Key/Value pairs must be stored in the array.
Implementation will include the following methods:

### 1. put()
Method updates the key/value pair in the hash map.
If given key already exists in hash map, 
its associated value will be replaced with the new value.
If the given key is not in the hash map, a new key/value pair will be added.

### 1. get()
Method returns the value associated with the given key. If the key is not in the hash map, the method returns None.

### 2. remove()
Method removes the given key and its associated value from the hash map. If the key
is not in the hash map, the method does nothing (no exception needs to be raised).

### 3. contains_key()
Method returns True if the given key is in the hash map, otherwise it returns False.

### 4. clear()
Method clears the contents of the hash map. It does not change the underlying hash table capacity.

### 5. empty_buckets()
Method returns the number of empty buckets in the hash table.

### 6. resize_table()
Method changes the capacity of the internal hash table. All existing key/value pairs remain in the new hash map, and all hash table links are rehashed.

### 7. table_load()
Method returns the current hash table load factor.

### 8. get_keys()
Method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter.

### 9. __iter__()
Method enables the hash map to iterate across itself.

### 10. __next__()
Method will return the next item in the hash map, based on the current location of the iterator
