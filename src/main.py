import curses
from curses import newwin, wrapper
import time
import random
import Generator

def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()

def menu(stdscr):
	stdscr.clear()
	stdscr.addstr("MENÚ\n")
	stdscr.addstr("Escoge una modalidad\n")
	stdscr.addstr("1. Por cantidad de palabras\n")
	stdscr.addstr("2. Escribe una frase aleatoria\n")
	stdscr.addstr("3. Por límite de tiempo\n")
	stdscr.addstr("4. Escribe un libro\n")
	stdscr.addstr("5. Salir\n")

	key = stdscr.getkey()
	return key

def display_text(stdscr, target, current, wpm=0):
	# text_window = curses.newwin(curses.COLS, 20, 0, 0)
	# box(text_window)
	stdscr.addstr(target)
	stdscr.addstr(f"\nWPM: {wpm}")
	stdscr.move(0, 0)
	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)
		try:
			stdscr.addstr(char, color)
		except curses.error:
			pass

def load_text(modo):
	if modo == "1":
		gen = Generator.Generator()
		wordlist = gen.generateWords(4)
		words = ' '.join(x for x in wordlist)
		return words
	elif modo == "2":
		with open("text.txt", "r") as f:
			lines = f.readlines()
			return random.choice(lines).strip()
	
	return 0

def wpm_test(stdscr, modo):
	target_text = load_text(modo)
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			stdscr.nodelay(False)
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
	modo = menu(stdscr)

	while modo != "5":
		if modo == "1":
			wpm_test(stdscr, modo)
			stdscr.clear()
			stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
			stdscr.getkey()
		
		if modo == "2":
			wpm_test(stdscr, modo)
			stdscr.clear()
			stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
			stdscr.getkey()
			
		if modo == "3":
			stdscr.clear()
			stdscr.addstr("MODO: por límite de tiempo")
			stdscr.addstr("\nPress any key to continue...")
			stdscr.getkey()

		if modo == "4":
			stdscr.clear()
			stdscr.addstr("MODO: escribe un libro")
			stdscr.addstr("\nPress any key to continue...")
			stdscr.getkey()
			
		modo = menu(stdscr)

wrapper(main)