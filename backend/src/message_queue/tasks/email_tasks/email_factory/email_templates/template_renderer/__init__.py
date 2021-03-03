from abc import ABC, abstractmethod

import jinja2

from .. import script_path


class TemplateRenderer(ABC):
    @abstractmethod
    def _create_template_uri(self) -> str:
        pass

    def render(self, **render_vars) -> str:
        template_filename = self._create_template_uri()
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
        return environment.get_template(template_filename).render(render_vars)
