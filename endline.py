#!/usr/bin/python3

import os
import sys
import argparse

version = "1.1"
show_warnings = True

default_end = os.linesep
unix_end = "\n"
win_end = "\r\n"
mac_end = "\r"

def main(argv):
	using_stdin = not sys.stdin.isatty()
	parse = argparse.ArgumentParser(description="Change file line ending (LF, CRLF, or CR).")
	if not using_stdin:
		parse.add_argument("input", metavar="<input-file>", nargs=1, help="input file")
	parse.add_argument("-v", "--version", action="version", version="%(prog)s " + version)
	parse.add_argument("-o", dest="output", metavar="<output-file>", nargs=1, help="optional output file")
	parse.add_argument("-u", "--unix", dest="unix", action="store_true", help="use unix style (LF) line endings")
	parse.add_argument("-w", "--windows", dest="windows", action="store_true", help="use windows style (CRLF) line endings")
	parse.add_argument("-m", "--mac", dest="mac", action="store_true", help="use mac style (CR) line endings")
	args = parse.parse_args(argv)

	if not using_stdin:
		i = args.input[0]
	o = args.output

	if o:
		o = o[0]

	if not (using_stdin or os.path.exists(i)):
		print("error: '" + i + "' doesn't exist", file=sys.stderr)
		exit(1)

	if o and os.path.exists(o):
		if show_warnings:
			print("warning: '" + o + "' will be overwritten", file=sys.stderr)

	if using_stdin:
		txt = sys.stdin.read()
	else:
		f = open(i, "r")
		txt = f.read()
		f.close()

	multiple_ends = False
	end = default_end
	if args.mac:
		end = mac_end
	if args.windows:
		if end != default_end:
			multiple_ends = True
		end = win_end
	if args.unix:
		if end != default_end:
			multiple_ends = True
		end = unix_end

	if multiple_ends and show_warnings:
		if end == unix_end:
			print("warning: defaulting to unix style (LF) endings", file=sys.stderr)
		else:
			print("warning: defaulting to windows style (CRLF) endings", file=sys.stderr)

	if o:
		f = open(o, "w", newline=end)
		f.write(txt)
		f.close()
	else:
		for line in txt.split("\n")[:-1]:
			print(line, end=end)

if __name__ == '__main__':
	main(sys.argv[1:])
