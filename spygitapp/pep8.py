from django.shortcuts import render_to_response

import os
import string
import tempfile
from fnmatch import fnmatch

from models import Error, Run, File, RunError, Line


def add_file_to_set(myset, dirname, fnames):
    """Used with os.path.walk to make a list of all files"""

    for filename in fnames:
        name = dirname + '/' + filename
        if fnmatch(name, '*.py'):
            myset.add(name)


def parse_pep8(run, git_path, output):
    """Parse the pep8 output, store the results"""

    errfiles_set = set()
    errortype_set = set()
    lineno_set = set()

    # Add all files in the project to the db
    allfiles = set()
    os.path.walk(git_path, add_file_to_set, allfiles)
    for filename in allfiles:
        filename = filename.replace(git_path + '/', '', 1)
        runfile = File(filename=filename, run=run)
        runfile.save()

    # Generate a set of error types, error files, and lines
    for line in output.readlines():
        filename, lineno, errnum, errtext = string.split(line, ':', 3)
        lineno = int(lineno)
        filename = filename.replace(git_path + '/', '', 1)

        # Create sets to remove duplicates
        errfiles_set.add(filename)

        # Add new err types to the db
        if (errnum, errtext) not in errortype_set:
            errortype_set.add((errnum, errtext))
            if not Error.objects.filter(error_type=errnum):
                err = Error(error_type=errnum, short_descr=errtext)
                err.save()

        # Create a set of line numbers for each file
        for ln in range(max(1, lineno - 3), lineno + 4):
            lineno_set.add((filename, ln))

        # Add err instances to the db
        runfile = File.objects.get(run=run, filename=filename)
        errtype = Error.objects.get(error_type=errnum)
        runerr = RunError(error=errtype, file=runfile, line_number=lineno,
                          error_descr=errtext)
        runerr.save()

    # Add lines to the db
    for filename in errfiles_set:
        runfile = File.objects.get(run=run, filename=filename)

        f = open(git_path + '/' + filename, 'r')
        lineno = 1
        for line in f:
            if (filename, lineno) in lineno_set:
                linetext = Line(file=runfile, line_number=lineno, text=line)
                linetext.save()
            lineno = lineno + 1
        f.close()


def run_pep8(git_url, path, name, rev):
    """Check out the git project, run pep8, store the results"""

    # Do not allow duplicates of the same project/rev
    old_run = Run.objects.filter(project_name=name, git_revision=rev)
    if not old_run:
        run = Run(project_name=name, project_url=git_url, git_revision=rev)
        run.save()
        pep8_pipe = os.popen("pep8 -r %s" % path)
        parse_pep8(run, path, pep8_pipe)
        pep8_pipe.close()

    os.system("rm -rf %s" % os.path.dirname(path))
