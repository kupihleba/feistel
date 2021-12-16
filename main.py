import logging
from copy import copy
from typing import List, Tuple

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def byte_xor(ba1: List, ba2: List) -> List:
    return [a ^ b for a, b in zip(ba1, ba2)]


def pp(arr) -> str:
    if type(arr) is int:
        return str(arr)
    return ' '.join(map(str, arr))


class Engine:
    def __init__(self, s, p, keys):
        self._n = len(s)
        self._s = s  # Substitution block
        self._p = p  # Permutation block
        self._keys = keys
        self._iter = 0
        self._register = [0] * self._n

    def __substitute(self, val: List) -> List:
        bin = int(''.join(map(str, val)), 2)
        logger.debug('Substitution')
        res_bin = self._s[bin]
        res = list(map(int, f'{res_bin:b}'))
        res = [0] * (len(val) - len(res)) + res
        logger.debug(f'{pp(val)} ({bin}) -> {pp(res)} ({res_bin})')
        return res

    def __permutate(self, val: List) -> List:
        logger.debug('Permutation')
        res = copy(val)
        for dest, src in enumerate(self._p):
            res[dest] = val[src]
        logger.debug(f'{pp(val)} -> {pp(res)}')
        return res

    def run(self, input):
        self._register = list(input)
        print('REG: ', pp(self._register))
        for _ in range(len(self._keys)):
            print('REG: ', pp(self._step()))
        return self._register

    def _step(self):
        half = len(self._register) // 2
        left, right = self._register[:half], self._register[half:]
        key = self._keys[self._iter]
        print(
            f'ITERATION {self._iter}:',
            f'{pp(left)} | {pp(right)}',
            f'ROUND KEY: {pp(key)}',
            sep='\n'
        )

        # F
        logger.debug('XOR')
        block = byte_xor(right, key)
        logger.debug(f'{pp(right)} ^ {pp(key)} -> {pp(block)}')
        half_block = len(block) // 2
        l_block, r_block = block[:half_block], block[half_block:]
        logger.debug(f'{pp(l_block)} | {pp(r_block)}')
        l_s = self.__substitute(l_block)
        r_s = self.__substitute(r_block)
        s = l_s + r_s
        p = self.__permutate(s)

        logger.debug('XOR')
        new_p = byte_xor(left, p)
        logger.debug(f'{pp(left)} ^ {pp(p)} -> {pp(new_p)}')
        self._register = right + new_p
        self._iter += 1
        return self._register


def main(s: Tuple, p: Tuple, keys: Tuple, data: Tuple):
    e = Engine(s, p, keys)
    result = e.run(data)
    print(
        f'MSG:\t{pp(data)}',
        f'RES:\t{pp(result)}',
        sep='\n'
    )


if __name__ == '__main__':
    main(  # Example:
        s=(14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
        p=(0, 4, 1, 6, 2, 6, 3, 7),
        keys=(
            (1,) * 8,
            (1, 0, 1, 0, 1, 0, 1, 0),
            (0, 1, 0, 1, 0, 1, 0, 1),
            (1,) * 8,
        ),
        data=(0,) * 16
    )
