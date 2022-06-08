class Input():
    def get_input(self, stdscr, limit):
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

        stdscr.addstr("\n\nPress any key to save settings or ESC to cancel...")
        key = stdscr.getkey()

        if ord(key) == 27: # ESC (cancelar)
            text = "-1"

        return text