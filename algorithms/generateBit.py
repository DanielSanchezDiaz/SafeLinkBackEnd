#!/usr/bin/env python
# contact me: artem [at] dinaburg [dot] org
import sys
import socket
import tldextract

def bitflip(num, pos):
    shiftval = 1 << pos

    if num & shiftval > 0:
        return num & (~shiftval)
    else:
        return num | shiftval

def is_valid(charnum):
    if  (ord('0') <= charnum <= ord('9')) or\
        (ord('a') <= charnum <= ord('z')) or\
        (ord('A') <= charnum <= ord('Z')) or\
        charnum == ord('-'):
        return True
    else:
        return False


def generate(fullDomain):
    parts = tldextract.extract(fullDomain)
    name = parts.domain
    suffix = parts.suffix
    ret = []
    for i in range(0, len(name)):
        val = name[i]
        for bit in range(0, 8):
            newval = bitflip(ord(val), bit)
            if is_valid(newval) and val.lower() != chr(newval).lower():
                newname = name[:i] + chr(newval)
                if i + 1 < len(name):
                    newname += name[i + 1:]
                ret.append('%s.%s' % (newname, suffix))
    return ret

def generate_tld_bitflips(tld):
    name = tld
    ret = []
    for i in range(0, len(name)):
        val = name[i]
        for bit in range(0, 8):
            newval = bitflip(ord(val), bit)
            if is_valid(newval) and val.lower() != chr(newval).lower():
                newname = name[:i] + chr(newval)
                if i + 1 < len(name):
                    newname += name[i + 1:]
                if tldextract.extract(newname).suffix != "":
                    ret.append(newname)
    return ret

def usage():
    print("Usage:")
    print("python bs_models.py <domain name> (-tld)")
    print("")
    print("example:")
    print("python bs_models.py www.google.com")
    print("")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()
        sys.exit()
    name = sys.argv[1]

    if len(sys.argv) > 2:
        if sys.argv[2] == "-tld":
            print(generate_tld_bitflips(name))
    else:
        print(generate(name))





