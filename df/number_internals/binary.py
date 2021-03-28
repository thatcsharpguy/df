from typing import List

import numpy as np

SIZE_TYPES = {np.float64: (11, 53), np.float32: (8, 24), np.float128: (15, 113)}


def join(*args):
    return " | ".join(args)


def show_float(number: float, type_=np.float64):
    show_binary_float(
        number, number_to_bitstring(np.array(number, dtype=type_)), *SIZE_TYPES[type_]
    )


def bit_word_to_mantissa_val(bitword: str) -> float:
    mantissa = int(bitword, base=2)
    return mantissa / (2.0 ** len(bitword))


def show_binary_float(
    expected_number: float, bit_word: str, exponent_size: int, mantissa_size: int
):
    mantissa_size -= 1
    bias = (2 ** (exponent_size - 1)) - 1
    total_width = exponent_size + mantissa_size + 1

    bit_chunks = slice_string(bit_word, 1, exponent_size, mantissa_size)

    sign = -1 if bit_word[0:1] == "1" else 1
    exponent = int(bit_word[1 : 1 + exponent_size], base=2) - bias
    mantissa = bit_word_to_mantissa_val(bit_word[1 + exponent_size : total_width])
    infinite = exponent == 2 ** (exponent_size - 1)

    print(
        join(
            "Sign".ljust(4), "Exp".ljust(exponent_size), "Mantissa".ljust(mantissa_size)
        )
    )
    print(f"   {join(*bit_chunks)}")
    print(
        join(f"{sign:4d}", f"{exponent:{exponent_size}}", f"{mantissa:{mantissa_size}}")
    )
    if infinite:
        print("Infinite/NaN")
    else:
        print(f"  = {sign} * {1 + mantissa} * 2^{exponent}")
        print(f"  = {sign} * {1.0 + mantissa} * {2 ** exponent}")
        print(f"  = {expected_number:.20f}")

    print()


def slice_string(word: str, *steps: List[int]) -> List[str]:
    out = []
    word_length = len(word)
    original_length = sum(steps)
    steps = list(steps)

    if original_length < word_length:
        steps.append(word_length - original_length)

    i = 0
    for step in steps:
        out.append(word[i : i + step])
        i = i + step

    return out


def number_to_bitstring(x: np.array) -> str:
    endianess = x.dtype.newbyteorder("B")
    return "".join(f"{d:08b}" for d in x.astype(endianess).tobytes())
