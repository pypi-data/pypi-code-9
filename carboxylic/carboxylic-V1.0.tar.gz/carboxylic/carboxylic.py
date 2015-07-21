from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import instruction

class CarboxylicHalt(Exception):
    pass

class CarboxylicInterpreter(object):

    def __init__(self, commands):
        self.accumulator = 0
        self.branchpoints = {}
        self.commands = commands
        self.counter = 0
        self.registers = {}
        
        while self.counter < len(self.commands):
            operator, operand = self.get_operator_and_operand(
                    self.commands[self.counter])
            if operator == "DEF":
                self.branchpoints.update({operand : self.counter})
            self.counter += 1
        
        self.counter = 0

    def start(self):
        while self.counter < len(self.commands):
            operator, operand = self.get_operator_and_operand(
                    self.commands[self.counter])
            try:
                self.execute(operator, operand)
            except CarboxylicHalt as e:
                print "Halted."
                break

            self.counter += 1
    
    def get_operator_and_operand(self, command):
        instructions = command.split()
        operator = instructions[0].upper() if 0 < len(instructions) else ""
        operand = instructions[1].upper() if 1 < len(instructions) else ""
        return [operator.upper(), operand]
    
    def execute(self, operator, operand):
        try:
            instruction.commands[operator](self, operand)
        except KeyError:
            pass

    def get_branch(self, operand):
        try:
            return self.branchpoints[operand]
        except KeyError:
            raise CarboxylicHalt("Branchpoint %s doesn't exist." % operand)
    
    def get_value(self, operand):
        try:
            return int(operand)
        except ValueError:
            try:
                return self.registers[operand]
            except KeyError:
                raise CarboxylicHalt("Undefined name %s." % operand)

def main():
    ap = ArgumentParser(description="Use the carboxylic interpreter.",
                        formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("script", type=open, help="The script to run.")
    args = ap.parse_args()

    try:
        CarboxylicInterpreter(args.script.readlines()).start()
    except:
        print "Halted."

    args.script.close()
    
if __name__ == "__main__":
    main()
