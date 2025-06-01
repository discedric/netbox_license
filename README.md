# NetBox License Plugin Documentation

This documentation is divided into two parts:

1. **User Guide** – for administrators or users who interact with the plugin through the NetBox web interface.
2. **Developer Documentation** – for developers maintaining, extending, or integrating the plugin.

---

## Part 1: User Guide

### Introduction

The NetBox License Plugin adds license management capabilities to NetBox. It allows users to track software and hardware licenses, define license types, assign licenses to devices or virtual machines, and monitor expiration dates and volume usage.

This guide explains how to use the plugin within the NetBox user interface.

---

### Accessing the Plugin

Once installed, the plugin adds new sections to the NetBox navigation menu:

- **Licenses**
- **License Types**
- **License Assignments**

These can be found in the main menu or under the “Plugins” section, depending on your NetBox configuration.

---

### License Types

#### What Are License Types?

License types define general properties shared by multiple licenses, such as:

- Name (e.g., Windows Server Standard, VMware vSphere)
- Volume type (e.g., per device, per core)
- Purchase model (e.g., perpetual, subscription)
- Optional: link to a base license (for expansion licenses)

#### Creating a License Type

1. Navigate to **License Types**.
2. Click **Add**.
3. Fill in the form:
   - **Name**: descriptive name of the license type.
   - **Volume type**: defines how the license should be counted.
   - **Purchase model**: indicates whether it's a subscription, perpetual license, etc.
   - **License model**: choose between "Base" or "Expansion".
   - If "Expansion" is selected: choose the base license this one expands.

4. Click **Create** to save.

---

### Licenses

#### Creating a License

1. Go to **Licenses**.
2. Click **Add**.
3. Complete the form:
   - **License key**: the actual license code or key.
   - **License type**: select from existing types.
   - **Volume**: total quantity available (e.g., number of devices it can be used for).
   - **Start and expiration dates**: for tracking duration.
   - Optional: serial number, tags, comments.

4. Click **Create**.

#### Viewing a License

On the license detail page, you will see:

- General information (key, type, volume, etc.)
- Current **assignments** to devices or VMs
- Any linked **child licenses** (if expansion licenses exist)
- A **progress bar** showing how much of the license volume is currently in use
- Expiration status (active, expired, or expiring soon)

---

### Assigning Licenses

#### To a Device or Virtual Machine

1. Navigate to **License Assignments**.
2. Click **Add**.
3. Fill in:
   - **License**: select a license with available volume.
   - **Device** or **Virtual Machine**: select one (not both).
   - **Assignment date** (optional): set when the license was assigned.
   - **Volume used**: number of units used in this assignment (e.g., 1 device = 1 unit).

4. Click **Create**.

> Note: The form automatically prevents over-assignment of licenses beyond their total volume.

#### Editing or Removing Assignments

- Use the list view to **edit** or **delete** existing assignments.
- You can also navigate to a license’s detail page to manage assignments directly from there.

---

### Tracking License Expiration

- Expiration dates are shown on each license’s detail page.
- Licenses are automatically marked as **expired** once the expiration date has passed.
- A built-in job (`check_expiring_licenses.py`) is available to detect expiring licenses. This can be extended to send alerts or generate reports.

---

### Bulk Operations

The plugin supports bulk editing and importing for:

- License Types
- Licenses
- Assignments

You can:
- Use checkboxes in list views and select **Bulk Edit** or **Bulk Delete**
- Import records via CSV using the **Import** button in each section

---

### Best Practices

- Use **License Types** to avoid duplication and simplify license management.
- Keep expiration dates and volume limits up to date.
- Regularly review the license usage to avoid overuse or expiration.
- Use tags to organize licenses by department, function, or purpose.

---

### Troubleshooting

| Problem | Solution |
|--------|----------|
| License cannot be assigned | Make sure there is available volume and a valid expiration date. |
| Form doesn't show the expected device/VM | Check if it's already assigned, or if filters are hiding it. |
| License is shown as expired | Verify the expiration date on the license detail page. |

---

### FAQ

**Can I assign one license to multiple devices?**  
Yes, as long as the license volume allows it. Each assignment consumes part of the license volume.

**What happens when a license expires?**  
The license is marked as expired in the UI. Assignments remain, but the status reflects its expiration.

**Can I track licenses per CPU core or VM instead of per device?**  
Yes. Use the volume type in the License Type to define how volume is counted.

**How do I handle expansion licenses?**  
Create a License Type with model "Expansion" and link it to a base license type.

---

### Need Help?

If you experience issues or need support, contact your NetBox administrator or plugin maintainer.

---

## Part 2: Developer Documentation

### Overview

The `netbox_license` plugin extends NetBox with a full-featured license management system. It allows users to create, edit, assign, and manage software and hardware licenses, including license types, volume tracking, expiration handling, and assignments to devices or virtual machines.

This documentation is intended for developers who want to understand, maintain, or extend the plugin.

---

### Plugin Structure

#### Top-Level Files

| File                | Purpose |
|---------------------|---------|
| `__init__.py`       | Marks the directory as a Python package. |
| `choices.py`        | Contains enums and choice fields for models and forms. |
| `jobs.py`           | Defines scheduled or background jobs, such as license expiration checks. |
| `navigation.py`     | Integrates the plugin into the NetBox UI menu. |
| `tables.py`         | Defines table layouts and columns for object list views. |
| `template_content.py` | Adds additional context to templates via context processors. |
| `urls.py`           | Routes URLs to views for licenses, license types, and assignments. |
| `version.py`        | Stores the plugin version for compatibility purposes. |

---

#### Key Subfolders

##### `models/`
- `license.py`: Defines the `License` model with key, volume, dates, relationships.
- `licensetype.py`: Defines types of licenses (base or expansion).
- `licenseassignment.py`: Assigns licenses to devices or virtual machines.

##### `views/`
- `license.py`, `licenseassignment.py`, `licensetype.py`: CRUD views for all major models.

##### `forms/`
- `bulk_edit.py`, `bulk_import.py`, `filtersets.py`, `models.py`: Forms for input, import, and filtering.

##### `filtersets/`
- Filter classes for each model used in views and APIs.

##### `tables/`
- Table definitions for list views in the UI.

##### `api/`
- REST API serializers, viewsets, and routing.

##### `graphql/`
- GraphQL types, filters, and schema configuration.

##### `migrations/`
- Database migrations for schema creation and updates.

##### `management/commands/`
- Includes `check_expiring_licenses.py` to identify upcoming expirations.

##### `templates/netbox_license/`
- Jinja2 templates for forms, detail views, and list pages.

##### `utils/`
- Utility functions shared across the plugin.

---

### Component Overview

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

### Development and Maintenance Tips

- To add new fields: update the model, create a migration, and update all related forms, templates, serializers, and filters.
- When changing relationships: check all affected components.
- To extend the API: modify or create new serializers and viewsets in `api/`.
- To update the UI: modify templates and tables as needed.
- To add features: follow the plugin structure from model to view.
- Always test changes with `python manage.py test` and apply migrations with `python manage.py migrate`.

---

### Installation (Developer Setup)

```bash
# In NetBox configuration:
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
