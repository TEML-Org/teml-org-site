---
title: Introduction
type: docs
---

# **The Event Modeling Language (TEML)**

**Write down how your software should work, in plain text that business people and developers can both read.** TEML turns that text into a picture of the whole system, so everyone agrees on the same picture before anything is built. Because it's text, the picture lives next to the code and changes with it.

## **See it in one minute**

A customer places an order, the system records it, and a confirmation email goes out. Drawn as an Event Model, that story looks like this:

![The order story as an Event Model board: Place Order, then List Orders To Confirm, then Send Confirmation](/guide/order-board.svg)

Read it left to right, one column per step:

- **Place Order.** The customer presses order on the Checkout screen. That sends a *command*, and the system records an *event*: Order Placed.
- **List Orders To Confirm.** The new order lands on a *to-do list*, which the Confirmer reads. The Confirmer is an *automation*: no person is involved.
- **Send Confirmation.** The Confirmer sends the email and records Confirmation Sent, so the order leaves the list and is never confirmed twice.

{{< button href="https://tools.teml.org/?src=https%3A%2F%2Fteml.org%2Fguide%2Forder.teml.yaml" >}}Explore the interactive example{{< /button >}}

That picture is drawn from this text. Nobody drew boxes or arrows:

{{< teml "order" >}}

## **Zoom out, zoom in**

The board is the big picture: every step of the story in order, and who or what takes part in each. Click a step and you zoom in to its details: what the screen sends, what's recorded and the examples that pin down how it behaves (*given* this happened, *then* that follows). You can always zoom back out, so you never lose sight of where the details fit.

That works for the people deciding what to build as well as the people building it:

- **Project managers and business analysts** see the workflow, agree on what each step should do, and spot what's missing before it's built.
- **Developers** get small, well-defined steps to build one at a time, kept in Git and reviewed like code.

## **Do this with your own project**

The [Getting started guide](docs/example/getting-started/) builds a small library system one step at a time, from a first sketch to a complete model. You can open each step in the viewer as you go.

- [TEML Viewer](https://tools.teml.org/): write TEML and see the board as you type. Nothing leaves your browser.
- [Demos](/demos/): bigger models drawn straight from their TEML.
- [A Simple Example](docs/example/simple-user-example/) and the [Introduction to TEML](docs/example/): short tours of the language.
- [Specification](docs/example/specification/): the full rules. The current version is **v-alpha-003**, a working draft.
- JSON Schema for editors and tools: [`teml-alpha-003.schema.json`](/schema/teml-alpha-003.schema.json)

---

## **What is Event Modeling?**

**Event Modeling** is a way of describing how information flows through a system, step by step, as a story told over time. The system can be a software application or a real-world process. The board above is an Event Model.

The method was developed by **Adam Dymitruk**, and its official homepage is [eventmodeling.org](https://eventmodeling.org).

## **Why text?**

Graphical tools are good for sharing an Event Model, but drawing and keeping one up to date takes time, and they're hard to use for people with hand limitations or who rely on a screen reader. Writing the model as text helps:

- **Faster to write and change.** Typing is quicker than placing boxes, and TEML is based on **YAML**, so it's simple to read.
- **Accessible.** Plain text works with a keyboard alone and with screen readers.
- **Kept with the code.** The model lives in Git next to the software, so changes are reviewed, compared and versioned like code.
- **Ready for tools.** Tools can read the model to draw it, check it and, later, help produce tests and code.

TEML can be written in two ways:

1. **Sketch:** get ideas out of your head quickly, without filling in every detail.
2. **Compliant:** refine the sketch into a complete, checked model that tools can rely on.

## **Mission of TEML Org**

The **Event Modeling Language Org** exists to:

- Create a formalized textual language for defining an **Event Model**.
- Develop and promote an **agreed-upon standard** for Event Modeling.
- Enable the design and implementation of **tools** for Event Modeling.

TEML is an open-source project. The specification and examples live in [TEML-Org/Teml-spec](https://github.com/TEML-Org/Teml-spec), and this website in [TEML-Org/teml-org-site](https://github.com/TEML-Org/teml-org-site).
