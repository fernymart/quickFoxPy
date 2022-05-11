import curses
from curses import newwin, wrapper
import time
import random
import Generator
from UserData import UserData

user_data = UserData()

# errors = 0
def save_results(wpm):
	if(wpm > 0):
		with open("../files/results.txt", "a") as file:
			file.write(f"{wpm}\n")

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
	stdscr.addstr("5. Configuración\n")
	stdscr.addstr("6. Estadísticas\n")
	stdscr.addstr("7. Salir\n")

	key = stdscr.getkey()
	return key

def config_menu(stdscr):
	stdscr.clear()
	stdscr.addstr("CONFIGURACION\n")
	stdscr.addstr("1. Cambiar límite de palabras\n")
	stdscr.addstr("2. Cambiar límite de tiempo\n")
	stdscr.addstr("3. Regresar")

	key = stdscr.getkey()
	return key

def get_input(stdscr, limit):
	count = 0
	text = ""
	while count < limit:
		key = stdscr.getkey()

		if ord(key) == 10 or ord(key) == 13: # Enter
			break

		stdscr.addstr(key)
		text += key
		count += 1

	stdscr.addstr(2, 0, "\nPresiona cualquier tecla para guardar...")
	stdscr.getkey()
	return text

def configuration(stdscr):
	key = config_menu(stdscr)

	while key != "3":
		if key == "1":
			stdscr.clear()
			stdscr.addstr("Límite actual: ")
			stdscr.addstr(str(user_data.get_word_limit()))
			stdscr.addstr("\nIngresa el nuevo límite (max. 3 digitos): ")
			s = get_input(stdscr, 3)

			try:
				user_data.update_word_limit(int(s))
			except:
				stdscr.addstr("\nError. Debes ingresar un número")
				stdscr.getkey()

		if key == "2":
			stdscr.clear()
			stdscr.addstr("Límite actual: ")
			stdscr.addstr(str(user_data.get_time_limit()))
			stdscr.addstr("\nIngresa el nuevo límite (max. 3 digitos): ")
			s = get_input(stdscr, 3)

			try:
				user_data.update_time_limit(int(s))
			except:
				stdscr.addstr("\nError. Debes ingresar un número")
				stdscr.getkey()

		key = config_menu(stdscr)

def display_text(stdscr, target, current, wpm=0):
	# text_window = curses.newwin(curses.COLS, 20, 0, 0)
	# box(text_window)
	# global errors
	stdscr.addstr(target)
	stdscr.addstr(f"\nWPM: {wpm}")
	stdscr.move(0, 0)
	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)
			# errors+=1
		try:
			stdscr.addstr(char, color)
		except curses.error:
			pass

def load_text(modo):
	if modo == "1":
		gen = Generator.Generator()
		wordlist = gen.generateWords(user_data.get_word_limit())
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
			return wpm
			# break

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

def display_estadisticas(stdscr):
	promedio = 0
	suma = 0
	with open("../files/results.txt", "r") as file:
		resultados = file.readlines()
		for resultado in resultados:
			suma+=float(resultado)
		promedio = suma / len(resultados)
	stdscr.addstr(2, 0, f"Promedio: {promedio} wpm")

def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
	modo = menu(stdscr)
	total_wpm = 0

	while modo != "7":
		if modo == "1":
			total_wpm = wpm_test(stdscr, modo)
			stdscr.clear()
			save_results(total_wpm)
			stdscr.addstr(1,0,f"Your speed was: {total_wpm} wpm")
			# stdscr.addstr(2,0,f"You had {errors} errors")
			stdscr.addstr(3, 0, "You completed the text! Press any key to continue...")
			stdscr.getkey()
		
		if modo == "2":
			total_wpm = wpm_test(stdscr, modo)
			stdscr.clear()
			save_results(total_wpm)
			stdscr.addstr(1,0,f"Your speed was: {total_wpm} wpm")
			# stdscr.addstr(2,0,f"You had {errors} errors")
			stdscr.addstr(3, 0, "You completed the text! Press any key to continue...")
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

		if modo == "5":
			configuration(stdscr)
			stdscr.clear()
		
		if modo == "6":
			stdscr.clear()
			stdscr.addstr(1, 0, "Estadisticas historicas")
			display_estadisticas(stdscr)
			# stdscr.addstr(1, 0, "Estadisticas historicas")
			stdscr.addstr(3, 0, "\nPress any key to continue...")
			stdscr.getkey()

		modo = menu(stdscr)
	


wrapper(main)
