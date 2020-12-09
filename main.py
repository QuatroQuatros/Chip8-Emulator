import sys
import pygame
from pygame import Rect, Color, draw
from cpu import CPU 


cpu = CPU()
def emular(game):
	teclas=[pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, 
	pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
	pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
	pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]
	width, height = 64, 32
	size = width * 10, height * 10
	pixels = width * height
	preto = (0,0,0)
	branco = (255, 255, 255)
	cores = [preto,branco]
	Colors = {
		0: Color(0,0,0, 255),
		1: Color(255, 255, 255, 255)
	}


	loop = 0
	screen = setup(size)

	cpu.iniciar(pixels)
	cpu.load_game(game)

	while True:
		cpu.emular()


		if (cpu.Bandeira == True and cpu.schip == True):
			desenhar(screen, cores, cpu, 128, 64)
			print('128x64')
			print(hex(cpu.opcode))

		elif (cpu.Bandeira == True and cpu.schip == False):
			desenhar(screen, cores, cpu,64, 32)
			print('64x32')

		events = pygame.event.get()
		get_keys(events, teclas, cpu)

def setup(size):
	screen = pygame.display.set_mode(size)
	screen.fill((0,0,0))
	return screen


def draw_pixel(screen, cores, x_pos, y_pos, cor):
	x_base = x_pos * 10
	y_base = y_pos * 10
	draw.rect(screen,cores[cor],(x_base, y_base, 10, 10))


def scroll_left(screen,cores,cpu,width, height):
	for y in range(height):
		for x in range(4, width):
			color = get_color(screen, cores, x, y)
			draw_pixel(screen, cores, x -4, y, color)
	'''
	for y in range(height):
		for x in range(width -4, width):
			draw_pixel(screen, cores, x, y, 0)
	'''
	update()

def desenhar(screen, cores, cpu, width, height):
	if cpu.scroll == 0:
		scroll_left(screen, cores, cpu, width, height)
	for x in range(width):
		for y in range(height):
			screen.fill(cores[cpu.pixels[x + (y * width)]], Rect(x*10,y*10,10,10))
	
	update()
	cpu.Bandeira = False
	cpu.scroll = -1
	print('opa===========',cpu.scroll)

'''
	if cpu.scroll == 0:
		tile = scroll(screen,cores,cpu,width, height)
	else:
'''
	
def update():
	pygame.display.flip()

def get_color(screen, cores, x, y):
	x_pos = x * 10
	y_pos = y * 10
	color = screen.get_at((x_pos,y_pos))
	if color == cores[0]:
		color = 0
	else:
		color = 1
	return color

def scroll_screen_right():
	if cpu.scroll == 1:
		width += 4
		cpu.scroll = -1



def get_keys(events, teclas, cpu):
	for event in events:
		event_type = -1
		if event.type == pygame.KEYDOWN:
			event_type = 1
		elif event.type == pygame.KEYUP:
			event_type = 0
		elif event.type == pygame.QUIT:
			sys.exit(0)

		if event_type == 0 or event_type == 1:
			if event.key in teclas:
				i = teclas.index(event.key)
				cpu.teclas[i] = event_type

if __name__ == '__main__':
	game = sys.argv[1]
	emular(game)