import sys
import requests
import hashlib


def password_hash(password):
    hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    hash_head, hash_trail = hash[:5], hash[5:]
    return (hash_head, hash_trail)


def request_api(hash):
    url = 'https://api.pwnedpasswords.com/range/' + hash
    response = requests.get(url)
    return response.text


def hash_count(hashes, hash):
    hashes_list = (item.split(':') for item in hashes.splitlines())
    for value, count in hashes_list:
        if value == hash:
            return count
    return 0


passwords = sys.argv[1:]

for item in passwords:
    secret = '*' * len(item)
    hash_head, hash_tail = password_hash(item)
    response = request_api(hash_head)
    count = hash_count(response, hash_tail)
    if count:
        print(
            f'Password {secret} was found {count} times, please choose a more secure pass!')
    else:
        print(f'Password {secret} was not found, good to go!')
