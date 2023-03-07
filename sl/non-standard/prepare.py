import sys

for line in sys.stdin:
    if "\t" in line:
        line_split = line.split("\t")
        if " " in line_split[1]:
            line_split[1] = line_split[1].replace(" ", "")
        line = "\t".join(line_split)
    sys.stdout.write(line)