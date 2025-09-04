import requests, os
from file_processor import FileProcessor
from hasher import hash_chunks
from merkle_tree import build_merkle_root

def receiver_setup(paste_url):
    response = requests.get(paste_url, headers={"Accept": "text/plain"})
    if response.status_code != 200:
        print("❌ Failed to fetch manifest.")
        return

    blocks = response.text.strip().split("\n\n")
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        try:
            filename = lines[0].split(":", 1)[1].strip()
            merkle_root = lines[1].split(":", 1)[1].strip()
            download_url = lines[2].split(":", 1)[1].strip()
        except IndexError:
            print(f"❌ Malformed block:\n{block}")
            continue
        
        print(f"📄 Parsed block:\nFilename: {filename}\nMerkle root: {merkle_root}\nDownload URL: {download_url}")



        print(f"🌐 Downloading '{filename}' from {download_url}")
        file_response = requests.get(download_url)
        if file_response.status_code != 200:
            print(f"❌ Failed to download '{filename}'")
            continue

        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", filename)
        with open(file_path, "wb") as f:
            f.write(file_response.content)

        processor = FileProcessor(folder_name="data", num_chunks=256)
        processor.transmit()
        chunks = hash_chunks(processor.file_chunks[filename]["chunks"])
        local_root = build_merkle_root([c["hash"] for c in chunks])

        if local_root == merkle_root:
            print(f"✅ Verified '{filename}'")
            processor.reassemble()
        else:
            print(f"❌ Integrity check failed for '{filename}'")


paste_url = input("🔗 Paste the manifest link from sender: ").strip()
receiver_setup(paste_url)

