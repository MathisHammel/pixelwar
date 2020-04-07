import sys

def read_file(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]
        return lines

proofs = [
    # *read_file('proofs_25i.txt'),
    # *read_file('proofs_25o.txt'),
    # *read_file('proofs_52i.txt'),
    # *read_file('data/proofs_52o.txt'),
    # *read_file('data/proofs_522.txt')[358:],
    # *read_file('data/proofs_hihihi.txt'),
    # *read_file('data/proofs_hohoho.txt'),
    # *read_file('data/proofs_ioioio.txt'),
    # *read_file('data/proofs_hahaha.txt'),
    # *read_file('data/proofs.txt'),
    # *read_file('data/proofs_cg.txt'),
    # *read_file('data/proofs_codingame.txt'),
    # *read_file('data/proofs_Hammel.txt'),
    # *read_file('data/proofs_lolilolz.txt'),
    # *read_file('data/proofs_CGG.txt'),
    # *read_file('data/proofs_CodinGame.txt'),
    # *read_file('data/proofs_CGlove.txt'),
    # *read_file('data/proofs_lolilola.txt'),
    # *read_file('data/proofs_lolilolb.txt'),
    # *read_file('data/proofs_golri.txt'),
    # *read_file('data/proofs_golri2.txt'),
    *read_file('proofs_java.txt')[24576:],
    *read_file('proofs_java_2.txt')[4882:]
]

if __name__ == '__main__':
    print(len(proofs))
