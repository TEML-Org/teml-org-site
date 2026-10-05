---
weight: 200
title: "Specification (v-alpha-003)"
---

# TEML Specification

> Copied from [`spec/teml-alpha-003.md`](https://github.com/TEML-Org/Teml-spec/blob/main/spec/teml-alpha-003.md) in the Teml-spec repository. Edit it there, then run `scripts/sync-from-spec.py`.

**Version:** `teml.org/v-alpha-003` (draft)
**Status:** Working draft. Anything here may change before the first stable version.
**Machine-readable schema:** [`schema/teml-alpha-003.schema.json`](/schema/teml-alpha-003.schema.json)
**Website:** <https://teml.org>
**Previous version:** [`teml.org/v-alpha-002`](https://github.com/TEML-Org/Teml-spec/blob/main/spec/teml-alpha-002.md). See [Changes from v-alpha-002](#changes-from-v-alpha-002) at the end.

---

## 1. Introduction

TEML is a textual language for documenting an [Event Model](https://eventmodeling.org). It is based on YAML, so it is fast to write and simple to read.

Graphical Event Modeling tools work well for sharing a model visually. However, they take time to build and maintain, and they can be hard to use for people with disabilities. TEML provides a plain-text alternative that offers:

- better accessibility for people with hand limitations and for screen-reader users;
- faster input, because everything is typed text;
- plain-text files that work with version control such as Git;
- a standard format that tools can read to produce documents and code, and that tools can write when documenting existing code.

### 1.1 Two ways to write TEML

TEML is designed for two styles of use (§2):

1. **Sketch.** A pseudo-code style for quickly getting ideas out of your head and into a text editor. You include only as much detail as your team needs.
2. **Compliant.** A refined, fully specified version that can be fed into processors for code generation, validation and rendering.

The same constructs are used in both styles. A compliant document is a sketch with every detail filled in.

### 1.2 Conventions

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

A **processor** is any tool that reads TEML: a validator, renderer, code generator, and so on.

---

## 2. Sketch and compliant documents

A document that contains an `apiVersion` (§4.1) is a **compliant** document. A document without one is a **sketch**.

| | Sketch | Compliant |
|---|---|---|
| Header (`apiVersion`, `metadata`) | optional | required |
| Property types | optional; properties can be listed by name only | required |
| Change slice `events` | optional | required |
| References | should resolve | **MUST** resolve |
| Processor problems | reported as **warnings** | reported as **errors** |

Processors **SHOULD** accept sketches and do what they can with them, such as rendering whatever is present.

A sketch, which is still valid YAML:

```yaml
aggs:
  - UserAgg: [id, firstName, lastName, age]

views:
  - UserView: [id, firstName, lastName, age]

slices:
  - AddUser:
      events: [AddedUser]
      views: [UserView]

  - RenameUser:
      events:
        - RenamedUser: [id, firstName, lastName]
      views:
        - UserView: [firstName, lastName]
```

> **Note.** A sketch MUST still be valid YAML. Writing `UserAgg: id` and continuing on the next lines with `firstName`, `lastName` produces a single string (`"id firstName lastName"`), not a list. Use a flow list such as `[id, firstName, lastName]`, or a block list with `- id` on each line.

---

## 3. Files

- A TEML document **MUST** be a single YAML document, encoded as UTF-8.
- The file extension **SHOULD** be `.teml.yaml`, which keeps YAML editor support working.

Compliant documents **MAY** start with this comment, which lets YAML-aware editors provide autocomplete and validation:

```yaml
# yaml-language-server: $schema=https://teml.org/schema/teml-alpha-003.schema.json
```

### 3.1 Extensions

Any mapping **MAY** contain keys that start with `x-`, for example `x-color: orange`. Processors **MUST** ignore extension keys they do not understand.

In compliant documents, every other key that this spec does not define is an **error**. The exceptions are property maps (§6), whose keys are property names.

---

## 4. Document structure

```yaml
apiVersion: teml.org/v-alpha-003
metadata:
  name: sample

types:       []    # reusable property shapes and enums      §6.4
actors:      []    # people and roles who use the system     §10.1
screens:     []    # user interfaces                         §10.2
systems:     []    # external systems that call our API      §11
automations: []    # processes that run without a person     §9
aggs:        []    # aggregates                              §7
views:       []    # read models                             §8
slices:      []    # the timeline, in order                  §12
```

Each section is optional, but a model without `slices` describes nothing. Sections **MAY** appear in any order.

### 4.1 `apiVersion`

The version of the TEML specification the document follows. It is a string of the form `teml.org/<version>`. For this version it **MUST** be:

```yaml
apiVersion: teml.org/v-alpha-003
```

### 4.2 `metadata`

| Key | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Name of the model. |
| `description` | string | no | |
| `version` | string | no | Version of *the model* (not of TEML). |

### 4.3 Named lists

`types`, `actors`, `screens`, `systems`, `automations`, `aggs`, `views` and `slices` are all **named lists**: lists whose items are single-key mappings from a **name** to a **body**.

```yaml
views:
  - UserView:
      id: g
      firstName: s
```

- Names **MUST** match `^[A-Za-z][A-Za-z0-9_]*$` and **MUST** be unique within their list.
- List order is meaningful for `slices`, which run left to right on the timeline (§12). For the other lists, order only affects presentation.

---

## 5. References

Wherever one element refers to another, it uses the other element's **name** as a plain string:

```yaml
aggs:
  - UserAgg:
      id: g
slices:
  - AddUser:
      agg: UserAgg
```

The key holding a reference says what kind of element it names: `agg` names an aggregate, `screen` a screen, and so on. Names only need to be unique within their own list.

In a compliant document, every reference **MUST** resolve to an element defined in the document. In a sketch, references **MAY** name elements that are not defined; processors **SHOULD** warn about them and treat them as free text.

TEML does not use YAML anchors (`&`), aliases (`*`) or merge keys (`<<`). A reference that is not a string is an error.

---

## 6. Properties and types

Aggregates, views, commands and events describe their data with **props**.

### 6.1 Property maps

In a compliant document, props are a mapping from property name to a **property spec**:

```yaml
id: g                  # type
middleName: s?         # optional
roles: s[]             # list
address: Address       # named type (§6.4)
phones: Phone[]        # list of a named type
name:                  # nested object
  first: s
  last: s
```

A **property spec** is one of:

| YAML form | Meaning |
|---|---|
| **string** | A type expression (§6.2). |
| **mapping** | A nested object; the mapping is itself a property map. |

For a list of objects, define the object as a named type (§6.4) and use `TypeName[]`.

Property names **MUST** match `^[A-Za-z_][A-Za-z0-9_]*$` and **SHOULD** be camelCase.

### 6.2 Type expressions

```
type-expr       ::= base-type list-suffix* optional-suffix?
base-type       ::= primitive | TypeName
list-suffix     ::= "[]"
optional-suffix ::= "?"
```

- `T[]` is a list of `T`.
- `T?` marks the property as optional. The `?` comes last, so `s[]?` is an optional list of strings.

### 6.3 Primitive types

| Type | Meaning |
|---|---|
| `g` | Globally unique identifier |
| `s` | Text |
| `int` | Whole number |
| `dec` | Exact decimal (money, quantities) |
| `bool` | `true` / `false` |
| `date` | Calendar date (ISO 8601) |
| `dt` | Date and time with time zone (ISO 8601) |
| `any` | Unspecified |

None of these names may be used as a `types` name.

### 6.4 Named types (`types`)

`types` is a named list of reusable shapes. A body is either a property map (an object type) or a mapping with an `enum` list:

```yaml
types:
  - Address:
      street: s
      city: s
  - UserStatus:
      enum: [Active, Suspended]
```

A body that has an `enum` key **MUST NOT** have any other keys.

### 6.5 Props in sketches

In a sketch, props **MAY** be a **list of property names** without types:

```yaml
UserAgg: [id, firstName, lastName]
```

A compliant document **MUST** use a property map.

---

## 7. Aggregates (`aggs`)

Aggregates are the parts of the system that handle commands and enforce business rules. Their events form the streams at the bottom of the board.

`aggs` is a named list (§4.3). Each body is the aggregate's props (§6):

```yaml
aggs:
  - UserAgg:
      id: g
      firstName: s
      lastName: s
      age: int
```

---

## 8. Views (`views`)

Views are read models: projections of event data used for querying or presentation.

`views` is a named list (§4.3). Each body is the view's props:

```yaml
views:
  - UserView:
      id: g
      firstName: s
      lastName: s
      age: int
```

Change slices declare which views their events update (§12.4). View slices declare where a view is read (§12.6).

---

## 9. Automations (`automations`)

An **automation** is a process that runs without a person involved, such as a policy, saga, scheduled job or integration. Event Modeling draws it as a ⚙ processor.

An automation works from a view, its **to-do list**, and issues commands. A view slice records that the automation reads the view (§12.6), and each change slice it issues a command in names it as the trigger (§12.5).

```yaml
automations:
  - WelcomeEmailer:
      description: Sends a welcome email to each newly added user.
      schedule: every minute
```

| Key | Type | Description |
|---|---|---|
| `description` | string | |
| `schedule` | string | When it runs, if time-based. Free text or a cron expression. |

---

## 10. Actors and screens

People reach the system through screens. In Event Modeling, each actor gets a swimlane across the top of the board, and that actor's screens sit in it. External systems (§11) are the machine counterpart: they reach the system through its API.

### 10.1 Actors (`actors`)

`actors` is a named list (§4.3) of the people and roles who use the system. The body is optional.

```yaml
actors:
  - Guest:
      description: Someone booking or staying at the hotel.
  - FrontDesk:
```

| Key | Type | Description |
|---|---|---|
| `description` | string | |

### 10.2 Screens (`screens`)

`screens` is a named list of user interfaces: pages, forms, dialogs, or anything a person looks at or acts on.

```yaml
screens:
  - RoomSearch:
      actor: Guest
      wireframe: https://figma.com/file/abc
```

| Key | Type | Description |
|---|---|---|
| `actor` | Actor name | Who uses the screen. |
| `description` | string | |
| `wireframe` | string | URL or relative path of a mockup or image. |

A screen is used in two places:
- as the **trigger** of a slice, where a person issues the command from it (§12.5);
- as a **reader** of a view slice, where it displays the view (§12.6).

---

## 11. External systems (`systems`)

An **external system** is software outside the model, such as a payment provider, a shipping carrier or a partner's service.

An external system cannot put events into our model. Events are facts recorded by *our* system. Instead, the external system **calls our API**, for example with a webhook callback, and that call issues one of our commands. The command produces our own events, which update views like any other events. Event Modeling calls this a **translation**: the outside world's information is translated into our commands and events.

`systems` is a named list (§4.3) of the external systems that call the model:

```yaml
systems:
  - PaymentProvider:
      description: Card payments. Calls POST /webhooks/payments when a charge succeeds.
```

| Key | Type | Description |
|---|---|---|
| `description` | string | What the system is, and how it calls us (for example, which webhook). |

A change slice whose command is issued by an external system names that system as its trigger (§12.5):

```yaml
- ConfirmPayment:
    trigger: { system: PaymentProvider }    # the provider's webhook calls our API
    command:
      ConfirmPayment: { orderId: g, amount: dec, providerReference: s }
    events:
      - PaymentConfirmed: { orderId: g, amount: dec }
```

On a board, each external system gets a swimlane at the top, next to the actors, because it plays the same role: it starts a command from outside the model.

---

## 12. Slices (`slices`)

`slices` is a named list (§4.3). **List order is timeline order** (left to right on the board). There are two kinds of slice:

- A **change slice** changes the system. Something triggers a **command**, the command results in one or more **events**, and those events update **views**. A change slice is identified by having `events`.
- A **view slice** reads the system. It names one **view** and the screens or automations that read it (§12.6). It is identified by having `view`.

A slice **MUST** be exactly one of these kinds.

```yaml
slices:
  - AddUser:              # change slice
      agg: UserAgg
      events:
        - AddedUser:
            id: g
            firstName: s
            lastName: s
      views: [UserView]

  - ShowUsers:            # view slice
      view: UserView
      readBy:
        - screen: UserList
```

### 12.1 Change slice keys

| Key | Type | Description |
|---|---|---|
| `agg` | Aggregate name | The aggregate affected by the slice. |
| `trigger` | Trigger | §12.5. What issues the command. |
| `command` | Command | §12.2. Optional; inferred from the slice name when omitted. |
| `events` | list of Event | §12.3. **Required** in compliant documents. |
| `views` | list of View update | §12.4. Views updated by the slice's events. |
| `story` | string | URL or identifier of the related story or ticket. |
| `status` | string | Free-form state of the slice. Recommended values are `Planned`, `InDev`, `Completed` and `Declined`. `Declined` means the team decided not to build the slice; its `description` **SHOULD** say why. |
| `description` | string | |
| `specs` | list of Spec | §13. |

### 12.2 Command

A command is the request to do something. Its name **SHOULD** be imperative, for example `AddUser` or `DoSomething`.

| Form | Meaning |
|---|---|
| omitted | The command is inferred. Its name is the slice name, and its props are unspecified. |
| string | The command's name; props unspecified. |
| single-key mapping | The command's name, mapped to its props (§6), written like an event (§12.3). |

```yaml
command:
  AddUser:
    id: g
    firstName: s
```

The name is usually the slice name. It can differ, for example when an automation's slice `SendBookingConfirmation` issues `SendConfirmationEmail`.

### 12.3 Events

An event is the fact that results from the command. It is the critical piece of information that a model captures. Its name **MUST** be in the past tense and **SHOULD** be declarative, for example `AddedUser` or `ItWasDone`.

`events` is a named list (§4.3) of the events the command produces. Most slices have one. Each item is either:

- a **string**: the event's name, with props unspecified (sketch); or
- a **single-key mapping** from the event's name to its props (§6).

```yaml
events:
  - PaymentReceived:
      bookingId: g
      amount: dec
  - BookingConfirmed:
      bookingId: g
```

In a compliant document, every event **MUST** have a property map.

An event is defined by the slice that produces it, and an event name **MUST** be unique across all slices.

### 12.4 View updates

Each item of a change slice's `views` list is one of:

| Form | Example | Meaning |
|---|---|---|
| name | `- UserView` | This slice updates `UserView`; which properties is not specified. |
| name with properties | `- UserView: [firstName, age]` | This slice updates `UserView`, touching the listed properties. |

Each listed property **MUST** be a property of the view. "Touched" covers both properties the event sets and properties used to find the view record, such as `id`.

### 12.5 Trigger

`trigger` records what issues the command. It is a single-key mapping:

| Form | Meaning |
|---|---|
| `trigger: { screen: AddUserForm }` | A person issues the command from the screen (§10.2). |
| `trigger: { automation: WelcomeEmailer }` | The automation issues the command (§9). |
| `trigger: { system: PaymentProvider }` | An external system issues the command by calling our API, for example a webhook callback (§11). |

When `trigger` is omitted, the trigger is unspecified.

### 12.6 View slices

A view slice shows where a view is read: a screen that displays it, or an automation that works from it as a to-do list. The events that build the view are already recorded by the change slices that update it (§12.4), so a view slice does not repeat them.

```yaml
- BrowseRooms:
    view: RoomAvailability
    readBy:
      - screen: RoomSearch
    specs:
      - name: shows a booked night as taken
        given:
          - RoomAdded: { roomNumber: "101" }
          - RoomBooked: { roomNumber: "101", checkIn: 2026-11-02, checkOut: 2026-11-03 }
        then:
          - RoomAvailability: { rooms: [ { roomNumber: "101", bookedNights: [2026-11-02] } ] }
```

| Key | Type | Description |
|---|---|---|
| `view` | View name | **Required.** The view being read. |
| `readBy` | list of Reader | Who reads the view. Each item is a single-key mapping: `screen: <Screen>` or `automation: <Automation>`. |
| `story` | string | |
| `status` | string | As for change slices (§12.1). |
| `description` | string | |
| `specs` | list of Spec | §13. |

A view slice **MUST NOT** contain the change-slice keys `agg`, `trigger`, `command`, `events` or `views`.

A view **MAY** appear in more than one view slice, for example when it is shown at different points on the timeline.

On a board, a view slice's readers are drawn to the **right** of its view, because the view must exist before anything can read it (Appendix C).

---

## 13. Specifications (Given / When / Then)

A slice **MAY** include `specs`, a list of scenarios written in Event Modeling's Given/When/Then form.

| Key | Type | Description |
|---|---|---|
| `name` | string | **Required.** What the scenario shows. |
| `given` | list of Instance | Events that have already happened. |
| `when` | Instance | The command under test. Change slices only. |
| `then` | list of Instance | **Required.** The expected outcome; see the table below. |

An **Instance** is a single-key mapping from an event, command or view name to example values. The values **MAY** be partial; only the properties that matter for the scenario need to appear.

What `then` holds depends on the slice:

| Slice | `when` | `then` |
|---|---|---|
| Change slice, triggered by a screen, an external system, or unspecified | the command | the events produced, **or** a single `error: <Name>` |
| Change slice, triggered by an automation | omitted | the commands the automation issues (an empty list means it does nothing) |
| View slice | omitted | exactly one instance of the slice's view, showing its state after the `given` events |

```yaml
specs:
  - name: adds a new user
    when:
      AddUser: { id: u-1, firstName: Ada, lastName: Lovelace }
    then:
      - AddedUser: { id: u-1, firstName: Ada, lastName: Lovelace }
  - name: rejects a duplicate id
    given:
      - AddedUser: { id: u-1 }
    when:
      AddUser: { id: u-1 }
    then:
      - error: UserAlreadyExists
```

---

## 14. Validation

These rules apply to compliant documents. For sketches, processors **SHOULD** report the same problems as warnings.

**Errors**

- E1 `apiVersion` is missing or not supported, or `metadata.name` is missing.
- E2 A name is duplicated within a named list, or an event name is used by more than one slice.
- E3 A reference does not resolve to a defined element of the expected kind (§5).
- E4 A property is untyped, or a type expression names an unknown type.
- E5 A slice is neither a change slice nor a view slice, or mixes keys of both kinds.
- E6 A view update lists a property the view does not have.
- E7 A spec instance names an unknown command, event or view, or a property it does not define; or its `when`/`then` does not fit the slice (§13).

**Warnings**

- W1 A view is not updated by any slice.
- W2 An actor, screen, system, automation or aggregate is defined but never referenced.
- W3 A view is updated but never read by a view slice.
- W4 An automation issues commands but does not read any view.
- W5 A slice's `status` is `Declined` but it has no `description` saying why.

---

## 15. Versioning

- `apiVersion` identifies the spec version as `teml.org/<version>`.
- Alpha versions are numbered `v-alpha-001`, `v-alpha-002`, and so on. Any alpha version may make breaking changes.
- Stable versions will be numbered `v001`, `v002`, and so on. Once stable versions exist, a newer version **SHOULD** only add optional features.
- Processors **MUST** reject an `apiVersion` they do not recognise.

---

## Appendix A. Examples

- [`Examples/user-sketch.teml.yaml`](https://github.com/TEML-Org/Teml-spec/blob/main/Examples/user-sketch.teml.yaml): a sketch.
- [`Examples/user-compliant.teml.yaml`](https://github.com/TEML-Org/Teml-spec/blob/main/Examples/user-compliant.teml.yaml): the user example as a compliant document.
- [`Examples/hotel.teml.yaml`](https://github.com/TEML-Org/Teml-spec/blob/main/Examples/hotel.teml.yaml): the classic Event Modeling hotel example, using actors, screens, view slices, automations, and an external payment provider that calls our API.

## Appendix B. Open questions

- **Multiple files.** An include mechanism for large models. Because references are names (§5), they can work across files.
- **Chapters.** Grouping slices into named chapters on the timeline.
- **Nested properties in view updates.** `- RoomAvailability: [rooms]` cannot say which properties *inside* `rooms` a slice touches. A dotted name such as `rooms.bookedNights` is one option.
- **Command errors.** Declaring the errors a command can produce, so that `error:` names in specs can be checked.
- **Repeated props.** A command's props often repeat its event's props. A shorthand could cut the duplication.
- **API endpoints.** Should `trigger: { system: … }` be able to name the endpoint the system calls (for example `POST /webhooks/payments`), the way a screen names its wireframe?
- **Systems reading views.** Should `readBy` accept `system:` for an external system that queries one of our views through the API?

## Appendix C. Drawing a board (informative)

This appendix describes how tools are expected to draw a TEML model as an Event Modeling board. It is informative: it does not affect whether a document is valid.

### C.1 Information flows left to right

The board is a timeline. **Anything that uses an element is drawn to its right**, never to its left, and never directly above it in the same column. In particular:

- In a view slice, the screens and automations that read the view are drawn to the **right** of the read model. On the timeline, a read model must exist before a screen can show it or an automation can work from it.
- In a change slice, the read models an event updates are drawn to the right of that event.

Within a change slice, the trigger is drawn directly above its command, and the command directly above its events. These happen together, at one point on the timeline, so they share a column.

### C.2 Columns and lanes

- **Columns:** one per slice, in the order of `slices`.
- **Lanes, top to bottom:**
  1. One lane per actor, holding that actor's screens (§10). Screens without an actor share a "Screens" lane.
  2. One lane per external system (§11).
  3. Automations.
  4. Commands and read models.
  5. One lane per aggregate, holding its events.

### C.3 Colours

Following Event Modeling convention: commands are blue, events orange, read models green, and screens white. Automations are marked with a gear (⚙).

## Changes from v-alpha-002

v-alpha-003 removes features rather than adding them. Each removed feature had a simpler equivalent already in the language.

- **Removed: YAML anchors, aliases and merge keys** (§5). References are always names. This removes the anchor rules, the define-before-use rule, and the `x` marker. Sections can now appear in any order.
- **Changed: view updates** (§12.4). `- <<: *UserView` with `prop: x` lines becomes `- UserView: [prop, …]`. Restating a property's type is no longer allowed.
- **Changed: one name per primitive type** (§6.3), and fewer primitives. The aliases (`guid`, `string`, `integer` and so on) are gone, as are `float`, `time`, `dur` and `uri`. Any of them can be added back later without breaking documents.
- **Changed: one way to write a list type** (§6.1). `[s]` is gone; use `s[]`. For a list of objects, define a named type and use `Name[]`.
- **Changed: one rule for references** (§5). In a compliant document every reference must resolve, including screens and automations. In a sketch, undefined names are warnings.
- **Renamed: `wfes` is now `automations`** (§9), and the trigger and reader keys are `automation:`.
- **Removed: `wfes` on change slices.** An automation now always works from a view: a view slice says it reads the view, and `trigger: { automation: … }` says which commands it issues. W4 checks for automations that read no view.
- **Changed: `event` and `events` are merged** into one `events` named list (§12.3). Each item is `EventName: props`, or just the name in a sketch.
- **Changed: a command is written like an event** (§12.2): `command: { AddUser: props }`, or just the name. The `name:` / `props:` keys are gone.
- **Removed: the (extension) labels.** Everything in this document is part of the spec.
- **Removed: warning W1** (past-tense and imperative names). It was a heuristic, better suited to a linter. The remaining warnings are renumbered W1–W4.
- **Changed:** the `status` section is folded into §12.1, and view slices move to §12.6.
- **Added: `Declined`** as a recommended `status` value (§12.1), for a slice the team decided not to build, with the reason in its `description`. W5 checks for the reason. Added on 2026-10-05.
- **Migrating:** change `apiVersion` to `teml.org/v-alpha-003`, then:
  - replace every alias (`*Name`) with the element's name and delete the anchors;
  - rewrite merged view references as `- ViewName: [touched, props]`;
  - replace type aliases with the short names, and `[T]` with `T[]` (moving lists of objects into named types);
  - rename `wfes` to `automations` and `wfe:` to `automation:`;
  - replace `event: { name: X, props: P }` with `events: [ { X: P } ]`;
  - replace `command: { name: X, props: P }` with `command: { X: P }`, using the slice name for X when `name` was omitted;
  - for each `wfes:` on a change slice, add a to-do view that the slice updates and a view slice whose `readBy` names the automation.
