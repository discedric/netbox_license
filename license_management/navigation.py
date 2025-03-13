from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

# License tab buttons
license_buttons = [
    PluginMenuButton(
        link='plugins:license_management:license_add', 
        title='Add License',
        icon_class='mdi mdi-plus-thick',
        permissions=["license_management.add_license"],
    )
]

# License menu item
license_items = [
    PluginMenuItem(
        link='plugins:license_management:license_list',
        link_text='Licenses', 
        permissions=["license_management.view_license"],
        buttons=license_buttons
    ),
    PluginMenuItem(
        link='plugins:license_management:list_assignments',  
        link_text='License Assignments',
        permissions=["license_management.view_license_assignment"],
        buttons=[
            PluginMenuButton(
                link='plugins:license_management:assignment_add',
                title='Add Assignment',
                icon_class='mdi mdi-plus-thick',
                permissions=["license_management.add_license_assignment"],
            )
        ]
    ),
]

# Top-Level Menu Handling
if get_plugin_config('license_management', 'top_level_menu'):
    menu = PluginMenu(
        label='License Management',
        groups=(('Licenses', license_items),),
        icon_class='mdi mdi-clipboard-text-multiple-outline'
    )
else:
    menu_items = license_items
