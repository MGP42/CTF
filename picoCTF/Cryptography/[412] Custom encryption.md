# Description
Can you get sense of this code file and write the function that will decode the given encrypted file content.
Find the encrypted file here flag_info and code file might be good to analyze and get the flag.

# Provided
- [custom_encryption.py](.prov/412-custom_encryption.py)
- [enc_flag](.prov/412-enc_flag)

# Progress
Starting with the flag, i get a,b and the cipher.

Looking at the encryption the python script, the code calls the test function first:

## Stripping down test
``` python
p = 97
g = 31
if not is_prime(p) and not is_prime(g):
    print("Enter prime numbers")
    return
a = randint(p-10, p)
b = randint(g-10, g)
```
This i can shrink down to:
``` python
p = 97
g = 31
a = 94
b = 29
```
as i get the values from the enc_flag.
``` python
u = generator(g, a, p)
v = generator(g, b, p)
key = generator(v, a, p)
b_key = generator(u, b, p)
shared_key = None
if key == b_key:
    shared_key = key
else:
    print("Invalid key")
    return
semi_cipher = dynamic_xor_encrypt(plain_text, text_key)
cipher = encrypt(semi_cipher, shared_key)
```
As i know that the script returned more than just a and b, it couldn't have entered the else case. Therefore: `key==b_key`. This allows me to strip the entire if clause:
``` python
shared_key = key
```
This removes the only use case of b so i go upward an remove the initialization of b_key and the variables that only get used for that. This removes the following lines:
``` python
u = generator(g, a, p
b_key = generator(u, b, p)
```
key also isn't used after the `shared_key=key` so instead of doing that i put it's value in shared_key directly. This reduces the test routine to:
``` python
def test(plain_text, text_key):
  p = 97
  g = 31
  a = 94
  b = 29
  print(f"a = {a}")
  print(f"b = {b}")
  v = generator(g, b, p)
  shared_key = generator(v, a, p)
  semi_cipher = dynamic_xor_encrypt(plain_text, text_key)
  cipher = encrypt(semi_cipher, shared_key)
  print(f'cipher is: {cipher}')
```
this removed the only occurences of `is_prime` so the entire function can go as well. The only occurence of randint has gone as well so the import is no longer necessary too. 
Considering the shared_key is only used once after and the entire upper part is just designed to create said shared_key, i will add a `print(shared_key)` to the test function and it once with arbitrary values to get said key.
``` python
test("abc","abc")
```
returns:
``` python
a = 94
b = 29
93
cipher is: [622, 0, 622]
```
This allows me to strip the code down even further:
``` python
def test(plain_text, text_key):
  semi_cipher = dynamic_xor_encrypt(plain_text, text_key)
  cipher = encrypt(semi_cipher, 93)
  print(f'cipher is: {cipher}')
```
With all the generator functin gone as well... away it goes.

I spotted the call to the encrypt function at the bottom so will try to create the decrypt function next:

## Create decrypt function
Looks rather simple to revert:
``` python
def decrypt(cipher, key):
    plaintext = ""
    for char in cipher:
        plaintext += chr(char // key// 311)
    return plaintext
```
quick test:
``` python
print(decrypt(encrypt("helloworld",13),13))
```
works like a charm.

So now the dynamic_xor_encrypt:
## dynamic_xor_decrypt
This is the only line really doing anything:
``` python
encrypted_char = chr(ord(char) ^ ord(key_char))
```
As a xor b xor b = a, it looks like i can just throw the cipher back in and get the correct result.
``` python
print(dynamic_xor_encrypt(dynamic_xor_encrypt("abcdef","qwertzuiopiuztrew"),"qwertzuiopiuztrew"))
```

Yeah no, that didn't work. So what else is there to it.
``` python
for i, char in enumerate(plaintext[::-1]):
```
Great.... it's reversed.... So just throw it in reversed... i guess
``` python
print(dynamic_xor_encrypt(dynamic_xor_encrypt("abcdef","qwertzuiopiuztrew")[::-1],"qwertzuiopiuztrew"))
```
It get's returned inversed.... Well what did i expect... just inverse the result again.
``` python
print(dynamic_xor_encrypt(dynamic_xor_encrypt("abcdef","qwertzuiopiuztrew")[::-1],"qwertzuiopiuztrew")[::-1])
```
good enough, i guess

Time to invert the test function:
## invert test
changing the original order of the encryption and using the decryption methods instead:
``` python
def test2(cipher,text_key):
    semi_cipher=decrypt(cipher,93)
    plain_text=dynamic_xor_encrypt(semi_cipher[::-1],text_key)[::-1]
    print(plain_text)
```
output:
```
picoCTF{custom_d2cr0pt6d_751a22dc}
```

# Full script
``` python
def decrypt(cipher, key):
    plaintext = ""
    for char in cipher:
        plaintext += chr(char // key// 311)
    return plaintext

def dynamic_xor_encrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)
    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    return cipher_text

def test2(cipher,text_key):
    semi_cipher=decrypt(cipher,93)
    plain_text=dynamic_xor_encrypt(semi_cipher[::-1],text_key)[::-1]
    print(plain_text)


c=[260307, 491691, 491691, 2487378, 2516301, 0, 1966764, 1879995, 1995687, 1214766, 0, 2400609, 607383, 144615, 1966764, 0, 636306, 2487378, 28923, 1793226, 694152, 780921, 173538, 173538, 491691, 173538, 751998, 1475073, 925536, 1417227, 751998, 202461, 347076, 491691]
test2(c,"trudeau")

```