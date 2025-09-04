import os

class FileProcessor:
    def __init__(self, folder_name="data", num_chunks=256):
        self.folder = folder_name
        self.num_chunks = num_chunks
        self.file_chunks = {}

    def transmit(self):
        for filename in os.listdir(self.folder):
            path = os.path.join(self.folder, filename)
            with open(path, "rb") as f:
                data = f.read()
            chunk_size = len(data) // self.num_chunks
            chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
            self.file_chunks[filename] = {"chunks": chunks}
            print(f"📦 Transmitted '{filename}' into {len(chunks)} chunks.")

    def reassemble(self):
        for filename, info in self.file_chunks.items():
            output_path = os.path.join("output", filename)
            os.makedirs("output", exist_ok=True)
            with open(output_path, "wb") as f:
                for chunk in info["chunks"]:
                    f.write(chunk)
            print(f"🛠️ Reassembled '{filename}' to 'output/{filename}'")
