import curses
from curses import newwin, wrapper
from re import S
import time
import random
import webbrowser
from emoji import emojize
import Generator
from PhraseMode import PhraseMode
from UserData import UserData
from WordMode import WordsMode
from connection import GameDB

user_data = UserData()
books = user_data.get_books()
game_db = GameDB()
errors = 0
char_count = 0
characters = user_data.get_characters() # caracteres en los que se equivoca el usuario

def save_results(wpm):
	user_data.update_characters(characters)
	with open("../files/wrong_chars.txt", "a") as file: # guarda la cantidad de caracteres en los equivocó por cada 10 escritos
			file.write(f"{10 * errors / char_count}\n")

	if(wpm is not None and wpm > 0):
		with open("../files/results.txt", "a") as file:
			file.write(f"{wpm}\n")

def skip_lines(lines, skip_words):
	'''Recorre la lista lines y salta skip_words palabras para llegar hasta donde el usuario se había quedado'''
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

		elif count + len(words) > skip_words: # queda en medio de una linea, así que comienza a irse por palabras
			lines_skipped += 1
			for word in words:
				count += 1
				if count > skip_words:
					extra_text += word + " "
			break

	# Devuelve el número de líneas completas que se saltó y las palabras que faltan por escribir de la línea donde se quedó el usuario
	return (lines_skipped, extra_text)

def main(stdscr):
	global errors
	color_correct, color_incorrect = user_data.get_colors()
	set_color(1, color_correct)
	set_color(2, color_incorrect)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
	modo = menu(stdscr)
	total_wpm = 0

	while modo != "8":
		errors = 0
		if modo == "1": # Cantidad de palabras
			total_wpm = wpm_test(stdscr, modo)
			stdscr.clear()
			save_results(total_wpm)
			stdscr.addstr(1, 0,f"Your speed was: {total_wpm} wpm")
			stdscr.addstr(2, 0,f"You made {errors} mistakes when writing a total of {char_count} characters.")
			stdscr.addstr(4, 0, "You completed the text! \nPress 1 to share on Twitter or any other key to continue...")
			key = stdscr.getkey()
			if key == "1":
				twitter_share(total_wpm, errors, char_count)
		
		if modo == "2": # Frase aleatoria
			total_wpm = wpm_test(stdscr, modo)
			stdscr.clear()
			save_results(total_wpm)
			stdscr.addstr(1, 0,f"Your speed was: {total_wpm} wpm")
			stdscr.addstr(2, 0,f"You made {errors} mistakes when writing a total of {char_count} characters.")
			stdscr.addstr(4, 0, "You completed the text! \nPress 1 to share on Twitter or any other key to continue...")
			key = stdscr.getkey()
			if key == "1":
				twitter_share(total_wpm, errors, char_count)
			
		if modo == "3": # Contrarreloj
			stdscr.clear()
			total_wpm=timed_test(stdscr)
			stdscr.clear()
			save_results(total_wpm)
			# stdscr.nodelay(True)
			# time.sleep(1)
			# stdscr.clear()
			stdscr.addstr(1, 0,f"Your speed was: {total_wpm} wpm")
			stdscr.addstr(2, 0,f"You made {errors} mistakes when writing a total of {char_count} characters.")
			stdscr.addstr(4, 0, "You completed the text! \nPress 1 to share on Twitter or any other key to continue...")
			key = stdscr.getkey()
			if key == "1":
				twitter_share(total_wpm, errors, char_count)

		if modo == "4": # Escribir un libro
			book = book_menu(stdscr)

			if book != -1:
				total_wpm = write_book(stdscr, book)
				stdscr.clear()
				save_results(total_wpm)
				stdscr.addstr(1, 0,f"Your speed was: {total_wpm} wpm")
				stdscr.addstr(2, 0,f"You made {errors} mistakes when writing a total of {char_count} characters.")
				stdscr.addstr(4, 0, "You completed the text! \nPress 1 to share on Twitter or any other key to continue...")
				key = stdscr.getkey()
				if key == "1":
					twitter_share(total_wpm, errors, char_count)
				stdscr.clear()

		if modo == "5": # Numpad
			total_wpm = wpm_test(stdscr, modo)
			stdscr.clear()
			save_results(total_wpm)
			stdscr.addstr(1, 0,f"Your speed was: {total_wpm} wpm")
			stdscr.addstr(2, 0,f"You made {errors} mistakes when writing a total of {char_count} characters.")
			stdscr.addstr(4, 0, "You completed the text! \nPress 1 to share on Twitter or any other key to continue...")
			key = stdscr.getkey()
			if key == "1":
				twitter_share(total_wpm, errors, char_count)

		if modo == "6": # Configuracion
			configuration(stdscr)
			stdscr.clear()
		
		if modo == "7": # Estadísticas
			stdscr.clear()
			stdscr.addstr(1, 0, "Statistics")
			promedio, promedio_chars = display_estadisticas(stdscr)

			stdscr.addstr("\n\nPress 1 to share your statistics on Twitter.")
			stdscr.addstr("\nPress 2 to share your statistics with other users of this app.")
			stdscr.addstr("\n\nPress any other key to return to main menu...")
			key = stdscr.getkey()

			if key == "2":
				id, user = user_data.get_user()
				if id is None:
					stdscr.addstr("\n\nIt seems like you do not have a registered user. Please, register one in the settings.")
					stdscr.getkey()
				else:
					game_db.post_stats(id, promedio, promedio_chars)
					percentage, percentage_chars = game_db.get_stats(promedio, promedio_chars)

					stdscr.addstr(f"\n\nIn terms of speed, you are above the {percentage:.2f}% of the users of this app.")
					stdscr.addstr(f"\nIn terms of number of mistakes made, you are above the {percentage_chars:.2f}% of the users of this app.")
					stdscr.addstr(f"\n\nPress 1 to share on Twitter.")
					stdscr.addstr("\nPress any other key to return to main menu...")

					key = stdscr.getkey()
					if key == "1":
						twitter_share(promedio, percentage)
			elif key == "1":
				twitter_share(promedio)


		modo = menu(stdscr)
	


wrapper(main)