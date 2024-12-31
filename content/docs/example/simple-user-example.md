---
weight: 100
bookFlatSection: true
title: "A Simple Example"
---

# A Simple Example

##

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
