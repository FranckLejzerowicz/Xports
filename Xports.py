#!/home/flejzerowicz/usr/miniconda3/bin/python3.6

import glob, os
import argparse
import subprocess
import multiprocessing as mp
from os.path import dirname, isdir, isfile, splitext, expanduser, abspath
import datetime

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', nargs = 1, required = True, help='Folder to walk through to find files for export.')
    parser.add_argument('-e', nargs = '*', required = False, default=['qzv'], help='Files extensions to select (default = qzv).')
    parser.add_argument('-o', nargs = 1, required = True, help='Output archive file.')
    parse=parser.parse_args()
    args=vars(parse)
    return args


def get_cur_time():
    cur_time = str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '-')
    return cur_time


def chunks(l, chunk_size, chunk_number=0):
    # Adapted from:
    # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    if chunk_size:
        return [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]
    else:
        n = len(l)//chunk_number
        return [l[i:i + n] for i in range(0, len(l), n)]


def get_input_files(folder, extensions):
    to_exports = []
    for root, dirs, files in os.walk(folder):
        for fil in files:
            ext = splitext(fil)[1]
            if ext in extensions:
                to_exports.append('%s/%s' % (root, fil))
    return to_exports


def move_exports(folder, folder_exp, to_exports):
    for to_export in to_exports:
        exported = to_export.replace(folder.rstrip('/'), folder_exp)
        if isfile(exported):
            continue
        if not isdir(dirname(exported)):
            subprocess.call(['mkdir', '-p', dirname(exported)])
        # print(['cp', to_export, exported])
        subprocess.call(['cp', to_export, exported])
        if exported.endswith('_ordination_emperor.qzv'):
            exported_tensor = '%s' % exported.split('_ordination_emperor.qzv')[0]
            # print(['cp', '-r', to_export.split('_ordination_emperor.qzv')[0], exported_tensor])
            subprocess.call(['cp', '-r', to_export.split('_ordination_emperor.qzv')[0], exported_tensor])


def create_archive(output, folder_exp):
    # print(['tar', 'czvf', output, '-C', folder_exp, '.'])
    # print(['rm', '-rf', folder_exp])
    cmd = ['tar', 'czf', output, '-C', folder_exp, '.']
    print('Creating archive %s:\n%s' % (output, ' '.join(cmd)))
    subprocess.call(cmd)
    print('Removing folder %s' % folder_exp)
    subprocess.call(['rm', '-rf', folder_exp])


if __name__ == '__main__':
    args = get_args()

    folder = args['i'][0]
    cur_time = get_cur_time()
    folder_exp = '%s/exports_%s' % (folder.rstrip('/'), cur_time)
    extensions = ['.%s' % x if x[0]!='.' else x for x in args['e']]
    output = args['o'][0]

    to_exports = get_input_files(folder, extensions)
    if len(to_exports) <= 8:
        to_exports_chunks = [[x] for x in to_exports]
    else:
        to_exports_chunks = chunks(to_exports, 0, 8)
    
    print('Moving %s files with extentions "%s" to %s' % (len(to_exports),
                                                          '", "'.join(extensions),
                                                          folder_exp))
    jobs = []
    for to_exports_chunk in to_exports_chunks:
        p = mp.Process(
            target=move_exports,
            args=(folder, folder_exp, to_exports_chunk,)
        )
        p.start()
        jobs.append(p)

    for j in jobs:
        j.join()

    create_archive(output, folder_exp)
    home = expanduser('~').split('/')[-1]
    print('Done! To copy this archive from barnacle to your home, copy-edit-paste this:\n')
    print('scp %s@barnacle.ucsd.edu:%s .' % (home, abspath(output)))
    print('(you may change "." by a path on your machine)')
