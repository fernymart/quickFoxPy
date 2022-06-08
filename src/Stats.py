from ProxyUserDataLoader import ProxyUserDataLoader
from RealUserDataLoader import RealUserDataLoader

class Stats():
    def display_estadisticas(self, stdscr):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()
        characters = userData.get_wrong_char()

        promedio = 0
        promedio_chars = 0
        suma = 0
        with open("../files/results.txt", "r") as file:
            resultados = file.readlines()
            for resultado in resultados:
                suma+=float(resultado)
            promedio = suma / len(resultados)

        suma = 0
        with open("../files/wrong_chars.txt", "r") as file:
            resultados = file.readlines()
            for resultado in resultados:
                suma+=float(resultado)
            promedio_chars = suma / len(resultados)

        stdscr.addstr(3, 0, f"Average: {promedio:.2f} wpm")
        stdscr.addstr(4, 0,f"The character you have gotten wrong more times is {characters}")
        stdscr.addstr(5, 0, f"On average you make {promedio_chars:.2f} mistakes every 10 characters.")
        return promedio, promedio_chars