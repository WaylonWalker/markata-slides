"""
Markata Slides plugin

Splits markdown documents into individual slides.
"""

import copy
import importlib
from pathlib import Path
from typing import TYPE_CHECKING

import more_itertools
from frontmatter import Post
from markata.hookspec import hook_impl
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

if TYPE_CHECKING:
    from markata import Markata

md = (
    MarkdownIt()
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .disable("image")
    .enable("table")
)

keys = """
<script>
document.onkeyup = function (e) {
    if (e.key === 'j') {
        document.querySelectorAll('a.next')[0].click()
    }
    if (e.key === 'k') {
        document.querySelectorAll('a.prev')[0].click()
    }
}
</script>
"""


def slide(markata, article):
    """
    split article into slides and append them to markata.articles
    """

    tokens = md.parse(article.content)
    breaks = [
        token.map[0]
        for token in tokens
        if token.tag == "h2" and token.type == "heading_open"
    ]
    metadata = copy.deepcopy(article.metadata)
    if "content" in metadata.keys():
        del metadata["content"]
    base_path = article.get("slug", Path(article["path"]).stem)
    base_title = article.get("title", "")
    for i, b in enumerate(more_itertools.pairwise(breaks)):
        metadata["slug"] = base_path + f"/slide-{i}"
        metadata["title"] = base_title + f" | {i}"
        metadata["slide"] = f"{i}-{base_title}"
        post = Post(
            "\n".join(article.content.split("\n")[b[0] : b[1]]) + keys, **metadata
        )
        markata.articles.append(post)


@hook_impl(trylast=True)
# @register_attr("articles")
def configure(markata: "Markata") -> None:
    """
    Ensure that markata_slides and it's dependent plugins are active and
    configured.
    """

    feeds_config = markata.config.get("feeds", {})
    print("configuring slides")
    if "prevnext" not in str(markata._pm.get_plugins()):
        markata._pm.register(importlib.import_module("markata.plugins.prevnext"))
        markata.hooks.append("markata.plugins.prevnext")
    if "slides" not in feeds_config.keys():
        feeds_config = {
            "slides": {
                "filter": '"slide" in post.keys()',
                "sort": 'post.get("slide", "")',
                "reverse": False,
            },
            **feeds_config,
        }
        markata.config["feeds"] = feeds_config


@hook_impl(trylast=True)
# @register_attr("articles")
def load(markata: "Markata") -> None:
    """
    split all articles into slides
    """
    for article in markata.articles:
        if article.get("slide", True):
            slide(markata, article)
