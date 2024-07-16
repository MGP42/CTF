# Description
Can you figure out how this program works to get the flag?
Connect to the program with netcat:
$ nc saturn.picoctf.net 55290
The program's source code can be downloaded here.

# Provided
-[402-picker-III.py](.prov/402-picker-III.py)

# Progress
[Part I]([400]%20Picker%20I.md) and [Part II]([401]%20Picker%20II.md)

I start the same as in Part II by looking at the Code
~~~ python
while(USER_ALIVE):
  choice = input('==> ')
  if( choice == 'quit' or choice == 'exit' or choice == 'q' ):
    USER_ALIVE = False
  elif( choice == 'help' or choice == '?' ):
    help_text()
  elif( choice == 'reset' ):
    reset_table()
  elif( choice == '1' ):
    call_func(0)
  elif( choice == '2' ):
    call_func(1)
  elif( choice == '3' ):
    call_func(2)
  elif( choice == '4' ):
    call_func(3)
  else:
    print('Did not understand "'+choice+'" Have you tried "help"?')
~~~
That's way different... fine i will do it as in Part I
~~~
==> 
~~~
Only the arrow this time...
~~~
==> 
Did not understand "" Have you tried "help"?
==> help

This program fixes vulnerabilities in its predecessor by limiting what
functions can be called to a table of predefined functions. This still puts
the user in charge, but prevents them from calling undesirable subroutines.

* Enter 'quit' to quit the program.
* Enter 'help' for this text.
* Enter 'reset' to reset the table.
* Enter '1' to execute the first function in the table.
* Enter '2' to execute the second function in the table.
* Enter '3' to execute the third function in the table.
* Enter '4' to execute the fourth function in the table.

Here's the current table:

1: print_table
2: read_variable
3: write_variable
4: getRandomNumber
==>
~~~
That limits the options quite a bit.... Back to the code:
~~~python
def help_text():
  print(
  '''
This program fixes vulnerabilities in its predecessor by limiting what
functions can be called to a table of predefined functions. This still puts
the user in charge, but prevents them from calling undesirable subroutines.

* Enter 'quit' to quit the program.
* Enter 'help' for this text.
* Enter 'reset' to reset the table.
* Enter '1' to execute the first function in the table.
* Enter '2' to execute the second function in the table.
* Enter '3' to execute the third function in the table.
* Enter '4' to execute the fourth function in the table.

Here's the current table:
  '''
  )
  print_table()
~~~
This doesn't do shit
~~~python
def reset_table():
  global func_table

  # This table is formatted for easier viewing, but it is really one line
  func_table = \
'''\
print_table                     \
read_variable                   \
write_variable                  \
getRandomNumber                 \
'''
~~~
Neither does this....
~~~python
def call_func(n):
  """
  Calls the nth function in the function table.
  Arguments:
    n: The function to call. The first function is 0.
  """
  
  # Check table for viability
  if( not check_table() ):
    print(CORRUPT_MESSAGE)
    return
  
  # Check n
  if( n < 0 ):
    print('n cannot be less than 0. Aborting...')
    return
  elif( n >= FUNC_TABLE_SIZE ):
    print('n cannot be greater than or equal to the function table size of '+FUNC_TABLE_SIZE)
    return
  
  # Get function name from table
  func_name = get_func(n)
  
  # Run the function
  eval(func_name+'()')
~~~
This does tho...

So every legal n can call a function.... probably determined in `get_func(n)`
~~~python
def get_func(n):
  global func_table
  
  # Check table for viability
  if( not check_table() ):
    print(CORRUPT_MESSAGE)
    return
  
  # Get function name from table
  func_name = ''
  func_name_offset = n * FUNC_TABLE_ENTRY_SIZE
  for i in range(func_name_offset, func_name_offset+FUNC_TABLE_ENTRY_SIZE):
    if( func_table[i] == ' '):
      func_name = func_table[func_name_offset:i]
      break
  
  if( func_name == '' ):
    func_name = func_table[func_name_offset:func_name_offset+FUNC_TABLE_ENTRY_SIZE]
  
  return func_name
~~~
In short it calls a function from the `func_table`, which is a variable and variables can be edited
~~~
==> 3
Please enter variable name to write: func_table
Please enter new value of variable: "win"
==> 1
Table corrupted. Try entering 'reset' to fix it
~~~
OK it's not that simple. The only time times this messange can appear is here:
~~~ python
if( not check_table() ):
  print(CORRUPT_MESSAGE)
~~~
~~~python
def check_table():
  global func_table
  
  if( len(func_table) != FUNC_TABLE_ENTRY_SIZE * FUNC_TABLE_SIZE):
    return False
  
  return True
~~~
So... 4 entries 32 chars each....
editing the original could work
~~~
print_table                     \
read_variable                   \
write_variable                  \
win                             \
~~~
Now as one line:
~~~
"print_table                     read_variable                   write_variable                  win                             "
~~~
Let's see:
~~~
==> 3
Please enter variable name to write: func_table
Please enter new value of variable: "print_table                     read_variable                   write_variable                  win                             "
==> 4
0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b 0x37 0x68 0x31 0x35 0x5f 0x31 0x35 0x5f 0x77 0x68 0x34 0x37 0x5f 0x77 0x33 0x5f 0x67 0x33 0x37 0x5f 0x77 0x31 0x37 0x68 0x5f 0x75 0x35 0x33 0x72 0x35 0x5f 0x31 0x6e 0x5f 0x63 0x68 0x34 0x72 0x67 0x33 0x5f 0x61 0x31 0x38 0x36 0x66 0x39 0x61 0x63 0x7d
~~~
works like a charm. Now the same decoding process with [Cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')&input=MHg3MCAweDY5IDB4NjMgMHg2ZiAweDQzIDB4NTQgMHg0NiAweDdiIDB4MzcgMHg2OCAweDMxIDB4MzUgMHg1ZiAweDMxIDB4MzUgMHg1ZiAweDc3IDB4NjggMHgzNCAweDM3IDB4NWYgMHg3NyAweDMzIDB4NWYgMHg2NyAweDMzIDB4MzcgMHg1ZiAweDc3IDB4MzEgMHgzNyAweDY4IDB4NWYgMHg3NSAweDM1IDB4MzMgMHg3MiAweDM1IDB4NWYgMHgzMSAweDZlIDB4NWYgMHg2MyAweDY4IDB4MzQgMHg3MiAweDY3IDB4MzMgMHg1ZiAweDYxIDB4MzEgMHgzOCAweDM2IDB4NjYgMHgzOSAweDYxIDB4NjMgMHg3ZA) in Part I:
~~~
picoCTF{7h15_15_wh47_w3_g37_w17h_u53r5_1n_ch4rg3_a186f9ac}
~~~
