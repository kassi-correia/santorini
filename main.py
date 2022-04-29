import sys
from SantoriniCLI import SantoriniCLI
from Exception import InvalidArgs







if __name__ == "__main__":
    try:
        print("running...")
        if (len(sys.argv)) > 5 or (len(sys.argv)) < 1:
            raise InvalidArgs()

        elif (len(sys.argv)) == 1:
            SantoriniCLI().run()

        elif (len(sys.argv)) == 2:
            if (sys.argv[1]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            SantoriniCLI(sys.argv[1]).run()

        elif (len(sys.argv)) == 3:
            if (sys.argv[1]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[2]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            SantoriniCLI(sys.argv[1], sys.argv[2]).run()

        elif (len(sys.argv)) == 4:
            if (sys.argv[1]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[2]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[3]) not in  ['on', 'off']:
                raise InvalidArgs()
            SantoriniCLI(sys.argv[1], sys.argv[2], sys.argv[3]).run()
        
        else:
            if (sys.argv[1]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[2]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[3]) not in  ['on', 'off']:
                raise InvalidArgs()
            if (sys.argv[4]) not in  ['on', 'off']:
                raise InvalidArgs()
            SantoriniCLI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).run()
   
    except InvalidArgs:
        print("Invalid arguments")
