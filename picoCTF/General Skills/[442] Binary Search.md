# Description
Want to play a game? As you use more of the shell, you might be interested in how they work! Binary search is a classic algorithm used to quickly find an item in a sorted list. Can you find the flag? You'll have 1000 possibilities and only 10 guesses.
Cyber security often has a huge amount of data to look through - from logs, vulnerability reports, and forensics. Practicing the fundamentals manually might help you in the future when you have to write your own tools!

# Provided
- [challenge.zip](.prov/442-challenge.zip)
  - home
    - ctf-player
      - drop-in
        - guessing_game.sh

# Analyse

Reading the script following part comes to my attention:
```
if (( guess < target )); then
    echo "Higher! Try again."
	elif (( guess > target )); then
		echo "Lower! Try again."
    else
		echo "Congratulations! You guessed the correct number: $target"
```

So it seems the script provides the information if the guess was above or below the flag.
As $2^{24} < 1000$ i should be able to solve this by always guessing the middle of the remaining possibilities.
In other words in every step guess: $\lfloor\frac{\text{highest posibility}-\text{lowest posibility}}{2}\rfloor+\text{lowest psoibility}$

As i do not have the flag file myself (duh) i launch the instance:

I then get provided:
- `ssh -p 53087 ctf-player@atlas.picoctf.net`
- `83dcefb7` (password)


# Progress
I connect and the game instantly starts:

Using the formula i set up earlier $ \lfloor\frac{1000-1}{2}\rfloor+1=500$<br>
I get higher as an answer.

I repeat with: $\lfloor\frac{1000-501}{2}\rfloor+501=750$<br>
Higher again.

Repeat:

| smallest | biggest | guess | result |
| --- | --- | --- | --- |
| 1 | 1000 | 500 | higher |
| 501 | 1000 | 750 | higher |
| 751 | 1000 | 875 | lower |
| 751 | 874 | 812 | higher |
| 813 | 874 | 843 | higher |
| 844 | 874 | 859 | higher |
| 860 | 874 | 867 | lower |
| 860 | 866 | 863 | lower |
| 860 | 862 | 861 | lower |
| 860 | 860 | 860 | correct |

`picoCTF{g00d_gu355_ee8225d0}`

# Simplification
Use Python:
``` python
x=1000
y=1
while True:
  z = (x-y)//2+y
  a=input("guess: "+str(z)+" (h)igher (l)ower (c)orrect: ")
  if a=='h':
    y=z+1
  elif(a=='l'):
    x=z-1
  if(x==y or a=='c'):
    print(str(x)+ " is the number")
    quit()
```