import curses
from curses import newwin, wrapper
from re import S
import time
import random
import Generator
from UserData import UserData
from connection import GameDB

user_data = UserData()
books = user_data.get_books()
game_db = GameDB()

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
	stdscr.addstr("3. Cambiar nombre de usuario\n")
	stdscr.addstr("4. Regresar\n")

	key = stdscr.getkey()
	return key

def book_menu(stdscr):
	stdscr.clear()
	stdscr.addstr("LIBROS\n")

	for i in range(0, len(books)):
		text = str(i+1) + ". " + books[i]["title"] + " ({:.4f})\n".format(books[i]["written"] / float(books[i]["total_words"]))
		stdscr.addstr(text)

	back_opt = len(books) + 1
	text = str(back_opt) + ". Regresar\n"
	stdscr.addstr(text)

	key = stdscr.getkey()

	if key == str(back_opt):
		return -1

	return int(key) - 1

def skip_lines(lines, skip_words):
	lines_skipped = 0
	extra_text = ""
	count = 0

	for line in lines:
		words = line.split()

		if count == skip_words: 
			break

		if count + len(words) <= skip_words: # salta linea completa
			lines_skipped += 1
			count += len(words)
			continue

		elif count + len(words) > skip_words: # queda en medio de una linea
			lines_skipped += 1
			for word in words:
				count += 1
				if count > skip_words:
					extra_text += word + " "
			break

	return (lines_skipped, extra_text)

def write_book(stdscr, book):
	show_lines = 1
	file_name = books[int(book)]["file_name"]
	file = open("books/" + file_name, "r", encoding="utf-8-sig")
	lines = file.readlines()
	file.close()
	skip_words = books[int(book)]["written"]

	lines_skipped, extra_text = skip_lines(lines, skip_words)

	start_line = lines_skipped
	target_text = extra_text + " ".join(lines[start_line:start_line + show_lines]).replace("\n", "") + " "
	current_text = []

	start_time = time.time()
	wpm = 0
	start_line += show_lines
	words = 0

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			current_text = []
			target_text = " ".join(lines[start_line:start_line + show_lines]).replace("\n", "")
			start_line += show_lines
			stdscr.clear()
			continue

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 32:
			words += 1

		if ord(key) == 27:
			stdscr.nodelay(False)
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0 and ord(current_text[-1]) == 32: # si borra un espacio, restar una palabra para no contarla doble
				words -= 1
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)

	user_data.update_written_words(int(book), words)

def get_input(stdscr, limit):
	count = 0
	text = ""
	while count < limit:
		key = stdscr.getkey()
		
		if ord(key) == 10 or ord(key) == 13: # Enter
			break

		if ( ord(key.upper()) >= 65 and ord(key.upper()) <= 90 ) or ( ord(key) >= 48 and ord(key) <= 57 ): # letra o numero
			stdscr.addstr(key)
			text += key
			count += 1

	stdscr.addstr("\n\nPresiona cualquier tecla para guardar o ESC para cancelar...")
	key = stdscr.getkey()

	if ord(key) == 27:
		text = "-1"

	return text

def configuration(stdscr):
	key = config_menu(stdscr)

	while key != "4":
		if key == "1":
			stdscr.clear()
			stdscr.addstr("Límite actual: ")
			stdscr.addstr(str(user_data.get_word_limit()))
			stdscr.addstr("\nIngresa el nuevo límite (max. 3 digitos): ")
			s = get_input(stdscr, 3)

			try:
				if s != "-1":
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
				if s != "-1":
					user_data.update_time_limit(int(s))
			except:
					stdscr.addstr("\nError. Debes ingresar un número")
					stdscr.getkey()

		if key == "3":
			stdscr.clear()
			id, user = user_data.get_user()
			if id is None:
				stdscr.addstr("Crea tu nombre de usuario (max. 10 caracteres): ")

				while id is None:
					newuser = get_input(stdscr, 10)

					if newuser == "-1": break

					newuser = newuser.strip()
					stdscr.clear()

					if newuser == "": 
						stdscr.addstr("Error. Ingresa otro nombre")
						stdscr.addstr("\nNombre: ")
						continue

					id = game_db.add_username(newuser)

					if id is None:
						stdscr.addstr("Error. Ingresa otro nombre")
						stdscr.addstr("\nNombre: ")
					else:
						user_data.save_user(id, newuser)

				stdscr.addstr("\nUsuario registrado correctamente.")
				stdscr.getkey()

			else:
				stdscr.addstr("Tu nombre de usuario actual es " + user)
				stdscr.addstr("\n\nIngresa tu nuevo nombre (max. 10 caracteres): ")
				newuser = get_input(stdscr, 10)

				if newuser != "-1":
					newuser = newuser.strip()
					updated = game_db.change_username(id, newuser)

					while not updated:
						stdscr.clear()
						stdscr.addstr("Error. Ingresa otro nombre")
						stdscr.addstr("\nTu nombre de usuario actual es ")
						stdscr.addstr(user)
						stdscr.addstr("\n\nNuevo nombre: ")
						newuser = get_input(stdscr, 10)

						newuser = newuser.strip()

						if newuser == "-1":
							break
						if newuser == "": 
							continue
						updated = game_db.change_username(id, newuser)

					user_data.save_user(id, newuser)

					stdscr.addstr("\nNombre de usuario cambiado correctamente.")
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
	return promedio

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
			book = book_menu(stdscr)

			if book != -1:
				write_book(stdscr, book)
				stdscr.clear()
				stdscr.addstr("\nPress any key to continue...")
				stdscr.getkey()
				stdscr.clear()

		if modo == "5":
			configuration(stdscr)
			stdscr.clear()
		
		if modo == "6":
			stdscr.clear()
			stdscr.addstr(1, 0, "Estadisticas historicas")
			promedio = display_estadisticas(stdscr)
			# stdscr.addstr(1, 0, "Estadisticas historicas")

			stdscr.addstr("\n\nPresiona 1 para publicar y comparar tus estadísticas con otros usuarios")
			stdscr.addstr("\no cualquier otra tecla para regresar...")
			key = stdscr.getkey()

			if key == "1":
				id, user = user_data.get_user()
				if id is None:
					stdscr.addstr("\n\nNo tienes un usuario registrado. Registra uno en la configuración.")
				else:
					game_db.post_stats(id, promedio)
					percentage = game_db.get_stats(promedio)

					stdscr.addstr(f"\n\nTe encuentras por encima del {promedio:.2f}% de los usuarios de esta aplicación.")

				key = stdscr.getkey()

		modo = menu(stdscr)
	


wrapper(main)
