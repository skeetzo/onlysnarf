import sys
import os

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    os.system("python3 "+os.path.join(os.path.dirname(os.path.realpath(__file__)),'snarf.py')+" "+" ".join(args))

if __name__ == "__main__":
    try:
        main()
    except:
        print(sys.exc_info()[0])
        print("Shnarf!")
    finally:
        sys.exit(0)