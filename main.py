from file_processor import FileProcessor
from hasher import hash_chunks
from merkle_tree import build_merkle_root
from protected_store import store_merkle_root

processor = FileProcessor(folder_name="data", num_chunks=256)
processor.transmit()

for filename, info in processor.file_chunks.items():
    chunks = hash_chunks(info["chunks"])
    root = build_merkle_root([c["hash"] for c in chunks])
    store_merkle_root(root)
