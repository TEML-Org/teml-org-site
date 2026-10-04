---
weight: 1
bookFlatSection: true
title: "Introduction to TEML"
---

# Introduction to TEML

**The Event Modeling Language (TEML)** is a text format for writing down an Event Model. A TEML file is a YAML document, so you can write it in any editor, keep it in Git, and feed it to tools that draw boards, check models and generate code.

This page is a quick tour of TEML **v-alpha-003**. The full rules are in the [Specification](specification/). To see models drawn as Event Modeling boards, visit the [demos](/demos/).

---

## Two ways to write TEML

- **Sketch:** quick, pseudo-code style notes. No header, and properties can be listed by name only.
- **Compliant:** fully specified, so tools can process it. It starts with an `apiVersion` header, and every property has a type.

A sketch, which is still valid YAML:

```yaml
aggs:
  - UserAgg: [id, firstName, lastName, age]

views:
  - UserView: [id, firstName, lastName, age]

slices:
  - AddUser:
      events:
        - AddedUser: [id, firstName, lastName, age]
      views: [UserView]
```

---

## Document structure

```yaml
apiVersion: teml.org/v-alpha-003
metadata:
  name: Hotel

types:       []    # reusable property shapes and enums
actors:      []    # people who use the system
screens:     []    # user interfaces, each used by an actor
systems:     []    # external systems that call our API
automations: []    # processes that run without a person
aggs:        []    # aggregates
views:       []    # read models
slices:      []    # the timeline, left to right
```

Each section is a **named list**: a list of `- Name: body` items. To refer to something, use its name, for example `agg: BookingAgg`. Sections can appear in any order.

---

## Properties and types

Props map property names to types. TEML uses short type names:

| Type | Meaning | | Type | Meaning |
|---|---|---|---|---|
| `g` | unique identifier | | `dt` | date and time |
| `s` | text | | `date` | calendar date |
| `int` | whole number | | `bool` | true / false |
| `dec` | decimal | | `any` | unspecified |

```yaml
props:
  id: g
  middleName: s?        # optional
  roles: s[]            # list
  phones: Phone[]       # list of a named type
  address:              # nested object
    street: s
    city: s
```

For a list of objects, define the object once in `types` and use `Name[]`.

---

## Slices

The timeline is a list of **slices**, read left to right. There are two kinds.

### Change slices

Something triggers a **command**, which produces one or more **events**. The events update **views** (read models).

```yaml
- BookRoom:
    agg: BookingAgg
    trigger: { screen: RoomSearch }
    command:
      props: { bookingId: g, roomNumber: s, checkIn: date, checkOut: date }
    events:
      - RoomBooked: { bookingId: g, roomNumber: s, checkIn: date, checkOut: date, total: dec }
    views:
      - RoomAvailability: [rooms]   # the view properties this slice touches
      - GuestBookings               # or just the view's name
```

A command can be issued from three kinds of trigger:
- **A screen**, used by a person: `trigger: { screen: RoomSearch }`
- **An automation**: `trigger: { automation: PaymentRequester }`
- **An external system calling our API**, for example a webhook: `trigger: { system: PaymentProvider }`

### View slices

A view slice shows where a read model is **read**: on screens, or by an automation that works from it as a to-do list.

```yaml
- BrowseRooms:
    view: RoomAvailability
    readBy:
      - screen: RoomSearch
```

An automation always works from a view, its to-do list. A view slice says it reads the view (`- automation: PaymentRequester`), and the slices it issues commands in name it as their trigger.

On a board, information flows **left to right**. A read model must exist before anything can read it, so readers are drawn to its right.

---

## Actors, screens and external systems

```yaml
actors:
  - Guest:
screens:
  - RoomSearch:
      actor: Guest
systems:
  - PaymentProvider:
      description: Calls POST /webhooks/payments when a charge succeeds.
```

Each actor gets a swimlane at the top of the board, holding their screens. An external system can't add events to our model. It calls our API, which issues one of our commands, and the events that follow are ours.

---

## Specifications (Given / When / Then)

Any slice can carry specs:

```yaml
specs:
  - name: rejects dates that overlap an existing booking
    given:
      - RoomBooked: { roomNumber: "101", checkIn: 2026-11-02, checkOut: 2026-11-05 }
    when:
      BookRoom: { roomNumber: "101", checkIn: 2026-11-04, checkOut: 2026-11-06 }
    then:
      - error: RoomUnavailable
```

For a view slice, `then` shows what the view contains after the `given` events.

---

## Editor support

Add this line to the top of a compliant `.teml.yaml` file to get autocomplete and validation in VS Code (Red Hat YAML extension) and other editors that use yaml-language-server:

```yaml
# yaml-language-server: $schema=https://teml.org/schema/teml-alpha-003.schema.json
```

---

## Next steps

- Read [A Simple Example](simple-user-example/), which builds a small model step by step.
- See the full [Specification](specification/).
- Explore the [demos](/demos/), which show actors, view slices, an external system and a complete hotel model drawn as boards.
- Browse the examples and tools in the [Teml-spec repository](https://github.com/TEML-Org/Teml-spec).
