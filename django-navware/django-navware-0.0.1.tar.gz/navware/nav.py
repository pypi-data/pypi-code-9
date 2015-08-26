from django.core.urlresolvers import reverse


def build_nav(request, nav):
    """
    Given a dictionary, return a sorted navigation list
    """

    loggedin = request.user.is_authenticated()
    items = [nav[key] for key in sorted(list(nav))]

    best_match_url = ''
    new_nav = []
    for item in items:

        # handle authenticated users
        if item['pre_login_visible'] and item['post_login_visible']:
            pass  # show at all time
        elif item['post_login_visible'] and loggedin:
            pass  # show to authenticated users only
        elif item['pre_login_visible'] and not loggedin:
            pass  # show to unauthenticated users only
        else:
            continue  # hide at all time (e.g. disabling a feature, etc.)

        # handle staff and super users
        if item['superuser_required'] and not request.user.is_superuser:
            continue  # hide from non-superusers
        if item['staff_required'] and not request.user.is_staff:
            continue  # hide from non-staff

        try:
            item['url'] = reverse(item['reversible'])
        except:
            item['url'] = item['reversible']

        # record the based matched url on the requested path
        if len(item['url']) > 1 and item['url'] in request.path:
            if len(best_match_url) < len(item['url']):
                best_match_url = item['url']

        new_nav.append(item)

    # mark the best match url as selected (breadcrumbs ...)
    matched_index = -1
    for item in new_nav:
        if best_match_url == item['url']:
            matched_index = new_nav.index(item)
            break
    if matched_index > -1:
        new_nav[matched_index]['selected'] = True

    return new_nav
