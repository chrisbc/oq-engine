# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2012-2018 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

from openquake.hazardlib.gsim.atkinson_boore_2003 import (
    AtkinsonBoore2003SInter,
    AtkinsonBoore2003SSlab,
    AtkinsonBoore2003SInterNSHMP2008,
    AtkinsonBoore2003SSlabNSHMP2008,
    AtkinsonBoore2003SSlabCascadiaNSHMP2008,
    AtkinsonBoore2003SSlabJapanNSHMP2008
)

from openquake.hazardlib.tests.gsim.utils import BaseGSIMTestCase

# Test data generated from OpenSHA implementation


class AtkinsonBoore2003SInterTestCase(BaseGSIMTestCase):
    GSIM_CLASS = AtkinsonBoore2003SInter

    def test_mean(self):
        self.check('AB03/AB03SInter_MEAN.csv',
                   max_discrep_percentage=0.1)

    def test_std_total(self):
        self.check('AB03/AB03SInter_STD_TOTAL.csv',
                   max_discrep_percentage=0.1)

    def test_std_intra(self):
        self.check('AB03/AB03SInter_STD_INTRA.csv',
                   max_discrep_percentage=0.1)

    def test_std_inter(self):
        self.check('AB03/AB03SInter_STD_INTER.csv',
                   max_discrep_percentage=0.1)


class AtkinsonBoore2003SSlabTestCase(BaseGSIMTestCase):
    GSIM_CLASS = AtkinsonBoore2003SSlab

    def test_mean(self):
        self.check('AB03/AB03SSlab_MEAN.csv',
                   max_discrep_percentage=0.1)

    def test_std_total(self):
        self.check('AB03/AB03SSlab_STD_TOTAL.csv',
                   max_discrep_percentage=0.1)

    def test_std_intra(self):
        self.check('AB03/AB03SSlab_STD_INTRA.csv',
                   max_discrep_percentage=0.1)

    def test_std_inter(self):
        self.check('AB03/AB03SSlab_STD_INTER.csv',
                   max_discrep_percentage=0.1)


class AtkinsonBoore2003SInterNSHMP2008TestCase(BaseGSIMTestCase):
    GSIM_CLASS = AtkinsonBoore2003SInterNSHMP2008
    # test data generated from subrutine 'getABsub' in 'hazSUBXnga.f'

    def test_mean(self):
        self.check('AB03/AB03SInterGlobalNSHMP_MEAN.csv',
                   max_discrep_percentage=0.5)

    def test_std_total(self):
        self.check('AB03/AB03SInterGlobalNSHMP_STD_TOTAL.csv',
                   max_discrep_percentage=0.1)


class AtkinsonBoore2003SSlabNSHMP2008TestCase(BaseGSIMTestCase):
    GSIM_CLASS = AtkinsonBoore2003SSlabNSHMP2008
    # test data generated from subrutine 'getABsub' in 'hazgridXnga2.f'

    def test_mean(self):
        self.check('AB03/AB03SSlabGlobalNSHMP_MEAN.csv',
                   max_discrep_percentage=0.3)

    def test_std_total(self):
        self.check('AB03/AB03SSlabGlobalNSHMP_STD_TOTAL.csv',
                   max_discrep_percentage=0.1)


class AtkinsonBoore2003SSlabCascadiaNSHMP2008TestCase(BaseGSIMTestCase):
    GSIM_CLASS = AtkinsonBoore2003SSlabCascadiaNSHMP2008
    # test data generated from subrutine 'getABsub' in 'hazgridXnga2.f'

    def test_mean(self):
        self.check('AB03/AB03SSlabCascadiaNSHMP_MEAN.csv',
                   max_discrep_percentage=0.2)

    def test_std_total(self):
        self.check('AB03/AB03SSlabCascadiaNSHMP_STD_TOTAL.csv',
                   max_discrep_percentage=0.1)


class AtkinsonBoore2003SSlabJapanNSHMP2008TestCase(BaseGSIMTestCase):
    GSIM_CLASS = AtkinsonBoore2003SSlabJapanNSHMP2008
    # Test data generated by applying increments from Table 3 to results for
    # Cascadia. Because of nonlinear effects the error was over 10%, but by
    # removing tests generating amplitdues over 0.25 g the error came down to
    # 0.15%. To be clear; the error was in the test vector not in the
    # implementation.

    def test_mean(self):
        self.check('AB03/AB03SSlabJapanNSHMP_MEAN.csv',
                   max_discrep_percentage=0.2)

    def test_std_total(self):
        self.check('AB03/AB03SSlabJapanNSHMP_STD_TOTAL.csv',
                   max_discrep_percentage=0.1)
