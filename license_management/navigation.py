from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

# License tab buttons
license_buttons = [
    PluginMenuButton(
        link='plugins:license_management:license_add',
        title='Add License',
        icon_class='mdi mdi-plus-thick',
        permissions=["license_management.add_license"],
    ),
    PluginMenuButton(
        link='plugins:license_management:license_bulk_import',
        title='Import Licenses',
        icon_class='mdi mdi-upload',
        permissions=["license_management.add_license"],
    ),
]

# License Assignment tab buttons
license_assignments_buttons = [
    PluginMenuButton(
        link='plugins:license_management:licenseassignment_add',
        title='Add Assignment',
        icon_class='mdi mdi-plus-thick',
        permissions=["license_management.add_licenseassignment"],
    ),
    PluginMenuButton(
        link='plugins:license_management:licenseassignment_bulk_import',
        title='Import Assignments',
        icon_class='mdi mdi-upload',
        permissions=["license_management.add_licenseassignment"],
    ),
]

# License Type tab buttons
license_type_buttons = [
    PluginMenuButton(
        link='plugins:license_management:licensetype_add',
        title='Add License Type',
        icon_class='mdi mdi-plus-thick',
        permissions=["license_management.add_licensetype"],
    ),
    PluginMenuButton(
        link='plugins:license_management:licensetype_bulk_import',
        title='Import License Types',
        icon_class='mdi mdi-upload',
        permissions=["license_management.add_licensetype"],
    ),
]

# Menu items
license_items = [
    
    PluginMenuItem(
        link='plugins:license_management:licensetype_list',
        link_text='License Types',
        permissions=["license_management.view_licensetype"],
        buttons=license_type_buttons
    ),

    PluginMenuItem(
        link='plugins:license_management:license_list',
        link_text='Licenses',
        permissions=["license_management.view_license"],
        buttons=license_buttons
    ),
    
    PluginMenuItem(
        link='plugins:license_management:licenseassignment_list',
        link_text='License Assignments',
        permissions=["license_management.view_licenseassignment"],
        buttons=license_assignments_buttons
    ),
]

# Top-Level Menu Handling
if get_plugin_config('license_management', 'top_level_menu'):
    menu = PluginMenu(
        label='Licenses',
        groups=(('Licenses', license_items),),
        icon_class='mdi mdi-clipboard-text-multiple-outline'
    )
else:
    menu_items = license_items
