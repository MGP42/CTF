# Description
How about some hide and seek?

# Provided
- [unkown.zip](.prov/408-unkown.zip)
  - ukn_reality.jpg

# Progress
As this is an image the first thing i tend to do with it is throwing it into [https://www.aperisolve.com/](https://www.aperisolve.com/)<br>
The only interesting part seems to be the Strings part:
``` xml
JFIF
7http://ns.adobe.com/xap/1.0/
<?xpacket begin='
' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x='adobe:ns:meta/' x:xmptk='Image::ExifTool 11.88'>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
 <rdf:Description rdf:about=''
  xmlns:cc='http://creativecommons.org/ns#'>
  <cc:attributionURL rdf:resource='cGljb0NURntNRTc0RDQ3QV9ISUREM05fZGVjYTA2ZmJ9Cg=='/>
 </rdf:Description>
</rdf:RDF>
</x:xmpmeta>
```
Here one line looks suspicious:
`<cc:attributionURL rdf:resource='cGljb0NURntNRTc0RDQ3QV9ISUREM05fZGVjYTA2ZmJ9Cg=='/>`

This string looks like it's base64 encoded, so [CyberChef](https://gchq.github.io/CyberChef/) it is. One base64 decoding later i got the flag:
`picoCTF{ME74D47A_HIDD3N_deca06fb}`