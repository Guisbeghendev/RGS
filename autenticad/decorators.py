from django.core.exceptions import PermissionDenied

def user_has_level(required_level):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Verifica se o nível do usuário é suficiente
                if request.user.level >= required_level:
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied  # Se não tiver o nível, nega o acesso
            else:
                raise PermissionDenied  # Se não estiver autenticado, nega o acesso
        return _wrapped_view
    return decorator
