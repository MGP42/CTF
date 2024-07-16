# Description
People keep trying to trick my players with imitation flags. I want to make sure they get the real thing! I'm going to provide the SHA-256 hash and a decrypt script to help you know that my flags are legitimate.

# Provided
- [challenge.zip](.prov/450-challenge.zip)
  - files/
  - checksum.txt
  - decrypt.sh

# Progress
`sha256sum files/*` provides all hashes of the files in the files folder
```
4666cbea94c25fe9c9f3bf5066a8c911d451a9add3edf33cf0dded9877ea74d0  files/047MJYW7
48985dcd07f0571bb58e7c1a78ec18ea53a0d867f4d2e1e45adb8b3467b51a73  files/0CbGv6a3
74a7a6b4fc16b48a5285abd3bc0b823e6a1cda7d3f9fcacbd58120d98fbb4e13  files/0E56AVSC
0cfdd4d83c0d0978dc1b4169bb73e3fd84f9c05ca1a6edb400dd86fd107de484  files/0QUxtltc
464a72f5728ae07e79965aae147fcb3e78494d0255f7bb9bc3531a50a4ddd8ec  files/0XKkalUj
```

`cat checksum.txt` provides the sha256 hash we're looking for:
```
467a10447deb3d4e17634cacc2a68ba6c2bb62a6637dad9145ea673bf0be5e02
```

Considering the huge number of files i decided to use `sha256sum` again and pipe it into `grep`:<br>
`sha256sum files/* | grep 467a10447deb3d4e17634cacc2a68ba6c2bb62a6637dad9145ea673bf0be5e02`<br>
produces:
```
467a10447deb3d4e17634cacc2a68ba6c2bb62a6637dad9145ea673bf0be5e02  files/c6c8b911
```

I then try to decrypt the found file with:<br>
`decrypt.sh files/c6c8b911`

This results in:<br>
`picoCTF{trust_but_verify_c6c8b911}`

# All in One
To do it all in one line i use `sha256sum` and pipe the result into `grep`. I then use `cut` to extract the file name. I wrap the entire thing with `$()` so i can use it as argument for the decrypt script.

`decrypt.sh $(sha256sum files/* | grep $(cat checksum.txt) | cut -d' ' -f3)`