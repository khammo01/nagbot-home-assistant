# NagBot Home Assistant Blueprints

Reusable Home Assistant automations extracted from a working smart home and
rebuilt as configurable blueprints. The repository contains no household entity
IDs, addresses, credentials, camera images, or notification destinations.

## Blueprints

### OLED screen sleep with deep standby recovery

Uses a display's native screen switch for ordinary idle periods, permits full
standby after extended inactivity, and cancels an in-flight shutdown whenever
occupancy or computer activity returns.

[![Import OLED blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fkhammo01%2Fnagbot-home-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fnagbot%2Foled_screen_sleep.yaml)

### AI camera motion triage

Acknowledges motion immediately, compares an initial and delayed camera frame,
requests structured analysis through Home Assistant's AI Task integration, and
routes meaningful, routine, and failed results to user-selected actions.

[![Import AI camera blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fkhammo01%2Fnagbot-home-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fnagbot%2Fai_camera_motion_triage.yaml)

### Stable smart-scale identification

Identifies one of two people only when a stable measurement is close to the
saved reference and clearly wins over the other profile. Presence narrows the
candidates, while uncertain readings remain unassigned and cannot corrupt a
profile.

[![Import scale blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fkhammo01%2Fnagbot-home-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fnagbot%2Fsmart_scale_two_person.yaml)

### Power-based appliance completion and retrieval

Uses separate sustained start and completion thresholds to tolerate ordinary
heater or motor cycling. Two input_boolean helpers preserve the active cycle and
waiting-for-retrieval states across restarts; opening the appliance door clears
the waiting state.

[![Import appliance blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fkhammo01%2Fnagbot-home-assistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fnagbot%2Fappliance_completion_retrieval.yaml)

## Installation

Use an **Import Blueprint** button above, or copy a file into:

```text
config/blueprints/automation/nagbot/
```

In Home Assistant, open **Settings → Automations & scenes → Blueprints**, reload
blueprints, and create an automation from the imported blueprint. The selectors
guide you through every required entity and action.

See [setup and behavior notes](docs/SETUP.md) before enabling a blueprint on a
real appliance, camera, or display.

## Design principles

- No hard-coded devices, rooms, people, network addresses, or notification services.
- Unknown and unavailable states fail safe where an action could power equipment down.
- Persistent state uses ordinary Home Assistant helpers rather than hidden files.
- Notification and announcement behavior is supplied through action selectors.
- AI camera analysis uses structured output and a provider-neutral AI Task entity.
- Every blueprint uses restart, single, or queued execution deliberately to control races.

## Development

Install the development dependency and run the repository checks:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/check_blueprints.py
```

The checks parse every blueprint, verify its required schema, and reject common
private-installation artifacts before publication.

## License

Released under the [MIT License](LICENSE).
