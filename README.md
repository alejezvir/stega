# stega

Encryption text in image with password, using PIL

This program works in two modes of operations: encryption and decryprion

Encryption:
Text to encrypt and password for input
Symbols of text and password are xoring element by element
Recived string of binary elements are encrypt in list of pixels
The new list of pixels uses for writing in  new image

Decryption:
List of pixels are reading 
You got an decrypted text
