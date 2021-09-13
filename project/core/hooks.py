from wagtail.core import hooks

@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
    discarded_menu_items = [
        'documents',
        'images',
        'explorer',
        'reports',
        'settings'
    ]
    for item in menu_items:
        print(item.name)
    menu_items[:] = [item for item in menu_items if item.name not in discarded_menu_items]