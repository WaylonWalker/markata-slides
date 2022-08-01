import copy
from pathlib import Path

import more_itertools
from frontmatter import Post
from markata.hookspec import hook_impl
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

md = (
     MarkdownIt()
     .use(front_matter_plugin)
     .use(footnote_plugin)
     .disable("image")
     .enable("table")
 )

keys = '''
<script>
document.onkeyup = function (e) {
    if (e.key === 'j') {
        document.querySelectorAll('a.prev')[0].click()
    }
    if (e.key === 'k') {
        document.querySelectorAll('a.next')[0].click()
    }
}
</script>
'''


def slide(markata, article):

    tokens = md.parse(article.content)
    breaks = [token.map[0] for token in tokens if token.tag == "h2" and token.type == "heading_open"]
    metadata = copy.deepcopy(article.metadata)
    if 'content' in metadata.keys():
        del metadata['content']
    base_path = article.get("slug", Path(article["path"]).stem)
    base_title = article.get("title", '')
    for i, b in enumerate(more_itertools.pairwise(breaks)):
        metadata['slug'] = base_path + f'/slide-{i}'
        metadata['title'] = base_title + f' | {i}'
        metadata['slide'] = f'{i}-{base_title}'
        post = Post('\n'.join(article.content.split('\n')[b[0]:b[1]]) + keys, **metadata)
        markata.articles.append(post)


@hook_impl(trylast=True)
# @register_attr("articles")
def load(markata: "MarkataMarkdown") -> None:
    for article in markata.articles:
        if article.get('slide', True):
            slide(markata, article)
