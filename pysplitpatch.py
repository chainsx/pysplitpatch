#!/usr/bin/env python3
import os
import sys


class Splitter:
    def __init__(self, file):
        self.filename = file
        self.fullname = False

    def fullname(self, opt):
        self.fullname = opt

    def validFile(self):
        return os.path.exists(self.filename) and os.access(self.filename, os.R_OK)

    def createFile(self, filename):
        if os.path.exists(filename):
            print(f"File {filename} already exists. Renaming patch.")
            appendix = 0
            zero = str(appendix).rjust(3, '0')
            while os.path.exists(f"{filename}.{zero}"):
                appendix += 1
                zero = str(appendix).rjust(3, '0')
            filename += f".{zero}"
        else:
            path = ""
            tokens = filename.split("/")
            for i in (range(len(tokens) - 1)):
                path = path + tokens[i]
                if i != len(tokens) - 1:
                    path = path + "/"
            if not os.path.exists(path) and path != "":
                os.makedirs(path)
        return open(filename, "w")

    def getFilepath(self, line):
        path = ""
        tokens = line.split(" ")
        tokens = tokens[-1].split(":")
        tokens = tokens[0].split("/")
        for i in (range(len(tokens) - 1)):
            path = path + tokens[i + 1]
            if i != len(tokens) - 2:
                path = path + "/"

        if self.fullname:
            return "-".join(tokens)
        else:
            return path.rstrip("\n")

    def splitByFile(self):
        outfile = None
        stream = open(self.filename, 'rb')
        while True:
            line = stream.readline()

            if line.startswith(b'diff '):
                if outfile:
                    outfile.close()
                filename = self.getFilepath(line.decode())
                filename += ".patch"
                print("processing: " + filename)
                outfile = self.createFile(filename)
                outfile.write(line.decode())
            else:
                if outfile:
                    outfile.write(line.decode("utf8", "ignore"))
            if not line:
                break


def help():
    print(f"""SYNOPSIS
    splitpatch FILE.patch

OPTIONS
    -h,--help
    -V,--version""")


def parsedOptions():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("ERROR: missing argument. See --help.")
        sys.exit(1)

    opts = {}

    opt = sys.argv[1]
    if opt in ['-h', '--help']:
        opts['help'] = True
    elif opt in ['-V', '--version']:
        opts['version'] = True
    elif opt.startswith('-'):
        print(f"ERROR: Unknown option: {opt}. See --help.")
        sys.exit(1)

    opts['file'] = sys.argv[-1]

    return opts


def main():
    opts = parsedOptions()

    if opts.get('help'):
        help()
        sys.exit()

    s = Splitter(opts['file'])
    if not s.validFile():
        print(f"File does not exist or is not readable: {opts['file']}")

    s.splitByFile()


if __name__ == '__main__':
    main()
