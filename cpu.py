import sys
from random import randint
from time import time

class CPU():
	def iniciar(self, pixels):
		# define os valores de fonte, com um tamanho de 80
		self.fontset = [0xF0, 0x90, 0x90, 0x90, 0xF0, 
		0x20, 0x60, 0x20, 0x20, 0x70, 
		0xF0, 0x10, 0xF0, 0x80, 0xF0, 
		0xF0, 0x10, 0xF0, 0x10, 0xF0, 
		0x90, 0x90, 0xF0, 0x10, 0x10, 
		0xF0, 0x80, 0xF0, 0x10, 0xF0, 
		0xF0, 0x80, 0xF0, 0x90, 0xF0, 
		0xF0, 0x10, 0x20, 0x40, 0x40, 
		0xF0, 0x90, 0xF0, 0x90, 0xF0, 
		0xF0, 0x90, 0xF0, 0x10, 0xF0, 
		0xF0, 0x90, 0xF0, 0x90, 0x90, 
		0xE0, 0x90, 0xE0, 0x90, 0xE0, 
		0xF0, 0x80, 0x80, 0x80, 0xF0, 
		0xE0, 0x90, 0x90, 0x90, 0xE0, 
		0xF0, 0x80, 0xF0, 0x80, 0xF0, 
		0xF0, 0x80, 0xF0, 0x80, 0x80]
		# inicia a memoria com 4K 
		self.memory = [0] * 4096
		# inicia os opcodes
		self.opcode = 0
		#inicia o contador do programa 512 bytes, pois o 
		# resto esta reservado para o interpretador CHIP8 
		self.pc = 0x200
		#inicia o contador de pilha
		self.sp = 0
		#inicia o indicador
		self.I = 0
		# inicia os 16 registradores de V0 a VF
		self.V = [0] * 16
		#inicia o array com os pixels da tela
		self.pixels = [0] * pixels
		#inicia a pilha
		self.pilha = []
		#inicia a Bandeira para avisar o desenho
		self.Bandeira = True
		#inicia as teclas
		self.teclas = [0] * 16
		#declara o tempo
		self.tempo = time()
		# controlador de resolucao
		self.schip = False
		#inicia o RPL
		self.rpl = 0

		self.scroll = -1


		#self.src_ch = [0] * (128*64)


		#Temporizadores
		#inicia o temporizador de som
		self.som = 0
		#inicia o temporizador de atraso
		self.delay = 0

		#carrega as fontes para os endereços 0x00 a 0x50 (80 campos)
		for i in range(len(self.fontset)):
			self.memory[i] = self.fontset[i]

		print('valores iniciados')

	def load_game(self, game):
		#abre o jogo
		with open(game, 'rb') as f:
			byte_game = f.read()
			for i in range(len(byte_game)):
				# grava o jogo depois dos 512 bytes(0x200)
				self.memory[self.pc + i] = byte_game[i]
			print(self.memory)

	def desenhar_normal(self, x_pos, y_pos, n):
		self.V[0xF] = 0
		pixel = 0
		for y in range(n): #altura
			pixel = self.memory[self.I + y]
			for x in range(8): #8
				i = x_pos + x + ((y_pos + y) * 64)
				if pixel &  ( 0x80  >>x ) != 0 and not (y + y_pos >= 32 or x + x_pos >= 64):
					if self.pixels[i] == 1:
						self.V[0xF] = 1
					self.pixels[i] ^= 1
		self.Bandeira = True


	def desenhar_extendido(self, x_pos, y_pos, n):
		self.V[0xF] = 0
		pixel = 0
		for y in range(n): #altura
			for x_bytes in range(2):
				pixel = self.memory[self.I + y]
			for x in range(16): #8
				i = x_pos + x + ((y_pos + y) * 128) #128
				if pixel &  ( 0x100  >>x ) != 0 and not (y + y_pos >= 64 or x + x_pos >= 128): #0x100#0x80
					if self.pixels[i] == 1:
						self.V[0xF] = 1 #0x20#0xF
					self.pixels[i] ^= 1
		self.Bandeira = True

	def emular(self):
		self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1] 
	
		vx = (self.opcode & 0x0F00) >> 8
		vy = (self.opcode & 0x00F0) >> 4

		print('opcode=',hex(self.opcode))
		#print(hex(self.pc))

		#print('talvez este opcode',hex(self.opcode & 0x0F00 != 0x0000))
		if (self.opcode & 0xF000 == 0x0000):
				#00E0
			if(self.opcode == 0x00E0):
				for i in range(len(self.pixels)):
					self.pixels[i] = 0
				self.Bandeira = True
				print('00E0')

				#00EE
			elif(self.opcode == 0x00EE):
				self.pc = self.pilha.pop()
				print('00EE')
#--------------------------------------------------------------
#				SUPERCHIP-8 REGISTERS

				#00CN rola a tela n pixels para baixo
			#elif(self.opcode == 0x00C1):
				#print('00CN')


				#00FB rola a tela 4 pixels à direita
			#elif(self.opcode == 0x00FB):
				#self.scroll = 1

				'''
				for y in range(128):			
					for x in range(64-1,3,-1):
						self.pixels[x+ 64 * y] = self.pixels[(x-4) + 64*y]
						self.src_ch[x + (64 * y)] = 1
					for x in range(4):
						self.pixels[x + 64 * y] = 0
						self.src_ch[x + 64 * y] = 1
				print('00FB')
				'''


				#00FC rola a tela 4 pixels à esquerda
			elif(self.opcode == 0x00FC):
				self.scroll = 0
				#self.Bandeira = True
				print('00FC')

			   #00FD Sai do interpretador chip8
			elif(self.opcode == 0x00FD):
				#break
				print('00FD')	

#----------------------------------------------------------


				#00FE - Ajusta a tela para 64x32
			elif(self.opcode == 0x00FE):
				from main import setup
				size = 64 * 10, 32 *10
				setup(size)
				pixels = 64 * 32
				self.pixels = [0] * pixels
				self.schip = False
				print('00FE')

				#00FF - Redimensiona a tela para 128x64
			elif(self.opcode == 0x00FF):
				from main import setup
				size = 128 *10, 64 *10 
				setup(size)
				pixels = 128 * 64
				self.pixels = [0] * pixels 
				self.schip = True
				print('00FF')

				#0NNN
			elif(self.opcode & 0X0FFF != 0x0000):
				self.pc = (self.opcode & 0X0FFF) -2
				print('0NNN')


			else:
				self.pc -= 2

			#1NNN
		elif(self.opcode & 0xF000 == 0x1000):
			self.pc = (self.opcode & 0X0FFF) - 2
			print('1NNN')

			#2NNN
		elif(self.opcode & 0xF000 == 0x2000):
			self.pilha.append(self.pc)
			self.pc = (self.opcode & 0x0FFF) - 2
			print('2NNN')

			#3XNN
		elif(self.opcode & 0xF000 == 0x3000):
			if self.V[vx] == self.opcode & 0x00FF:
				self.pc += 2
			print('3XNN')

			#4XNN
		elif(self.opcode & 0xF000 == 0x4000):
			if self.V[vx] != self.opcode & 0x00FF:
				self.pc += 2
			print('4XNN')


			#5XNN
		elif(self.opcode & 0xF000 == 0x5000):
			if self.V[vx] == self.V[vy]:
				self.pc +=2
			print('5XNN')


			#6XNN
		elif(self.opcode & 0xF000 == 0x6000):
			self.V[vx] = self.opcode & 0x00FF
			print('6XNN')

			#7XNN
		elif(self.opcode & 0xF000 == 0x7000):
			self.V[vx] += self.opcode & 0x00FF
			self.V[vx] &= 0XFF
			print('7XNN')

			#8
		elif(self.opcode & 0xF000 == 0x8000):
			l = self.opcode & 0x000F
			print('l =', hex(l))

				#8XY0
			if(l == 0x0000):
				self.V[vx] = self.V[vy]
				print('8XY0')

				#8XY1
			elif(l == 0x0001):
				self.V[vx] = self.V[vx] | self.V[vy]
				print('8XY1')

				#8XY2
			elif(l == 0x0002):
				self.V[vx] = self.V[vx] & self.V[vy]
				print('8XY2')

				#8XY3
			elif(l == 0x0003):
				self.V[vx] = self.V[vx] ^ self.V[vy]
				print('8XY3')

				#8XY4
			elif(l == 0x0004):
				self.V[vx] += self.V[vy]
				if self.V[vx] > 0xFF:
					self.V[0xF] = 1
				else:
					self.V[0xF] = 0
				self.V[vx] &= 0xFF
				print('8XY4')

				#8XY5
			elif(l == 0x0005):
				if self.V[vx] < self.V[vy]:
					self.V[0xF] = 0
				else:
					self.V[0xF] = 1
				self.V[vx] -= self.V[vy]
				self.V[vx] &= 0xFF
				print('8XY5')

				#8XY6
			elif(l == 0x0006):
				self.V[0xF] = self.V[vx] & 0x01 
				self.V[vx]  = self.V[vx] >> 1
				print('8XY6')

				#8XY7
			elif(l == 0x0007):
				if self.V[vx] > self.V[vy]:
					self.V[0xF] = 0
				else:
					self.V[0xF] = 1
				self.V[vx] = self.V[vy] - self.V[vx]
				self.V[vx] &= 0xFF
				print('8XY7')

				#8XYE
			elif(l == 0x000E):
				self.V[0xF] = self.V[vx] & 0x80
				self.V[vx]  = self.V[vx] << 1
				print('8XYE')

			else:
				self.pc -=2

			#9XNN
		elif(self.opcode & 0xF000 == 0x9000):
			if self.V[vx] != self.V[vy]:
				self.pc += 2
			print('9XNN')

			#ANNN
		elif(self.opcode & 0xF000 == 0xA000):
			self.I = self.opcode & 0x0FFF
			print('ANNN')

			#BNNN
		elif(self.opcode & 0xF000 == 0xB000):
			self.pc = (self.opcode & 0x0FFF) + self.V[0x0] -2
			print('BNNN')

			#CXNN
		elif(self.opcode & 0xF000 == 0xC000):
			rand = randint(0, 0xFF)
			self.V[vx] = rand & (self.opcode & 0x00FF)
			print('CXNN')

			#DXYN
		elif(self.opcode & 0xF000 == 0xD000):
			xcord = self.V[vx]
			ycord = self.V[vy]
			altura = self.opcode & 0x000F
			pixel = 0
			self.V[0xF] = 0
			#print(altura)
			#input('parei:')


			if self.schip == True:
				self.desenhar_extendido(xcord, ycord, altura)

			elif self.schip == True and altura == 0:
				self.desenhar_extendido(xcord, ycord, 16)
				input('ok')

			else:
				self.desenhar_normal(xcord, ycord, altura)

			'''

			elif self.schip == True:
				for y in range(altura): #altura
					pixel = self.memory[self.I + y]
					for x in range(8): #8
						i = xcord + x + ((ycord + y) * 128) #128
						if pixel &  ( 0x80  >>x ) != 0 and not (y + ycord >= 64 or x + xcord >= 128): #0x100#0x80
							if self.pixels[i] == 1:
								self.V[0xF] = 1 #0x20#0xF
							self.pixels[i] ^= 1
				self.Bandeira = True

			else:
				for y in range(altura): #altura
					pixel = self.memory[self.I + y]
					for x in range(8): #8
						i = xcord + x + ((ycord + y) * 64)
						if pixel &  ( 0x80  >>x ) != 0 and not (y + ycord >= 32 or x + xcord >= 64):
							if self.pixels[i] == 1:
								self.V[0xF] = 1
							self.pixels[i] ^= 1

				#print('DXY0')

				self.Bandeira = True
				print('DXYN')
		'''

			#E
		elif(self.opcode & 0xF000 == 0xE000):
				#EX9E
			if (self.opcode & 0x00FF == 0x009E):
				if self.teclas[self.V[vx]] == 1:
					self.pc += 2
				print('EX9E')

				#EXA1
			elif(self.opcode & 0x00FF == 0X00A1):
				if self.teclas[self.V[vx]] == 0:
					self.pc += 2
				print('EXA1')

			else:
				self.pc -= 2

			#F
		elif(self.opcode & 0xF000 == 0xF000):
			nn = self.opcode & 0x00FF

				#FX07
			if (nn == 0x0007):
				self.V[vx] = self.delay
				print('FX07')

				#FX0A
			elif(nn == 0x000A):
				tecla = -1
				for i in range(len(self.teclas)):
					if self.teclas[i] == 1:
						tecla = i
						break

				print('FX0A')

				if tecla >= 0:
					self.V[vx] = tecla
				else:
					self.pc -= 2
				print('FX0A')

				#FX15
			elif(nn == 0x0015):
				self.delay = self.V[vx]
				print('FX15')


				#FX18
			elif(nn == 0x0018):
				self.som = self.V[vx]
				print('FX18')

				#FX1E
			elif(nn == 0x001E):
				self.I += self.V[vx]
				print('FX1E')

				#FX29
			elif(nn == 0x0029):
				self.I = self.V[vx] * 5
				print('FX29')

#---------------------------------------------------
#			REGISTRADOR SUPERCHIP-8

				#FX30
			elif(nn == 0x0030):
				self.I = self.V[vx] * 10
				print('FX30')

#---------------------------------------------------


				#FX33
			elif(nn == 0x0033):
				self.memory[self.I] = self.V[vx] //100
				self.memory[self.I + 1] = (self.V[vx] //10) % 10
				self.memory[self.I + 2] = (self.V[vx] % 100) % 10
				print('FX33')

				#FX55
			elif(nn == 0x0055):
				for n in range(vx + 1):
					self.memory[self.I + n] = self.V[n]
				print('FX55')

				#FX65
			elif(nn == 0x0065):
				for n in range(vx + 1):
					self.V[n] = self.memory[self.I + n]
				print('FX65')

#---------------------------------------------------
#			REGISTRADOR SUPERCHIP-8 RPL
			
				#FX75
			elif (nn == 0x0075):
				self.rpl = self.V[vx]
				print('FX75')

				#FX85
			elif(nn == 0x0085):
				self.V[vx] = self.rpl
				print('FX85')
			
			else:
				self.pc -= 2
#---------------------------------------------------


		else:
			#print(hex(self.opcode))
			#print('decrementei')
			self.pc -= 2

		self.pc += 2
		#print('incrementei')
		#print('opcode=',hex(self.opcode))


		pytime = time()
		if pytime - self.tempo >= 1.0/60:
			if self.delay > 0:
				self.delay -= 1
			if self.som > 0:
				sys.stdout.write("\a")
				self.som -= 1

			self.tempo = pytime
