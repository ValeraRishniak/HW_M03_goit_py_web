from time import time
from multiprocessing import Pool, cpu_count


def factorize(numbers):
    for num in numbers:
        result_lst = []
        for i in range (1, max(numbers)+1):
            if num % i == 0:
                result_lst.append(i)
        # print(f'Divisors of {num} is {result_lst}\n')
        


if __name__ == '__main__':

    numbers = [128, 255, 99999, 10651060, 106510609]
    t1 = time()
    result = factorize(numbers)
    print(f'synchronous: {time() - t1}')
    processors = cpu_count()    
    t2 = time()
    pool = Pool(processors)
    result = pool.apply_async(factorize, numbers)
    print(f'parallel computing by {processors} processors {time() - t2}')
