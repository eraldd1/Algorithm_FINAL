import os
import sys
import random
import time
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")

sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 11"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 31"))

from open_address_hashtable import OpenAddressHashTable
from hash_functions import hashpjw

primary_hash = hashpjw

# Test the setup
print("Testing setup...")
ht_test = OpenAddressHashTable(m=10, h1=primary_hash)
print(f"✓ Created OpenAddressHashTable with size 10")

test_val_int = primary_hash(123)
test_val_str = primary_hash("ABC")
print(f"✓ hashpjw(123) = {test_val_int}")
print(f"✓ hashpjw('ABC') = {test_val_str}")

ht_test.insert("test")
print(f"✓ Successfully inserted 'test' into hash table")

print("\nReady!")


# Generating dataset and insert into hash table

print("Dataset Generation and Insertion")


n = 1000
stations = list(range(n))

# m = 2*n gives plenty of space to reduce clustering
ht = OpenAddressHashTable(m=2 * n, h1=primary_hash)

#insert each station
for s in stations:
    ht.insert(s)

print(f"\nInserted {n} stations successfully!")
print(f"Table size (m): {ht.m}")
print(f"Load factor (α): {n / ht.m:.2f}")
print(f"\nExample slots (first 20):")
print(ht.table[:20])

occupied_slots = sum(1 for slot in ht.table if slot is not None)
print(f"\nVerification:")
print(f"  Expected occupied slots: {n}")
print(f"  Actual occupied slots: {occupied_slots}")
print(f"  Match: {'✓' if occupied_slots == n else '✗'}")

print(f"\nHash distribution sample (first 10 stations):")
for i in range(10):
    hash_val = primary_hash(i) % ht.m
    print(f"  Station {i}: hash = {primary_hash(i)}, slot = {hash_val}")


print("Ready for timing measurements!")


print("Timing membership checks")

num_queries = 10000
queries = [random.randint(0, n - 1) for _ in range(num_queries)]

start = time.perf_counter()

for q in queries:
    ht.search(q)

end = time.perf_counter()

total_time = end - start
avg_time = total_time / num_queries

print(f"\nPerformed {num_queries} membership checks.")
print(f"Total time: {total_time:.6f} seconds")
print(f"Average time per search: {avg_time * 1e6:.3f} microseconds")


dataset_sizes = [1000, 5000, 10000, 25000, 50000]
results = []


print("Multi-size performance measurement")

for n in dataset_sizes:
    print(f"\n Testing n = {n}")

    # generate dataset
    stations = list(range(n))

    # build table
    ht = OpenAddressHashTable(m=2 * n, h1=primary_hash)

    for s in stations:
        ht.insert(s)

    # run random queries
    num_queries = 10000
    queries = [random.randint(0, n - 1) for _ in range(num_queries)]

    start = time.perf_counter()

    for q in queries:
        ht.search(q)

    end = time.perf_counter()

    total_time = end - start
    avg_time = total_time / num_queries

    print(f"  Inserted {n} stations into table of size {ht.m}")
    print(f"  Load factor (α): {n / ht.m:.2f}")
    print(f"  Average lookup time: {avg_time * 1e6:.3f} microseconds")

    results.append((n, avg_time))



# Display summary table
print("\nSummary of Results:")

print(f"{'Dataset Size (n)':<20} {'Avg Time (μs)':<20}")

for n, avg_time in results:
    print(f"{n:<20} {avg_time * 1e6:<20.3f}")



print("Generating plot and saving results")

# Extract X and Y values
sizes = [n for (n, t) in results]
times = [t * 1e6 for (n, t) in results]

# Save results to CSV file
output_file = "hash_table_results.csv"
with open(output_file, 'w') as f:
    f.write("Dataset_Size,Average_Time_Microseconds\n")
    for n, avg_time in results:
        f.write(f"{n},{avg_time * 1e6:.6f}\n")


# Create matplotlib plot
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', linewidth=2, markersize=10, color='#2E86AB', label='Observed Time')

plt.title("Average Search Time vs Dataset Size\n(Open Addressing Hash Table - Linear Probing)",
          fontsize=13, fontweight='bold')
plt.xlabel("Dataset Size (n)", fontsize=11)
plt.ylabel("Average Search Time (microseconds)", fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')

# Add value labels on points
for size, time_val in zip(sizes, times):
    plt.annotate(f'{time_val:.2f}μs',
                 xy=(size, time_val),
                 xytext=(0, 10),
                 textcoords='offset points',
                 ha='center',
                 fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

# Add theoretical O(1) reference line (mean of all measurements)
mean_time = sum(times) / len(times)
plt.axhline(y=mean_time, color='red', linestyle='--',
            label=f'O(1) Reference (mean = {mean_time:.2f}μs)', alpha=0.7, linewidth=2)

plt.legend(fontsize=10)
plt.tight_layout()

# Save plot
plot_filename = "hash_table_performance.png"
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')


# Display plot
plt.show()


print("Complete!")
