from VirtualProxy.ProxyUserDataLoader import ProxyUserDataLoader
from VirtualProxy.RealUserDataLoader import RealUserDataLoader

class SaveResults():
    def save_results(self, wpm, errors, char_count):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()
        characters = userData.get_characters()
        userData.update_characters(characters)
        
        with open("../files/wrong_chars.txt", "a") as file: # guarda la cantidad de caracteres en los equivocó por cada 10 escritos
                file.write(f"{10 * errors / char_count}\n")

        if(wpm is not None and wpm > 0):
            with open("../files/results.txt", "a") as file:
                file.write(f"{wpm}\n")