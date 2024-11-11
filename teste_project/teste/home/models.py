from django.contrib import messages
from django.db import models, IntegrityError
from django.db.models import ProtectedError
from django.utils import timezone
from django_softdelete.models import SoftDeleteModel

from core.settings import AUTH_USER_MODEL


class CustomBaseModel(SoftDeleteModel):
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    modified_at = models.DateTimeField(blank=True)
    modified_by = models.ForeignKey(AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def custom_save(self, request):
        try:
            self.modified_by = request.user
            self.modified_at = timezone.now()
            obj = super().save()
            messages.success(request, "Cadastrado com sucesso.")
            print(timezone.now())
            # retorna o objeto que foi salvo
            return obj

        except IntegrityError:
            messages.warning(request, "Este registro já existe.")

        except Exception as e:
            messages.warning(request, "Error na criação." + e)

    def custom_update(self, request):
        try:
            self.modified_by = request.user
            self.modified_at = timezone.now()
            super().save()
            messages.success(request, "Alterado com sucesso.")

        except IntegrityError:
            messages.warning(request, "Este registro já existe.")

        except Exception as e:
            messages.warning(request, "Error na alteração." + e)

    def custom_delete(self, request):
        try:
            self.modified_by = request.user
            self.modified_at = timezone.now()
            super().save()
            super().delete()
            messages.success(request, "Excluido com sucesso.")
            return True

        except ProtectedError:
            messages.warning(request, "Este registro ainda está sendo usado em outro lugar.")

        except Exception as e:
            messages.warning(request, "Error ao excluir.")
            print(e)
