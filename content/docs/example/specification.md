---
weight: 200
title: "Specification (v-alpha-002)"
---

# TEML Specification

> Copied from [`spec/teml-alpha-002.md`](https://github.com/TEML-Org/Teml-spec/blob/main/spec/teml-alpha-002.md) in the Teml-spec repository. Edit it there, then run `scripts/sync-from-spec.py`.

**Version:** `teml.org/v-alpha-002` (draft)
**Status:** Working draft. Anything here may change before the first stable version.
**Machine-readable schema:** [`schema/teml-alpha-002.schema.json`](/schema/teml-alpha-002.schema.json)
**Website:** <https://teml.org>
**Previous version:** [`teml.org/v-alpha-001`](https://github.com/TEML-Org/Teml-spec/blob/main/spec/teml-alpha-001.md). See [Changes from v-alpha-001](#changes-from-v-alpha-001) at the end.

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

Sections marked **(extension)** were proposed in this spec repository and do not yet appear on teml.org. They are optional; a document that does not use them loses nothing.

---

## 2. Sketch and compliant documents

A document that contains an `apiVersion` (§4.1) is a **compliant** document. A document without one is a **sketch**.

| | Sketch | Compliant |
|---|---|---|
| Header (`apiVersion`, `metadata`) | optional | required |
| Property types | optional; properties can be listed by name only | required |
| Change slice `event` | optional | required |
| References | should resolve | **MUST** resolve |
| Processor problems | reported as **warnings** | reported as **errors** |

Processors **SHOULD** accept sketches and do what they can with them, such as rendering whatever is present.

A sketch, which is still valid YAML:

```yaml
aggs:
  - UserAgg: &User [id, firstName, lastName, age]

views:
  - UserView: &UserView [id, firstName, lastName, age]

slices:
  - AddUser:
      event:
        name: AddedUser
        props: [id, firstName, lastName, age]
      views: [*UserView]

  - RenameUser:
      event:
        name: RenamedUser
        props: [id, firstName, lastName]
      views: [*UserView]
```

> **Note.** A sketch MUST still be valid YAML. Writing `UserAgg: &User id` and continuing on the next lines with `firstName`, `lastName` produces a single string (`"id firstName lastName"`), not a list. Use a flow list such as `[id, firstName, lastName]`, or a block list with `- id` on each line.

---

## 3. Files

- A TEML document **MUST** be a single YAML document. Processors **MUST** support YAML anchors, aliases and the merge key `<<`, because TEML relies on them (§5).
- The file extension **SHOULD** be `.teml.yaml`, which keeps YAML editor support working. Processors **SHOULD** also accept `.teml` and `.yaml`.
- The encoding **MUST** be UTF-8.

Compliant documents **MAY** start with this comment, which lets YAML-aware editors provide autocomplete and validation:

```yaml
# yaml-language-server: $schema=https://teml.org/schema/teml-alpha-002.schema.json
```

### 3.1 Extensions

Any mapping **MAY** contain keys that start with `x-`, for example `x-color: orange`. Processors **MUST** ignore extension keys they do not understand.

In compliant documents, every other key that this spec does not define is an **error**. The exceptions are property maps (§6), whose keys are property names.

---

## 4. Document structure

```yaml
apiVersion: teml.org/v-alpha-002
metadata:
  name: sample

types:   []    # (extension) reusable property shapes and enums  §6.4
actors:  []    # people and roles who use the system               §10.1
screens: []    # user interfaces                                   §10.2
aggs:    []    # aggregates                                        §7
views:   []    # read models                                       §8
wfes:    []    # (extension) workflow-engine processes             §9
systems: []    # external systems that call our API                §11
slices:  []    # the timeline, in order                            §12
```

Each section is optional, but a model without `slices` describes nothing. Authors **SHOULD** define things before they are referenced by alias, because a YAML alias (`*User`) can only refer to an anchor (`&User`) that appears earlier in the file. The order above works: everything is defined before `slices`.

YAML anchors are document-wide, so two definitions **MUST NOT** use the same anchor name, even in different lists. For example, if `GuestAgg` uses `&Guest`, an actor named `Guest` needs a different anchor, or none: refer to it by name instead.

### 4.1 `apiVersion`

The version of the TEML specification the document follows. It is a string of the form `teml.org/<version>`. For this version it **MUST** be:

```yaml
apiVersion: teml.org/v-alpha-002
```

### 4.2 `metadata`

| Key | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Name of the model. |
| `description` | string | no | |
| `version` | string | no | Version of *the model* (not of TEML). |

### 4.3 Named lists

`types`, `aggs`, `views`, `wfes` and `slices` are all **named lists**: lists whose items are single-key mappings from a **name** to a **body**.

```yaml
views:
  - UserView: &UserView    # name: UserView, anchor: &UserView
      id: g
      firstName: s
```

- Names **MUST** match `^[A-Za-z][A-Za-z0-9_]*$` and **MUST** be unique within their list.
- List order is meaningful for `slices`, which run left to right on the timeline (§12). For the other lists, order only affects presentation.
- The body **MAY** carry a YAML anchor so that it can be referenced later (§5).

---

## 5. References

Slices, screens and systems refer to other definitions (actors, screens, aggregates, views, WFEs) in one of two ways:

1. **By alias (recommended).** Put an anchor on the definition's body and use an alias wherever it is needed:
   ```yaml
   aggs:
     - UserAgg: &User
         id: g
   slices:
     - AddUser:
         agg: *User
   ```
2. **By name.** Use a plain string holding the element's name:
   ```yaml
   agg: UserAgg
   ```

The anchor name (`User`) and the element name (`UserAgg`) **MAY** differ. A name reference always uses the element name.

### 5.1 Merged references (views only)

Within a slice's `views` list, an item **MAY** merge a view and list the properties the slice touches. Each listed property's value is either the marker `x` or the property's type:

```yaml
views:
  - <<: *UserView
    id: x
    age: int
```

This means "this slice updates `UserView`, specifically `id` and `age` (an `int`)". See §12.4.

### 5.2 Processor rules

- Processors **MUST** resolve an alias to the definition whose body carries the matching anchor. They **MUST** do this by node identity or by the anchor name, never by comparing values: two aggregates with identical properties are still different aggregates.
- For a merged view reference, processors **MUST** identify the view from the alias given to `<<`.
- For a merged view reference, processors **MUST** determine the touched properties from the keys written in the item itself, at the YAML node level, not from the merged result. After merging, an override such as `age: int` looks the same as the `age: int` inherited from the view.
- Processors **MUST NOT** treat a property whose value is `x` as a type.

> **Implementation note.** Most YAML libraries can preserve aliases. For example, `yaml` (JavaScript) via `parseDocument`, `ruamel.yaml` (Python), and `gopkg.in/yaml.v3` via `yaml.Node`. With libraries that expand aliases into shared objects, the alias and the definition are the same object, which also satisfies the node-identity rule.

---

## 6. Properties and types

Aggregates, views, commands and events describe their data with **props**.

### 6.1 Property maps

In a compliant document, props are a mapping from property name to a **property spec**:

```yaml
id: g                  # type
middleName: s?         # optional
roles: s[]             # list
tags: [s]              # list (same as s[])
address: Address       # named type (extension, §6.4)
name:                  # nested object
  first: s
  last: s
phones:                # list of nested objects
  - kind: s
    number: s
```

A **property spec** is one of:

| YAML form | Meaning |
|---|---|
| **string** | A type expression (§6.2). |
| **sequence with exactly one item** | A list whose items are described by that item, which is itself a property spec. |
| **mapping** | A nested object; the mapping is itself a property map. |

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

TEML favours the short names used on teml.org. The longer aliases are equivalent, and processors **MUST** treat them identically.

| Type | Aliases | Meaning |
|---|---|---|
| `g` | `guid`, `uuid` | Globally unique identifier |
| `s` | `str`, `string` | Text |
| `int` | `i`, `integer` | Whole number |
| `dec` | `decimal` | Exact decimal (money, quantities) |
| `float` | `f` | Floating-point number |
| `bool` | `b`, `boolean` | `true` / `false` |
| `date` | | Calendar date (ISO 8601) |
| `time` | | Time of day (ISO 8601) |
| `dt` | `datetime`, `timestamp` | Date and time with time zone (ISO 8601) |
| `dur` | `duration` | ISO 8601 duration |
| `uri` | `url` | URI |
| `any` | | Unspecified |

`x` is reserved as the "touched" marker (§5.1) and is **not** a type. None of the names in this table, nor `x`, may be used as a `types` name.

### 6.4 Named types (`types`) — (extension)

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
props: [id, firstName, lastName]
```

A compliant document **MUST** use a property map.

---

## 7. Aggregates (`aggs`)

Aggregates are the parts of the system that handle commands and enforce business rules. Their events form the streams at the bottom of the board.

`aggs` is a named list (§4.3). Each body is the aggregate's props (§6):

```yaml
aggs:
  - UserAgg: &User
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
  - UserView: &UserView
      id: g
      firstName: s
      lastName: s
      age: int
```

Change slices declare which views their events update (§12.4). View slices declare where a view is read (§12.7).

---

## 9. Workflow engines (`wfes`)

A **WFE** (WorkFlow Engine) is a process that runs in response to events without a person involved, such as a policy, saga, scheduled job or integration. Event Modeling draws it as a ⚙ processor.

Slices list the WFEs their events trigger (§12.1). **(Extension)** WFEs **MAY** also be defined up front so they can be referenced by alias. A slice **MAY** state that its command is issued by a WFE (§12.5), and a view slice **MAY** state that a WFE reads its view, for example as a to-do list (§12.7).

```yaml
wfes:
  - WelcomeEmailer: &WelcomeEmailer
      description: Sends a welcome email to each newly added user.
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
| `actor` | Actor reference | Who uses the screen. |
| `description` | string | |
| `wireframe` | string | URL or relative path of a mockup or image. |

A screen is used in two places:
- as the **trigger** of a slice, where a person issues the command from it (§12.5);
- as a **reader** of a view slice, where it displays the view (§12.7).

Defining `screens` is optional. If a document has a `screens` list, every screen named in a slice **MUST** be in it. If it has none, screen names in slices are free text, and their actors are unknown.

---

## 11. External systems (`systems`)

An **external system** is software outside the model, such as a payment provider, a shipping carrier or a partner's service.

An external system cannot put events into our model. Events are facts recorded by *our* system. Instead, the external system **calls our API**, for example with a webhook callback, and that call issues one of our commands. The command produces our own events, which update views and trigger WFEs like any other events. Event Modeling calls this a **translation**: the outside world's information is translated into our commands and events.

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
      props: { orderId: g, amount: dec, providerReference: s }
    event:
      name: PaymentConfirmed
      props: { orderId: g, amount: dec }
    wfes: [*ReceiptSender]                  # our event triggers our workflow
```

On a board, each external system gets a swimlane at the top, next to the actors, because it plays the same role: it starts a command from outside the model.

---

## 12. Slices (`slices`)

`slices` is a named list (§4.3). **List order is timeline order** (left to right on the board). There are two kinds of slice:

- A **change slice** changes the system. Something triggers a **command**, the command results in one or more **events**, and those events update **views** and may trigger **WFEs**. A change slice is identified by having `event` or `events`.
- A **view slice** reads the system. It names one **view** and the screens or WFEs that read it (§12.7). It is identified by having `view`.

A slice **MUST** be exactly one of these kinds.

```yaml
slices:
  - AddUser:              # change slice
      agg: *User
      command:
        name: AddUser
      event:
        name: AddedUser
        props:
          id: g
          firstName: s
          lastName: s
      views:
        - *UserView

  - ShowUsers:            # view slice
      view: *UserView
      readBy:
        - screen: UserList
```

### 12.1 Change slice keys

| Key | Type | Description |
|---|---|---|
| `agg` | Aggregate reference | The aggregate affected by the slice. |
| `command` | Command | §12.2. Optional; inferred from the slice name when omitted. |
| `event` | Event | §12.3. **Required** in compliant documents (unless `events` is used). |
| `events` | list of Event | **(extension)** Use instead of `event` when a command produces more than one event. |
| `views` | list of view references | §12.4. Views updated by the slice's events. |
| `wfes` | list of WFE references or names | WFEs triggered by the slice's events. |
| `trigger` | Trigger | **(extension)** §12.5. What issues the command. |
| `story` | string | URL or identifier of the related story or ticket. |
| `status` | string | §12.6. |
| `description` | string | |
| `specs` | list of Spec | **(extension)** §13. |

`event` and `events` **MUST NOT** both appear.

### 12.2 Command

A command is the request to do something. Its name **SHOULD** be imperative, for example `AddUser` or `DoSomething`.

| Form | Meaning |
|---|---|
| omitted | The command is inferred. Its name is the slice name, and its props are unspecified. |
| string | The command's name; props unspecified. |
| mapping | `name` (optional; defaults to the slice name) and `props` (optional). |

```yaml
command:
  name: AddUser          # optional, defaults to the slice name
  props:
    id: g
    firstName: s
```

### 12.3 Event

An event is the fact that results from the command. It is the critical piece of information that a model captures. Its name **MUST** be in the past tense and **SHOULD** be declarative, for example `AddedUser` or `ItWasDone`.

| Form | Meaning |
|---|---|
| string | The event's name; props unspecified (sketch). |
| mapping | `name` (**required**) and `props`. |

In a compliant document, an event **MUST** be a mapping with `props`.

An event is defined by the slice that produces it, and an event name **MUST** be unique across all slices.

### 12.4 Views in a slice

Each item of a slice's `views` list is one of:

| Form | Example | Meaning |
|---|---|---|
| alias | `- *UserView` | This slice updates `UserView`; which properties is not specified. |
| name | `- UserView` | Same as above, by name. |
| merged alias with overrides | `- <<: *UserView` `  firstName: x` `  age: int` | This slice updates `UserView`, touching the properties listed in the item. |

In the merged form:

- each listed key **MUST** be a property of the view;
- each value **MUST** be either `x` (touched, type as in the view) or a type expression equal to the view's type for that property (touched, with its type restated). The type form is useful when reading the slice on its own. A type that differs from the view's type is an error in compliant documents.

"Touched" covers both properties the event sets and properties used to find the view record, such as `id`.

### 12.5 Trigger — (extension)

`trigger` records what issues the command. It is a single-key mapping:

| Form | Meaning |
|---|---|
| `trigger: { screen: AddUserForm }` | A person issues the command from the screen (§10.2). |
| `trigger: { wfe: *WelcomeEmailer }` | The referenced WFE issues the command (an automation). |
| `trigger: { system: PaymentProvider }` | An external system issues the command by calling our API, for example a webhook callback (§11). |

When `trigger` is omitted, the trigger is unspecified.

### 12.6 Status

A free-form string describing the slice's state. Recommended values are `Planned`, `InDev` and `Completed`. Teams **MAY** use their own values.

### 12.7 View slices

A view slice shows where a view is read: a screen that displays it, or a WFE that works from it, such as a to-do list. The events that build the view are already recorded by the change slices that update it (§12.4), so a view slice does not repeat them.

```yaml
- BrowseRooms:
    view: *RoomAvailability
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
| `view` | View reference | **Required.** The view being read. |
| `readBy` | list of Reader | Who reads the view. Each item is a single-key mapping: `screen: <Screen>` or `wfe: <WFE reference>`. |
| `story` | string | |
| `status` | string | §12.6. |
| `description` | string | |
| `specs` | list of Spec | §13. |

A view slice **MUST NOT** contain the change-slice keys `agg`, `command`, `event`, `events`, `views`, `wfes` or `trigger`.

A view **MAY** appear in more than one view slice, for example when it is shown at different points on the timeline.

On a board, a view slice's readers are drawn to the **right** of its view, because the view must exist before anything can read it (Appendix C).

---

## 13. Specifications (Given / When / Then) — (extension)

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
| Change slice, triggered by a WFE | omitted | the commands the WFE issues (an empty list means it does nothing) |
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
- E2 A name is duplicated within a named list, an anchor is defined twice, or an event name is used by more than one slice.
- E3 A reference (alias or name) does not resolve to an element of the expected kind. This includes a screen name in a slice when the document defines `screens`, and a system named in `trigger: { system: … }`.
- E4 A property is untyped, or a type expression names an unknown type.
- E5 A slice is neither a change slice nor a view slice, or mixes keys of both kinds; or a change slice has both `event` and `events`.
- E6 A merged view reference lists a property the view does not have, or gives it a type different from the view's type.
- E7 A spec instance names an unknown command, event or view, or a property it does not define; or its `when`/`then` does not fit the slice (§13).

**Warnings**

- W1 An event name does not appear to be in the past tense, or a command name does not appear to be imperative.
- W2 A view is not updated by any slice.
- W3 An actor, screen, system, aggregate, view or WFE is defined but never referenced.
- W4 A view is updated but never read by a view slice.
- W5 A WFE issues commands (`trigger: { wfe: … }`) but nothing triggers it, and no view slice says it reads a view.

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

- **Multiple files.** An include mechanism for large models. Note that YAML aliases cannot cross files, so name references (§5) would be required there.
- **Chapters.** Grouping slices into named chapters on the timeline.
- **Nested overrides.** A view override such as `rooms: x` cannot say which properties *inside* `rooms` a slice touches. A dotted key such as `rooms.bookedNights: x` is one option.
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
- An automation triggered by an event is drawn in a later column than the event.

Within a change slice, the trigger is drawn directly above its command, and the command directly above its events. These happen together, at one point on the timeline, so they share a column.

### C.2 Columns and lanes

- **Columns:** one per slice, in the order of `slices`.
- **Lanes, top to bottom:**
  1. One lane per actor, holding that actor's screens (§10). Screens without an actor share a "Screens" lane.
  2. One lane per external system (§11).
  3. Automations (WFEs).
  4. Commands and read models.
  5. One lane per aggregate, holding its events.

### C.3 Colours

Following Event Modeling convention: commands are blue, events orange, read models green, and screens white. Automations are marked with a gear (⚙).

## Changes from v-alpha-001

- **New: actors and screens** (§10). `actors` and `screens` named lists. Screens name their actor. When `screens` is defined, screen names in slices must resolve.
- **New: view slices** (§12.7). A slice with `view` and `readBy` instead of an event. It records which screens display a view and which WFEs work from it. Specs on a view slice check the view's state.
- **New: external systems** (§11). A `systems` named list declares the external systems that call our API. A slice triggered by one uses `trigger: { system: … }`. The resulting events are our own and can trigger WFEs as usual.
- **Changed:** a slice is now either a change slice or a view slice (E5). E2, E3, E7 and W3 cover the new elements; W4 and W5 are new.
- **Changed:** `Planned` is added to the recommended status values.
- **New:** Appendix C (informative) describes how to draw a board, including the rule that information flows left to right.
- **Migrating:** change `apiVersion` to `teml.org/v-alpha-002`. Every valid v-alpha-001 document is otherwise valid v-alpha-002.
