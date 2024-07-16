# Description
Our data got corrupted on the way here. Luckily, nothing got replaced, but every block of 3 got scrambled around! The first word seems to be three letters long, maybe you can use that to recover the rest of the message.

# Provided
[message.txt](.prov/312-message.txt)

# Progress
message.txt:
```
heTfl g as iicpCTo{7F4NRP051N5_16_35P3X51N3_V9AAB1F8}7
```

Just from looking at this i already see what happened... The first character of every block of 3 moved to the right. So just move it back to the left...

Well but what if i hadn't seen that... The Description already provides the hint that blocks of 3 got scrambeled. There are exactly `3! = 6`posibilities in which way 3 characters can be ordered.
```
123
132
213
231
312
321
```

Time for coding:
``` python
c="heTfl g as iicpCTo{7F4NRP051N5_16_35P3X51N3_V9AAB1F8}7"
size=3

c=[c[i:i+size] for i in range(0,len(c),size)]

out=""
for i in c:
  out+=i[2]+i[0]+i[1]

print(out)
```

```
The flag is picoCTF{7R4N5P051N6_15_3XP3N51V3_A9AFB178}
```
# Beyond
So much for the solution, but what if i wouldn't have known the "key"
``` python
from itertools import permutations

c="heTfl g as iicpCTo{7F4NRP051N5_16_35P3X51N3_V9AAB1F8}7"
size=3

c=[c[i:i+size] for i in range(0,len(c),size)]

keys=permutations(range(size))

for key in keys:
  out=""
  for i in c:
    for j in key:
      out+=i[j]
  print(out)
```
```
heTfl g as iicpCTo{7F4NRP051N5_16_35P3X51N3_V9AAB1F8}7
hTef lga si ipcCoT{F74RNP5015N_61_53PX35N13V_9AABF187}
ehTlf  ga sicipTCo7{FN4R0P5N151_63_53PX15N_3VA9A1BF}87
eThl f ag iscpiToC7F{NR405PN5116_35_3XP1N5_V3AA91FB}78
The flag is picoCTF{7R4N5P051N6_15_3XP3N51V3_A9AFB178}
Teh lfa gi spcioTCF7{RN450P5N161_53_X3PN15V_3AA9F1B7}8
```
could be expanded with
``` python
if "pico" in out:
  quit()
```
to stop after getting the flag the first time. This could cause multiple different issues especially when dealing with longer blocks. A way better option would be to only print when the string contains a known plaintext.



