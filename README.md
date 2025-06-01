# NetBox License Plugin – Developer Documentation

## Overzicht

De `netbox_license` plugin breidt NetBox uit met een systeem voor licentiebeheer. De plugin ondersteunt het aanmaken, bewerken, toewijzen en beheren van software- en hardwarelicenties, inclusief types, volumes, looptijden en koppelingen aan toestellen of virtuele machines.

Deze documentatie is bedoeld voor ontwikkelaars die deze plugin willen begrijpen, onderhouden of uitbreiden.

---

## Structuur van de Plugin

### Top-Level Bestanden

| Bestand               | Doel |
|-----------------------|------|
| `__init__.py`         | Markeert de directory als een Python-package. |
| `choices.py`          | Bevat enums en keuzelijsten voor modellen en formulieren (bijv. licentietypes, volumetypes). |
| `jobs.py`             | Definieert geplande taken of achtergrondjobs, zoals licentie-expiratierapporten. |
| `navigation.py`       | Integreert de plugin in het NetBox-navigatiemenu. |
| `tables.py`           | Definieert tabellen en kolomstructuren voor weergave in de UI. |
| `template_content.py` | Voegt extra context toe aan templates via context processors. |
| `urls.py`             | Routeert URLs naar views voor licenties, types en toewijzingen. |
| `version.py`          | Bevat de pluginversie (voor compatibiliteitscontrole). |

---

### Belangrijke Subfolders

#### `models/`
Bevat de datamodellen van de plugin.

- `license.py`: Definieert het `License`-model (sleutel, volume, verloopdatum, parent-child relaties).
- `licensetype.py`: Bevat `LicenseType` (perpetual, subscription, expansion, volume types).
- `licenseassignment.py`: Beschrijft toewijzingen van licenties aan devices of virtuele machines.

#### `views/`
Django views voor webverkeer.

- `license.py`: CRUD voor `License`.
- `licensetype.py`: CRUD voor `LicenseType`.
- `licenseassignment.py`: CRUD voor `LicenseAssignment`.

#### `forms/`
Django formulieren.

- `bulk_edit.py`: Bulkbewerkingen op licenties.
- `bulk_import.py`: CSV-import van licentiegegevens.
- `filtersets.py`: Formulieren voor filtering.
- `models.py`: Formulieren voor individuele objecten.

#### `filtersets/`
Django-filtersets voor geavanceerde filtering.

- `licenses.py`, `licensetypes.py`, `licenseassignments.py`: Filtermogelijkheden op views en API.

#### `tables/`
Tabelweergaves voor NetBox UI.

- Definieert welke velden in tabellen getoond worden.

#### `api/`
REST API toegang.

- `serializers/`: Serializers voor alle modellen (inclusief nested representaties).
- `views.py`: Viewsets voor CRUD via API.
- `urls.py`: API-routes.

#### `graphql/`
GraphQL API-ondersteuning.

- `types.py`, `schema.py`, `filters.py`: Biedt toegang tot licentiegegevens via GraphQL.

#### `migrations/`
Django-migraties voor databaseopbouw.

- `0001_initial.py`: Eerste migratie (tabelstructuur).
- Volgende bestanden wijzigen velden of relaties.

#### `management/commands/`
Aangepaste commando’s.

- `check_expiring_licenses.py`: Detecteert licenties die binnenkort verlopen.

#### `templates/netbox_license/`
Jinja2-templates voor UI-weergave.

- Detail-, lijst- en formulierweergaves.
- Bevat o.a. `license.html` (detailpagina met voortgangsbalk, toewijzingen, child-licenties).

#### `utils/`
Hulpfuncties voor gedeelde logica.

---

## Hoe Alles Samenwerkt

| Component | Verantwoordelijkheid |
|----------|----------------------|
| **Models** | Structuur van gegevens (License, LicenseType, LicenseAssignment). |
| **Migrations** | Zet de database op en houdt schemawijzigingen bij. |
| **Forms & Filtersets** | UI- en API-gebruikersinteractie, filtering en validatie. |
| **Views** | Verwerken van webverkeer en koppeling naar templates. |
| **Templates** | UI-weergave in de browser. |
| **Tables** | Structureren van lijstweergaves. |
| **API/GraphQL** | Toegang tot plugin via REST of GraphQL voor integraties. |
| **Management Commands** | Automatisering van achtergrondtaken. |
| **Navigation & template_content** | Plugin-integratie in de NetBox-interface. |

---

## Ontwikkel- en Onderhoudstips

- **Nieuwe velden toevoegen**: Update het model, maak een migratie, en pas formulieren, templates, serializers en filtersets aan.
- **Relaties wijzigen**: Controleer afhankelijkheden in forms, views, templates, API, etc.
- **API uitbreiden**: Pas serializers en API viewsets aan.
- **UI aanpassen**: Wijzig templates en tabellen.
- **Nieuwe features toevoegen**: Volg bestaande structuur – begin bij het model en werk omhoog naar views en templates.
- **Altijd testen na wijzigingen** met `python manage.py test` en `migrate`.

---

## Installatie (voor ontwikkelaars)

```bash
# In NetBox config:
PLUGINS = ['netbox_license']
PLUGINS_CONFIG = {
  'netbox_license': {
    # Optionele configuratie
  }
}

# Installeren:
$ git clone <plugin-url> netbox/netbox_license
$ pip install -e .
$ python manage.py migrate
$ systemctl restart netbox
