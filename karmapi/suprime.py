from math import sqrt

def suprime(n):

    end = int(sqrt(n))
    print('end is:', end + 1)
    show_at = 10
    for f in range(2, end + 1):
        if f > show_at:
            print (f,'is current int percent done:', f / end)
            show_at = show_at * 10

        if n % f == 0:
            print(f,'is factor of n')
            return False

    return True


if __name__ == '__main__':
    #n = input("enter a number: ")

    #n = int(n)

    import sys

    for n in sys.argv[1:]:
        n = int(n)
        isprime = suprime(n)

        print(n, isprime)    




