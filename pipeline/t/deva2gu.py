"""deva2gu: convert Devanagari text to Gujarati script (Unicode block offset), keeping danda/double danda."""
import sys,re
def conv(s):
    out=[]
    for ch in s:
        o=ord(ch)
        if 0x0900<=o<=0x097F and ch not in '।॥':
            g=o+0x180
            out.append(chr(g))
        else: out.append(ch)
    return ''.join(out)
if __name__=='__main__':
    print(conv(open(sys.argv[1],encoding='utf-8').read()))
