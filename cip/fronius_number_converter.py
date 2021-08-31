calc_speed = lambda x : x * 327.67 * 2 / 65535 - 327.67
calc_speed2 = lambda x : x * 327.68 * 2 / 65535

re_calc_speed2 = lambda x : int(x / 327.68 / 2 * 65535)

x = 1062
print(calc_speed2(x))
print(re_calc_speed2(calc_speed2(x)))
