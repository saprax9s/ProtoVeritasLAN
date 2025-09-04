import requests
import shutil
import os
import socket
from file_processor import FileProcessor
from hasher import hash_chunks
from merkle_tree import build_merkle_root

def publish_all_merkle_roots():
    processor = FileProcessor(folder_name="data", num_chunks=256)
    processor.transmit()

    # Get sender's IP address
    ip = socket.gethostbyname(socket.gethostname())
    print(f"🌐 Using IP: {ip}")
    payload_lines = []

    for filename, info in processor.file_chunks.items():
        # Hash the actual chunks
        chunks = hash_chunks(info["chunks"])
        root = build_merkle_root([c["hash"] for c in chunks])

        # Copy file to server_files/
        os.makedirs("server_files", exist_ok=True)
        src = os.path.join("data", filename)
        dst = os.path.join("server_files", filename)
        shutil.copy2(src, dst)

        # Construct download URL
        download_url = f"http://{ip}:5000/download/{filename}"

        # Add to manifest payload
        payload_lines.append(f"Filename: {filename}")
        payload_lines.append(f"Merkle root: {root}")
        payload_lines.append(f"Download URL: {download_url}")
        payload_lines.append("")  # Spacer between files

    # Join all lines into one payload
    payload = "\n".join(payload_lines)

    # POST to Paste.rs
    response = requests.post("https://paste.rs/", data=payload.encode())

    if response.status_code == 201:
        print(f"📡 Manifest published successfully:\n{response.text.strip()}")
    elif response.status_code == 206:
        print("⚠️ Manifest partially uploaded (too large).")
        print(f"Partial link: {response.text.strip()}")
    else:
        print(f"❌ Failed to publish manifest. Status code: {response.status_code}")

if __name__ == "__main__":
    publish_all_merkle_roots()
