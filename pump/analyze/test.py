

def test():
    T2_MIN=10
    T2_MAX=11
    T4_MIN=10
    T4_MAX=12
    T2=T2_MIN
    T4=T4_MIN
    while T2 >= T2_MIN and T2 <= T2_MAX:
        T2 = T2 + 0.1
        while T4 >= T4_MIN and T4 <= T4_MAX:
            print(T2,T4)
            T4 = T4 + 0.1
    print(T2)
    i = 0
    while i < 3:
        print("这是第%d行" % i)
        j = 0
        while j < 4:
            print("学python")
            j += 1
        print()
        i += 1


if __name__ == '__main__':
    test()



