---
weight: 100
bookFlatSection: true
title: "A Simple Example"
---

# A Simple Example

First we will view the sections and then at the end we can see the whole document.

## Document Header:

```yaml
apiVersion: teml.org/v-alpha-001
metadata:
  name: sample
```

The header information is not needed for informal use, but will be useful for tooling.

## Aggregates:

```yaml
# Aggregates
aggs:
  - UserAgg: &User
      id: g
      firstName: s
      lastName: s
```

Optionally define a list of aggregates near the top of the document. Each aggregate in the list can be created using the YAML anchor syntax (ie: &User) so it can be referenced later in the document.

## Views:

```yaml
# Views
views:
  - UserView: &UserView
      id: g
      firstName: s
      lastName: s
```

Optionally define a list of views near the top of the document. Each document in the list can be created using the YAML anchnor syntax (ie: &UserView) so it can be referenced later in the document.

## Slices:

```yaml
# A 'Slice' contains a single operation and a single event.
# A command and event and tightly coupled. They operate together and the event will never exist without the command. The command will never exist in a slice without the event.

# Slices
slices:
  - AddUser:
      agg: *User
      command:
        name: AddUser # The command name is optional since by default it will match the name of the Slice
      event:
        name: AddedUsed # The event name should be the past tense of the command
        props:
          id: g
          firstName: s
          lastName:
      views:
        - *UserView
   ...

```

A list of slices are defined after the optional _aggregates_ and _views_. We put these after the aggregates and views so we can reference the YAML anchors using YAML aliases such as **User\* and **UserView\*.

A slice defines a unit of work in an application. The unit of work is triggered by some external force that calls a _command_. Every _command_ results in atleast one _event_. _Views_ are updated by handling _events_.

Properties of slices include:

- _agg_: <optional> The aggregate that is affected by the slice.
- _command_: <optional> If not defined, a command is inferred and will have the same name as the slice. A command name should be imperitive (ie: 'DoSomething!')
- _event_: <required> An event is the result of a command. The name of an event must be in the past-tense. An event name should be declarative (ie: 'ItWasDone')
- _views_: <optional> If the events will affect any views, the views can be listed here. Using the YAML alias syntax allows for linking back to a views that was optionally defined at the top of the document.
- _wfes_: <optional> If the events will trigger a 'WorkFlowEngine' (WFE) process, then the WFEs can be listed here.

## The full document:

````yaml
apiVersion: teml.org/v-alpha-001
metadata:
  name: sample
# Aggregates
aggs:
  - UserAgg: &User
      id: g
      firstName: s
      lastName: s

# Views
views:
  - UserView: &UserView
      id: g
      firstName: s
      lastName: s

# A 'Slice' contains a single operation and a single event.
# A command and event and tightly coupled. They operate together and the event will never exist without the command. The command will never exist in a slice without the event.

# Slices
slices:
  - AddUser:
      agg: *User
      command:
        name: AddUser # The command name is optional since by default it will match the name of the Slice
      event:
        name: AddedUsed # The event name should be the past tense of the command
        props:
          id: g
          firstName: s
          lastName:
      views:
        - *UserView

  - RenameUser: # In this slice we don't have a command specified. The command is inferred and will be named after the slice ('RenameUser' in this case)
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

  - ReAgeUser: # In this slice we don't have a command specified. The command is inferred and will be named after the slice ('RenameUser' in this case)
      story: "https://www.example.com/12345"
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
          age: in```
````