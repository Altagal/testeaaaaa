from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple

exclude_softdelete_fields = ["created_at", "deleted_at", "restored_at", "modified_at", "modified_by", ]


class PrimatoModelForm(ModelForm):
    # variaveis customizadas para exibição de texto de ajuda antes e apos cada campo input no form
    prepend = None
    append = None

    def __init__(self, *args, readonly=None, **kwargs, ):

        # variavel privada
        __first_loop = True

        super().__init__(*args, **kwargs)

        #   Limpa os sulfixos do label de todos os campos do form
        self.label_suffix = ""

        for visible in self.visible_fields():

            #   Define a classe de todos os campos visiveis como 'form-control'
            visible.field.widget.attrs['class'] = 'form-control'

            if __first_loop:
                __first_loop = False
                # Execução no primeiro laço (primeiro form).

            #   AJUSTES PERSONALIZADOS POR TIPO DE CAMPO
            # visible.field.widget retirado de .venv\Lib\site-packages\django\forms\widgets.py

            if type(visible.field.widget).__name__ == "DateInput":  # Ajusta type do input para tipo 'date'
                visible.field.widget.input_type = 'date'
                visible.field.widget.format = '%Y-%m-%d'

            if type(visible.field.widget).__name__ == "CheckboxInput":  # Adiciona a classe 'form-check' aos campos bool para coerencia visual
                visible.field.widget.attrs['class'] = 'form-check'

            if type(visible.field.widget).__name__ == "ClearableFileInput":  # Ajuste do campo vazio de selectbox para coerencia visual
                visible.field.widget.attrs['accept'] = 'image/*'
                visible.field.widget.input_type = 'file'
                visible.field.widget.template_name = "django/forms/widgets/file.html"

            if type(visible.field.widget).__name__ == "ClearableFileInput" and readonly:
                visible.field.widget.input_type = "hidden"

            if type(visible.field).__name__ == "ModelMultipleChoiceField":  # Muda o tipo de seletor, de select para checkbox
                visible.field = MultipleChoiceField(choices=visible.field.choices, widget=CheckboxSelectMultiple())
                # Corrige a atribuição inicial dos campos. Quando le um registro ja preenchido, marca como selecionado.
                if visible.initial:
                    relation_id = []
                    for relation in visible.initial:
                        relation_id.append(relation.id)
                    visible.initial = relation_id

            if type(visible.field.widget).__name__ == "Textarea":  # and visible.field.widget.input_type == text:
                visible.field.widget.attrs['rows'] = 3

        # Define readonly quando o for inicializado com "readonly=True"
        if readonly:
            for visible in self.visible_fields():
                visible.field.required = False
                visible.field.disabled = True
                visible.field.widget.attrs['readonly'] = True

        #   Substitui as mensagens de erro
        for field in self.fields.values():
            field.error_messages = {'required': 'Este campo é obrigatorio.',
                                    'unique': "Este registro já existe no sistema."}

    class Meta:
        abstract = True
