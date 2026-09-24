from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return (
            hasattr(request.user, 'perfil')
            and request.user.perfil.tipo == 'ADMIN'
        )


class IsFuncionarioOuAdmin(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return (
            hasattr(request.user, 'perfil')
            and request.user.perfil.tipo in [
                'ADMIN',
                'FUNCIONARIO'
            ]
        )