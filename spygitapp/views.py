from django.shortcuts import render_to_response
from django.shortcuts import redirect

from pep8 import run_pep8
from spygitapp.models import Error, Run, File, RunError, Line


def project_overview(request, project_name):
    """Display overview of an entire project and it's runs"""

    # FIXME: Don't want to use __contains here once the name isn't the same as
    #        the project url

    runs = []

    # Find all runs and how many errors for each of them
    for run in Run.objects.filter(project_name__contains=project_name).order_by('date'):
        errors = 0

        for file in File.objects.filter(run=run).order_by('filename'):
            errors += len(RunError.objects.filter(file=file))

        runs.append({'run_obj': run, 'errors': errors})

    return render_to_response('project_overview.html', {'runs': runs})


def project(request, project_name, rev):
    """Display full project layout given a specific revision"""

    files = []

    file_objs = File.objects.filter(run__project_name__contains=project_name,
                                    run__git_revision=rev).order_by('filename')

    for file in file_objs:
        errors = 0

        for error in RunError.objects.filter(file=file):
            errors = errors + 1

        files.append({'file_obj': file, 'errors': errors})

    # Just build this here b/c its a bit easier
    url = "/%s/%s" % (project_name, rev)
    return render_to_response('project.html', {'files': files, 'url': url})


def file_detail(request, project_name, rev, filename):
    file = File.objects.get(run__project_name__contains=project_name,
                    run__git_revision=rev, filename=filename)

    lines = Line.objects.filter(file=file)

    # Pass this b/c if there are no errors there will be no lines, so can't
    # show the filename
    return render_to_response('file.html', {'lines': lines, 'filename': filename})


def pep_view(request, **view_args):
    try:
        if request.method == 'GET':
            run_pep8(request.GET.get('repo'))
        return render_to_response('peptest.html')
    except:
        return redirect('/')
