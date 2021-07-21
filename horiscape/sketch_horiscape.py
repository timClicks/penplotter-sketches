import itertools

import numpy as np
import vpype as vp
import vsketch
from shapely.geometry import MultiLineString, Point, Polygon
from shapely.ops import unary_union


class HLineSketch(vsketch.SketchClass):
    page_size = vsketch.Param("a4", choices=vp.PAGE_FORMATS.keys())
    number_of_circles = vsketch.Param(15, 0)
    margin = vsketch.Param(15, 0, unit="mm")
    base_pitch = vsketch.Param(3.0, unit="mm")
    min_radius = vsketch.Param(10.0, unit="mm")
    max_radius = vsketch.Param(50, unit="mm")

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(self.page_size)

        width = round((vsk.width - 2 * self.margin) / self.base_pitch) * self.base_pitch
        height = round((vsk.height - 2 * self.margin) / self.base_pitch) * self.base_pitch

        mls0 = MultiLineString(
            [
                [(0, y), (width, y)]
                for y in np.arange(0, height + self.base_pitch, self.base_pitch)
            ]
        )
        mls1 = MultiLineString(
            [
                [(0, y), (width, y)]
                for y in np.arange(self.base_pitch / 2, height, self.base_pitch)
            ]
        )
        mls2 = MultiLineString(
            [
                [(0, y), (width, y)]
                for y in np.arange(self.base_pitch / 6, height, self.base_pitch / 4)
            ]
        )

        mls3 = MultiLineString(
            [
                [(0, y), (width, y)]
                for y in np.arange(self.base_pitch / 12, height, self.base_pitch / 8)
            ]
        )

        # build a separation
        yy = np.linspace(0, height, 100)
        xx = np.array([vsk.noise(y * 0.0051) for y in yy]) * width / 5.4 + 3 * width / 5 - 90
        p1 = Polygon(list(zip(xx, yy)) + [(width, height), (width, 0)])

        # page = Polygon([(0,0), (height,0), (width,height), (0, width)])
        vsk.geometry(mls0)

        circles = []
        for _ in range(self.number_of_circles):
            circle = Point(vsk.random(0, width), vsk.random(0, height)).buffer(
                vsk.random(self.min_radius, self.max_radius)
            )
            circles.append(circle)

        circles2 = []
        for _ in range(int(self.number_of_circles / 3)):
            circle = Point(vsk.random(0, width), vsk.random(0, height)).buffer(
                vsk.random(self.min_radius, self.max_radius)
            )
            circles2.append(circle)

        all_geom = circles + [p1]
        itrsct = unary_union(
            [a.intersection(b) for a, b in itertools.combinations(all_geom, 2)]
        )
        vsk.geometry(mls1.intersection(unary_union(all_geom)))
        vsk.geometry(mls2.intersection(itrsct))
        vsk.geometry(mls3.intersection(unary_union(circles2)))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    HLineSketch.display()
