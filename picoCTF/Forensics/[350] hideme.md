# Description
Every file gets a flag.
The SOC analyst saw one image been sent back and forth between two people. They decided to investigate and found out that there was more than what meets the eye.

# Provided
- [flag.png](.prov/350-flag.png)

# Progress
As this is an image the first thing i do is to throw it into [https://www.aperisolve.com/](https://www.aperisolve.com/)

Binwalk detected a zip in this png, so i downloaded the binwalk archive:
the archive contains a secret folder with another flag.png
![](./.img/350-1.png)
`picoCTF{Hiddinng_An_Imag3_within_@n_image_d55982e8}`

