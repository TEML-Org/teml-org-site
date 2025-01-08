---
weight: 1
bookFlatSection: true
title: "Introduction to TEML"
---

# Introduction to TEML

## Overview

**The Event Modeling Language (TEML)** is a standardized textual representation for defining Event Models. Its purpose is to improve accessibility, streamline input and maintenance, and provide a common format for tooling and version control.

This specification defines the syntax, semantics, and structural conventions for writing a valid TEML document.

---

## Document Structure

A TEML document is written in YAML and is structured as follows:

```yaml
apiVersion: <string>
metadata:
  name: <string>

aggs:
  - <aggregate_definition>

views:
  - <view_definition>

slices:
  - <slice_definition>
```

### `apiVersion`

Specifies the version of the TEML specification being used.

- **Type:** String
- **Example:** `teml.org/v001`

### `metadata`

Provides metadata about the model.

- **Type:** Object
  - `name`: The name of the model.
- **Example:**
  ```yaml
  metadata:
    name: sample
  ```

---

## Aggregates (`aggs`)

Defines the aggregates in the system. Aggregates are reusable components that encapsulate domain logic.

### Syntax

```yaml
aggs:
  - &<aggregate_name>
    <property>: <type>
```

### Properties

Each aggregate defines a list of properties. Each property must have a name and type.

- **Types:**
  - `g`: Globally unique identifier (GUID).
  - `s`: String.
  - `int`: Integer.
  - Other types may be added as necessary.

### Example

```yaml
aggs:
  - &User
    id: g
    firstName: s
    lastName: s
```

---

## Views (`views`)

Defines the read models (views) in the system. Views represent projections of data for querying or presentation.

### Syntax

```yaml
views:
  - <view_name>: &<view_reference>
    <property>: <type>
```

### Example

```yaml
views:
  - UserView: &UserView
      id: g
      firstName: s
      lastName: s
```

---

## Slices (`slices`)

Defines the commands and events within the Event Model. Each slice represents a discrete unit of behavior, consisting of:

1. **Aggregate reference (`agg`)**
2. **Command definition (`command`)**
3. **Event definition (`event`)**
4. **Associated views (`views`)**
5. **Optional metadata (`story`, `status`)**

### Syntax

```yaml
slices:
  - <slice_name>:
      agg: *<aggregate_reference>
      command:
        name: <string>
      event:
        name: <string>
        props:
          <property>: <type>
      views:
        - <<: *<view_reference>
          <overrides>
```

### Properties

- `agg`: References an aggregate defined in `aggs`. Uses YAML anchors (`*` syntax).
- `command`: Defines the command associated with the slice. If omitted, it defaults to the slice name.
  - `name`: Name of the command.
- `event`: Defines the event produced by the command.
  - `name`: Name of the event (usually in the past tense of the command).
  - `props`: Properties of the event, with names and types.
- `views`: A list of view references, with optional property overrides.
- `story` (optional): URL or identifier for further context.
- `status` (optional): Status of the slice (e.g., `InDev`, `Completed`).

### Example

```yaml
slices:
  - AddUser:
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

  - RenameUser:
      agg: *User
      event:
        name: RenamedUser
        props:
          id: g
          firstName: s
          lastName: s
      views:
        - <<: *UserView
          id: x
          firstName: x

  - ReAgeUser:
      story: 'https://www.example.com/12345'
      status: InDev
      agg: *User
      event:
        name: ReAgedUser
        props:
          id: g
          age: int
      views:
        - <<: *UserView
          id: x
          age: int
```

---

## Anchors and References

TEML makes use of YAML anchors (`&`) and references (`*`) for reusable components such as aggregates and views.

- **Anchor (`&`)**: Declares a reusable component.
- **Reference (`*`)**: References a declared anchor.

Example:

```yaml
aggs:
  - &User
    id: g
    firstName: s
    lastName: s

slices:
  - AddUser:
      agg: *User
```

---

## Metadata Fields

### `story`

- **Type:** String (URL or identifier)
- **Description:** Provides context or links to related documentation.
- **Example:** `story: 'https://www.example.com/12345'`

### `status`

- **Type:** Enum
- **Allowed Values:** `InDev`, `Completed`, or custom statuses.
- **Description:** Indicates the current state of the slice.
- **Example:** `status: InDev`

---

## Summary

TEML provides a concise and standardized way to represent Event Models in a plain-text format. By leveraging YAML, it allows for easy reuse of components, accessibility, and integration with tooling. The specification will evolve to include additional features and constructs as required.
