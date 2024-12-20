from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

test_buttons = [
    PluginMenuButton (
        link='plugins:license_management:test_view',
        title='test',
        icon_class='mdi mdi-plus-thick',
        permissions=["license_management.test"],
    )
]

test_items = (
    PluginMenuItem(
        link='plugins:license_management:test_view',
        link_text='Test',
        permissions=["license_management.test"],
        buttons= test_buttons
    ),
)

if get_plugin_config('license_management', 'top_level_menu'):
    menu = PluginMenu(
        label=f'Licenses',
        groups=(
            ('testing',test_items),
        ),
        icon_class = 'mdi mdi-clipboard-text-multiple-outline'
    )
else:
    menu_items = test_items