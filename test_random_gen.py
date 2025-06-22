from random import sample
from sys import argv, exit

count = 10

def main():
    if len(argv) < 2:
        print('Usage: python test_random_gen.py <filename>')
        exit(1)
    
    filename = argv[1]
    
    testdata = [str(_) for _ in sample(range(1, 101), count)]
    line = ' '.join(testdata)

    with open(f'{filename}.txt', 'w') as f:
        f.write(line)
    print(f'written shxt to {filename}.txt successfully uwu')

if __name__ == "__main__":
    main()
