import hashlib

def build_merkle_root(hashes):
    if len(hashes) == 1:
        return hashes[0]
    new_level = []
    for i in range(0, len(hashes), 2):
        left = hashes[i]
        right = hashes[i+1] if i+1 < len(hashes) else left
        combined = hashlib.sha256((left + right).encode()).hexdigest()
        new_level.append(combined)
    return build_merkle_root(new_level)

def build_merkle_levels(hashes):
    levels = [hashes]
    while len(hashes) > 1:
        new_level = []
        for i in range(0, len(hashes), 2):
            left = hashes[i]
            right = hashes[i+1] if i+1 < len(hashes) else left
            combined = hashlib.sha256((left + right).encode()).hexdigest()
            new_level.append(combined)
        levels.append(new_level)
        hashes = new_level
    return levels
