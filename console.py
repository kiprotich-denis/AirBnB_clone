#!/usr/bin/python3
"""import modules"""
import cmd
import json
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """contains the entry point of the command interpreter"""

    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command exit the program"""
        return True

    def do_EOF(self, arg):
        """exit the program"""
        print()
        return True

    def emptyline(self):
        """shouldn’t execute anything by enter"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the id"""
        if arg is None or arg == "":
            print("** class name missing **")
        elif arg not in storage.classes():
            print("** class doesn't exist **")
        else:
            base = storage.classes()[arg]()
            base.save()
            print(base.id)

    def do_show(self, arg):
        """ Prints the string representation of an instance
        based on the class name and id"""
        if arg is None or arg == "":
            print("** class name missing **")
        else:
            words = arg.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                keys = "{}.{}".format(words[0], words[1])
                if keys not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[keys])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if arg is None or arg == "":
            print("** class name missing **")
        else:
            words = arg.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                keys = "{}.{}".format(words[0], words[1])
                if keys not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[keys]
                    storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based
        or not on the class name"""
        if arg not in storage.classes():
            print("** class doesn't exist **")
        if arg is None or arg == "":
            lst = [str(obj) for key, obj in storage.all().items()]
            print(lst)
        else:
            words = arg.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                lst = [str(obj) for key, obj in storage.all().items(
                    ) if type(obj).__name__ == words[0]]
                print(lst)

    def do_update(self, arg):
        """Updates an instance based on the class name
        and id by adding or updating attribute"""
        if arg is None or arg == "":
            print("** class name missing **")
            return
        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
