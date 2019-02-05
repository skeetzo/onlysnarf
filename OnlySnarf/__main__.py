import sys
import os

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    os.system("python3 OnlySnarf/onlysnarf.py "+" ".join(args))

if __name__ == "__main__":
    try:
        main()
    except:
        # print(sys.exc_info()[0])
        print("Shnarf!")
    finally:
        sys.exit(0)