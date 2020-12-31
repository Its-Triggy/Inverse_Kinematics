##########################################################################################
#-----------------------------------------SETUP------------------------------------------#
##########################################################################################
import pygame
from numpy import pi, sin, cos, arctan2

#colors
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

#PyGame Setup
pygame.init()

# Set the width and height of the screen [width,height]
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption("Inverse Kinematics")
clock = pygame.time.Clock()


##########################################################################################
#----------------------------------------CLASSES-----------------------------------------#
##########################################################################################
class Section:	
	def __init__(self, length, angle, thickness):
		self.B = (int(WIDTH/2), HEIGHT)
		self.length = length
		self.angle = angle
		self.A = self.calcA()
		self.thickness = thickness
	
	def draw(self):
		pygame.draw.line(screen, WHITE, self.A, self.B, self.thickness)		
		
	def calcA(self):
		return (self.B[0] - self.length * cos(self.angle), self.B[1] - self.length * sin(self.angle))
	
	def calcB(self):
		return (self.A[0] - self.length * cos(self.angle), self.A[1] - self.length * sin(self.angle))
	
	def updateB(self, point):
		self.angle = arctan2(point[1]-self.A[1], point[0]-self.A[0])
		self.B = point
		self.A = self.calcA()
	
	def updateA(self, point):
		self.angle = arctan2(point[1]-self.B[1], point[0]-self.B[0])
		self.A = point
		self.B = self.calcB()
		
##########################################################################################
#---------------------------------------MAIN LOOP----------------------------------------#
##########################################################################################
length = 5
arm = [Section(100, 45 * (pi/180), 5*(length+1)-5*(i+1)) for i in range(length)]
root = (int(WIDTH/2), HEIGHT)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	
	
	pos = pygame.mouse.get_pos()	
	
	arm[length-1].updateB(pos)
	for i in range(1,length):
		arm[length-i-1].updateB(arm[length-i].A)
	
	arm[0].updateA(root)
	for i in range(1,length):
		arm[i].updateA(arm[i-1].B)


	#Draw
	screen.fill(BLACK)	
	for sec in arm:
		sec.draw()
	
	pygame.display.flip()
	clock.tick(60)
		
pygame.quit()
exit()

	