import bpy

keys = []

def register_keymap():
    wm = bpy.context.window_manager
    keyconfig = wm.keyconfigs.addon
    keymap = keyconfig.keymaps.new(name="3D View", space_type="VIEW_3D")
    keymapitems = keymap.keymap_items.new("wm.call_menu", "F", "PRESS", ctrl=True, shift=True)
    keymapitems.properties.name = 'GEM_MT_MainMenu'
    keys.append((keymap, keymapitems))

def unregister_keymap():

    for km, kmi in keys:
        km.keymap_items.remove(kmi)

    keys.clear()
