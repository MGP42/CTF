# Description
We found a brand new type of encryption, can you break the secret code? (Wrap with picoCTF{}) kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm new_caesar.py

# Provided
- [new_caesar.py](.prov/158-new_caesar.py)

# Progress
Starting at the "main"
``` python
flag = "redacted"
key = "redacted"
```
2 unknown things... G R E A T

~~~ python
assert all([k in ALPHABET for k in key])
assert len(key) == 1
~~~
It clearly returned something so i won't need that when reversing, but it's good to know that they key has a length of 1.

~~~ python
b16 = b16_encode(flag)
~~~
~~~ python
def b16_encode(plain):
  enc = ""
  for c in plain:
    binary = "{0:08b}".format(ord(c))
    enc += ALPHABET[int(binary[:4], 2)]
    enc += ALPHABET[int(binary[4:], 2)]
  return enc
~~~
OK the decoder as first step:

~~~ python
def b16_decode(enc):
plain=""
for first,second in zip(enc[::2], enc[1::2]):
  binary  = "{0:08b}".format(ALPHABET.index(first))[4:]
  binary += "{0:08b}".format(ALPHABET.index(second))[4:]
  plain  += chr(int(binary,2))
return plain
~~~
works great, so what next:
~~~ python
for i, c in enumerate(b16):
  enc += shift(c, key[i % len(key)])
~~~
reverting the shift routine:
~~~ python
def back_shift(c,k):
  t1 = ord(c) - LOWERCASE_OFFSET
  t2 = ord(k) - LOWERCASE_OFFSET
  return ALPHABET[(t1 - t2) % len(ALPHABET)]
~~~
now for the testing:
~~~ python
b16 = b16_encode(flag)
enc = ""
for i, c in enumerate(b16):
  enc += shift(c, key[i % len(key)])
print(enc)

b16=""
for i, c in enumerate(enc):
  b16 += back_shift(c, key[i % len(key)])
flag=b16_decode(b16)
print(flag)
~~~
works perfectly!!

Now only the key is missing... Only 1 character, so bruteforce, i guess:
~~~ python
for i in range (0,256):
  key=chr(i)
  b16=""
  for i, c in enumerate(enc):
    b16 += back_shift(c, key[i % len(key)])
  flag=b16_decode(b16)
  print(flag)
~~~
this should do, i guess
~~~
.
.
.


@`BrtFwDuHJCArIFGBArwvsCFHCIDBurrI
et_tu?_1ac5f3d7920a85610afeb2572831daa8
TcNcd.N PR$U"S&(!/P'$% /PUTQ!$&!'" SPP'
CR=RS=OADBOODC@BOO
2A,AB
>32?1>>031
!01û-/ñ"ÿ óõþü-ôñòýü-"!.þñóþôÿý --ô
/
/ ê
ìàîâäíëãàáìëíàâíãîìã
ùÙùÛ
ßÝÑÓÜÚ
      ÒßÐÛÚ

           ÜßÑÜÒÝÛ

                  Ò
ÈèÊúüÎÿÌýÀÂËÉúÁÎÏÊÉúÿþûËÎÀËÁÌÊýúúÁ
íü×üý·×¹éë½î»ì¿±º¸é°½¾¹¸éîíêº½¿º°»¹ìéé°
ÜëÆëì¦Æ¨ØÚ¬ÝªÛ® ©§Ø¯¬­¨§ØÝÜÙ©¬®©¯ª¨ÛØØ¯
ËÚµÚÛµÇÉÊÇÇÌËÈÊÇÇ
~~~
i mean it would probably do, but fuck this output. I will remove the newlines:
~~~python
banned = ['\n', '\r', '\r\n', '\u2028', '\u2029', '\u0085']

for i in range (0,256):
  key=chr(i)
  b16=""
  for i, c in enumerate(enc):
    b16 += back_shift(c, key[i % len(key)])
  flag=b16_decode(b16)
  if all(ban not in flag for ban in banned):
      print(flag)
~~~
result:
~~~
ËÚµÚÛµÇÉÊÇÇÌËÈÊÇÇ¸¸¹su¥§yªw¨{}vt¥|yzut¥ª©¦vy{v|wu¨¥¥|
§¨bdhfjleckhidcehjekfdk
et_tu?_1ac5f3d7920a85610afeb2572831daa8
TcNcd.N PR$U"S&(!/P'$% /PUTQ!$&!'" SPP'
CR=RS=OADBOODC@BOO
!01û-/ñ"ÿ óõþü-ôñòýü-"!.þñóþôÿý --ô
íü×üý·×¹éë½î»ì¿±º¸é°½¾¹¸éîíêº½¿º°»¹ìéé°
ÜëÆëì¦Æ¨ØÚ¬ÝªÛ® ©§Ø¯¬­¨§ØÝÜÙ©¬®©¯ª¨ÛØØ¯
ËÚµÚÛµÇÉÊÇÇÌËÈÊÇÇ¸¸¹su¥§yªw¨{}vt¥|yzut¥ª©¦vy{v|wu¨¥¥|
§¨bdhfjleckhidcehjekfdk
et_tu?_1ac5f3d7920a85610afeb2572831daa8
TcNcd.N PR$U"S&(!/P'$% /PUTQ!$&!'" SPP'
CR=RS=OADBOODC@BOO
!01û-/ñ"ÿ óõþü-ôñòýü-"!.þñóþôÿý --ô
íü×üý·×¹éë½î»ì¿±º¸é°½¾¹¸éîíêº½¿º°»¹ìéé°
ÜëÆëì¦Æ¨ØÚ¬ÝªÛ® ©§Ø¯¬­¨§ØÝÜÙ©¬®©¯ª¨ÛØØ¯
ËÚµÚÛµÇÉÊÇÇÌËÈÊÇÇ
~~~
Meh, should have probably used regex instead
~~~ python
if re.match(r'^[\x20-\x7E]*$',flag) and re.match("[A-Za-z]",key):
  print(key+" "+flag)
~~~
So i limit the flag to ascii characters and the key to the Alphabet
~~~
E et_tu?_1ac5f3d7920a85610afeb2572831daa8
F TcNcd.N PR$U"S&(!/P'$% /PUTQ!$&!'" SPP'
U et_tu?_1ac5f3d7920a85610afeb2572831daa8
V TcNcd.N PR$U"S&(!/P'$% /PUTQ!$&!'" SPP'
e et_tu?_1ac5f3d7920a85610afeb2572831daa8
f TcNcd.N PR$U"S&(!/P'$% /PUTQ!$&!'" SPP'
u et_tu?_1ac5f3d7920a85610afeb2572831daa8
v TcNcd.N PR$U"S&(!/P'$% /PUTQ!$&!'" SPP'
~~~
Well down to 2 strings. I probably have to test both *sigh*. Considering one of them contains spaces i will test the other first:
```
picoCTF{et_tu?_1ac5f3d7920a85610afeb2572831daa8}
```
# Full Code
~~~python
import string
import re

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_decode(enc):
  plain=""
  for first,second in zip(enc[::2], enc[1::2]):
    binary  = "{0:08b}".format(ALPHABET.index(first))[4:]
    binary += "{0:08b}".format(ALPHABET.index(second))[4:]
    plain  += chr(int(binary,2))
  return plain

def back_shift(c,k):
  t1 = ord(c) - LOWERCASE_OFFSET
  t2 = ord(k) - LOWERCASE_OFFSET
  return ALPHABET[(t1 - t2) % len(ALPHABET)]

enc="kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm"

for i in range (0,256):
  key=chr(i)
  b16=""
  for i, c in enumerate(enc):
    b16 += back_shift(c, key[i % len(key)])
  flag=b16_decode(b16)
  if re.match(r'^[\x20-\x7E]*$',flag) and re.match("[A-Za-z]",key):
      print(key+" "+flag)
~~~