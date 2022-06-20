import numpy

# Неплохо бы вместо циклов всякие фокусы нампая
# Зато с примером из условия все правильно считаем
# тут тоже assume массив одномерный (я тупой не умею в нампай просто)
def get_ewma(data_array : numpy.array, window_size : int, last_weight : int) -> numpy.array:
    res = []
    total_weight = 0.
    tmp = last_weight
    for i in range(window_size):
        total_weight += tmp
        tmp *= 2
    for i in range(window_size, len(data_array) + 1):
        s = 0.
        lw = last_weight
        for j in range(i - window_size, i):
            # print(f"i = {i}, j = {j}")
            s += lw * data_array[j]
            lw *= 2
        res.append(s / total_weight)
    return numpy.array(res)
