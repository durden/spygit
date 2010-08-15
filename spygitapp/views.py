from django.shortcuts import render_to_response

from pep8 import run_pep8
from spygitapp.models import Error, Run, File, RunError, Line


def file_detail(request):
    text = """
        def __render_page(name, active):

            show_page = get_object_or_404(Page, name=name)
            blogs = None
            pages = None

            # Add the 'latest' info to the homepage
            if name == "Home":
                blogs = Blog.objects.all().order_by("-updated")[:3]
                pages = Page.objects.all().order_by("-updated")[:2]

                # Figure out what page to link to
                for page in pages:
                    # FIXME: Bad to hardcode these names here b/c now there are
                    #        dependencies here, views, and urls
                    if page.name == "Our Story":
                        page.link = "story"
                    elif page.name == "Gift Registry":
                        page.link = "gifts"
                    else:
                        page.link = "home"

            return render_to_response('page.html', {'page': show_page,
                                      'active': active, 'blogs': blogs,
                                      'pages': pages})
        """

    return render_to_response('file.html', {'text': text})


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

    # FIXME: This won't work if the same revision is run more than once!
    files = File.objects.filter(run__project_name__contains=project_name,
                                    run__git_revision=rev)

    return render_to_response('project.html', {'files': files})


def pep_view(request, **view_args):
    run_pep8("git://github.com/durden/spygit.git")

    return render_to_response('peptest.html')
