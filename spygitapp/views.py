from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from random import randint

from pep8 import run_pep8
from spygitapp.models import Error, Run, File, RunError, Line

djangodash_urls = list([
    "git://github.com/juanodicio/Destino",
    "git://github.com/beetletweezers/tweezers",
    "git://github.com/kennyshen/buzzfire",
    "git://github.com/bubly/Bub.ly",
    "git://github.com/durden/spygit",
    "git://github.com/tereno/DjangoDash",
    "git://github.com/igorsobreira/wifimap",
    "git://github.com/chronossc/dashline",
    "git://github.com/lukeman/django-dash-2010",
    "git://github.com/elegion/voices-in-the-head",
    "git://github.com/brianmacdonald/djangodash10",
    "git://github.com/badri",
    "git://github.com/etown/GiantPangolin",
    "git://github.com/edorian/Build-your-own-Textadventure",
    "git://github.com/hashfeedr/hashfeedr",
    "git://github.com/LeanIntoIt/tubez",
    "git://github.com/stephrdev/loetwerk",
    "git://github.com/sirmmo/UrbanFabric",
    "git://github.com/moxypark/transphorm.me",
    "git://github.com/frac/djangodash2010",
    "git://github.com/justinlilly/permachart",
    "git://github.com/sebleier/Left-Break",
    "git://github.com/nnrcschmdt/Django-Dash-2010",
    "git://github.com/playpauseandstop/try-django",
    "git://github.com/ericflo/servertail",
    "git://github.com/jibaku/dashed2010",
    "git://github.com/eppsilon/beavers",
    "git://github.com/pydanny/scaredofrabbits",
    "git://github.com/threadsafelabs/crywolf",
    "git://github.com/jtauber/team566",
    "git://github.com/alex-morega/djangodash",
    "git://github.com/jmibanez/DjangoDash",
    "git://github.com/ddosen/FoodTruckTrak",
    "git://github.com/gulopine/frankenboxen",
    "git://github.com/jezdez/holt",
    "git://github.com/dlo/nightwriters",
    "git://github.com/malcolmt/remember_me",
    "git://github.com/TripleLabel/tapz",
    "git://github.com/pnomolos/Django-Dash-2010",
    "git://github.com/brixtonasias/groshlist",
    "git://github.com/codysoyland/snowman"])


def home(request):
    runs = set(Run.objects.all().order_by('-date')[0:3])
    total_projects = len(set(Run.objects.all()))
    max_errors = 0
    worst_proj = ""

    # Find all the projects and find the ones with most errors
    for run in Run.objects.all():
        errors = 0

        for file in File.objects.filter(run=run).order_by('filename'):
            errors += len(RunError.objects.filter(file=file))

        if errors and errors > max_errors:
            worst_proj = run
            max_errors = errors

    return render_to_response('home.html',
         {'projects': runs,
          'total_projects': total_projects,
          'worst_proj': worst_proj,
          'max_errors': max_errors,
          'default_url': djangodash_urls[randint(0, len(djangodash_urls)-1)]})


def projects(request):
    """Display listing of projects"""

    runs = set(Run.objects.all())
    return render_to_response('projects.html', {'projects': runs})


def project_overview(request, project_name):
    """Display overview of an entire project and it's runs"""

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


def project_cloud(request, project_name, rev):
    """Display full project layout given a specific revision"""

    files = []

    file_objs = File.objects.filter(run__project_name=project_name,
                                    run__git_revision=rev).order_by('filename')

    max_errors = 0
    total = 0
    err_set = set()

    for file in file_objs:
        errors = 0

        for error in RunError.objects.filter(file=file):
            errors = errors + 1
            total = total + 1

        if errors > max_errors:
            max_errors = errors

        err_set.add(errors)

    # Create a list of all the errors and bin them
    err_list = list(err_set)
    err_list.sort()
    dividers = list()
    for num in range(1, 10):
        dividers.append(err_list[len(err_list) * num / 10])

    for file in file_objs:
        errors = 0

        for error in RunError.objects.filter(file=file):
            errors = errors + 1

        # Assign each file to an error weight bin
        weight = 0
        if max_errors:
            for divider in dividers:
                if errors < divider:
                    break
                weight = weight + 1

        files.append({'file_obj': file, 'errors': errors, 'weight': weight})

    if not len(files):
        raise Http404

    # Just build this here b/c its a bit easier
    url = "/%s/%s" % (project_name, rev)
    return render_to_response('project_cloud.html',
                              {'files': files, 'url': url, 'total': total})


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
            error = error[0].error_descr
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
            raise Http404

        return HttpResponseRedirect('/%s/%s' % (proj_name, rev))

    return HttpResponseRedirect('/')
