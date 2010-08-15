Spygit is a simple web application developed for the 2010 [django dash](http://djangodash.com).
It is meant to make it easier to validate your python code against the official
[PEP8](http://www.python.org/dev/peps/pep-0008/) standards.  Hopefully it will allow you to
submit your project, provide you with the errors, and allow you to share proof that your
code is standards compliant.  Also, it should help you find out what isn't compliant and
point it out.

The application is packed up for install with pip.  See the requirements.pip file for more
information on the dependencies.  The main trick is to make sure the pep8 script is installed
in the path where you are running the application.

You can double check this by running 'which pep8' on your *nix box.  If this returns nothing, you don't have it installed or it's not in the path.  To remedy this situation try using easy_install to install pep8, 'easy_install pep8'.  This should do the trick if the pip requirements file didn't do it.
