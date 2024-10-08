# Description
We have so much faith in RSA we give you not just the product of the primes, but their sum as well!

# Provided
- [gen.py](.prov/310-gen.py)
- [output.txt](.prov/310-output.txt)

# Ressources
- [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))

# Progress
First i looked at the output.txt which gives me n, c and x:<br>
<details><summary>Values</summary>
x = 429cf99b5dd5dde9f016095be650d5b0a9a73e648aa72324cb8eb05bd14c1b913539a97f5417474f6014de830ad6dee028dd8908e593b1e99c4cc88f400127214036e71112292e58a2ccffc48f57524aee90f9858d935c7a86297a90c7fe48b80f6c4e8df9eaae501ef40da7984502457255fbc8a9e1574ec6ba210be134f192
n = 64fc90f5ca6db24f7bfc6419de407596d29a9ecda526101b8d0eff2181e9b8ed1538a1cbabe4dfc5bcd899976e7739f8b448815b50db36a994c5b1df97981d562c663113fc5ee84f3206aecd18248fb4e9bddf205c8119e8437f7d6522e63d05bc357ae4969a4b3000b8226f8d142c23c4e38cdb0c385bf9564e8a115e4c52b7a2e3a9073a5d99d7bec3bca6452cf0c1b8d8b6b123cc6a6980cf14088d6a2bbb5ed36b85cb0003e535bd16d79ad54ff5b26e62f57de074654493d3a26a149786d5fbf61b42c9305092eb018aa3db3cb18b24f188ae520bd18acf9ffced09a2ba302a520f6e2bfd8eea9adc01eb8ee941181694a3ab493e1aa53fbbbf2851a591
c = 56ed81bbc149701110f0a15e2e6078ab926d74ee2c11b804ae4fad4333a25c247f38bb74867922438d10ce529b75f5ee5e29ce71d6f704cc0644f7e78d60a2af8921fbc49326280e3f0c00f2769e837363cbb05dc3f30bda8fdc94111fb025008eae562ae57029d5cfde6bdd09893a738187578d22f82a5f8769f093681662329f05b262c2054f91696a24f631ba8132f3d92ae7758c91fa9b5657e4944c5d5f93afb4af68908d004ae5f97071bcaceb7d0034297eeb897f972b44b0d7def52f46ee45d386a5e24ed613bf7e5177c6e10f69a3d3de0f0c30de0b15d360ee81da3d277a4acf47b6df389c24615884b692e604eba711fc28c34bc56227b8455705
</details>
WTF is x probably the sum they were talking of... also no e so this might get dirty rather quickly.

Next the gen.py:<br>
great x is indeed p+q and e is hardcoded 65537

While i already wrote an attack against this problem that runs in O(log(n))
``` python
# adjusts p and q by s
def adjust(p,q,s):
  if p*q>n:
    p-=s
    q+=s
  else:
    p+=s
    q-=s
  return p,q

# adjust p and q in logarithmic steps
def crack(x,n):
  p=x//2
  q=p
  s=p//2-1
  while p*q!=n:
    p,q=adjust(p,q,s)
    s=s//2 if s%2==0 else s//2+1
  return p,q

p,q=crack(x,n)
```
This is completely stupid as it can just be solved with math:
Rearrange:

$`
\begin{aligned}
n=p\cdot q&~~~~~~~~&x=p+q\\
p=\frac{n}{q}&&p=x-q\\
\end{aligned} 
`$

Substitue:

$`
\begin{aligned}
\frac{n}{q}=x-q
\end{aligned}
`$

Solve:

$`
\begin{aligned}
\frac{n}{q}&=x-q\\
n&=(x-q)\cdot q\\
&=xq-q^2\\
-n&=q^2-xq\\
-n-(\frac{x}{2})^2&=q^2-xq+(\frac{x}{2})^2\\
-n+\frac{x^2}{4}&=(q-\frac{x}{2})^2\\
\pm\sqrt{-n+\frac{x^2}{4}}&=q-\frac{x}{2}\\
\pm\sqrt{-n+\frac{x^2}{4}}+\frac{x}{2}&=q
\end{aligned}
`$

<details><summary>MONKA</summary>
It just came to my attention that while writing that down that i did not consider the option for $q_1$ and $q_2$ which didn't matter as the option that i do not take is equal to p.
  
In other words $q_1=q$ and $q_2=p$
</details>

Calculate p with $x-p=q$
With the Math part out of the way the system can be solved using python:<br>
``` python
from egcd import egcd
import math
x = int(0x1429cf99b5dd5dde9f016095be650d5b0a9a73e648aa72324cb8eb05bd14c1b913539a97f5417474f6014de830ad6dee028dd8908e593b1e99c4cc88f400127214036e71112292e58a2ccffc48f57524aee90f9858d935c7a86297a90c7fe48b80f6c4e8df9eaae501ef40da7984502457255fbc8a9e1574ec6ba210be134f192)
n = int(0x64fc90f5ca6db24f7bfc6419de407596d29a9ecda526101b8d0eff2181e9b8ed1538a1cbabe4dfc5bcd899976e7739f8b448815b50db36a994c5b1df97981d562c663113fc5ee84f3206aecd18248fb4e9bddf205c8119e8437f7d6522e63d05bc357ae4969a4b3000b8226f8d142c23c4e38cdb0c385bf9564e8a115e4c52b7a2e3a9073a5d99d7bec3bca6452cf0c1b8d8b6b123cc6a6980cf14088d6a2bbb5ed36b85cb0003e535bd16d79ad54ff5b26e62f57de074654493d3a26a149786d5fbf61b42c9305092eb018aa3db3cb18b24f188ae520bd18acf9ffced09a2ba302a520f6e2bfd8eea9adc01eb8ee941181694a3ab493e1aa53fbbbf2851a591)
c = int(0x56ed81bbc149701110f0a15e2e6078ab926d74ee2c11b804ae4fad4333a25c247f38bb74867922438d10ce529b75f5ee5e29ce71d6f704cc0644f7e78d60a2af8921fbc49326280e3f0c00f2769e837363cbb05dc3f30bda8fdc94111fb025008eae562ae57029d5cfde6bdd09893a738187578d22f82a5f8769f093681662329f05b262c2054f91696a24f631ba8132f3d92ae7758c91fa9b5657e4944c5d5f93afb4af68908d004ae5f97071bcaceb7d0034297eeb897f972b44b0d7def52f46ee45d386a5e24ed613bf7e5177c6e10f69a3d3de0f0c30de0b15d360ee81da3d277a4acf47b6df389c24615884b692e604eba711fc28c34bc56227b8455705)
e = 65537

q=math.isqrt(-n+(x**2)//4)+(x//2)
p=x-q

phi=(p-1)*(q-1)

d=egcd(phi,e)[2]%phi
m=pow(c,d,n)

print(bytes.fromhex(hex(d)[2:]).decode('utf-8'))
```
Results in: `picoCTF{pl33z_n0_g1v3_c0ngru3nc3_0f_5qu4r35_24929c45}`
