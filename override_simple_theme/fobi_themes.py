from fobi.base import theme_registry

from fobi.contrib.themes.bootstrap3.fobi_themes import Bootstrap3Theme

__all__ = ('JustSpacesTheme',)


class JustSpacesTheme(Bootstrap3Theme):
    """Overriding the "simple" theme for Just Spaces."""

    html_classes = ['my-simple-theme']
    base_template = 'override_simple_theme/base.html'

# It's important to set the `force` argument to True, in
# order to override the original theme. Force can be applied
# only once.
theme_registry.register(JustSpacesTheme, force=True)
