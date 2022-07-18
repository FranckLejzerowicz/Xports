# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
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
    show_default=True, help="Files extensions to select."
)
@click.option(
    "-r", "--p-regex", required=False, multiple=True, default=None,
    show_default=False, help="Regex for file names to select."
)
@click.option(
    "-o", "--o-archive", required=True, help="Output archive file."
)
@click.option(
    "-l", "--p-local", required=False, default='USERWORK',
    help='If not creating the tar locally, create it there.'
)
@click.option(
    "--local/--no-local", required=False, default=False,
    help="Creates the tar locally, and not in $USERWORK."
)
@click.version_option(__version__, prog_name="Xports")


def standalone_xports(
        i_folder,
        p_exts,
        p_regex,
        p_local,
        o_archive,
        local
):

    xports(
        i_folder,
        p_exts,
        p_regex,
        p_local,
        o_archive,
        local
    )


if __name__ == "__main__":
    standalone_xports()
