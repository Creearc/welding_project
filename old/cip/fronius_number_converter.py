calc_speed = lambda x : x * 327.67 * 2 / 65535 - 327.67
calc_speed2 = lambda x : x * 327.68 * 2 / 65535

re_calc_speed = lambda x : int((327.67 + x) * 65535 / 327.68 / 2) 
re_calc_speed2 = lambda x : int(x / 327.68 / 2 * 65535)

x = 39321
y = 6
print(calc_speed2(x))
print(re_calc_speed2(calc_speed2(x)))
print(re_calc_speed2(x))

print(calc_speed(x))
print(re_calc_speed(calc_speed2(x)))
print(re_calc_speed(x))
