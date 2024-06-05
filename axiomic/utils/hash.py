
import hashlib
import base64

def hash_blake2(s):
    return hashlib.blake2b(s.encode()).hexdigest()

def hash_as_base32(s):
    hash_bytes = hashlib.blake2b(s.encode()).digest()
    return base64.b32encode(hash_bytes).decode('utf-8')


def short_hash(string):
    return hash_as_base32(string)[:12]




if __name__ == '__main__':
    print(short_hash('Hello, world!')) # 3