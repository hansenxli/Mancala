# Erick Sirisoukh and Hansen Li
# Mancala Final Project

import pygame as pg

class Mancala:
	def __init__(self, beans, ai):
		# list for board
		self.board = []
		for i in range(15):
			# for mancala dishes
			if i == 6 or i == 13:
				self.board.append(0)
			else:
				self.board.append(beans)
		# keeps track of current player
		if ai == "Yes":
			self.AI = 1
		else:
			self.AI = 0
			self.curPlayer = 0


	def startGame(self):
		pg.init()
		self.clock = pg.time.Clock()
		# draws screen
		self.screen = pg.display.set_mode((1000, 700))
		pg.display.set_caption('Mancala')
		self.screen.fill((200,200,255))

		# font
		self.font = pg.font.SysFont('Comic Sans MS', 18)
		self.textColor = (0,0,0)
		self.double = 0

		# writes instructions on screen
		instructions1 = self.font.render("Objective: Collect the most beans in your mancala, the large dish at the end of each board.", 1, self.textColor)
		instructions2 = self.font.render("Instructions: Select a dish from your side and each bead from that dish will be placed in subsequent dishes", 1, self.textColor)
		instructions3 = self.font.render("(one per dish) in a counterclockwise motion. If the last bean lands in your mancala you get to go again.", 1, self.textColor)
		instructions4 = self.font.render("Players skip their opponent's mancala. The game ends when one player no longer has beans in any of their dishes.", 1, self.textColor)
		instructions5 = self.font.render("The player with the most beans in their mancala wins.", 1, self.textColor)
		instructions6 = self.font.render("Capture Rule: If the last bean lands in an empty dish on your side of the board, you get to automatically place", 1, self.textColor)
		instructions7 = self.font.render("that and any beans directly opposite that dish into your mancala.", 1, self.textColor)
		instructions8 = self.font.render("Press Enter to begin", 1, self.textColor)
		self.screen.blit(instructions1, (30, 30))
		self.screen.blit(instructions2, (30, 80))
		self.screen.blit(instructions3, (30, 100))
		self.screen.blit(instructions4, (30, 120))
		self.screen.blit(instructions5, (30, 140))
		self.screen.blit(instructions6, (30, 190))
		self.screen.blit(instructions7, (30, 210))
		self.screen.blit(instructions8, (30, 260))

		pg.display.flip()
		event = pg.event.poll()
		while not (event.type == pg.KEYDOWN and event.key == pg.K_RETURN):
			if event.type == pg.QUIT:
				quit()
			self.clock.tick(50)
			event = pg.event.poll()

		# To Do:
		# Customize it so users can choose 2-player or computer

	def drawBoard(self):
		self.screen.fill((200,200,255))

		earthporn = pg.image.load('2048.jpg')
		self.screen.blit(earthporn, (0,0))
		# draws board with wood image
		woodboard = pg.image.load('wood.jpg')
		self.screen.blit(woodboard, (100, 250))

		# draw Player 2 mancala
		pg.draw.ellipse(self.screen, (255,255,255), (110, 260, 80, 180), 0)
		mancala2 = self.font.render(str(self.board[13]), 1, self.textColor)
		self.screen.blit(mancala2, (150, 350))

		# draw Player 1 mancala
		pg.draw.ellipse(self.screen, (255,255,255), (810, 260, 80, 180), 0)
		mancala1 = self.font.render(str(self.board[6]), 1, self.textColor)
		self.screen.blit(mancala1, (850, 350))

		for i in range(12,6,-1):
			pg.draw.circle(self.screen, (255,255,255), (1450-(i * 100), 300), 40, 0)
			dish = self.font.render(str(self.board[i]), 1, self.textColor)
			self.screen.blit(dish, (1450-(i * 100), 300))


		for i in range(6):
			pg.draw.circle(self.screen, (255,255,255), (250 + (i * 100), 400), 40, 0)
			dish = self.font.render(str(self.board[i]), 1, self.textColor)
			self.screen.blit(dish, (250 + (i * 100), 400))


		pg.display.flip()


	def playerMove(self):
		# determines who the current player is
		if self.curPlayer == 0:
			turn = self.font.render("Player 1's turn", 1, self.textColor)
			self.screen.blit(turn, (470, 470))
			if self.double == 1:
				turn2 = self.font.render("You get to go again!", 1, self.textColor)
				self.screen.blit(turn2, (450, 120))
		else:
			turn = self.font.render("Player 2's turn", 1, self.textColor)
			self.screen.blit(turn, (470, 200))
			if self.double == 1:
				turn2 = self.font.render("You get to go again!", 1, self.textColor)
				self.screen.blit(turn2, (450, 120))
		pg.display.flip()
		event = pg.event.poll()
		while not (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
			if event.type == pg.QUIT:
				quit()
			self.clock.tick(50)
			event = pg.event.poll()

		x, y = event.pos

		if self.curPlayer == 0:
			# if Player 1's click is not on their side of the board
			if not (200 < x < 800 and 350 < y < 450):
				message = self.font.render('Click on your side of the board', 1, self.textColor)
				self.screen.blit(message, (100, 500))
				pg.display.flip()
				pg.time.delay(1000)
				return
			# for Player 1's side
			if 350 < y < 450:
				index = (x-200)/100
			a = self.board[index]
			# checks if selected dish has 0 beans in it
			if a == 0:
				return
			# updates board list with transferred beans
			skip = 0
			capture = 0
			self.board[index] = 0
			for bean in range(1, a + 1):
				b = (index + bean)%14
				if b == 5:
					skip = 0
				if b == 13:
					skip = 1
					self.board[13] -= 1
					self.board[0] += 1
				elif skip == 1:
					b += 1
			# activates capture rule switch if conditions met
				if self.board[b] == 0 and self.board[(12-2*b + b)] != 0 and b < 6 and b >= 0:
					capture = 1
				else:
					capture = 0
				self.board[b] += 1
				if b == 6:
					self.double = 1
				else:
					self.double = 0
			# activates capture rule
			if capture == 1:
				self.board[6] += self.board[b] + self.board[(12-2*b) + b]
				self.board[b] = 0
				self.board[(12-2*b) + b] = 0
				captured = self.font.render('Captured', 1, self.textColor)
				self.screen.blit(captured, (490, 170))
				pg.display.flip()
				pg.time.delay(1000)
			print (self.board)

		else:
			# if Player 2's click is not on their side of the board
			if not (200 < x < 800 and 250 < y < 350):
				message = self.font.render('Click on your side of the board', 1, self.textColor)
				self.screen.blit(message, (100, 500))
				pg.display.flip()
				pg.time.delay(1000)
				return
			# for Player 2's side
			if 250 < y < 350:
				i = (x-200)/100
				index = (12-2*i) + i
			a = self.board[index]
			# checks if selected dish has 0 beans in it
			if a == 0:
				return
			# updates board list with transferred beans
			skip = 0
			capture = 0
			self.board[index] = 0
			for bean in range(1, a + 1):
				b = (index + bean)%14
				if b == 12:
					skip = 0
				if b == 6:
					skip = 1
					self.board[6] -= 1
					self.board[7] += 1
				elif skip == 1:
					b += 1
		# activates capture rule switch if conditions met
				if self.board[b] == 0 and self.board[(12-b)] and b >= 7 and b < 13:
					capture = 1
				else:
					capture = 0
				self.board[b] += 1
				if b == 13:
					self.double = 1
				else:
					self.double = 0
		# activates capture rule
			if capture == 1:
				self.board[13] += self.board[b] + self.board[(12-b)]
				self.board[b] = 0
				self.board[(12-b)] = 0
				captured = self.font.render('Captured', 1, self.textColor)
				self.screen.blit(captured, (490, 170))
				pg.display.flip()
				pg.time.delay(1000)
			print (self.board)

		# switches players, lets you go again if you got your last piece in your mancala
		if self.double == 0:
			self.curPlayer = (self.curPlayer + 1) % 2

	def playerAI(self):
		# Implement AI
		turn = self.font.render("It's Your Turn", 1, self.textColor)
		self.screen.blit(turn, (470,470))
		if self.double == 1:
			turn2 = self.font.render("You get to go again!", 1, self.textColor)
			self.screen.blit(turn2, (450,120))
		pg.display.flip()
		event = pg.event.poll()
		while not (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
			if event.type == pg.QUIT:
				quit()
			self.clock.tick(50)
			event = pg.event.poll()

		x, y = event.pos

		if not (200 < x < 800 and 350 < y < 450):
			message = self.font.render('Click on your side of the board', 1, self.textColor)
			self.screen.blit(message, (100, 500))
			pg.display.flip()
			pg.time.delay(1000)
			return
		if 350 < y < 450:
			index = (x-200)/100
		a = self.board[index]
		if a == 0:
			return
		skip = 0
		capture = 0
		self.board[index] = 0
		for bean in range(1, a + 1):
			b = (index + bean)%14
			if b == 5:
				skip = 0
			if b == 13:
				skip = 1
				self.board[13] -= 1
				self.board[0] += 1
			elif skip == 1:
				b += 1
		# activates capture rule switch if conditions met
			if self.board[b] == 0 and self.board[(12-2*b) + b] != 0 and b < 6 and b >= 0:
				capture = 1
			else:
				capture = 0
			self.board[b] += 1
			if b == 6:
				self.double = 1
			else:
				self.double = 0
		# activates capture rule
		if capture == 1:
			self.board[6] += self.board[b] + self.board[(12-2*b) + b]
			self.board[b] = 0
			self.board[(12-2*b) + b] = 0
			captured = self.font.render('Captured', 1, self.textColor)
			self.screen.blit(captured, (490, 170))
			pg.display.flip()
			pg.time.delay(1000)
		print (self.board)

		capture = 0
		aiturn = self.font.render('Computer Turn', 1, self.textColor)
		self.screen.blit(aiturn, (470,200))
		pg.display.flip()
		pg.time.delay(1000)
		step = 0
		for aidish in range(12,6,-1):
			if step == 0:
				if aidish + self.board[aidish] == 13:
					a = self.board[aidish]
					for bean in range (1, a + 1):
						b = (index + bean)%14
						if b == 12:
							skip = 0
						if b == 6:
							skip = 1
							self.board[6] -= 1
							self.board[7] += 1
						elif skip == 1:
							b += 1
						self.board[b] += 1
					return
				step = 1
			if step == 1:
				for bead in range (1, a + 1):
					b = (index + bean)%14
				if b == 12:
					skip = 0
				if b == 6:
					skip = 1
					self.board[6] -= 1
					self.board[7] += 1
				elif skip == 1:
					b += 1
				b = b%14
				if self.board[b] == 0:
					capture = 1
				self.board[b] += 1
				if capture == 1:
					self.board[6] += self.board[b] + self.board[(12-2*b) + b]
					self.board[b] = 0
					self.board[(12-2*b) + b] = 0
					captured = self.font.render('Captured', 1, self.textColor)
					self.screen.blit(captured, (490, 170))
					pg.display.flip()
					pg.time.delay(1000)
				print (self.board)
			else:
				temp = 0
				for aidish in range(12,6,-1):
					if temp < self.board[aidish]:
						temp = self.board[aidish]
				for bean in range (1, a + 1):
					b = (index + bean)%14
					if b == 12:
						skip = 0
					if b == 6:
						skip = 1
						self.board[6] -= 1
						self.board[7] += 1
					elif skip == 1:
						b += 1
					self.board[b] += 1
		print (self.board)

		for i in range(7,13):
			pg.draw.circle(self.screen, (255,255,255), (1450-(i * 100), 300), 40, 0)
			dish = self.font.render(str(self.board[i]), 1, self.textColor)
			self.screen.blit(dish, (1450-(i * 100), 300))

	def endGame(self):
		# checks the total number of beans on Player 1's side
		total1 = 0
		for dish in self.board[:6]:
			total1 += dish
		# checks the total number of beans on Player 2's side
		total2 = 0
		for dish in self.board[7:13]:
			total2 += dish
		# if the total number of beans on either side is 0, then the game is over
		if total1 == 0 or total2 == 0:
			# adds the remaining beans on a player's side to their respective mancala
			self.board[6] += total1
			self.board[13] += total2

			# end game screen and message
			self.screen.fill((200,200,255))

			if total2 > total1:
				message = self.font.render('Player 2 won!', 1, self.textColor)
				self.screen.blit(message, (100, 500))
			elif total1 > total2:
				message = self.font.render('Player 1 won!', 1, self.textColor)
				self.screen.blit(message, (100, 500))
			elif total1 == total2:
				message = self.font.render('Draw!', 1, self.textColor)
				self.screen.blit(message, (100, 500))

			# new game option
			newGameOption = self.font.render('New Game?', 1, self.textColor)
			self.screen.blit(newGameOption, (500, 500))

			event = pg.event.poll()
			while not (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
				if event.type == pg.QUIT:
					quit()
				self.clock.tick(50)
				event = pg.event.poll()

			x, y = event.pos

			if 500 < x < 700 and 500 < y < 700:
				main()

			pg.display.flip()
			pg.time.delay(3000)
			return True

#	def AI(self):


		# To Do:
		# Implement new game option

def main():
	beans = int(raw_input("Please enter the number of starting beads: "))
	ai = raw_input("Would you like to play against the computer? (Yes or No): ")
	game = Mancala(beans,ai)
	game.startGame()
	game.drawBoard()
	while not game.endGame():
		if game.AI == 0:
			num = 1
			print ("Turn", num)
			game.playerMove()
			game.drawBoard()
			num += 1
		else:
			game.playerAI()
			game.drawBoard()
	event = pg.event.poll()
	while not event.type == pg.QUIT:
		event = pg.event.poll()

	# To Do:
	# Delete any error-checking prints in terminal

if __name__ == '__main__':
	main()