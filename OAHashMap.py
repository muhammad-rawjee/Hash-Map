# Name: Muhammad Ali Rawjee
# OSU Email: rawjeem@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/04/2022
# Description: Implement a HashMap using a dynamic array to store our hash table,
#              and Implement Open Addressing with Quadratic Probing for collision
#              resolution inside that dynamic array. key/value pairs must be stored in the array.
#              Implementation will include the following methods:
#
#              put()
#              get()
#              remove()
#              contains_key()
#              clear()
#              empty_buckets()
#              resize_table()
#              table_load()
#              get_keys()
#              __iter__(), __next__()

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
         Method updates the key/value pair in the hash map.
         If given key already exists in hash map, its associated value will be replaced with the new value.
         If the given key is not in the hash map, a new key/value pair will be added.
        """
        # Get load factor
        table_load = self.table_load()

        # Resize HashMap
        if table_load >= 0.5:
            self.resize_table(2 * self._capacity)

        # Calculate hash index
        hash_index = self._hash_function(key) % self._capacity

        # If bucket is None, insert
        if self._buckets[hash_index] is None:
            self._buckets[hash_index] = HashEntry(key, value)
            self._size += 1
        # If key values match and tombstone value is true
        elif self._buckets[hash_index].key == key and self._buckets[hash_index].is_tombstone:
            self._buckets[hash_index] = HashEntry(key, value)
            self._size += 1
        # If key values at bucket are the same, replace
        elif self._buckets[hash_index].key == key:
            self._buckets[hash_index] = HashEntry(key, value)
        # If buckets tombstone value is true
        elif self._buckets[hash_index].is_tombstone:
            self._buckets[hash_index] = HashEntry(key, value)
            self._size += 1
        # Start quadratic probing process, calculate new index
        else:
            count = 1
            quad_index = (hash_index + count**2) % self._capacity

            # Quadratic probe, till empty bucket is found, if found insert or replace accordingly
            while self._buckets[quad_index] is not None and count <= self._capacity:
                # If key values match and tombstone value is true
                if self._buckets[quad_index].key == key and self._buckets[quad_index].is_tombstone:
                    self._buckets[quad_index] = HashEntry(key, value)
                    self._size += 1
                    break
                # If key values at bucket are the same, replace
                elif self._buckets[quad_index].key == key:
                    self._buckets[quad_index] = HashEntry(key, value)
                    break
                # If buckets tombstone value is true
                elif self._buckets[quad_index].is_tombstone:
                    self._buckets[quad_index] = HashEntry(key, value)
                    self._size += 1
                    break

                # Recalculate quad index
                count += 1
                quad_index = (hash_index + count**2) % self._capacity

            # If there's an empty bucket, insert
            if self._buckets[quad_index] is None:
                self._buckets[quad_index] = HashEntry(key, value)
                self._size += 1

    def table_load(self) -> float:
        """
        Method returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets in the hash table.
        """
        num_empty_buckets = self._capacity - self._size
        return num_empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table. All existing key/value pairs
        remain in the new hash map, and all hash table links are rehashed.
        """
        # If new_capacity passed parameter is less than 1
        if new_capacity < 1 or new_capacity < self._size:
            return None

        # Save the buckets to re-enter later
        save_buckets = self._buckets

        # Empty bucket
        self._buckets = DynamicArray()
        self._size = 0
        potential_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity

        # Calculate new capacity value
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = potential_capacity

        # Fill up buckets with none (Reinitialize)
        for _ in range(self._capacity):
            self._buckets.append(None)

        # Add all values from save_buckets to self._buckets
        for i in range(save_buckets.length()):
            if save_buckets[i] is not None and save_buckets[i].is_tombstone is False:
                self.put(save_buckets[i].key, save_buckets[i].value)

    def get(self, key: str) -> object:
        """
         Method returns the value associated with the given key. If the key is not in the hash
         map, the method returns None.
        """
        # Calculate hash index
        hash_index = self._hash_function(key) % self._capacity

        # If bucket is empty
        if self._buckets[hash_index] is None:
            return None
        # If key at index matches, key param value and tombstone value is False
        elif self._buckets[hash_index].key == key and self._buckets[hash_index].is_tombstone is False:
            return self._buckets[hash_index].value

        # Start quadratic probing process, calculate new index
        count = 1
        quad_index = (hash_index + count**2) % self._capacity

        # Checks for first iteration of quad_index (Same as above)
        if self._buckets[quad_index] is None:
            return None
        elif self._buckets[quad_index].key == key and self._buckets[hash_index].is_tombstone is False:
            return self._buckets[quad_index].value

        # Loop till key value at quad index and key param match
        while self._buckets[quad_index].key != key and count <= self._capacity:
            # Recalculate index for quad probing
            count += 1
            quad_index = (hash_index + count**2) % self._capacity
            # If bucket at hash_index is empty
            if self._buckets[quad_index] is None:
                return None

        # Loop ends and either key values match or they don't
        if self._buckets[quad_index].key == key and self._buckets[quad_index].is_tombstone is False:
            return self._buckets[quad_index].value

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if the given key is in the hash map, otherwise it returns False.
        Function is almost identical to the one above
        """
        # Calculate hash index
        hash_index = self._hash_function(key) % self._capacity

        # If bucket is empty
        if self._buckets[hash_index] is None:
            return False
        elif self._buckets[hash_index].key == key:
            return True

        # Start quadratic probing process, calculate new index
        count = 1
        quad_index = (hash_index + count**2) % self._capacity

        # Checks for first iteration of quad_index (Same as above)
        if self._buckets[quad_index] is None:
            return False
        elif self._buckets[quad_index].key == key:
            return True

        # Loop till key value at quad index and key param match
        while self._buckets[quad_index].key != key and count <= self._capacity:
            count += 1
            quad_index = (hash_index + count ** 2) % self._capacity
            if self._buckets[quad_index] is None:
                return False

        # If key value at quad index and key param match return True
        if self._buckets[quad_index].key == key:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).
        """
        # Calculate hash index
        hash_index = self._hash_function(key) % self._capacity

        # If bucket is empty
        if self._buckets[hash_index] is None:
            return None
        # If match AND tombstone value is False, set tombstone value to True AND reduce self._size by one
        elif self._buckets[hash_index].key == key and self._buckets[hash_index].is_tombstone is False:
            self._buckets[hash_index].is_tombstone = True
            self._size -= 1
            return None
        # Start quadratic probing process, calculate quad index
        else:
            count = 1
            quad_index = (hash_index + count**2) % self._capacity
            # Iterate till empty bucket is found
            while self._buckets[quad_index] is not None and count <= self._capacity:
                # If key at quad_index matches param key AND tombstone value is False
                if self._buckets[quad_index].key == key and self._buckets[quad_index].is_tombstone is False:
                    self._buckets[quad_index].is_tombstone = True
                    self._size -= 1
                    return None
                # Re-calculate quad index
                count += 1
                quad_index = (hash_index + count ** 2) % self._capacity

            # If at the end of quadratic probing, empty bucket is found
            if self._buckets[quad_index] is None:
                return None

    def clear(self) -> None:
        """
        Method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        self._size = 0
        for i in range(self._capacity):
            self._buckets[i] = None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map. The order of the keys in the dynamic array does not matter.
        """
        # Initialize DynamicArray
        return_array = DynamicArray()

        # Iterate through bucket and if bucket is not Empty and tombstone value is False
        # Append to return_array
        for i in range(self._capacity):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                return_array.append((self._buckets[i].key, self._buckets[i].value))

        return return_array

    def __iter__(self):
        """
        Method enables the hash map to iterate across itself.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Method will return the next item in the hash map, based on the current location of the iterator
        """
        try:
            # If bucket at index is empty or tombstone value is True, move to next index
            while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone is True:
                self._index = self._index + 1

        except DynamicArrayException:
            raise StopIteration

        # Calculate next value in iterator
        next_value = self._buckets[self._index]
        # Move to Next index (avoid infinite loop)
        self._index = self._index + 1
        return next_value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)