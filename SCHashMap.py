# Name: Muhammad Ali Rawjee
# OSU Email: rawjeem@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/04/2022
# Description: Implement a HashMap using a dynamic array to store our hash table,
#              and implement chaining for collision resolution using a singly linked list class .
#              Use a dynamic array to store our hash table,and implement chaining for
#              collision resolution using a singly linked list using the following methods:
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
#
#              Implemented a standalone function "find_mode()" outside of the HashMap class
#              that receives a dynamic array (that is not guaranteed to be sorted).
#              This function will return a tuple containing, in this order,
#              a dynamic array comprising the mode (most occurring) value/s of the array,
#              and an integer that represents the highest frequency (how many times they appear).


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
         If given key already exists in the hash map,
         associated value is replaced with the new value.
         If given key is not in the hash map, new key/value pair is added
        """
        # Get load factor
        load_factor = self.table_load()

        # Resize HashMap if load factor >= 1.0
        if load_factor >= 1.0:
            self.resize_table(2 * self._capacity)

        # Calculate hash_index
        hash_index = self._hash_function(key) % self._capacity
        # Get linked list at that hash_index
        curr_linked_list = self._buckets[hash_index]

        # If key is already in linked list, replace
        if curr_linked_list.contains(key):
            curr_linked_list.remove(key)
            curr_linked_list.insert(key, value)

        # If key not in linked list, insert and increment size by one
        else:
            curr_linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets in the hash table.
        """
        # Counter variable
        num_empty_buckets = 0

        # Iterate through self._buckets and count number of empty nodes
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                num_empty_buckets += 1

        return num_empty_buckets

    def table_load(self) -> float:
        """
        Method returns the current hash table load factor.
        """
        # Calculate Load Factor
        load_factor = self._size / self._capacity
        return load_factor

    def clear(self) -> None:
        """
        Method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table. All existing key/value pairs
        must remain in the new hash map, and all hash table links must be rehashed.
        """
        # If new_capacity less than 1, return None
        if new_capacity < 1:
            return None

        # save_buckets holds values of soon-to-be cleared buckets
        save_buckets = self._buckets

        # Clear buckets
        self._buckets = DynamicArray()

        # Calculate self._capacity value using is_prime and next_prime methods
        potential_capacity = self._next_prime(new_capacity)
        self._size = 0
        self._capacity = new_capacity

        # If new capacity already prime
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = potential_capacity

        # Remake buckets, Append linked lists
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Put values in save_buckets into appropriate buckets
        for i in range(save_buckets.length()):
            # If bucket (linked_list) is not empty
            if save_buckets[i].length() != 0:
                for j in save_buckets[i]:
                    self.put(j.key, j.value)

    def get(self, key: str):
        """
        Method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        # Calculate hash_index and appropriate linked list
        hash_index = self._hash_function(key) % self._capacity
        curr_linked_list = self._buckets[hash_index]

        # If linked list contains the key, return its appropriate value pair
        if curr_linked_list.contains(key):
            return curr_linked_list.contains(key).value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """
        # Calculate hash_index and its appropriate linked list
        hash_index = self._hash_function(key) % self._capacity
        curr_linked_list = self._buckets.get_at_index(hash_index)

        # If linked list contains the key return True, else return False
        if curr_linked_list.contains(key):
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing
        """
        # Calculate hash_index and its appropriate linked list
        hash_index = self._hash_function(key) % self._capacity
        curr_linked_list = self._buckets.get_at_index(hash_index)

        # If linked list contains the key, remove it and decrement size by one.
        if self.contains_key(key):
            curr_linked_list.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map. The order of the keys in the dynamic array does not matter.
        """

        return_array = DynamicArray()

        for i in range(self._capacity):
            # If bucket (linked list) is not empty
            if self._buckets[i].length() != 0:
                for j in self._buckets[i]:
                    return_array.append((j.key, j.value))

        return return_array

    def get_hash_function(self):
        """
        Getter method for hash_function
        """
        return self._hash_function

    def get_buckets(self):
        """
        Getter method for self._buckets
        """
        return self._buckets


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Function receives a dynamic array.
    Function will return a tuple containing, a dynamic array comprising the mode
    value/s of the array, and an integer that represents the highest frequency.
    """

    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    dupl_checker = HashMap()
    return_array = DynamicArray()
    hash_function = map.get_hash_function()

    # Make instances in map with their respective counts
    for i in range(da.length()):
        # If value in da list is unique, put in map HashMap()
        if not map.contains_key(da[i]):
            map.put(da[i], 1)
        # If value NOT unique increment current value by one.
        elif map.contains_key(da[i]):
            # Get hash index and its linked list, find the node and increase the value by one
            map_buckets = map.get_buckets()
            hash_index = hash_function(da[i]) % map.get_capacity()
            curr_linked_list = map_buckets[hash_index]
            node_to_modify = curr_linked_list.contains(da[i])
            node_to_modify.value += 1

    # Map buckets now has the updated buckets
    map_buckets = map.get_buckets()

    # For the first index in da (DynamicArray), set its key as the mode (curr_mode) and its value as frequency
    # (curr_mode_frequency).
    curr_mode_hash_index = hash_function(da[0]) % map.get_capacity()
    curr_mode_linked_list = map_buckets[curr_mode_hash_index]
    curr_mode_node = curr_mode_linked_list.contains(da[0])
    curr_mode = curr_mode_node.key
    curr_mode_frequency = curr_mode_node.value

    # Put the first index of da and 1 as key in dupl_checker HashMap.
    dupl_checker.put(da[0], 1)
    return_array.append(curr_mode)

    # Iterate through da (DynamicArray)
    for i in range(1, da.length()):
        # Find hash_index, its linked_list and its appropriate node
        check_mode_hash_index = hash_function(da[i]) % map.get_capacity()
        check_mode_linked_list = map_buckets[check_mode_hash_index]
        check_mode_node = check_mode_linked_list.contains(da[i])

        # Current key in node (potential mode val)
        check_mode = check_mode_node.key
        # Current value in node (frequency)
        check_mode_frequency = check_mode_node.value

        # Check if value is not a duplicate in dupl_checker and check mode frequency is equal to curr mode frequency
        if check_mode_frequency == curr_mode_frequency and not dupl_checker.contains_key(da[i]):
            # Add (key, 1) to dupl_checker
            dupl_checker.put(da[i], 1)
            return_array.append(check_mode)

        # If the curr mode frequency is more (key is node then)
        elif check_mode_frequency > curr_mode_frequency:
            # Clear dupl_checker and add (da[i], 1) to dupl_checker
            dupl_checker = HashMap()
            dupl_checker.put(da[i], 1)

            # Reset curr_mode_frequency
            curr_mode_frequency = check_mode_frequency

            # Clear return array and append check_mode
            return_array = DynamicArray()
            return_array.append(check_mode)

    return (return_array, curr_mode_frequency)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")



# sgrhfmddg