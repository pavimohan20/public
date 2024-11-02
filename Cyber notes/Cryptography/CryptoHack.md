`chr(i)`: translate i (integer) into corresponding ASCII character
\><`ord(c)`

`bytes.fromhex(h)`: convert hexadecimal to ASCII number to character
\><`hex(b)`: returns hex (has the prefix `0x` that may need to be removed)

Base64 uses a 64 characters alphabet to encode binary data

`import base64` > `base64.b64encode()`


To encrypt, messages need to be converted into numbers on which mathematical operations can be applied
```
message: HELLO  
ascii bytes: [72, 69, 76, 76, 79]  
hex bytes: [0x48, 0x45, 0x4c, 0x4c, 0x4f]  
base-16: 0x48454c4c4f  
base-10: 310400273487
```
*to decrypt you simply follow the reverse path*


XOR compares bits, if they are the same then it returns 0, otherwise 1. The operator is either noted "⊕" or "^"
`0110 ^ 1010 = 1100`

