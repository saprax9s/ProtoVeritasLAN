from file_processor import FileProcessor
from hasher import hash_chunks
from merkle_tree import build_merkle_levels

filename = "sample.pdf"
expected_root = input("\n📜 Paste the expected Merkle root for verification:\n> ").strip()

processor = FileProcessor(folder_name="demo_data", num_chunks=256)
chunks = processor.chunk_file(filename)
chunk_hashes = [c["hash"] for c in hash_chunks(chunks)]
levels = build_merkle_levels(chunk_hashes)

print(f"\n📄 Verifying File: {filename}")
print(f"🔢 Total Chunks: {len(chunk_hashes)}")
print(f"🧬 Reconstructed Merkle Root: {levels[-1][0]}")
print(f"📜 Expected Merkle Root:     {expected_root}")

if levels[-1][0] == expected_root:
    print("\n✅ Verification Passed")
else:
    print("\n❌ Verification Failed")
