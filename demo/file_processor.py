import os

class FileProcessor:
    def __init__(self, folder_name, num_chunks=256):
        self.folder_name = folder_name
        self.num_chunks = num_chunks

    def chunk_file(self, filename):
        path = os.path.join(self.folder_name, filename)
        with open(path, "rb") as f:
            data = f.read()

        chunk_size = max(1, len(data) // self.num_chunks)
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        return chunks
