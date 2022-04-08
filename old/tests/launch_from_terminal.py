import os
##
##result = os.system(r'"python A:/Projects/welding_project/old/tests/1.py bert"')
##print(result)
import zipfile
import subprocess
path = 'A:/Projects/welding_project/services/layers_splitter_service.py'
path = 'A:/Projects/welding_project/services/convert_ls_2_tp_service.py'
disk = path[:2]
path = path.split('/')
path, programm = '/'.join(path[:-1]), path[-1]

args = 'A:/Projects/welding_project/layers_splitter/data ' \
       'A:/Projects/welding_project/layers_splitter/data_result2 ' \
       ''
p = subprocess.Popen("{} & cd {} & python {} {}".format(disk, path, programm, args).split(),
                          stdout=subprocess.PIPE,
                          shell=True)

out, err = p.communicate()

result = out.decode('cp1251', errors='surrogateescape')
result = result.split('\n')
print('[{}]\nCode:\n{}\nOut:\n{}\n[end]'.format(programm, result[-3], result[-2]))


print(os.getcwd())
