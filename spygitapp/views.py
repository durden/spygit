from django.shortcuts import render_to_response

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
