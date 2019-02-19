from fobi.base import theme_registry

from fobi.contrib.themes.foundation5.fobi_themes import Foundation5Theme

__all__ = ('JustSpacesTheme',)


class JustSpacesTheme(Foundation5Theme):
    """Overriding the "simple" theme for Just Spaces."""

    html_classes = ['my-simple-theme']
    base_template = 'override_simple_theme/base.html'
    form_ajax = 'override_simple_theme/snippets/form_ajax.html'
    form_snippet_template_name = \
        'override_simple_theme/snippets/form_snippet.html'


# It's important to set the `force` argument to True, in
# order to override the original theme. Force can be applied
# only once.
theme_registry.register(JustSpacesTheme, force=True)
