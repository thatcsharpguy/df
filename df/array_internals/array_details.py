import numpy as np


def show_array_details(arr: np.array):
    details = [
        ("Shape", arr.shape),
        ("Stride", arr.strides),
        ("Type", arr.dtype),
        ("Elements", arr.size),
        ("Bytes", arr.nbytes),
        ("Bits", arr.itemsize * 8),
    ]

    for label, value in details:
        print(f"{(label+':').ljust(12)}{str(value)}")
    print()