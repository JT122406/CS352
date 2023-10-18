import hashlib


message = "Ethernet cables are like the roads of the Internet, carrying data traffic to its destinations."
key = "186e3bdc82d21a2682ee8e82eb5fe868"
sha256_hash = hashlib.sha256()
sha256_hash.update(message.encode('ascii'))
sha256_hash.update(key.encode('ascii'))
sign = sha256_hash.hexdigest()
print(sign)
message2 = "Imagine a network as a virtual neighborhood, where devices are houses and data packets are mail going from one address to another."
key2 = "0e32e7adfb5e1b3bc416b1846ccfe934"
signature1 = "443c65586b40fde1d240974eef1844550e22ababb29e6ce5ccc94bcadbbda826"
signature2 = "d4be92f06c6d289fa4c564c5a7f682e29797b27e8d9cd472eaae34193fee86c2"
sha256_hash.update(message2.encode('ascii'))
sha256_hash.update(key2.encode('ascii'))
sign2 = sha256_hash.hexdigest()
print(sign2)
sha256_hash2 = hashlib.sha256()
sha256_hash2.update(message2.encode('ascii'))
sha256_hash2.update(key2.encode('ascii'))
sign3 = sha256_hash2.hexdigest()
print(sign3)