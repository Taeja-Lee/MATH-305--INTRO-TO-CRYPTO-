# Python code to implement Vigenere Cipher
# This code is contributed by Pratik Somwanshi
# Modified by Dr. Z at 6/15/2024

# This function generates the
# key in a cyclic manner until
# it's length isn't equal to
# the length of original text
def generateKey(string, key):
	key = list(key)
	if len(string) == len(key):
		return(key)
	else:
		for i in range(len(string) -
					len(key)):
			key.append(key[i % len(key)])
	return("" . join(key))
	
# This function returns the
# encrypted text generated
# with the help of the key
def Encryption(string, key):
	cipher_text = []
	for i in range(len(string)):
		x = (ord(string[i]) +
			ord(key[i])) % 26
		x += ord('A')
		cipher_text.append(chr(x))
	return("" . join(cipher_text))
	
# This function decrypts the
# encrypted text and returns
# the original text
def Decryption(cipher_text, key):
	orig_text = []
	for i in range(len(cipher_text)):
		x = (ord(cipher_text[i]) -
			ord(key[i]) + 26) % 26
		x += ord('A')
		orig_text.append(chr(x))
	return("" . join(orig_text))
	
# Driver code
if __name__ == "__main__":
	#string = "GEEKSFORGEEKS"
	#keyword = "AYUSH"
	plaintext = "CAMPBELLUNIVERSITY"
	keyword = "HOME"
	key = generateKey(plaintext, keyword)
	print("plainText: ", plaintext)
	print("key: ", keyword)
	print()
	cipher_text = Encryption(plaintext,key)
	print("Encrypted text :", cipher_text)
	print()
	decrypted_text = Decryption(cipher_text, key)
	print("Decrypted Text :", decrypted_text)

