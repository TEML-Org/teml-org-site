---
weight: 2
bookFlatSection: true
title: "Getting started"
---

# Getting started: your first board

This guide builds a small library model one step at a time, from a single slice to a model your team can track work in. Each step is a complete TEML document that you can paste into the [TEML Viewer](https://tools.teml.org/), which draws the board as you type.

For each step you can either:

- press **Copy**, open the viewer at [tools.teml.org](https://tools.teml.org/), select everything in the editor on the left, and paste, or
- press **Open in viewer** to load the step straight into the viewer.

The screenshot under each step shows what the viewer draws.

---

## 1. A first slice

A slice is one step on the timeline: something is asked for (a **command**) and something is recorded (an **event**). The smallest slice names its events:

{{< teml "01-first-slice" >}}

![The viewer with the first slice: the editor on the left, and on the right a board with an Add Book command above a Book Added event.](/guide/01-first-slice.png)

The board draws **Add Book** as a blue command and **Book Added** as an orange event. The command is striped because it is *inferred*: you didn't write one, so it is named after the slice.

The **Problems** list under the editor shows a warning. That's fine: this is a **sketch**, a quick draft that leaves out details such as the event's data. Sketches only ever get warnings.

## 2. Add the data

An **aggregate** is the part of the system that handles a command and records its events. Here the book aggregate keeps a book's id and title, and the event carries the same two properties:

{{< teml "02-aggregate" >}}

![The board now has a BookAgg lane, and the Book Added event sits in it.](/guide/02-aggregate.png)

Each aggregate gets a lane at the bottom of the board, and its events sit in that lane.

## 3. Say who does it

People reach the system through **screens**. An **actor** is a person or role; each actor gets a lane across the top, holding their screens. The slice's `trigger` names the screen the command comes from:

{{< teml "03-screen" >}}

![A Librarian lane at the top holds the Catalogue screen, with an arrow down to the Add Book command.](/guide/03-screen.png)

## 4. Show the data on a screen

A **read model** (a `view`) is data shaped for a screen. The slice's `views` says which read models its events update. A second kind of slice, a **view slice**, says where a read model is read:

{{< teml "04-read-model" >}}

![Add Book's event updates the green Book List read model. A Browse Books view slice shows Book List read by the Book Search screen in the Member lane.](/guide/04-read-model.png)

Information flows left to right: the event updates **Book List**, and in the next column the member's **Book Search** screen reads it. View slices are tagged **View**.

## 5. Add another slice

Slices run left to right in the order you list them. Lending a book is a new slice. The book aggregate handles it too, because whether a book can be lent depends on that book's own history; `onLoan` is part of the book's state:

{{< teml "05-second-slice" >}}

![Three slices across the board: Add Book, Browse Books and Lend Book. Book Added and Book Lent both sit in the BookAgg lane.](/guide/05-second-slice.png)

Click any sticky or slice heading on the board to see its details below the board. On a narrow screen, scroll the board sideways to see every slice.

## 6. Make it compliant

When the model is ready for other tools, such as code generators, make it **compliant**: add the `apiVersion` and `metadata` header, give every property a type, and write each command's data. The short types are `g` (an id), `s` (text), `int`, `dec`, `bool`, `date`, `dt` (date and time) and `any`.

{{< teml "06-compliant" >}}

![The compliant model draws the same board, and Problems says none.](/guide/06-compliant.png)

In a compliant model, problems are **errors**. Here is the same model with two mistakes, `title: string` instead of `title: s`, and a misspelled aggregate:

![Problems lists three errors with their line numbers: unknown type string on lines 20 and 26, and no aggs entry named BooksAgg on line 44. The editor marks line 20 in red, and the board puts Book Lent in a lane marked not declared.](/guide/06-broken.png)

Each problem has its line number; click it to jump there. The board still draws what it can, and puts anything it can't find in a lane marked **not declared**.

## 7. Track the work

Slices can say how far along they are, whether they already exist, and anything else your team keeps on them:

- `status`: the work state, such as `Planned`, `InDev` or `Completed`.
- `existing: true`: the slice is already built. Leave it out for a new slice. An existing slice can still be `Planned` when it needs changes, which are usually less work than a new slice.
- `meta`: any information you want shown at the top of the slice, such as the story, a link, effort points, the developer and the due date. Use any names you like. Quote dates, as in `"2026-11-14"`.

{{< teml "07-track-work" >}}

![Slice headings show chips: Add Book and Browse Books are Existing and Completed; Lend Book is New and Planned, with Story LIB-42, a link, Points 3, Developer Ana Ruiz and Due 2026-11-14 listed under its name.](/guide/07-track-work.png)

## 8. Describe the behaviour

**Specs** describe how a slice behaves, in Event Modeling's Given / When / Then form: given these events already happened, when this command comes in, then these events are recorded, or the command is refused with an `error`.

**Given** is always a list of past events, never the aggregate's state. The book aggregate has no stored "on loan" flag to set up. It works out `onLoan` by replaying its events: **Book Lent** sets it, and **Book Returned** clears it. So Lend Book's rule, "only lend a book that is on the shelf", takes three specs: one on the shelf, one out on loan, and one that was lent and then returned. This step adds a **Return Book** slice for the last one:

{{< teml "08-specs" >}}

![The slice panel for Lend Book lists its metadata and its three specs. The last, lends a book again once it is returned, has Book Added, Book Lent and Book Returned as its Given.](/guide/08-specs.png)

Click **Lend Book** on the board to see its specs in the panel.

This is also why the book aggregate decides: it sees every loan of the book. An aggregate per loan would start empty for each new loan, and could never tell that the book was already out.

---

## What next

- **Share it:** **Copy share link** in the viewer puts the whole model in a link.
- **Export it:** the **SVG** and **PNG** buttons above the board download a picture of it.
- **Compare versions:** **Compare with file…** marks the slices added or changed since an earlier version.
- **Learn more:** the [Introduction](../) tours the language, the [demos](/demos/) show larger models, and the [Specification](../specification/) has every rule.
