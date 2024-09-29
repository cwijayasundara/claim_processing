from langchain.storage import LocalFileStore
import random

# Instantiate the LocalFileStore with the root path
file_store = LocalFileStore("local_docs")

key_1 = random.randrange(1, 10000)
key_2 = random.randrange(1, 10000)

# convert the key to string
key_1 = str(key_1)
key_2 = str(key_2)

# Set values for keys
file_store.mset([(key_1, b"value1"), (key_2, b"value2")])

# Get values for keys
values = file_store.mget([key_1, key_2])  # Returns [b"value1", b"value2"]
print(values)

# Delete keys
file_store.mdelete([key_1])

# Iterate over keys
for key in file_store.yield_keys():
    print(key)  # noqa: T201