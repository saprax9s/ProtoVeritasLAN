from file_processor import FileProcessor
from hasher import hash_chunks
from merkle_tree import build_merkle_levels

filename = "sample.pdf"
processor = FileProcessor(folder_name="demo_data", num_chunks=256)
chunks = processor.chunk_file(filename)
chunk_hashes = [c["hash"] for c in hash_chunks(chunks)]
levels = build_merkle_levels(chunk_hashes)

print(f"\n📄 File: {filename}")
print(f"🔢 Total Chunks: {len(chunk_hashes)}")

print("\n🔗 Chunk Hashes:")
for i, h in enumerate(chunk_hashes):
    print(f"  [{i}] {h}")

print("\n🌲 Merkle Tree Levels:")
for depth, level in enumerate(levels):
    print(f"  Level {depth}:")
    for h in level:
        print(f"    {h}")

print(f"\n🧬 Final Merkle Root: {levels[-1][0]}")
