import math

from rest_framework.renderers import BrowsableAPIRenderer


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)

        ctx['display_edit_forms'] = False

        return ctx

    def show_form_for_method(self, view, method, request, obj):
        """We never want to do this! So just return False."""
        return False

    def get_rendered_html_form(self, data, view, method, request):
        """Why render _any_ forms at all. This method should return
        rendered HTML, so let's simply return an empty string.
        """
        return ""


class ConvertBytes:
    def __init__(self, data):
        """
        Convert Bytes

        :param int data: Data to convert
        """

        self.data = data

        if data is None:
            raise ValueError('Missing data parameter.')

        if type(self.data) is not int:
            raise TypeError('Data should be an INT')

    def to_kb(self):
        return math.ceil(self.data * 1024)

    def to_mb(self):
        return math.ceil(self.data / 1024)
