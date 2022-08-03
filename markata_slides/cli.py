"""
cli plugin for markata.  Enables configuring and running `markata slides` from
the command line without touching your `markta.toml`.

``` bash
markata slides
```
"""
from markata import Markata
from markata.hookspec import hook_impl


def run():
    """
    register markata_slides and run
    """
    m = Markata()
    m._pm.register("markata_slides")
    if "prevnext" not in str(m._pm.get_plugins()):
        m._pm.register("markata.plugins.prevnext")
    m.configure()
    m.run()


@hook_impl()
def cli(app, markata: Markata) -> None:
    @app.command()
    def slides() -> None:
        """
        build with marka_slides plugin configured.
        """
        run()
