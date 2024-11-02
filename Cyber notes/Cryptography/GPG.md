*GNU Privacy Guard: free open-source implementation of OpenPGP standard, allows users to encrypt and digitally sign data/communications, providing privacy and authentication through the use of public key cryptography.*

[GPG Tutorial](https://www.devdungeon.com/content/gpg-tutorial)

1. Create my key

`gpg --gen-key`: create private key
`gpg --export -a [public key] > [name of public key].asc`: export into .asc file for future use

2. Import partner's key

`gpg --show-keys [partner_key.asc]`: check if fingerprint matches
`gpg --import [partner_key.asc]`: import into keyring

3. Encrypt

`gpg --encrypt --sign --armor --recipient [partner public key] [file to be encrypted]`
*File will be encrypted in a file.asc format*

4. Decrypt

`gpg --decrypt [file.asc] > [file]`
___

OSINT tip:

`gpg --auto-key-locate keyserver --locate-keys [target email]`: automated method to locate keys based on email address

Techniques to detect if I was targeted by this:
`grep "keyserver" /var/log/syslog | grep "search-keys"`
`tcpdump port 11371 # Common keyserver port`