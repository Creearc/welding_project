import os
import zipfile
import subprocess
import time

splitter_path = '../layers_splitter_service.py'
converter_path = '../convert_ls_2_tp_service.py'

def get_paths(path):
    disk = path[:2]
    path = path.split('/')
    path, programm = '/'.join(path[:-1]), path[-1]
    return disk, path, programm

def run_script(disk, path, programm, args):
    p = subprocess.Popen("{} & cd {} & python {} {}".format(disk, path, programm, args).split(),
                          stdout=subprocess.PIPE,
                          shell=True)

    out, err = p.communicate()

    result = out.decode('cp1251', errors='surrogateescape')
    result = result.split('\n')
    #print('[{}]\nCode:\n{}\nOut:\n{}\n[end]'.format(programm, result[-3], result[-2]))
    return int(result[-3])
    

def unzip(file):
    folder = file.replace('\\', '/').split('/')[0]
    name = str(time.time()).split('.')[0]
    output_path = '{}/{}'.format(folder, name)
    os.makedirs(output_path)
    with zipfile.ZipFile(file) as zf:
        zf.extractall(output_path)
    os.remove(file)

    files = os.listdir(output_path)
    if len(files) > 0:
        output_path = '{}/{}'.format(output_path, files[0])

    return output_path, name

def zip(folder, output_folder, name):
    name = "{}.zip".format(name)
    output_file = "{}/{}".format(output_folder, name)
    print(folder)
    with zipfile.ZipFile(output_file, "w") as zf:
        #zf.write(folder)
        for filename in os.listdir(folder):
            zf.write(os.path.join(folder, filename),
                     filename)
                
    return name
    


def split_layers(path_arg, d):
    disk, path, programm = get_paths(splitter_path)

    input_path = '{}/{}'.format(os.getcwd(), path_arg)
    output_path = '{}/{}_layers'.format(os.getcwd(), path_arg)

    args = '{} {} {}'.format(input_path, output_path, d)
    
    run_script(disk, path, programm, args)
    
    return '{}_layers'.format(path_arg)


def convert(path_arg, split):
    disk, path, programm = get_paths(converter_path)

    if split:   
        input_path = '{}/{}_layers'.format(os.getcwd(), path_arg)
    else:
        input_path = '{}/{}'.format(os.getcwd(), path_arg)
    output_path = '{}/{}_tp'.format(os.getcwd(), path_arg)

    args = '{} {}'.format(input_path, output_path)
    
    run_script(disk, path, programm, args)
    
    return '{}_tp'.format(path_arg)

