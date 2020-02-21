# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import click

from Xports import __version__
from Xports._xports import xports


@click.command()
@click.option(
    "-i", "--i-folder", required=True,
    help="Folder to walk through to find files for export."
)
@click.option(
    "-e", "--p-exts", required=False, multiple=True, default=['qzv'],
    show_default=True, help="Files extensions to select (default = qzv)."
)
@click.option(
    "-o", "--o-archive", required=True, help="Output archive file."
)
@click.version_option(__version__, prog_name="routine_qiime2_analyses")


def standalone_xports(
        i_folder,
        p_exts,
        o_archive
):

    xports(
        i_folder,
        p_exts,
        o_archive
    )


if __name__ == "__main__":
    standalone_xports()
