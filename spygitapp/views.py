from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist

from pep8 import run_pep8
from spygitapp.models import Error, Run, File, RunError, Line


def home(request):
    runs = set(Run.objects.all().order_by('date')[0:3])
    return render_to_response('home.html', {'projects': runs})


def projects(request):
    """Display listing of projects"""

    runs = set(Run.objects.all())
    return render_to_response('projects.html', {'projects': runs})


def project_overview(request, project_name):
    """Display overview of an entire project and it's runs"""

    # FIXME: Don't want to use __contains here once the name isn't the same as
    #        the project url

    runs = []

    # Find all runs and how many errors for each of them
    for run in Run.objects.filter(project_name=project_name).order_by('date'):
        errors = 0

        for file in File.objects.filter(run=run).order_by('filename'):
            errors += len(RunError.objects.filter(file=file))

        runs.append({'run_obj': run, 'errors': errors})

    if not len(runs):
        raise Http404

    return render_to_response('project_overview.html', {'runs': runs})


def project(request, project_name, rev, full_listing=True):
    """Display full project layout given a specific revision"""

    files = []

    file_objs = File.objects.filter(run__project_name=project_name,
                                    run__git_revision=rev).order_by('filename')

    for file in file_objs:
        errors = 0

        for error in RunError.objects.filter(file=file):
            errors = errors + 1

        if not full_listing and errors:
            files.append({'file_obj': file, 'errors': errors})
        elif full_listing:
            files.append({'file_obj': file, 'errors': errors})

    if not len(files):
        raise Http404

    # Just build this here b/c its a bit easier
    url = "/%s/%s" % (project_name, rev)
    return render_to_response('project.html', {'files': files, 'url': url})


def file_detail(request, project_name, rev, filename):
    lines = []
    file = File.objects.get(run__project_name__contains=project_name,
                    run__git_revision=rev, filename=filename)
    all_lines = Line.objects.filter(file=file).order_by('line_number')

    # Match up the lines with which ones have errors
    for line in all_lines:
        error = RunError.objects.filter(file=file,
                                        line_number=line.line_number)

        # Just report the first error... We may want to improve this later
        if len(error):
            error = error[0].error
        else:
            error = None

        lines.append({'line_obj': line, 'error': error})

    url = "/%s/%s" % (project_name, rev)

    # Pass filename b/c if there are no errors there will be no lines, so can't
    # show it
    return render_to_response('file.html',
                              {'lines': lines, 'filename': filename,
                                'url': url})


def pep_view(request, **view_args):
    if request.method == 'GET':
        try:
            (proj_name, rev) = run_pep8(request.GET.get('repo'))
        except:
            return redirect('/')

        return HttpResponseRedirect('/%s/%s' % (proj_name, rev))

    return HttpResponseRedirect('/')
