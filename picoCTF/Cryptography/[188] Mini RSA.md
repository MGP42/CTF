# Description
What happens if you have a small exponent? There is a twist though, we padded the plaintext so that (M ** e) is just barely larger than N. Let's decrypt this: ciphertext

# Provided
- [ciphertext](.prov/188-ciphertext)

# Progress
Looking at the ciphertext i get n,e and c.

Considering the description says they chose the values in a way that m^e is barely larger than n, i would assume that m^e=n+c.

As i do not know of a method that can take roots beyond the 2nd for this large numbers in python, i will build my own:
``` python
x=c+n

m=0
t=n
while t!=0:
  t=t//2
  if (m+t)**e<=x:
    m+=t

print(bytes.fromhex(hex(m)[2:]).decode('utf-8'))
```
result: `ValueError: non-hexadecimal number found in fromhex() arg at position 279`

OK.. WHAT, time to check the number: `print(x-m**e)`
```
53690904607441300842623774254422904516338120701013132159503798261511788781376027348776750293293605383900657721713388037584821966655703968595695345880067460570648215781229748813294245391141910490739151135723970007424766595416096198269487821149079787015000596060891514110094060560283490270685053083360778145311167212082930314400742124100893467531343897984287701485205071107465839161616565818073114662094169514360820428536393159463893556023653095222080303473431320895112822776284288010914639257590633803103412270389106318880328581927189474406588633189697592186964288584487711297418970723365897410411664938824887363085829983250571598941161110893941788226521454070550791964153
```

Yeah that's definitely the wrong number.... Checking above and below:
``` python
print(x-(m-1)**e)
print(x-(m+1)**e)
```
``` python
113794816745817931452802938576779487664025287032134233430016847098436799107421202560152440066076342811104210282113625056814786668935392782290706296270207904330014870382613350129193825425271127494606176249564551582448344324162221840832311760683310215059563165533204805184370606946606190377054405015899751686424059741676477542267130618651427699974095582079930069091082078400737692341804490785099443843170439236415766327890738824659481544767677952680853310451042951138606897353103249769109784230946996319034186384654126414700610938368305993115698132999982576080743578800419843150989476248093783335584468758895873466803116638359539202544034843441507368312500924083505328020580

-6413007530935329767555390067933678631349045630107969111009250575413221544669147862598939479489132043302894838686848981645142735623984845099315604510072983188718438820153852502605334642987306513127873978116611567598811133330029444293336118385150641029561973411421776964182485826039209835684298849178195395801725317510616913465646370450490027500752518502600567069155940391054045690463186066934260435072333912005640350544154490347556900417037131253403738241111104362857797046916092176056080200716498011782097165348107536297503189379375391082265246946104083359524121817900506864585297537280032009239928765587914726535407513589369756011717279148384455246328864214577320802038
```
FUCK.... looks like barely larger is larger than i expected, time to wrap the entire thing in a loop to test for higher multipliers of n:
``` python
m=0
c_full=c
c_guess=0

while c_guess!=c_full:
  c_full+=n
  step=n
  while step!=0:
    step=step//2
    c_guess=(m+step)**e
    if c_guess<=c_full:
      m+=step

print(m)
print(bytes.fromhex(hex(m)[2:]).decode('utf-8'))
```
Yeah, that's already running for a minute, pretty sure it will find it eventually, but i might as well optimize it in the meantime. While resetting step everytime to n works just fine it is very slow and totally unnecessary. A number slightly bigger than the 3rd root should do
``` python
step_max=0
step=n
while step>0:
  step=step//2
  if (step_max+step)**3<n:
    step_max+=step
```
Oh well the original version already finished and gave me the result:
``` python
1787330808968142828287809319332701517353332911736848279839502759158602467824780424488141955644417387373185756944952906538004355347478978500948630620749868180414755933760446136287315896825929319145984883756667607031853695069891380871892213007874933611243319812691520078269033745367443951846845107464675742664639073700700745451895920079741
picoCTF{e_sh0u1d_b3_lArg3r_a166c1e3}
```

*This was pure luck, this code should not have gotten a result. I will provide a working code further down*

# Improvement
Just cause it stopped doesn't mean i'm done. Having the problem solved also means i can debug it faster. Dividing m**e by n results in 3533, which allows me to start the rotuine already more than 3000 steps in.<br>
``` python 
c_full=c+n*3530
```

Time to implement:
``` python
step_max=0
step=n
while step>0:
  step=step//2
  if (step_max+step)**3<n:
    step_max+=step


m=0
c_full=c+n*3530
c_guess=0

while c_guess!=c_full:
  c_full+=n
  step=step_max
  while step!=0:
    step=step//2
    c_guess=(m+step)**e
    if c_guess<=c_full:
      m+=step

print(m)
print(bytes.fromhex(hex(m)[2:]).decode('utf-8'))
```
Well, this doesn't work. Make sense as i have rounded down the root calculation while i should have rounded it up:
``` python
step=step_max+1
```
Still doesn't work... Odd
``` python
step=step_max*2
```
Hold on still not?? Why?? Cause i did not consider that m is already partially set when reaching the 3530 loop...
I can calculate the state at 3530 to solve that tho.
``` python
#calculate root(n,e)
step_max=0
step=n
while step>0:
  step=step//2
  if (step_max+step)**e<n:
    step_max+=step
step_max+=1

m=step_max  #cause that's the minimum it will need anyway
c_full=c  
c_guess=0

#calculate c
while c_guess!=c_full:
  c_full+=n
  step=step_max  #higher is ridicolous and slow
  while step!=0:
    c_guess=(m+step)**e
    if c_guess<=c_full:
      m+=step
    step=step//2
  c_guess=m**e

print(m)
print(bytes.fromhex(hex(m)[2:]).decode('utf-8'))
```
I'm not sure if that's even close to optimal but it did run in 20 seconds instead of 3 minutes, which is fast enough for now

# I'm a fucking idiot
Nevermind, this is complete garbage, there is so much wrong with this:
```
step=step//2
```
This is incredibly stupid. Looking at a step starting at 23 and the following loops:
```
23
11
5
2
1
0
```
1+2+5+11=19 So it the potential necessary steps for 20, 21 and 22 are missing. It's a miracle that i got a result in the first place. To fix that i will change that to:
``` python
step=(step+1)//2
```
which will always round for the ceiling instead of the floor. Looking at 23 again:
```
23
12
6
3
2
1
0
```
1+2+3+6+12=24 So it can get all the numbers. But i need an additional if clause, because:
``` python
step=1
step=(step+1)//2
step=(1+1)//2
step=1
```
which means step can never be 0 and i can't stop at 1 already as for example 8:
```
8
4
2
1
0
```
2+4=6 missing the 7. So with the ifclause this is an actual working code:
``` python
while c_guess!=c_full:
c_full+=n
step=step_max
while step>0:
  c_guess=(m+step)**e
  if c_guess<= c_full:
    m+=step
    c_store=c_guess
  if step==1:
    step=0
    c_guess=c_store
  step=(step+1)//2
```
But now numbers can get bigger than the already checked one, which means unnecessary checks... Hold on i do a binary search anyway so just choose m=2^x.

This also solves the floor problem, which means step=step//2 this works again and i do not have to do an additional check when reaching 1...
``` python
step=2
while step<=step_max:
  step=step*2
step_max=step
```
So one if clause and one addition less than before.... progress!!

All this results in this:
``` python
#calculate root(n,e)
step_max=0
step=n
while step>0:
  step=step//2
  if (step_max+step)**e<n:
    step_max+=step
step_max+=1

step=2
while step<=step_max:
  step=step**2
step_max=step

m=0
c_full=c-n
c_guess=0
#calculate c
while c_guess!=c_full:
  c_full+=n
  step=step_max
  while step>0:
    c_guess=(m+step)**e
    if c_guess<= c_full:
      m+=step
      c_store=c_guess
    step=step//2
  c_guess=c_store

print(m)
print(bytes.fromhex(hex(m)[2:]).decode('utf-8'))
```
And it also runs in 20 seconds.