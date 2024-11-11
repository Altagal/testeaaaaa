from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from foos.models import Foo
from home.forms import exclude_softdelete_fields, CustomModelForm


class FooForm(CustomModelForm):
    class Meta:
        model = Foo
        exclude = exclude_softdelete_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.all().wrap(Div, css_class='col-6')
