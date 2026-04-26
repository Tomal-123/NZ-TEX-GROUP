from taskmanager.decorators import get_user_permissions


def user_permissions_context(request):
    """
    Context processor to add user permissions to all templates.
    """
    if request.user.is_authenticated:
        return {
            'user_permissions_dict': get_user_permissions(request.user)
        }
    return {
        'user_permissions_dict': {}
    }
