from cmd import Cmd
from colorama import Fore, Back, Style
import pyfiglet


def banner():
    print("\n\n")
    result = pyfiglet.figlet_format("Black", font = "gothic") # lean/alligator/hollywood/gothic
    print(Fore.RED + result)
    print(Style.RESET_ALL)

def banner2():
    result2 = pyfiglet.figlet_format("Tabby", font = "gothic")
    print(Fore.RED + result2)
    print(Style.RESET_ALL)



class MyPrompt(Cmd):
    prompt = 'BlackTabby# '
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_add(self, inp):
        print(Fore.RED  + "adding '{}'".format(inp))
        print(Style.RESET_ALL)
    def help_add(self):
        print(Fore.RED + "Add a new entry to the system.")
        print(Style.RESET_ALL)

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == '__main__':
    banner()
    banner2()
    MyPrompt().cmdloop()
