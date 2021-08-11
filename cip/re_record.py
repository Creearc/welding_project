to_bin = lambda x : bin(int.from_bytes(x, 'big'))[2:]
reverse = lambda x : x[::-1]
to_normal = lambda x : ''.join([reverse(x[i * 4 : i * 4 + 4]) for i in range(len(x) // 4)])


fi = open('record_1.py', 'r')
fo = open('record_1_n.py', 'w')
fo.write('arr = [\n')
for l in fi:
  info = l[17:-2]
  fo.write('{},\n'.format(info))
  
fo.write(']\n')
fi.close()
fo.close()
