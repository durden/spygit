from django.shortcuts import render_to_response

import os
import string
import tempfile
from models import Error, Run, File, RunError, Line


def add_file_to_set(myset, dirname, fnames):
    """Used with os.path.walk to make a list of all files"""

    for filename in fnames:
        myset.add(dirname + '/' + filename)


def parse_pep8(run, git_prj_path, output):
    """Parse the pep8 output, store the results"""

    errfiles_set = set()
    errortype_set = set()
    lineno_set = set()

    # Add all files in the project to the db
    allfiles = set()
    os.path.walk(git_prj_path, add_file_to_set, allfiles)
    for filename in allfiles:
        filename = filename.replace(git_prj_path + '/', '', 1)
        runfile = File(filename = filename, run = run)
        runfile.save()

    # Generate a set of error types, error files, and lines
    for line in output.readlines():
        filename, lineno, errnum, errtext = string.split(line, ':', 4)
        lineno = int(lineno)
        filename = filename.replace(git_prj_path + '/', '', 1)

        # Create sets to remove duplicates
        errfiles_set.add(filename)

        # Add new err types to the db
        if (errnum, errtext) not in errortype_set:
            errortype_set.add((errnum, errtext))
            if not Error.objects.filter(error_type = errnum):
                err = Error(error_type = errnum, short_descr = errtext,
                        long_descr = errtext)
                err.save()
                print "Add ERRTYPE %s %s" % (errnum, errtext)

        # Create a set of line numbers for each file
        for ln in range(max(0,lineno - 3), lineno + 4):
            lineno_set.add((filename,ln))

        # Add err instances to the db
        runfile = File.objects.get(run = run, filename = filename)
        #FIXME: should only get one error back
        #errtype = Error.objects.get(error_type = errnum, short_descr = errtext)
        errtype = Error.objects.filter(error_type = errnum)[0]
        runerr = RunError(error = errtype, file = runfile, line_number = lineno)
        runerr.save()

    # Add lines to the db
    for filename in errfiles_set:
        runfile = File.objects.get(run = run, filename = filename)
    
        f = open(git_prj_path + '/' + filename, 'r')
        lineno = 0
        for line in f:
            if (filename, lineno) in lineno_set:
                linetext = Line(file = runfile, line_number = lineno, text = line)
                linetext.save()
            lineno = lineno + 1
        f.close()


def run_pep8(git_prj_name):
    """Check out the git project, run pep8, store the results"""

    print "Starting..."
    run = Run(project_name = git_prj_name, project_url = git_prj_name)
    run.save()

    git_prj_path = tempfile.mkdtemp(prefix='spygit-')
    os.system("git clone %s %s > /dev/null" % (git_prj_name, git_prj_path))
    pep8_pipe = os.popen("pep8 %s" % git_prj_path)
    parse_pep8(run, git_prj_path, pep8_pipe)
    pep8_pipe.close()
    os.system("rm -rf %s" % git_prj_path)
    print "Done"
