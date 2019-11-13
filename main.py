from chaininghashtable import ChainingHashTable
from linearprobinghashtable import LinearProbingHashTable
from doublehashinghashtable import DoubleHashingHashTable
from quadraticprobinghashtable import QuadraticProbingHashTable

# Main program to test HashTable classes
keys = [ 35, 0, 22, 94, 220, 110, 4 ]
chaining = ChainingHashTable()
linear_probing = LinearProbingHashTable()
qp1 = QuadraticProbingHashTable()
double_hashing = DoubleHashingHashTable()
for key in keys:
    chaining.insert(key)
    linear_probing.insert(key)
    qp1.insert(key)
    double_hashing.insert(key)

# Show tables after inserts.
print ("Chaining: initial table:")
print (chaining)
print()

print ("Linear Probing: initial table:")
print (linear_probing)
print()

print ("Quadratic Probing: initial table:")
print (qp1)
print()

print ("Double Hashing: initial table:")
print (double_hashing)
print()

# Show tables after removing item 0
print ("=======================================")
chaining.remove(0)
linear_probing.remove(0)
qp1.remove(0)
double_hashing.remove(0)

print ("Chaining: after removing 0:")
print(chaining)
print()

print ("Linear Probing: after removing 0:")
print(linear_probing)
print()

print ("Quadratic Probing: initial table:")
print (qp1)
print()

print ("Double Hashing: after removing 0:")
print(double_hashing)