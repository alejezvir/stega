
from PIL import Image
import numpy as np
import random
import tkinter


def shortest_sequence_range(*args): 
	return range(len(sorted(args, key=len)[0]))

# кодирование текста по заполненному паролю
def create_datasets_to_code (password, text):

	g = ((password[i], text[i])							
   		for i in shortest_sequence_range(password,text) )
	arr=[]

	for item in g:
		arr.append(ord(item[0])^ord(item[1]))			# xor Пароля и текста

	return arr


array_bin_codem=[]
pixels=[]
encryption_pixels = []

def encr_pass(password,pixels):
	pixels[0] = len(password)
	return pixels

# кодирует в массив пикселей информацию 
def encryption (code_message, pixels, password):
	
	array_bin_codem=[]
	zstring = '0'

	for i in code_message:
		a = bin(i)[2:]

		while len(a) != 8:
			a = zstring+a

		for j in a:
			array_bin_codem.append(int(j))

	g = ([array_bin_codem[i], pixels[i]]
		for i in shortest_sequence_range(array_bin_codem,pixels))

	for item in g:
		if (item[0] == 1) and (item [1] % 2 == 0):
			item[1] = item[1] + 1
		if (item[0] == 0) and (item [1] % 2 != 0):
			item[1] = item[1] - 1
		encryption_pixels.append(item[1])

	return encryption_pixels


# восстановление пароля по его длине
def auto_password_eq_passwordnew (password, len_password):
	i = 0
	while i < len_password:
		if len(password) != len_password:
			for a in password:
				password= password+a
				if len(password) == len_password:
						break
		i=i+1
	return password

# автосаполнение пароля
def auto_password_eq_text (password, text):
	i = 0
	while i < len(text):
		if len(password) != len(text):
			for a in password:
				password= password+a
				if len(password) == len(text):
						break
		i=i+1
	return password

# расшифровка сообщения (работает при автозаполненом по длине паролю и с одинаковой точкой входа)
def decryption(encryption_pixels, passwd):

	decryption_bin_pixels=[]
	decryption_bin_pixels_new = []
	decryption_dec_pixels = []
	a=[]

	for i in encryption_pixels:
		if i % 2 == 1:
			decryption_bin_pixels.append(1)
		if i % 2 == 0:
			decryption_bin_pixels.append(0)
	
	decryption_bin_pixels_new =[decryption_bin_pixels[d:d+8] for d in range(0, len(decryption_bin_pixels), 8)]
	arr=[]
	
	for i in decryption_bin_pixels_new:
		a =''.join(map(str,i))
		arr.append(int(a,2))

	g = ([ord(passwd[i]), arr[i]]
		for i in shortest_sequence_range(passwd,arr))

	arr_msg = []

	for item in g:
		a = item[0]^item[1]
		arr_msg.append(chr(a))

	msg = ''.join(arr_msg)

	return msg


# Основная часть программы
def main():

	img = Image.open(input("path to img: "))
	pix=img.load()
	width = img.size[0]
	height = img.size[1]
	pix=img.load()


	arr_pix=[]
	for i in range (width):
		for j in range (height):
			arr_pix.append(pix[i,j][0])
			arr_pix.append(pix[i,j][1])
			arr_pix.append(pix[i,j][2])


	print ( 'to encrypt type: "encryption" ' ,'\n'
			'to decrypt type: "decryption" ')

	vvod = input('your choice? ')

	if vvod == 'encryption':
		input_text = input('type text: ')
		passwd = (input ('your password: '))
		print ('yor text:        ', input_text)
		print ('your password:   ', passwd)

		passwd = auto_password_eq_text(passwd, input_text)
		code_message = create_datasets_to_code(passwd,input_text)
		encr_pass(passwd,arr_pix)
		test = encryption(code_message,arr_pix[ord(passwd[0]):], passwd)
		img.putpixel((0,0), (arr_pix[0], arr_pix[1], arr_pix[2]))

		a = 0 
		while a != len(arr_pix):								# меняем исходный массив пикселей закодированными пикселями
			if len(test) == a:
				break
			arr_pix[a+ord(passwd[0])] = test[a]
			a=a+1

		arr_pix3 =[arr_pix[d:d+3] for d in range(0, len(arr_pix), 3)]
		i=0
		j=0
		pi = 0
		count = 0

		while count != len(arr_pix3):
			img.putpixel((i,j), (arr_pix3[pi][0], arr_pix3[pi][1], arr_pix3[pi][2]))
			pi = pi + 1 
			j = j + 1
			if j == height:
				i = i+1
				j = 0
			count = count +1

		img.save(input('type path to save: '), "BMP")
		print ('your file have been saved')

	if vvod =='decryption':
		passwd = input('type password: ')
		passwd = auto_password_eq_passwordnew(passwd, pix[0,0][0] )
		print('message in the image: ',decryption (arr_pix[ord(passwd[0]):], passwd))

main()

