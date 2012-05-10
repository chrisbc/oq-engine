# nhlib: A New Hazard Library
# Copyright (C) 2012 GEM Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Module :mod:`nhlib.geo.surface.planar` contains :class:`PlanarSurface`.
"""
import numpy

from nhlib.geo.surface.base import BaseSurface
from nhlib.geo.mesh import RectangularMesh
from nhlib.geo import geodetic
from nhlib.geo.nodalplane import NodalPlane


class PlanarSurface(BaseSurface):
    """
    Planar rectangular surface with two sides parallel to the Earth surface.

    :param mesh_spacing:
        The desired distance between two adjacent points in the surface mesh
        in both horizontal and vertical directions, in km.
    :param strike:
        Strike of the surface is the azimuth from ``top_left`` to ``top_right``
        points.
    :param dip:
        Dip is the angle between the surface itself and the earth surface.

    Other parameters are points (instances of :class:`~nhlib.geo.point.Point`)
    defining the surface corners in clockwise direction starting from top
    left corner. Top and bottom edges of the polygon must be parallel
    to earth surface and to each other.

    See :class:`~nhlib.geo.nodalplane.NodalPlane` for more detailed definition
    of ``strike`` and ``dip``. Note that these parameters are supposed
    to match the factual surface geometry (defined by corner points), but
    this is not enforced or even checked.

    :raises ValueError:
        If either top or bottom points differ in depth or if top edge
        is not parallel to the bottom edge, if top edge differs in length
        from the bottom one, or if mesh spacing is not positive.
    """
    #: The maximum angle between top and bottom edges for them
    #: to be considered parallel, in degrees.
    ANGLE_TOLERANCE = 0.1
    #: Maximum difference between lengths of top and bottom edges
    #: in kilometers.
    LENGTH_TOLERANCE = 1e-3

    def __init__(self, mesh_spacing, strike, dip,
                 top_left, top_right, bottom_right, bottom_left):
        super(PlanarSurface, self).__init__()
        if not (top_left.depth == top_right.depth
                and bottom_left.depth == bottom_right.depth):
            raise ValueError("top and bottom edges must be parallel "
                             "to the earth surface")

        top_azimuth = top_left.azimuth(top_right)
        bottom_azimuth = bottom_left.azimuth(bottom_right)
        azimuth_diff = abs(top_azimuth - bottom_azimuth)
        if azimuth_diff > 180:
            azimuth_diff = abs(360 - azimuth_diff)
        if not (azimuth_diff < self.ANGLE_TOLERANCE):
            raise ValueError("top and bottom edges must be parallel")

        top_length = top_left.distance(top_right)
        bottom_length = bottom_left.distance(bottom_right)
        if not abs(top_length - bottom_length) < self.LENGTH_TOLERANCE:
            raise ValueError("top and bottom edges must have "
                             "the same length")
        self.length = top_length

        if not mesh_spacing > 0:
            raise ValueError("mesh spacing must be positive")
        self.mesh_spacing = mesh_spacing

        NodalPlane.check_dip(dip)
        NodalPlane.check_strike(strike)
        self.dip = dip
        self.strike = strike

        # we don't need to check if left edge has the same length
        # as right one because previous checks guarantee that.
        self.width = top_left.distance(bottom_left)

        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left

    def _create_mesh(self):
        """
        See :meth:`nhlib.surface.base.BaseSurface._create_mesh`.
        """
        llons, llats, ldepths = geodetic.intervals_between(
            self.top_left.longitude, self.top_left.latitude,
            self.top_left.depth,
            self.bottom_left.longitude, self.bottom_left.latitude,
            self.bottom_left.depth,
            self.mesh_spacing
        )
        rlons, rlats, rdepths = geodetic.intervals_between(
            self.top_right.longitude, self.top_right.latitude,
            self.top_right.depth,
            self.bottom_right.longitude, self.bottom_right.latitude,
            self.bottom_right.depth,
            self.mesh_spacing
        )
        mlons, mlats, mdepths = [], [], []
        for i in xrange(len(llons)):
            lons, lats, depths = geodetic.intervals_between(
                llons[i], llats[i], ldepths[i], rlons[i], rlats[i], rdepths[i],
                self.mesh_spacing
            )
            mlons.append(lons)
            mlats.append(lats)
            mdepths.append(depths)
        return RectangularMesh(numpy.array(mlons), numpy.array(mlats),
                               numpy.array(mdepths))

    def get_strike(self):
        """
        Return strike value that was provided to the constructor.
        """
        return self.strike

    def get_dip(self):
        """
        Return dip value that was provided to the constructor.
        """
        return self.dip
