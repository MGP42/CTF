# Description
Morse code is well known. Can you decrypt this?
Download the file here.
Wrap your answer with picoCTF{}, put underscores in place of pauses, and use all lowercase.

# Provided
- [morse_chal.wav](.prov/280-morse_chal.wav)

# Progress
Yeah, I'm not a seaman and can't even write down the dots and lines at this speed. So I could look at the wave and decode it by hand:
![](.img/280-1.png)
or I just use a decoder like [this one](https://databorder.com/transfer/morse-sound-receiver/)
This provides me with the string: `WH47 H47H 90D W20U9H7`

As per wishes in the description, I throw that in python (not even sure if that was faster than just doing it real quick myself):
`print("picoCTF{"+str("WH47 H47H 90D W20U9H7").lower().replace(' ','_')+"}")`<br>
which results in: `picoCTF{wh47_h47h_90d_w20u9h7}`