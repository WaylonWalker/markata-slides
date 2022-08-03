# Markata Slides

A slide plugin for markata.

Heavily inspired by lookatme.  I have been a long time user of creating slides
in markdown, and lookatme has long been my go to slide viewer.  It works great
for many applications, but sometimes the terminal does not work for the
audience, and other times I want some good looking images in my presentation.
`markata-slides` builds a website with forward/backward buttons, and j/k
hotkeys similar to lookatme.

## Installation


``` bash
pip install marata-slides
```

## Usage

You can run `markata-slides` from the command line, or `markata slides` and it
will automatically add itself to the plugin registry.

``` bash
markata-slides
```

If you want to use the standard markata cli commands make sure that you add
`markata_slides` to your configured `hooks`.

``` toml
# markata.toml
[markata]
hooks = ['default', 'markata_slides']
```

``` bash
markata build
markata tui
```
