def register_addon():
    from .addon_prefs import register_addon_preferences
    register_addon_preferences()

    from .keymap import register_keymap
    register_keymap()

    from ..menu import register_menus
    register_menus()

    from ..operator import register_operators
    register_operators()

    from ..panel import register_panels
    register_panels()

    from ..property import register_properties
    register_properties

def unregister_addon():
    from .addon_prefs import unregister_addon_preferences
    unregister_addon_preferences()

    from .keymap import unregister_keymap
    unregister_keymap()

    from ..menu import unregister_menus
    unregister_menus()

    from ..operator import unregister_operators
    unregister_operators()

    from ..panel import unregister_panels
    unregister_panels()
