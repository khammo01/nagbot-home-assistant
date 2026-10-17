# Setup and behavior notes

## OLED screen sleep

Select every occupancy and computer-use binary sensor that should keep the panel
awake. The automation shuts down only when every selected sensor explicitly says
`off`; an `unknown` or `unavailable` sensor blocks shutdown.

Use **recovery actions** for steps such as powering an outlet, turning on the TV,
waiting for webOS to reconnect, or selecting an input. Those actions must be safe
to repeat. Use **full-standby actions** for the TV's real power-off command. An
activity change restarts the automation, which cancels any older sleep countdown.

## AI camera motion triage

This blueprint requires an AI Task entity that supports image attachments. The
first frame is written to `/media` by default. If you run multiple instances,
give each one a different snapshot filename and matching media-source URL.

The configurable actions receive these variables:

- `ai_title`
- `ai_message`
- `ai_category`
- `ai_urgent`

For example, a mobile notification action can use `{{ ai_title }}` as its title
and `{{ ai_message }}` as its message. Keep camera retention and cloud-AI privacy
requirements in mind. The repository does not enable recording or retention.

## Stable smart-scale identification

Create one `input_number` helper per person and initialize each with a reasonable
reference weight. The blueprint updates only the confidently selected helper.
If both people are eligible, the closest profile must win by the configured lead.
If neither profile meets the rules, the unknown action runs and no helper changes.

The identified action receives `measured_weight`, `identified_name`, and
`identified_reference`. The unknown action receives `measured_weight`.

## Appliance completion and retrieval

Create two `input_boolean` helpers per appliance:

1. Cycle active
2. Waiting for retrieval

Choose a running threshold above standby power and a completion threshold below
all normal heater or motor pauses. Start with a 60-second completion debounce,
then tune it from traces. The completion action runs only after a known active
cycle. Opening the selected door clears the waiting helper and runs the retrieval
action.

Test thresholds while watching the live power sensor before relying on the
automation for food safety or unattended equipment.
