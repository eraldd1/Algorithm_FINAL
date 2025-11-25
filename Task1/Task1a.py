import os
import sys

# Set up paths to import CLRS library
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")

sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 11"))

# Import the hash table implementation from the CLRS library
from open_address_hashtable import OpenAddressHashTable


#Dataset
stations = ["A", "B", "C", "D", "E"]

def primary_hash(k):
    return sum(ord(c) for c in str(k))

ht = OpenAddressHashTable(m=10, h1=primary_hash)

for s in stations:
    ht.insert(s)

print("Stations inserted:", stations)

result = ht.search("D")
print("Is 'D' operational?: ", bool(result))

print("\nInternal state :", ht.table)

print("\nInternal state (formatted):")
for i, slot in enumerate(ht.table):
    print(f"  Slot {i}: {slot}")






