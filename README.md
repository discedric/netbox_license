# NetBox License Plugin – Developer Documentation

## Overview

The `netbox_license` plugin extends NetBox with a full-featured license management system. It allows users to create, edit, assign, and manage software and hardware licenses, including license types, volume tracking, expiration handling, and assignments to devices or virtual machines.

This documentation is intended for developers who want to understand, maintain, or extend the plugin.

---

## Plugin Structure

### Top-Level Files

| File                | Purpose |
|---------------------|---------|
| `__init__.py`       | Marks the directory as a Python package. |
| `choices.py`        | Contains enums and choice fields for models and forms (e.g., license types, volume types). |
| `jobs.py`           | Defines scheduled or background jobs, such as license expiration checks. |
| `navigation.py`     | Integrates the plugin into the NetBox UI menu. |
| `tables.py`         | Defines table layouts and columns for object list views. |
| `template_content.py` | Adds additional context to templates via context processors. |
| `urls.py`           | Routes URLs to views for licenses, license types, and assignments. |
| `version.py`        | Stores the plugin version for compatibility purposes. |

---

### Key Subfolders

#### `models/`
Contains the plugin's data models.

- `license.py`: Defines the `License` model, including license key, volume, expiration, and parent-child relationships.
- `licensetype.py`: Defines the `LicenseType` model (e.g., perpetual, subscription, expansion).
- `licenseassignment.py`: Defines license assignments to devices or virtual machines.

#### `views/`
Django views for handling HTTP requests.

- `license.py`: CRUD views for the `License` model.
- `licensetype.py`: CRUD views for `LicenseType`.
- `licenseassignment.py`: CRUD views for `LicenseAssignment`.

#### `forms/`
Django forms used in the plugin.

- `bulk_edit.py`: Forms for bulk editing license-related objects.
- `bulk_import.py`: Forms for CSV import.
- `filtersets.py`: Forms for UI filtering.
- `models.py`: Forms for creating and editing individual objects.

#### `filtersets/`
Django FilterSets for advanced filtering.

- `licenses.py`, `licensetypes.py`, `licenseassignments.py`: Define filters for views and the API.

#### `tables/`
Table definitions for the NetBox UI.

- Specifies which fields are displayed and how object tables are rendered.

#### `api/`
Exposes plugin functionality through REST API endpoints.

- `serializers/`: Serializers for all models, including nested representations.
- `views.py`: API viewsets for CRUD operations.
- `urls.py`: Defines API routes.

#### `graphql/`
GraphQL support for querying license data.

- `types.py`, `schema.py`, `filters.py`: Define the GraphQL schema, types, and filters for licenses.

#### `migrations/`
Django migrations for initializing and updating the database schema.

- `0001_initial.py`: Creates initial database tables.
- Additional files apply field or relationship changes.

#### `management/commands/`
Custom Django management commands.

- `check_expiring_licenses.py`: Detects licenses nearing expiration for reporting or automation purposes.

#### `templates/netbox_license/`
Jinja2 templates for the plugin's web interface.

- Includes list, detail, and form views.
- Notably includes `license.html`, which displays license details, progress indicators, assignments, and related licenses.

#### `utils/`
Shared utility functions used throughout the plugin.

---

## Component Overview

| Component                | Responsibility |
|--------------------------|----------------|
| Models                   | Define the structure for License, LicenseType, and LicenseAssignment. |
| Migrations               | Create and update the database schema. |
| Forms and Filtersets     | Provide input validation and filtering for the UI and API. |
| Views                    | Handle HTTP requests and render templates. |
| Templates                | Display content in the NetBox web interface. |
| Tables                   | Format object list views. |
| API and GraphQL          | Expose data for integration and automation. |
| Management Commands      | Automate scheduled and background tasks. |
| Navigation and Templates | Integrate the plugin into the NetBox UI. |

---

## Development and Maintenance Tips

- To add new fields: update the model, create a migration, and update all relevant forms, templates, serializers, and filtersets.
- When changing relationships: update the models and check all dependent components.
- To extend the API: modify or create new serializers and viewsets in the `api/` module.
- For UI changes: update Jinja2 templates and the relevant table definitions.
- To implement new features: follow the plugin structure—start with models, then add forms, views, templates, and tests.
- Always test changes with `python manage.py test` and apply migrations using `python manage.py migrate`.

---

## Installation (Developer Setup)

```bash
# In NetBox configuration (configuration.py):
PLUGINS = ['netbox_license']
PLUGINS_CONFIG = {
  'netbox_license': {
    # Optional plugin settings
  }
}

# Installation:
$ git clone <plugin-url> netbox/netbox_license
$ pip install -e .
$ python manage.py migrate
$ systemctl restart netbox
