import yaml
import logging
import sys
import pprint
import re

'''
== Reminder of available Exception ==

Exception 	            Base class for all exceptions
StopIteration 	        Raised when the next() method of an iterator does not point to any object.
SystemExit 	            Raised by the sys.exit() function.
StandardError 	        Base class for all built-in exceptions except StopIteration and SystemExit.
ArithmeticError     	Base class for all errors that occur for numeric calculation.
OverflowError 	        Raised when a calculation exceeds maximum limit for a numeric type.
FloatingPointError 	    Raised when a floating point calculation fails.
ZeroDivisonError 	    Raised when division or modulo by zero takes place for all numeric types.
AssertionError 	        Raised in case of failure of the Assert statement.
AttributeError 	        Raised in case of failure of attribute reference or assignment.
EOFError 	            Raised when there is no input from either the raw_input() or input() function and the end of file is reached.
ImportError 	        Raised when an import statement fails.
KeyboardInterrupt 	    Raised when the user interrupts program execution, usually by pressing Ctrl+c.
LookupError 	        Base class for all lookup errors.
IndexError              Raised when an index is not found in a sequence.
KeyError                Raised when the specified key is not found in the dictionary.
NameError 	            Raised when an identifier is not found in the local or global namespace.
UnboundLocalError       Raised when trying to access a local variable in a function or method but no value has been assigned to it.
EnvironmentError        Base class for all exceptions that occur outside the Python environment.
IOError                 Raised when an input/ output operation fails, such as the print statement or the open() function when trying to open a file that does not exist.
IOError                 Raised for operating system-related errors.
SyntaxError             Raised when there is an error in Python syntax.
IndentationError        Raised when indentation is not specified properly.
SystemError 	        Raised when the interpreter finds an internal problem, but when this error is encountered the Python interpreter does not exit.
SystemExit 	            Raised when Python interpreter is quit by using the sys.exit() function. If not handled in the code, causes the interpreter to exit.
ValueError 	            Raised when the built-in function for a data type has the valid type of arguments, but the arguments have invalid values specified.
RuntimeError 	        Raised when a generated error does not fall into any category.
NotImplementedError     Raised when an abstract method that needs to be implemented in an inherited class is not actually implemented.
'''

logger = logging.getLogger( 'defconf' )
logger.setLevel(logging.INFO)

type_list = {}
type_list['string'] = "<type 'str'>"
type_list['integer'] = "<type 'int'>"
type_list['dict'] = "<type 'dict'>"
type_list['bool'] = "<type 'bool'>"
type_list['list'] = "<type 'list'>"


def main():

    ## Get CLI arguments
    config_file_name = sys.argv[1]
    definition_file_name = sys.argv[2]

    logger.info('Will load Config "%s" and def "%s"', config_file_name, definition_file_name )

    ## load master definition file
    # master_definition_file = open('definitionfile.def.yml')
    # master_definition = yaml.load(master_definition_file)

    ## load definition file and validate it (to be implemented)
    definition_file = open(definition_file_name)
    definition = yaml.load(definition_file)

    ## load configuration file and validate it
    config_file = open(config_file_name)

    config = yaml.load(config_file)

    try:
        validate_config( config, definition, config_file_name )
        print ' = Configuration file valid = '
    except Exception as e:
        logger.error('Configuration file not valid : ' + str(e))

def validate_config( config_file, definition_file, name ):
    validate_dict( config_file, definition_file['validate']['main'], definition_file, 'root' )

def validate_dict( config, definition, definition_file, name ):
    global type_list
    logger.debug('->validate_dict() Start for %s ', name )

    ## Go over all elements of config
    for key, value in config.iteritems():
        item_name = name + '.' + key
        # For each element check if exists in definition unless * is defined
        if not definition.has_key('*') and not definition.has_key(key):
            raise IndexError("Unable to find " + item_name + " in definition file")

    # Check if All mandatory elements are present
    for key, value in definition.iteritems():
        if value.has_key('mandatory') and value['mandatory'] == 1 and not config.has_key(key):
            raise IndexError("Mandatory element " + item_name + " has not been found ")

    ######
    ## Check Element content
    ######
    for key, value in config.iteritems():

        ## Define name to use for logging and reporting
        ## If needed update the key in case it's *
        item_name = name + '.' + key
        initial_key = key
        if not definition.has_key(key):
            logger.debug('->validate_dict() Key replace to "*" for %s', item_name )
            key = '*'

        item_type = type(value)
        logger.debug('->validate_dict() %s Check element content, type is %s ', item_name, str(item_type) )

        ## Check type if type is define
        if definition[key].has_key('type'):
            logger.debug('->validate_dict() %s: Option "type" found, will check if is %s', item_name, definition[key]['type'] )

            if str(item_type) == "<type 'dict'>" or str(item_type) == "<type 'list'>" or str(item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>" or str(item_type) == "<type 'bool'>":
                if type_list[definition[key]['type']] != str(item_type):
                    raise ValueError(item_name +": Type is not valid for '" + item_name + "': expect '" + type_list[definition[key]['type']] + "' found '" + str(item_type))
            else:
                raise RuntimeError(item_name + ": Type not supported " + str(item_type))

        ## Check values if define
        if definition[key].has_key('values'):
            logger.debug('->validate_dict() %s: Option "values" found, will check if is %s', item_name, definition[key]['values'] )

            do_match = 0
            for def_value in definition[key]['values']:
                if str(item_type) == "<type 'list'>":
                    for entry_value in value:
                        if value == def_value:
                            do_match = 1
                elif  str(item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>":
                    if value == def_value:
                        do_match = 1
                else:
                    raise NotImplementedError("Values option is not supportd with type: " + str(item_type) )

            if do_match == 0:
                raise ValueError("Element value is not valid for '" + item_name + "': expect '" + str(definition[key]['values']) + "' found '" + str(value))

        ## Check Regex
        if definition[key].has_key('validate'):
            logger.debug('->validate_dict() %s: Option "validate" found, will check it', item_name )
            validate_name = definition[key]['validate']
            validate_type = ''

            # check if is a Validate Block or a Regex

            logger.debug('->validate_dict() %s: Will check search for %s in validate and regex sections', item_name, validate_name )

            if definition_file['validate'].has_key(validate_name):
                validate_type = 'block'

            elif definition_file['regex'].has_key(validate_name):
                validate_type = 'regex'
            else:
                raise AttributeError(item_name + " Option validate: Unable to find '" + definition[key]['validate'] + "'  neither in Validate nor regex section")

            ## Do the test based on the type
            if validate_type == 'regex':
                do_match = 0
                reg = re.compile(definition_file['regex'][validate_name])

                if str(item_type) == "<type 'list'>":
                    for entry_value in value:
                        if reg.match( entry_value ):
                            do_match = 1
                elif  str(item_type) == "<type 'str'>" or str(item_type) == "<type 'int'>":
                    if reg.match( value ):
                        do_match = 1
                else:
                    raise NotImplementedError("Regex option is not supportd with type: " + str(item_type) )

                if do_match == 0:
                    raise ValueError(item_name + ": Value is not valid, do not match regex '" + validate_name + "' - value(s): " + str(value))

            elif validate_type == 'block':
                validate_name = definition[key]['validate']
                logger.debug('->validate_dict() %s: Will check block %s with %s', item_name, initial_key, validate_name )

                validate_dict(config[initial_key], definition_file['validate'][validate_name], definition_file, item_name)

            else:
                raise RuntimeError("Unexpected error, should never end here")

    ############
    ## Add default value if not define
    #############
    for key, value in definition.iteritems():
        if value.has_key('default') and not config.has_key(key):
            item_name = name + '.' + key
            logger.debug('->validate_dict() %s: Default value missing', item_name )
            config[key] = value['default']

if __name__ == '__main__':
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
    main()
