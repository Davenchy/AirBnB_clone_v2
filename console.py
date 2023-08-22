#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import models


def read_next_string_token(line):
    r"""Reads next string token in line

    Args:
        line (str): line to read

    Returns:
        tuple: (token: string, rest_of_line: line)

    Example:
        >>> line = r'"value\"1\"" "value2"'
        >>> read_next_string_token(line)
        ('value"1"', ' "value2"')"""

    token, rest_of_line, ignore, tokened = "", "", False, False

    for c in line:
        if tokened:
            rest_of_line += c
        elif ignore:
            ignore = False
            token += c
        elif c == '\\':
            ignore = True
        elif c == '"':
            if len(token) != 0:
                tokened = True
        else:
            token += c

    return token, rest_of_line


def tokenize_args(args):
    r"""Takes args as key/value pairs with spaces between and returns dict with
    keys and values

    Args:
        args (str): args as key/value pairs with spaces between

    Returns:
        dict: dict with keys and values

    Examples:
        >>> tokenize_args(r'key1="value_1" key2="value\"2\"" num=123')
        {'key1': 'value 1', 'key2': 'value"2"', 'num': 123}"""

    data = dict()
    while args:
        key, _, args = args.partition("=")
        value = None

        if str(args).startswith('"'):
            # value, _, args = args[1:].partition('"')
            value, args = read_next_string_token(args)
            value = value.replace('_', ' ')
        else:
            value, _, args = args.partition(" ")
            if value.isdecimal():
                value = int(value)
            elif '.' in value:
                value = float(value)

        if value:
            data[key.strip()] = value

    return data


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float,
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class_name> . <command> ([ <id> [ <*args> or <**kwargs> ]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formatting - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # !FIX: possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, _):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, _):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, _):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class """

        if not args:
            print("** class name missing **")
            return

        cls, _, args = args.partition(" ")

        if not models.injector.hasClass(cls):
            print("** class doesn't exist **")
            return

        cls = models.injector[cls]
        new_instance = cls()
        args = tokenize_args(args)

        req_attrs = cls.getRequiredAttributes()
        for attr in req_attrs:
            if attr not in args:
                print("** missing attribute: {} **".format(attr))
                return

        # Looks like this is the way to do it, Holy Crab!!!
        for key, value in args.items():
            setattr(new_instance, key, value)

        print(new_instance.id)
        models.storage.new(new_instance)
        models.storage.save()

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type with params\n")
        print("[Usage]: create <className> <param 1> <param 2> ...\n")
        print("Where <className> is the name of the class to create")
        print(
            "and <param> is any number of parameters to assign to the class\n")

        print("The <param> format: <key_name>=<value>")
        print("Value types with examples:")
        print("\tint: 123")
        print("\tfloat: -123.456")
        print('\tstr: "string_\\"quote_escape\\"_string"')
        print("""\t\tStrings must be in double quotes
\t\tall '_' replaced by spaces
\t\tthe above example is solved to => String "quote_escape" String
""")
        print("Statement Example:\n\tcreate State name=\"California\"")

    def do_show(self, args):
        """ Method to show an individual object """

        if not args:
            print("** class name missing **")
            return

        c_name, _, c_id = args.partition(" ")
        c_id = c_id.strip()

        if not models.injector.hasClass(c_name):
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        BaseModel = models.general_injector['BaseModel']
        all_objs = models.storage.all(c_name)
        try:
            obj = all_objs[BaseModel.generateObjectKey(c_name, c_id)]
            print(obj)
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """

        if not args:
            print("** class name missing **")
            return

        c_name, _, c_id = args.partition(" ")
        c_id = c_id.strip()

        if not models.injector.hasClass(c_name):
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        obj = None
        try:
            BaseModel = models.general_injector['BaseModel']
            all_objs = models.storage.all(c_name)
            key = BaseModel.generateObjectKey(c_name, c_id)
            obj = all_objs[key]
        except KeyError:
            print("** no instance found **")

        if obj:
            models.storage.delete(obj)
            models.storage.save()

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class """

        if args:
            args = args.strip()
            if args not in models.injector.classes:
                print("** class doesn't exist **")
                return
        else:
            args = None

        print([str(v) for v in models.storage.all(args).values()])

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        args = args.split()
        args = None if not args else args[0]
        objs = models.storage.all(args)
        print(len(objs))

    def help_count(self):
        """ """
        print("Usage: count [<class_name>]")

    def do_update(self, args):
        """ Updates a certain object with new info """
        if not args:
            print("** class name missing **")
            return

        # isolate class_name from id/args, ex: (<cls>, delim, <id/args>)
        c_name, _, args = args.partition(" ")

        if not models.injector.hasClass(c_name):  # class name invalid
            print("** class doesn't exist **")
            return

        if not args:  # id not present
            print("** instance id missing **")
            return

        # isolate id from args
        c_id, _, args = args.partition(" ")

        # generate key from class and id
        BaseModel = models.general_injector['BaseModel']
        key = BaseModel.generateObjectKey(c_name, c_id)

        all_objs = models.storage.all(c_name)

        # determine if key is present
        if key not in all_objs:
            print("** no instance found **")
            return

        args = self.__parse_update_args(args)  # parse the passed args
        if not args:
            return

        obj = all_objs[key]  # get the instance by key
        self.__apply_update(obj, args)  # apply all updates to the object

    def __parse_update_args(self, args):
        """ Parses update method arguments

        Args:
            args (str): args as key/value pairs with spaces between
            or python like dictionary

        Returns: dict|None - either dictionary of attributes key/value or None
        """

        if not args:
            print("** attribute name missing **")
            return None

        # first determine if python like dict or key/value args
        if '{' in args and '}' in args and type(eval(args)) is dict:
            args = eval(args)
        else:  # isolate args
            att_name, att_val = None, None

            if args[0] == '"':  # check for quoted key
                second_quote = args.find('"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]
            else:
                att_name, _, args = args.partition(' ')

            if not args:  # no value
                print("** value missing **")
                return None

            # check for quoted val
            if args[0] == '"':
                att_val = args[1:args.find('"', 1)]
            else:
                att_val, _, args = args.partition(' ')

            args = {att_name: att_val}

        return args

    def __apply_update(self, obj, args):
        """Applies updates to an individual object

        Args:
            obj (BaseModel based Object): object to update
            args (dict): attributes to update key/value
        """
        for key, value in args.items():
            # ignore invalid attributes
            if key in ['__class__', 'id', 'updated_at', 'created_at']:
                print("** not allowed attribute name: {} **".format(key))
                return

            # type cast as necessary
            if key in HBNBCommand.types:
                value_type = HBNBCommand.types[key]
                value = value_type(value)

            # update the value
            setattr(obj, key, value)

        obj.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>")
        print(
            "Usage: update <className> <id> {'<attName>': '<attVal>', ...}\n")

    def do_classes(self, _):
        """ Lists all allowed classes """
        print([key for key in models.injector.keys])

    def help_classes(self):
        """ Help information for the classes command """
        print("Lists all classes of objects that can be instantiated.")
        print("[Usage]: classes\n")

    def do_attributes(self, arg):
        """ Lists all attributes of a class """

        arg = arg.strip()
        if not arg:
            print("** class name missing **")
            return
        if not models.injector.hasClass(arg):
            print("** class doesn't exist **")
            return

        req_attrs = models.injector[arg].getRequiredAttributes()
        print(req_attrs)

    def help_attributes(self):
        """ Help information for the attributes command """
        print("Lists all attributes of a class")
        print("[Usage]: attributes <className>\n")


if __name__ == "__main__":
    models.initModelsAndStorage()
    HBNBCommand().cmdloop()
