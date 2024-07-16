# Description
Can you figure out how this program works to get the flag?
Connect to the program with netcat:
$ nc saturn.picoctf.net 61163
The program's source code can be downloaded here.

# Provided
[picker-II.py](401-picker-II.py)

# Progress
The 2nd Part to the [first]([400]%20Picker%20I.md)

I think this time i will start with the script directly as i know what to expect. It's filled with the 2 esoteric functions again, which i will ignore like the first time.
Seems like the loop got change:
~~~python
    user_input = input('==> ')
    if( filter(user_input) ):
      eval(user_input + '()')
~~~
~~~python
def filter(user_input):
  if 'win' in user_input:
    return False
  return True
~~~
so the method from last time doesn't work anymore. Is there another function i can call...
~~~python
def getRandomNumber():
def exit():
def esoteric1():
def win():
def esoteric2():
def filter(user_input):
~~~
Nope, that doesn't lead anywhere.... So what about taking `win` apart....<br>
i can call `open('flag.txt', 'r').read()`, but how to put it in print... What about:
~~~python
print(open('flag.txt', 'r').read()).strip
~~~
~~~
==> print(open('flag.txt', 'r').read()).strip
picoCTF{f1l73r5_f41l_c0d3_r3f4c70r_m1gh7_5ucc33d_0b5f1131}
'NoneType' object has no attribute 'strip'
~~~
I really expected it to throw the error before printing, but hey i take it.<br>
Fun fact: This skips the entire hex encoding loop, that forced me to decode it the first time
~~~ python
  for c in flag:
    str_flag += str(hex(ord(c))) + ' '
  print(str_flag)
~~~