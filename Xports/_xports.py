# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import datetime
import subprocess
import multiprocessing as mp
from os.path import dirname, isdir, isfile, splitext, expanduser, abspath


def chunks(l: list, chunk_size: int, chunk_number: int = 0) -> list:
    # Adapted from:
    # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    if chunk_size:
        return [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]
    else:
        n = len(l)//chunk_number
        return [l[i:i + n] for i in range(0, len(l), n)]


def get_cur_time() -> str:
    cur_time = str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '-')
    return cur_time


def get_input_files(folder: str, extensions: list) -> list:
    to_exports = []
    for root, dirs, files in os.walk(folder):
        for fil in files:
            ext = splitext(fil)[1]
            if ext in extensions:
                to_exports.append('%s/%s' % (root, fil))
    return to_exports


def move_exports(folder: str, folder_exp: str, to_exports: list) -> None:
    for to_export in to_exports:
        exported = to_export.replace(folder.rstrip('/'), folder_exp)
        if isfile(exported):
            continue
        if not isdir(dirname(exported)):
            subprocess.call(['mkdir', '-p', dirname(exported)])
        subprocess.call(['cp', to_export, exported])
        if exported.endswith('_ordination_emperor.qzv'):
            exported_tensor = '%s' % exported.split('_ordination_emperor.qzv')[0]
            subprocess.call(['cp', '-r', to_export.split('_ordination_emperor.qzv')[0], exported_tensor])


def create_archive(output: str, folder_exp: str) -> None:
    cmd = ['tar', 'czf', output, '-C', folder_exp, '.']
    print('Creating archive %s:\n%s' % (output, ' '.join(cmd)))
    subprocess.call(cmd)
    print('Removing folder %s' % folder_exp)
    subprocess.call(['rm', '-rf', folder_exp])


def xports(folder: str, exts: tuple, archive: str) -> None:

    cur_time = get_cur_time()
    folder_exp = '%s/exports_%s' % (folder.rstrip('/'), cur_time)

    extensions = ['.%s' % x if x[0] != '.' else x for x in exts]

    to_exports = get_input_files(folder, extensions)

    if len(to_exports) <= 8:
        to_exports_chunks = [[x] for x in to_exports]
    else:
        to_exports_chunks = chunks(to_exports, 0, 8)

    print('Moving %s files with extentions "%s" to %s' % (
        len(to_exports), '", "'.join(extensions), folder_exp))

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

    create_archive(archive, folder_exp)
    home = expanduser('~').split('/')[-1]
    print('Done! To copy this archive from barnacle to your home, copy-edit-paste this:\n')
    print('scp %s@barnacle.ucsd.edu:%s .' % (home, abspath(archive)))
    print('(you may change "." by a path on your machine)')