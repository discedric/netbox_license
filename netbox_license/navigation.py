from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

### License ###

license_items = [
    
    PluginMenuItem(
        link='plugins:netbox_license:licensetype_list',
        link_text='License Types',
        permissions=["netbox_license.view_licensetype"],
        buttons= [
            PluginMenuButton(
                link='plugins:netbox_license:licensetype_add',
                title='Add License Type',
                icon_class='mdi mdi-plus-thick',
                permissions=["netbox_license.add_licensetype"],
            ),
            PluginMenuButton(
                link='plugins:netbox_license:licensetype_bulk_import',
                title='Import License Types',
                icon_class='mdi mdi-upload',
                permissions=["netbox_license.add_licensetype"],
            ),
        ],
    ),

    PluginMenuItem(
        link='plugins:netbox_license:license_list',
        link_text='Licenses',
        permissions=["netbox_license.view_license"],
        buttons= [
            PluginMenuButton(
                link='plugins:netbox_license:license_add',
                title='Add License',
                icon_class='mdi mdi-plus-thick',
                permissions=["netbox_license.add_license"],
            ),
            PluginMenuButton(
                link='plugins:netbox_license:license_bulk_import',
                title='Import Licenses',
                icon_class='mdi mdi-upload',
                permissions=["netbox_license.add_license"],
            ),
        ],
    ),
    
    PluginMenuItem(
        link='plugins:netbox_license:licenseassignment_list',
        link_text='License Assignments',
        permissions=["netbox_license.view_licenseassignment"],
        buttons= [
            PluginMenuButton(
                link='plugins:netbox_license:licenseassignment_add',
                title='Add Assignment',
                icon_class='mdi mdi-plus-thick',
                permissions=["netbox_license.add_licenseassignment"],
            ),
            PluginMenuButton(
                link='plugins:netbox_license:licenseassignment_bulk_import',
                title='Import Assignments',
                icon_class='mdi mdi-upload',
                permissions=["netbox_license.add_licenseassignment"],
            ),
        ],
    ),
]


### -> Add new Menu Items above this line if needed.

### Menu ###


if get_plugin_config('netbox_license', 'top_level_menu'):
    menu = PluginMenu(
        label=f'Licenses',
        groups=(
            ('Licenses', license_items),
        ),
        icon_class = 'mdi mdi-clipboard-text-multiple-outline'
    )
else:
    menu_items = license_items