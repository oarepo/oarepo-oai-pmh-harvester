class ActionLinks:

    def __init__(self, actions_links):
        self._actions_links = actions_links

    def should_render(self, obj, ctx):
        """Determine if the link should be rendered."""
        return True

    @staticmethod
    def vars(obj, vars):
        """Subclasses can overwrite this method."""
        pass

    def expand(self, obj, context):
        """Expand the URI Template."""
        ret = {}
        for action, link in self._actions_links.items():
            if link.should_render(obj, context):
                ret[action] = link.expand(obj, context)
        return ret
