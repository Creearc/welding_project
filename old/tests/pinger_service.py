import os

ips = ['192.168.68.{}'.format(i) for i in range(200, 210)]

for ip in ips:
    response = os.system("ping -n 1 {}".format(ip))
    print(ip, response)
