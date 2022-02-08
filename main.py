import sys
import camera

if len(sys.argv) < 2:
    print("No file or stdin mode specified! Use -i for stdin mode or -f (filename) for file mode.")

if sys.argv[1] == '-i':
    camera.track_stdin()
elif sys.argv[1] == '-f':
    if(len(sys.argv) < 3):
        print("No filename specified. Please specify a file name.")
    else:
        camera.track_file(sys.argv[2])
        print("Fardet")
else:
    print("Unrecognized option {}".format(sys.argv[1]))