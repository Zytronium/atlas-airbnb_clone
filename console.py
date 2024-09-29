#!/bin/python3
"""
This is the main module for running the command line interpreter,
aka the console. Run this to run the command line interpreter. Read
the readme for a list of commands and more detailed info.
"""
import sys
import webbrowser
from cmd import Cmd
from os import isatty
from time import sleep

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.colors import *
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(Cmd):
    """
    the main command line interpreter class
    """
    def __init__(self):
        super().__init__()
        if isatty(sys.stdin.isatty()):  # only sets intro in interactive
            self.intro = ('Welcome to AirBnB Clone Console! Type '
                          '"help" or "?" for a list of commands. Type '
                          '"exit" or "quit" to exit.')
            self.prompt = '(hbnb) \033[7m'  # reverses background & foreground
        else:
            self.prompt = '(hbnb) '

    def precmd(self, line):
        """
        overrides the default method the runs between when the input is parsed
        and when the command is run. This override resets the text color to
        undo the effect from adding \033[7m to the prompt, which reverses the
        background and foreground colors for the user input. This makes sure
        that the output doesn't retain this effect.
        :param line: user input
        :return: the same thing the original command returns, which is line,
        according to the source code for cmd.py.
        """
        reset_color()
        return super().precmd(line)

    def emptyline(self):
        """
        overrides default method that runs when en empty command is run.
        Instead, it will do nothing when there is no command.
        """
        pass

    def default(self, line):
        """
        Overrides default method that runs if the given command is not found.
        If the input is "easter egg" then it runs a hidden command that is not
        listed when you run "help"
        :param line: user input
        """
        if line == "easter egg":
            print("You found the easter egg!")
            sleep(3)
            webbrowser.open_new_tab(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            print("Never gonna give you up!")
        else:
            super().default(line)

    # ======================== user commands ========================

    # ======================== exit commands ========================

    @staticmethod
    def do_exit(args):
        """Exit the program."""
        return True

    @staticmethod
    def do_quit(args):
        """Exit the program."""
        return True

    @staticmethod
    def do_EOF(args):
        """EOF signal (usually ctl+d) will run this to exit the program."""
        print()  # Prints an extra line to force the next cmd prompt in
                 # the terminal to be on a separate line.
        return True

    # ================== data interaction commands ==================

    @staticmethod
    def do_create(clsname):
        """
Creates and saves an instance of className and prints the ID.
className: name of the class of the new instance to be created
Usage: create <className>
        """

        cls = HBNBCommand.get_class(clsname)
        if cls is None:
            return

        new_instance = cls()
        """clay - changed this to new_instance.save()"""
        new_instance.save() 
        print(new_instance.id)

    @staticmethod
    def do_update(argstr):
        """WIP | will not work
Usage: update <class name> <id> <attribute name> "<attribute value>
        """
        args = HBNBCommand.parse_args(argstr, 4)
        clsname = args[0]
        id = args[1]
        attr_name = args[2]
        attr_value = args[3]

        cls = HBNBCommand.get_class(clsname)
        if cls is None:
            return
        if id == '':
            print("** instance id missing **")
            return
        if attr_name == '':
            print("** attribute name missing **")
            return
        if attr_value == '':
            print("** value missing **")
            return

        instance_found = False
        for instance in storage.all().values():
            if type(instance) is cls and instance.id == id:
                setattr(instance, attr_name, attr_value)
                instance.save()
                instance_found = True
                break

        if not instance_found:
            print("** no instance found **")


        # WIP
    @staticmethod
    def do_destroy(argstr):
        """WIP | will not work
Usage: destroy <class name> <id>
        """
        args = HBNBCommand.parse_args(argstr, 2)
        clsname = args[0]
        id = args[1]

        if clsname == '':
            print("** class name missing **")
            return

        cls = HBNBCommand.get_class(clsname)
        if cls is None:
            return
        if id == '':
            print("** instance id missing **")
            return

        instance_found = False
        for content, instance in list(storage.all().items()):
            if type(instance) is cls and instance.id == id:
                del storage.all()[content]
                instance_found = True
                break

        if not instance_found:
            print("** no instance found **")
            return
        # WIP

    # ==================== data viewing commands ====================


    @staticmethod
    def do_show(argstr):
        """
Prints the string representation of an instance based on the class name and id
Usage: show <class name> <id>
        """
        args = HBNBCommand.parse_args(argstr, 2)
        clsname = HBNBCommand.get_class(args[0])
        id = args[1]
        
        if clsname is None:
            print("** class name missing **")
            return
        if id == '':
            print("** instance id missing **")
            return

        instance_found = False
        for instance in storage.all().values():
            if type(instance) is clsname and instance.id == id:
                print(instance)
                instance_found = True
                break

        if not instance_found:
            print("** no instance found **")
            return

    @staticmethod
    def do_all(clsname):
        """
Prints the representations of all instances of the given class name
Usage: all <class name>
        """
        cls = HBNBCommand.get_class(clsname)
        if cls is None:
            return
        instances = []
        for instance in storage.all().values():
            if type(instance) is cls:
                instances.append(str(instance))

        print(instances)

    # ====================== misc fun commands ======================

    @staticmethod
    def do_rickroll(args):
        """Rickrolls you"""
        webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    @staticmethod
    def do_selfdestruct(timer):
        """
Activates self-destruct mode, which starts a countdown from the specified
number, or 5 if not given. Exits the command line interpreter when
the countdown reaches 0.
Arguments: number (optional) - amount of seconds to count down from
Usage: selfdestruct <number>
        """
        t = 5
        if timer.isnumeric():
            t = int(timer)
        elif timer != '':
            print("Please specify a valid number, or leave blank.")
            return

        set_color('red')
        set_color('bold')
        set_color('reverse')
        set_color('blinking')
        print("SELF DESTRUCT MODE INITIATED.\n")
        reset_color()
        while t > 0:
            if t <= 3:
                set_color('light red')
            else:
                reset_color()
            sleep(1)
            print(t)
            t -= 1
        sleep(1)
        reset_color()
        set_color('yellow')
        print("The console has been obliterated. Goodbye.")
        reset_color()
        return True

    @staticmethod
    def get_class(clsname):
        if clsname == "":
            print("** class name missing **")
            return None
        if clsname == 'BaseModel':
            return BaseModel
        elif clsname == 'User':
            return User
        elif clsname == 'Review':
            return Review
        elif clsname == 'Amenity':
            return Amenity
        elif clsname == 'Place':
            return Place
        elif clsname == 'State':
            return State
        elif clsname == 'City':
            return City
        else:
            print("** class doesn't exist **")
            return None

    @staticmethod
    def parse_args(argstr, num_args = 3):
        """
        parse args by converting a string of args (argstr) into individual args
        :param argstr: args string
        :param num_args: number of args to parse. 3 by default if left empty
        :return: a list of args
        """
        args = argstr.split(' ')
        if len(args) < num_args:
            add_args = num_args - len(args)
            for i in range(add_args):
                args.append('')
        return args

if __name__ == '__main__':
    HBNBCommand().cmdloop()
