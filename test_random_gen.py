from random import sample
from sys import argv, exit

def main():
    if len(argv) < 2:
        print('Usage: python test_random_gen.py <filename>')
        exit(1)
    
    filename = argv[1]
    
    testdata = [str(_) for _ in sample(range(1, 101), 10)]
    line = ' '.join(testdata)

    with open(filename, 'w') as f:
        f.write(line)
    print(f'written shxt to {filename} successfully uwu')

if __name__ == "__main__":
    main()
