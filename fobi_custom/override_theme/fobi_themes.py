from fobi.base import theme_registry

from fobi.contrib.themes.foundation5.fobi_themes import Foundation5Theme

__all__ = ('JustSpacesTheme',)


class JustSpacesTheme(Foundation5Theme):
    """Overriding the Foundation5 theme for Just Spaces."""

    html_classes = ['override-theme']
    base_template = 'override_theme/base.html'
    edit_form_entry_ajax_template = 'override_theme/edit_form_entry_ajax.html'
    form_snippet_template_name = 'override_theme/snippets/form_snippet.html'
    edit_form_element_entry_template = 'override_theme/edit_form_element_entry.html'
    form_ajax = 'override_theme/snippets/form_ajax.html'
    form_entry_submitted_ajax_template = 'override_theme/form_entry_submitted_ajax.html'
    add_form_element_entry_ajax_template = 'override_theme/add_form_element_entry_ajax.html'


# It's important to set the `force` argument to True, in
# order to override the original theme. Force can be applied
# only once.
theme_registry.register(JustSpacesTheme, force=True)
