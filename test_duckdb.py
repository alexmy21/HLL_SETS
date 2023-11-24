import random
import string
from hset_core import HsetCore as hcore
import duckdb
from hll import Hll
from hll_set import HllSet
import pandas as pd

random.seed(42)
strings = [''.join(random.choices(string.ascii_uppercase, k=10)) for _ in range(200000)]
print('Initial dataset size: ', len(strings))

set_A = set(random.sample(strings, 28000))
set_B = set(random.sample(strings, 100000))
set_C = set(random.sample(strings, 122000))

hll_A = Hll(13)
hll_A._append(set_A)

hll_B = Hll(13)
hll_B._append(set_B)

hll_C = Hll(13)
hll_C._append(set_C)

# Create a HllSet
hll_set = HllSet(hll_A, label='A')

# Add some data to the HllSet
# hll_set.add("Hello")
# hll_set.add("World")

con = duckdb.connect('my_database.duckdb')

# Convert the HllSet to a record
# record = hll_set.toRecord()

# print(record)

# # Convert the record to a pandas DataFrame
# df = pd.DataFrame([hll_set.toRecord()])

# # Write the DataFrame to a DuckDB table
# # con.register('my_table', df)
# con.execute("CREATE TABLE IF NOT EXISTS my_table AS SELECT * FROM df")

# con.close()

# Execute the query
df = con.execute("SELECT * FROM my_table").fetchdf()

# Convert the DataFrame to a list of dictionaries
records = df.to_dict('records')

print(records)

# Print the records
for record in records:
    print(HllSet().fromRecord(record))