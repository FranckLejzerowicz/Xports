# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import re
import datetime
import subprocess
import socket
import multiprocessing as mp
from os.path import (abspath, basename, dirname, expanduser, expandvars,
                     isdir, isfile, splitext)


def chunks(l: list, chunk_number: int) -> list:
    # Adapted from:
    # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    n = len(l)//chunk_number
    return [l[i:i + n] for i in range(0, len(l), n)]


def get_cur_time() -> str:
    cur_time = str(
        datetime.datetime.now()
    ).split('.')[0].replace(' ', '-').replace(':', '-')
    return cur_time


def get_input_files(folder: str, p_regex: tuple, extensions: list) -> list:
    if p_regex:
        regex = re.compile(r'%s' % '|'.join(list(p_regex)), flags=re.IGNORECASE)
    to_exports = []
    for root, dirs, files in os.walk(folder):
        for fil in files:
            if p_regex:
                if re.search(regex, fil):
                    to_exports.append('%s/%s' % (root, fil))
                    continue
            ext = splitext(fil)[1]
            if ext in extensions:
                to_exports.append('%s/%s' % (root, fil))
    return to_exports


def move_exports(folder: str, folder_exp: str, to_exports: list) -> None:
    for to_export in to_exports:
        exp = to_export.replace(folder.rstrip('/'), folder_exp)
        if isfile(exp):
            continue
        if not isdir(dirname(exp)):
            subprocess.call(['mkdir', '-p', dirname(exp)])
        subprocess.call(['cp', to_export, exp])
        if exp.endswith('_ordination_emperor.qzv'):
            exp_tensor = '%s' % exp.split('_ordination_emperor.qzv')[0]
            subprocess.call(['cp', '-r', to_export.split(
                '_ordination_emperor.qzv')[0], exp_tensor])


def create_archive(output: str, folder_exp: str) -> None:
    cmd = ['tar', 'czf', output, '-C', folder_exp, '.']
    print('Creating archive %s:\n%s' % (output, ' '.join(cmd)))
    subprocess.call(cmd)
    print('Removing folder %s' % folder_exp)
    subprocess.call(['rm', '-rf', folder_exp])


def xports(folder: str, exts: tuple, p_regex: tuple, p_location: str,
           archive: str, local: bool) -> None:

    folder = abspath(folder)
    cur_time = get_cur_time()
    if local:
        folder_exp = '%s/exports_%s' % (abspath(folder).rstrip('/'), cur_time)
    else:
        if p_location in os.environ:
            folder_exp = '%s/exports_%s' % (os.environ[p_location], cur_time)
        else:
            folder_exp = '%s/exports_%s' % (p_location, cur_time)

    extensions = ['.%s' % x if x[0] != '.' else x for x in exts]
    to_exports = get_input_files(folder, p_regex, extensions)
    if len(to_exports) <= 8:
        to_exports_chunks = [[x] for x in to_exports]
    else:
        to_exports_chunks = chunks(to_exports, 8)

    print('Moving %s files with extentions "%s" to %s' % (
        len(to_exports), '", "'.join(extensions), folder_exp))

    jobs = []
    for to_exports_chunk in to_exports_chunks:
        p = mp.Process(
            target=move_exports,
            args=(folder, folder_exp, to_exports_chunk,))
        p.start()
        jobs.append(p)

    for j in jobs:
        j.join()

    archive = abspath(archive)
    if not local:
        if p_location in os.environ:
            archive = '%s/%s' % (os.environ[p_location], basename(archive))
        else:
            archive = '%s/%s' % (p_location, basename(archive))
    archive = expandvars(archive)
    create_archive(archive, folder_exp)
    user = expanduser('~').split('/')[-1]
    hostname = socket.gethostname()
    print('Done! To download from server to local, copy(-edit)-paste this:\n')
    print('scp %s@%s:%s .' % (user, hostname, archive))
