🛡️ Veritas Protocol Documentation
Autonomous, Multi-File, Merkle-Verified Transmission System

📦 Folder Structure
Code
veritas_protocol/
├── data/                    # Sender: original files | Receiver: downloaded files
├── output/                  # Receiver: reconstructed files
├── server_files/            # Sender: hosted files for download
├── file_processor.py        # Chunking + reassembly logic
├── hasher.py                # Hash chunks
├── merkle_tree.py           # Build Merkle root
├── file_server.py           # Flask server to host files
├── publish_merkle.py        # Sender: publish roots + links to Paste.rs
├── receiver_setup.py        # Receiver: fetch, verify, reconstruct
🧠 Script Roles
Script	Role
file_processor.py	Splits files into chunks and reassembles them
hasher.py	Hashes each chunk using SHA-256
merkle_tree.py	Builds a Merkle root from chunk hashes
file_server.py	Hosts files via Flask for receiver to download
publish_merkle.py	Publishes manifest with filename, Merkle root, and download URL
receiver_setup.py	Fetches manifest, downloads files, verifies integrity, reconstructs
🔁 Sender Workflow
1. Drop Files
Place all files to be transmitted into the data/ folder.
2. Publish Manifest
bash
python publish_merkle.py
•	Chunks and hashes each file
•	Builds Merkle roots
•	Copies files to server_files/
•	Publishes manifest to Paste.rs
•	Prints a link like:
Code
https://paste.rs/abc123xyz
3. Host Files
bash
python file_server.py
•	Starts Flask server at http://<your-ip>:5000/download/<filename>
•	Keep this running while receiver fetches
4. Share Manifest Link
Send the Paste.rs link to the receiver manually.
🔁 Receiver Workflow
1. Run Receiver Script
bash
python receiver_setup.py
2. Paste Manifest Link
When prompted:
Code
🔗 Paste the manifest link from sender:
Paste the full link:
Code
https://paste.rs/abc123xyz
3. Automatic Flow
•	Fetches manifest
•	Parses filename, Merkle root, and download URL
•	Downloads each file
•	Chunks and hashes locally
•	Verifies Merkle root
•	Reconstructs verified files into output/
🛠️ Key Fixes & Enhancements
•	✅ Defensive parsing with split(":", 1) to avoid index errors
•	✅ Debug print to show parsed blocks before download
•	✅ Manifest fetch uses headers={"Accept": "text/plain"} to avoid HTML
•	✅ Error handling for malformed blocks
•	✅ IP logic patched to use LAN IP or hardcoded fallback
🧪 Example Manifest Block
Code
Filename: sample.pdf
Merkle root: 26eaf2c8cade4f089e07035a806b8ba2c3c38952c3044fc8864f16d26b36fa35
Download URL: http://10.203.4.229:5000/download/sample.pdf
🌐 Network Requirements
•	Both sender and receiver must be on the same LAN (e.g. same Wi-Fi)
•	The receiver accesses the sender’s IP directly
•	For global access, port-forwarding or cloud hosting is required
💡 Future Enhancements
•	Wrap into CLI tools: veritas send and veritas receive
•	QR code generation for manifest links
•	Expiry logic for hosted files
•	Public server deployment with domain + HTTPS
•	Chunk encryption with identity-bound keys




🔍 Veritas Demo Suite
The demo/ folder contains an isolated sandbox for inspecting the core cryptographic flow of the Veritas protocol — no transmission, no manifest, just pure hashcraft.

📁 Structure
Code
demo/
├── demo_encode.py       # Chunk, hash, build Merkle tree, print breakdown
├── demo_verify.py       # Re-chunk, re-hash, rebuild tree, compare root
├── file_processor.py    # Chunking logic
├── hasher.py            # SHA-256 chunk hashing
├── merkle_tree.py       # Merkle root + level builder
├── demo_data/           # Drop test files here
⚙️ How to Use
Drop a file into demo/demo_data/ (e.g. sample.pdf)

Run the encoder:

bash
python demo/demo_encode.py
→ This prints chunk hashes, Merkle tree levels, and the final root

Run the verifier:

bash
python demo/demo_verify.py
→ Paste the expected Merkle root when prompted → It reconstructs the tree and verifies integrity

🧠 Why It Exists
This suite is designed for:

Debugging and inspecting Merkle anatomy

Teaching and onboarding new contributors

Verifying file integrity without full protocol setup


note: it's a fun little night motivation projects completely done using AI and basic python

