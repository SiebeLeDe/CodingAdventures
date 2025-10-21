# Started from; https://docs.manim.community/en/stable/tutorials/quickstart.html#overview

import manim as mm
import numpy as np


class ThreeDSurfacePlot(mm.ThreeDScene):
    def construct(self):
        resolution_fa = 40
        self.set_camera_orientation(phi=75 * mm.DEGREES, theta=-30 * mm.DEGREES)

        def param_gauss(u, v):
            x = u
            y = v
            sigma, mu = 0.4, [0.0, 0.0]
            d = np.linalg.norm(np.array([x - mu[0], y - mu[1]]))
            z = np.exp(-(d**2 / (2.0 * sigma**2)))
            return np.array([x, y, z])

        gauss_plane = mm.Surface(param_gauss, resolution=(resolution_fa, resolution_fa), v_range=[-2, +2], u_range=[-2, +2])

        gauss_plane.scale(2, about_point=mm.ORIGIN)
        gauss_plane.set_style(fill_opacity=1, stroke_color=mm.GREEN)
        gauss_plane.set_fill_by_checkerboard([mm.ORANGE, mm.BLUE], opacity=0.5)
        axes = mm.ThreeDAxes()
        self.begin_ambient_camera_rotation(rate=0.3)
        self.add(axes, gauss_plane)
        self.wait(3)
