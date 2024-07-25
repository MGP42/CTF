# Description
In RSA, a small e value can be problematic, but what about N? Can you decrypt this? values

# Provided
- [values](.prov/162-values)

# Progress
```
n: 831416828080417866340504968188990032810316193533653516022175784399720141076262857
```
8 digits characters, that's indeed very small...

How about a [Factorization Calculator](https://www.alpertron.com.ar/ECM.HTM)? Not going to do that myself.<br>
It says 6 Minutes, guess I will make some Tea.

Took it 9 Minutes, but who am I going to complain...
```
831 416828 080417 866340 504968 188990 032810 316193 533653 516022 175784 399720 141076 262857 (81 digits) = 1593 021310 640923 782355 996681 284584 012117 (40 digits) × 521911 930824 021492 581321 351826 927897 005221 (42 digits)
```
```
p =   1593 021310 640923 782355 996681 284584 012117 
q = 521911 930824 021492 581321 351826 927897 005221 
```

I could calculate that myself now, but I'm feeling lazy, so I will use a [Decipher](https://www.dcode.fr/rsa-cipher)

Error 0? Fine.... I do it myself -_-

For some reason, I decided to do it properly and went completely overkill for the task at hand.
Long story short, there is no an entire [python GUI](../../Tools/RSA%20Calculator.py). If I get bored enough I might even make it so values can be fed directly from console...

Anyway, I threw my values in the Tool and got the flag:
```
picoCTF{sma11_N_n0_g0od_23540368}
```