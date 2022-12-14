import sys
import logging
import runcli, runserver

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)s: %(message)s')
    if len(sys.argv) == 1:
        print("Usage: python main.py [cli|server]")
    elif len(sys.argv) == 2:
        if sys.argv[1] == "server":
            runserver.run()
        if sys.argv[1] == "cli":
            runcli.run()
        else:
            print("Invalid argument")

# TODO NEXT: Soheil - Video Playback
# TODO NEXT: Parsa + Sara - Server Client Communication