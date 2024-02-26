#!/usr/bin/python3
'''Module containing console - the entry point of the command interpreter'''
import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
classes = ["BaseModel", "User", "Amenity", "City", "Place", "Review", "State"]


def key_parser(line):
    """Handles case when argument is passed as:
    <create> <className> <attribute=value>
    """
    tokens = line.split()
    tokens = tokens[1:]
    key_val_dict = {}
    for token in tokens:
        key_val = token.split('=')
        if key_val[1][0] == '"':
            value = key_val[1].strip('"').replace('_', ' ')
        else:
            try:
                value = eval(key_val[1])
            except (SyntaxError, NameError):
                continue
        key_val_dict[key_val[0]] = value
    return key_val_dict


class HBNBCommand(cmd.Cmd):
    '''Command interpreter class'''
    prompt = "(hbnb) "

    def precmd(self, line: str) -> str:
        '''Formats argument before commands are executed'''
        # Check if input is in the format <Class>.<command>(options)
        if ("." in line and "(" in line.split(".")[1]
                and ")" in line.split(".")[1]):
            others = options = []
            update_dict = ''
            class_name = command = obj_id = attr = val = ""
            # Split line to extract classname
            args = line.split(".")
            class_name = args[0]
            # Split remaining string to extract command
            others = args[1].split("(")
            if len(others) > 0:
                command = others[0]
            # Check if other options are given and extract
            if len(others) > 1:
                options = others[1].rstrip(")").split(",", 1)
            # Extract Object ID
            if len(options) > 0:
                obj_id = options[0].replace('"', '').strip()
            if len(options) > 1:
                # Check if a dictionary was passed
                dict_attr_val = options[1].strip()
                if (dict_attr_val.startswith("{")
                        and dict_attr_val.endswith("}")):
                    update_dict = dict_attr_val
                #  If dictionary isn't passed extract single key and value pair
                elif len(dict_attr_val.split(",")) > 1:
                    attr = dict_attr_val.split(",")[0].replace('"', '').strip()
                    val = dict_attr_val.split(",")[1].replace('"', '').strip()
            result = f"{command} {class_name} {obj_id} "
            result += f"{update_dict if update_dict != '' else ''} "
            result += f"{attr} {val}"
            result = result.replace("  ", " ")
            return result
        return super().precmd(line)

    def emptyline(self) -> bool:
        '''Handles Emptyline'''
        return super().emptyline()

    def do_count(self, arg):
        '''
        Retrieves the number of instances of a class.
        Usage: <class name>.count()
        '''
        list_all = []
        if arg:
            if arg not in classes:
                print("** class doesn't exist **")
                return
            for key, value in storage.all().items():
                if arg in key.split("."):
                    list_all.append(str(value))
        else:
            list_all = [str(value) for key, value in storage.all().items()]
        print(len(list_all))

    def do_update(self, arg):
        '''
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        Usage:
        update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        <class name>.update(<id>, <attribute name>, <attribute value>)
        <class name>.update(<id>, <dictionary representation>)
        '''
        instance = ""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split(" ", 2)
        class_name = arg_list[0]
        if not class_name:
            print("** class name missing **")
            return
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) > 1:
            obj_id = arg_list[1]
        else:
            print("** instance id missing **")
            return
        for key, value in storage.all().items():
            if obj_id in key.split("."):
                instance = value
        if instance == "":
            print("** no instance found **")
            return
        if len(arg_list) > 2:
            # Check if Dictionary was passed as option
            if type(eval(arg_list[2])) in [dict]:
                dict_key = eval(arg_list[2])
                for key, value in dict_key.items():
                    try:
                        if type(eval(f"{value}")) in [int, float]:
                            value = eval(f"{value}")
                    except Exception:
                        pass
                    setattr(instance, key, value)
                    instance.save()
                return
            # If dictionary isn't passed, use key-value pair
            attribute = arg_list[2]
        else:
            print("** attribute name missing **")
            return
        if len(arg_list) > 3:
            attr_val = arg_list[3]
        else:
            print("** value missing **")
            return
        try:
            if type(eval(f"{attr_val}")) in [int, float]:
                attr_val = eval(f"{attr_val}")
        except Exception:
            pass
        setattr(instance, attribute, attr_val)
        instance.save()

    def do_all(self, arg):
        '''
        Prints all string representation of all instances
        based or not on the class name.
        Usage:
        <class name>.all()
        all BaseModel
        all
        '''
        list_all = []
        if arg:
            if arg not in classes:
                print("** class doesn't exist **")
                return
            for key, value in storage.all().items():
                if arg in key.split("."):
                    list_all.append(str(value))
        else:
            list_all = [str(value) for key, value in storage.all().items()]
        print(list_all)

    def do_destroy(self, arg):
        '''
        Deletes an instance based on the class name
        and id (save the change into the JSON file.
        Usage: <class name>.destroy(<id>).
        '''
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        class_name = arg_list[0]
        if not class_name:
            print("** class name missing **")
            return
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) > 1:
            obj_id = arg_list[1]
        else:
            print("** instance id missing **")
            return
        for key, value in storage.all().items():
            if obj_id in key.split("."):
                storage.delete(value)
                storage.save()
                return
        print("** no instance found **")
        return

    def do_show(self, arg):
        '''
        Prints the string representation of an instance
        based on the class name and id.
        Usage: <class name>.show(<id>)
        '''
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        class_name = arg_list[0]
        if not class_name:
            print("** class name missing **")
            return
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) > 1:
            obj_id = arg_list[1]
        else:
            print("** instance id missing **")
            return
        all = storage.all()
        for key, value in all.items():
            if obj_id in key.split("."):
                print(value)
                return
        print("** no instance found **")
        return

    def do_create(self, arg):
        '''
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id. Ex: $ create BaseModel.
        '''
        if not arg:
            print("** class name missing **")
            return
        class_name = arg.split()[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        new = eval(f"{class_name}()")
        key_dict = key_parser(arg)
        if key_dict:
            for key, value in key_dict.items():
                if hasattr(new, key):
                    setattr(new, key, value)
        new.save()
        print(new.id)

    def do_quit(self, arg):
        '''to exit the program'''
        return True

    def do_EOF(self, arg):
        '''to exit the program'''
        return True

    def do_help(self, arg: str) -> bool | None:
        '''Shows help for commands'''
        return super().do_help(arg)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
