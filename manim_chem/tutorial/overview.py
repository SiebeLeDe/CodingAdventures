# Started from; https://docs.manim.community/en/stable/tutorials/quickstart.html#overview

from typing import Sequence

import manim as mm
import numpy as np
from numpy.typing import NDArray

AxisType = NDArray | Sequence[float] | float


class ThreeDSurfacePlot(mm.ThreeDScene):
    def construct(self):
        resolution_fa = 32
        self.set_camera_orientation(phi=70 * mm.DEGREES)

        size_box = 1

        def param_particle_in_box(u: float, v: float) -> NDArray:
            lx, ly = size_box, size_box  # Dimensions of the box
            nx, ny = 1, 1  # Quantum numbers
            x = u
            y = v
            z = np.sqrt(2 / lx) * np.sqrt(2 / ly) * np.sin(nx * np.pi * x / lx) * np.sin(ny * np.pi * y / ly)
            return np.array([x, y, z])

        particle_box_surface = mm.Surface(param_particle_in_box, resolution=(resolution_fa, resolution_fa), v_range=[0, size_box], u_range=[0, size_box], should_make_jagged=True)

        particle_box_surface.set_style(fill_opacity=1, stroke_color=mm.GREEN)
        particle_box_surface.set_fill_by_checkerboard([mm.ORANGE, mm.BLUE], opacity=0.5)
        axes = mm.ThreeDAxes(x_range=[-2, 2, 0.1], y_range=[-2, 2, 0.1], z_range=[-1, 1, 0.5])
        axes_labels = mm.VGroup(mm.MathTex("x").next_to(axes.x_axis, mm.UP), mm.MathTex("y").next_to(axes.y_axis, mm.LEFT), mm.MathTex("z").next_to(axes.z_axis, mm.OUT))
        self.add(axes, particle_box_surface, axes_labels)
        self.wait(4)
        # self.begin_ambient_camera_rotation(rate=-0.3)
        # self.wait(3)
