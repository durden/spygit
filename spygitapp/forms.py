from random import randint

from django import forms
import git_help


class ProjectForm(forms.Form):
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

    url = forms.CharField(max_length=500, initial=djangodash_urls[
                            randint(0, len(djangodash_urls) - 1)])

    def clean_url(self):
        """Make sure the project can be retrieved, etc."""

        # Mask the errors as validation error so they show up on forms easily
        try:
            self.path, self.name = git_help.git_clone(self.cleaned_data['url'])
            self.rev = git_help.git_head_revision(self.path)
        except Exception, e:
            raise forms.ValidationError(e)

        # Custom form validation requires that your clean methods return the
        # data even if you don't change it!
        return self.cleaned_data['url']
