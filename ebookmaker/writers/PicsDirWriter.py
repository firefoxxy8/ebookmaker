#!/usr/bin/env python
#  -*- mode: python; indent-tabs-mode: nil; -*- coding: iso-8859-1 -*-

"""

PicsDirWriter.py

Copyright 2012 by Marcello Perathoner

Distributable under the GNU General Public License Version 3 or newer.

Copies pics into local directory. Needed for HTML and Xetex.

"""


import os

import libgutenberg.GutenbergGlobals as gg
from libgutenberg.Logger import info, debug, error

from ebookmaker import writers


class Writer (writers.BaseWriter):
    """ Writes Pics directory. """

    def copy_aux_files (self, job, dest_dir):
        """ Copy image files to dest_dir. Use image data cached in parsers. """

        for p in job.spider.parsers:
            if hasattr (p, 'resize_image'):
                src_uri = p.attribs.url
                fn_dest = gg.make_url_relative (job.base_url, src_uri)
                fn_dest = os.path.join (dest_dir, fn_dest)

                if gg.is_same_path (src_uri, fn_dest):
                    debug ('Not copying %s to %s: same file' % (src_uri, fn_dest))
                    continue
                debug ('Copying %s to %s' % (src_uri, fn_dest))

                fn_dest = gg.normalize_path (fn_dest)
                gg.mkdir_for_filename (fn_dest)
                try:
                    with open (fn_dest, 'wb') as fp_dest:
                        fp_dest.write (p.serialize ())
                except IOError as what:
                    error ('Cannot copy %s to %s: %s' % (src_uri, fn_dest, what))



    def build (self, job):
        """ Build Pics file. """

        dir = job.outputdir

        info ("Creating Pics directory in: %s" % dir)

        self.copy_aux_files (job, dir)

        info ("Done Pics directory in: %s" % dir)