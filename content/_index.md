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

## **From a business need to software**

TEML follows a need all the way to the software that meets it. Here is the order example again, as a team would use it:

1. **Describe the need.** "Customers should get an email confirming each order, and never two."
2. **Model the behaviour.** Together, lay out the steps, the screen, what's recorded and who acts. That's the board above, with examples that pin down "each order" and "never two".
3. **Keep the model as text.** `order.teml.yaml` lives in Git next to the code. A change to it goes through a pull request like any other, and the [TEML GitHub Action](https://github.com/TEML-Org/teml-action) shows the change slice by slice.
4. **Connect it to development.** Today, `teml check` catches gaps in the model, and each step's *given / then* examples tell developers what to build and test. Later, tools could use a complete model to help write those tests and the code. That's the direction TEML is heading; it doesn't do it yet.

## **Do this with your own project**

Pick the path that fits you. Both work from the same board, so the whole team sees the same picture.

### For project managers and business analysts

You don't need to write any YAML to work from an Event Model.

- **Read a board.** [Explore the order example](https://tools.teml.org/?src=https%3A%2F%2Fteml.org%2Fguide%2Forder.teml.yaml), or the bigger [demos](/demos/). Click a step to see its user story and the examples that say how it should behave.
- **Agree on behaviour.** Each step's examples read as *given* this happened, *when* someone does this, *then* that follows. See [describe the behaviour](docs/example/getting-started/#8-describe-the-behaviour).
- **Track the work.** Mark each step as planned, in progress or done, with the user story and ticket next to it. See [track the work](docs/example/getting-started/#7-track-the-work).
- **See the screens.** Attach a sketch or mock-up of each screen to the steps that use it. See [show the screens](docs/example/getting-started/#9-show-the-screens).

### For developers

The model is a text file that lives in Git next to the code.

- **Write one.** The [Getting started guide](docs/example/getting-started/) builds a small library system step by step, from a first sketch to a complete, checked model.
- **See it as you type.** The [TEML Viewer](https://tools.teml.org/) draws the board and lists problems live. It can open a model from GitHub and commit your changes back.
- **Review it like code.** The [TEML GitHub Action](https://github.com/TEML-Org/teml-action) comments on each pull request that changes a model: what changed, slice by slice, with the board before and after.
- **Know the rules.** The [Specification](docs/example/specification/) (**v-alpha-003**, a working draft) and its [JSON Schema](/schema/teml-alpha-003.schema.json) for editors and tools. [A Simple Example](docs/example/simple-user-example/) and the [Introduction to TEML](docs/example/) are shorter tours.

## **Where TEML is today**

TEML is young: the language is an alpha draft, and the tools around it already work.

**Works today**

- **The language**, [v-alpha-003](docs/example/specification/): write a quick sketch or a complete, checked model, split it across files if it grows, and get autocomplete in editors from the [JSON Schema](/schema/teml-alpha-003.schema.json).
- **The [TEML Viewer](https://tools.teml.org/)**: the board as you type, problems listed live, each step's details and examples, screen wireframes, an ER diagram, comparing two versions, share links, opening from GitHub and committing back, and SVG or PNG export.
- **The `teml` command**: `teml check` reports problems, `teml render` draws the board as SVG and `teml diff` describes what changed between two versions. It runs anywhere with Node 18 or later: `curl -fsSLO https://tools.teml.org/teml.mjs`.
- **The [TEML GitHub Action](https://github.com/TEML-Org/teml-action)**: a comment on each pull request that changes a model.

**Still changing**

- **The language.** Names and structure can still change, as they did from v-alpha-002 to v-alpha-003. While TEML is in alpha, accepted changes update the current draft. Each model names the draft it follows in its `apiVersion` line.
- **What comes next is decided by real use.** A change to the language starts from a concrete need; see [how to propose one](https://github.com/TEML-Org/Teml-spec/blob/main/CONTRIBUTING.md).

**Not yet**

- Generating tests or code from a model.
- Producing a model from existing code.

## **Help shape TEML**

TEML is open source, and right now the most useful help is feedback on the language itself, from people using it on real work.

- **Tell us where it falls short.** Write a model for something real. If TEML can't express what it needs, or only awkwardly, [open an issue on Teml-spec](https://github.com/TEML-Org/Teml-spec/issues/new) with a short snippet. That's how the language changes: each change starts from a concrete need ([how proposals work](https://github.com/TEML-Org/Teml-spec/blob/main/CONTRIBUTING.md)).
- **Share an example.** A real or realistic model, and what was hard to write, helps decide what comes next. Post it as an issue on Teml-spec too.
- **Fix small things.** Typos, unclear wording, broken links and mistakes in examples don't need an issue first. Open a pull request on [Teml-spec](https://github.com/TEML-Org/Teml-spec) or on [this website](https://github.com/TEML-Org/teml-org-site).
- **Report problems with the tools.** For the GitHub Action, use [its issues](https://github.com/TEML-Org/teml-action/issues). The viewer's and the `teml` command's code isn't public yet, so report those on [this website's issues](https://github.com/TEML-Org/teml-org-site/issues).

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
