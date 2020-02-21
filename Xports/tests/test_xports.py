# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import unittest

from Xports import (
    chunks,
    get_input_files
)


class MyTestChunks(unittest.TestCase):

    def setUp(self) -> None:
        cwd = os.getcwd()
        self.test_dir = '%s/folder' % cwd
        self.test_qzas = [
            "%s/folder/level_1/level_2.1/level_3.2/NOT_QZV_3.2.qza" % cwd,
            "%s/folder/level_1/level_2.1/NOT_QZV_2.1.qza" % cwd,
            "%s/folder/level_1/level_2.2/NOT_QZV_2.2.qza" % cwd,
            "%s/folder/level_1/level_2.3/NOT_QZV_2.3.1.qza" % cwd,
            "%s/folder/level_1/level_2.3/NOT_QZV_2.3.2.qza" % cwd,
            "%s/folder/level_1/QZA_1.qza" % cwd,
            "%s/folder/level_1/QZA_2.qza" % cwd
        ]
        self.test_qzvs = [
            "%s/folder/level_1/level_2.1/level_3.1/QZV_3.1.1.qzv" % cwd,
            "%s/folder/level_1/level_2.1/level_3.1/QZV_3.1.2.qzv" % cwd,
            "%s/folder/level_1/level_2.1/level_3.2/QZV_3.2.qzv" % cwd,
            "%s/folder/level_1/level_2.2/QZV_2.2.qzv" % cwd
        ]

    def test_get_input_files(self):
        to_exports = get_input_files(self.test_dir, ['.qza'])
        self.assertEqual(sorted(to_exports), sorted(self.test_qzas))
        to_exports = get_input_files(self.test_dir, ['.qzv'])
        self.assertEqual(sorted(to_exports), sorted(self.test_qzvs))
        to_exports = get_input_files(self.test_dir, ['qzv'])
        self.assertEqual(to_exports, [])
        to_exports = get_input_files(self.test_dir, ['qz'])
        self.assertEqual(to_exports, [])

    def test_chunks(self):
        cur_chunks_1 = chunks([1,2,3,4,5,6,7], 4)
        self.assertEqual(cur_chunks_1, [[1],[2],[3],[4],[5],[6],[7]])
        cur_chunks_2 = chunks([1,2,3,4,5,6,7,8], 4)
        self.assertEqual(cur_chunks_2, [[1,2], [3,4], [5,6], [7,8]])
        cur_chunks_3 = chunks([1,2,3,4,5,6,7,8,9], 4)
        self.assertEqual(cur_chunks_3, [[1,2], [3,4], [5,6], [7,8], [9]])


if __name__ == '__main__':
    unittest.main()
