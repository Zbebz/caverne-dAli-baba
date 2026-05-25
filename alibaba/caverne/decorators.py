from django.contrib.auth.decorators import user_passes_test

def unauth_required(
    function=None, index_url="/"
):
    """
    Decorator for views that checks that the user is not logged in, redirecting
    to the index page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=index_url,
        redirect_field_name=None,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def verified_required(function=None, login_url=None):
    """
    Decorator for views that checks that the user is verified, redirecting
    to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.verified,
        login_url=login_url,
        redirect_field_name=None,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator