from ..component_generator.componentgenerator import ComponentGenerator
from ..compositor.compositor import Compositor
from ..compositor.gridcompositor import GridCompositor
from ..compositor.movingcompositor import MovingCompositor


class CompositorGenerator(ComponentGenerator):

    def __init__(self, config):
        super().__init__(config)

    def process(self, cs: dict) -> Compositor:
        cs_type = cs["type"]

        if cs_type == "grid_compositor":
            return GridCompositor.create_from_config(self.config)
        elif cs_type == "moving_compositor":
            return MovingCompositor.create_from_config(self.config)
        else:
            return Compositor(self.config)
