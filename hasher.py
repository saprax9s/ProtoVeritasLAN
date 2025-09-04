import hashlib

def hash_chunks(chunks):
    return [{"hash": hashlib.sha256(chunk).hexdigest()} for chunk in chunks]
