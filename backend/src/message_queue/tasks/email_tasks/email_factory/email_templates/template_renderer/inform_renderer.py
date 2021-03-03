from src.message_queue.tasks.email_tasks.email_factory.email_templates.template_renderer import TemplateRenderer


class InformTemplateRenderer(TemplateRenderer):
    def _create_template_uri(self) -> str:
        return '/inform_template.html'

    def render(self, **render_vars) -> str:
        inform_render_vars = dict()
        inform_render_vars['name'] = render_vars.get('name', 'Name here')
        inform_render_vars['content'] = render_vars.get('content', 'To be or not to be')
        return super(InformTemplateRenderer, self).render(**inform_render_vars)
