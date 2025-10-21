# Started from; https://docs.manim.community/en/stable/tutorials/quickstart.html#overview

import manim as mm
import numpy as np


class ThreeDSurfacePlot(mm.ThreeDScene):
    def construct(self):
        resolution_fa = 40
        self.set_camera_orientation(phi=75 * mm.DEGREES, theta=-30 * mm.DEGREES)

        def param_particle_in_box(u, v):
            nx, ny = 1, 1  # Quantum numbers
            width, length = 2, 2  # Dimensions of the box
            x = u
            y = v
            z = np.sin(nx * np.pi * x / width) * np.sin(ny * np.pi * y / length)
            return np.array([x, y, z])

        particle_box_surface = mm.Surface(param_particle_in_box, resolution=(resolution_fa, resolution_fa), v_range=[0, 2], u_range=[0, 2])

        particle_box_surface.scale(2, about_point=mm.ORIGIN)
        particle_box_surface.set_style(fill_opacity=1, stroke_color=mm.GREEN)
        particle_box_surface.set_fill_by_checkerboard([mm.ORANGE, mm.BLUE], opacity=0.5)
        axes = mm.ThreeDAxes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.2])
        self.begin_ambient_camera_rotation(rate=0.7)
        self.add(axes, particle_box_surface)
        self.wait(3)
