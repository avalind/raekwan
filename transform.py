#!/usr/bin/env python
import fileinput


def process(line):
    parts = line.split()
    print("chr{0}\t{1}\t{2}".format(parts[0],
                                    int(parts[1])-10,
                                    int(parts[1])+10))

for line in fileinput.input():
    process(line)
