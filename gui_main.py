import sys
from SantoriniGUI import SantoriniGUI
from Exception import InvalidArgs







if __name__ == "__main__":
    try:
        if (len(sys.argv)) > 5 or (len(sys.argv)) < 1:
            raise InvalidArgs()

        elif (len(sys.argv)) == 1:
            SantoriniGUI()

        elif (len(sys.argv)) == 2:
            if (sys.argv[1]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            SantoriniGUI(sys.argv[1])

        elif (len(sys.argv)) == 3:
            if (sys.argv[1]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[2]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            SantoriniGUI(sys.argv[1], sys.argv[2])

        elif (len(sys.argv)) == 4:
            if (sys.argv[1]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[2]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[3]) not in  ['on', 'off']:
                raise InvalidArgs()
            SantoriniGUI(sys.argv[1], sys.argv[2], sys.argv[3])
        
        else:
            if (sys.argv[1]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[2]) not in  ['human', 'heuristic', 'random']:
                raise InvalidArgs()
            if (sys.argv[3]) not in  ['on', 'off']:
                raise InvalidArgs()
            if (sys.argv[4]) not in  ['on', 'off']:
                raise InvalidArgs()
            SantoriniGUI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
   
    except InvalidArgs:
        print("Invalid arguments")