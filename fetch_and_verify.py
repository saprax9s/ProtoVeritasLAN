import requests
import getpass
from merkle_tree import build_merkle_root
from hasher import hash_chunks
from file_processor import FileProcessor

def fetch_merkle_root():
    site_name = "VeritasPres"  # 🔒 Fixed tab name
    password = getpass.getpass("🔐 Enter ProtectedText password for VeritasPres: ")

    url = f"https://www.protectedtext.com/{site_name}"
    response = requests.post(url, data={"password": password})
    if response.status_code != 200:
        print("❌ Failed to connect to ProtectedText.")
        return None

    try:
        text_block = response.text.split('id="text"')[1].split("</textarea>")[0]
        root = text_block.split(">")[-1].strip()
        print(f"🌿 Fetched Merkle root: {root}")
        return root
    except Exception:
        print("⚠️ Could not parse Merkle root from response.")
        return None

def verify_and_reconstruct():
    processor = FileProcessor(folder_name="data", num_chunks=256)
    processor.transmit()

    for filename, info in processor.file_chunks.items():
        chunks = hash_chunks(info["chunks"])
        local_root = build_merkle_root([c["hash"] for c in chunks])
        remote_root = fetch_merkle_root()

        if not remote_root:
            print("❌ No Merkle root fetched. Aborting.")
            return

        if local_root == remote_root:
            print(f"✅ Verified integrity for '{filename}'")
            processor.reassemble()
        else:
            print(f"❌ Integrity check failed for '{filename}'")
