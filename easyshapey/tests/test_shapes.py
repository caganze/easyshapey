"""
Tests for easyshapey shape classes.
"""
import numpy as np
import pandas as pd
import pytest
import copy
import easyshapey as shapey
from easyshapey.core import Polygon, BadVerticesFormatError


# Test data
np.random.seed(42)
x = np.random.random(100)
y = np.random.random(100)
df = pd.DataFrame([x, y]).transpose()
df.columns = ['x', 'y']


class TestBox:
    """Tests for Box class."""

    def test_box_creation(self):
        b = shapey.Box()
        b.data = df
        assert len(b) == len(x)

    def test_box_rotation(self):
        b1 = shapey.Box()
        b1.data = df
        b2 = copy.deepcopy(b1)
        b2.rotate(np.pi / 2)
        assert b2.angle != b1.angle

    def test_box_selection(self):
        b = shapey.Box()
        b.data = df
        selected = b.select(df)
        assert len(selected) <= len(df)

    def test_box_length_preserved(self):
        b1 = shapey.Box()
        b1.data = df
        b2 = copy.deepcopy(b1)
        b2.rotate(np.pi / 2)
        assert len(b1) == len(b2)


class TestPolygon:
    """Tests for Polygon class."""

    def test_triangle_creation(self):
        """Triangle has 3 sides."""
        tri = Polygon(vertices=[(0, 0), (1, 0), (0.5, 1)])
        assert tri.n_sides == 3
        assert len(tri) == 3

    def test_square_creation(self):
        """Square has 4 sides."""
        sq = Polygon(vertices=[(0, 0), (1, 0), (1, 1), (0, 1)])
        assert sq.n_sides == 4

    def test_pentagon_creation(self):
        """Pentagon from regular vertices."""
        angles = np.linspace(0, 2*np.pi, 6)[:-1]
        verts = [(np.cos(a), np.sin(a)) for a in angles]
        poly = Polygon(vertices=verts)
        assert poly.n_sides == 5

    def test_auto_close(self):
        """Polygon auto-closes if needed."""
        poly = Polygon(vertices=[(0, 0), (1, 0), (1, 1)])
        assert poly.vertices[0] == poly.vertices[-1]

    def test_minimum_vertices_error(self):
        """Error on < 3 vertices."""
        with pytest.raises(BadVerticesFormatError):
            Polygon(vertices=[(0, 0), (1, 0)])

    def test_empty_vertices_error(self):
        """Error on empty vertices."""
        with pytest.raises(BadVerticesFormatError):
            Polygon(vertices=[])

    def test_triangle_area(self):
        """Triangle area = 0.5 * base * height."""
        tri = Polygon(vertices=[(0, 0), (2, 0), (1, 2)])
        assert np.isclose(tri.area, 2.0, rtol=1e-5)

    def test_square_area(self):
        """Square area = side^2."""
        sq = Polygon(vertices=[(0, 0), (2, 0), (2, 2), (0, 2)])
        assert np.isclose(sq.area, 4.0, rtol=1e-5)

    def test_center_square(self):
        """Square center at (1, 1)."""
        sq = Polygon(vertices=[(0, 0), (2, 0), (2, 2), (0, 2)])
        assert np.allclose(sq.center, (1.0, 1.0), rtol=1e-5)

    def test_contains_inside(self):
        """Point (1, 1) inside square."""
        sq = Polygon(vertices=[(0, 0), (2, 0), (2, 2), (0, 2)])
        assert sq.contains([(1, 1)])[0] is True

    def test_contains_outside(self):
        """Point (5, 5) outside square."""
        sq = Polygon(vertices=[(0, 0), (2, 0), (2, 2), (0, 2)])
        assert sq.contains([(5, 5)])[0] is False

    def test_rotation_preserves_center(self):
        """Rotation keeps center fixed."""
        sq = Polygon(vertices=[(0, 0), (1, 0), (1, 1), (0, 1)])
        c1 = sq.center
        sq.rotate(np.pi / 2)
        assert np.allclose(sq.center, c1, rtol=1e-5)

    def test_rotation_no_inplace(self):
        """Rotation with set_vertices=False returns new vertices."""
        sq = Polygon(vertices=[(0, 0), (1, 0), (1, 1), (0, 1)])
        orig = sq.vertices[0]
        new_vs = sq.rotate(np.pi / 2, set_vertices=False)
        assert sq.vertices[0] == orig
        assert new_vs is not None

    def test_select_dataframe(self):
        """Select points from DataFrame."""
        sq = Polygon(vertices=[(0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)])
        test_df = pd.DataFrame({'x': [0.25, 0.75], 'y': [0.25, 0.75]})
        selected = sq.select(test_df)
        assert len(selected) == 1  # Only (0.25, 0.25) inside

    def test_select_numpy(self):
        """Select points from numpy array."""
        sq = Polygon(vertices=[(0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)])
        data = np.array([[0.25, 0.75], [0.25, 0.75]])
        selected = sq.select(data)
        assert selected.shape[1] == 1

    def test_n_sided_polygon(self):
        """Create N-sided regular polygons."""
        for n in [3, 4, 5, 6, 8, 10, 20]:
            angles = np.linspace(0, 2*np.pi, n + 1)[:-1]
            verts = [(np.cos(a), np.sin(a)) for a in angles]
            poly = Polygon(vertices=verts)
            assert poly.n_sides == n

    def test_color_property(self):
        """Color setter/getter."""
        poly = Polygon(vertices=[(0, 0), (1, 0), (0.5, 1)])
        poly.color = 'red'
        assert poly.color == 'red'

    def test_shapetype_property(self):
        """Shapetype setter/getter."""
        poly = Polygon(vertices=[(0, 0), (1, 0), (0.5, 1)])
        assert poly.shapetype == 'polygon'

    def test_empty_polygon(self):
        """Empty polygon has length 0."""
        poly = Polygon()
        assert len(poly) == 0
        assert poly.n_sides == 0
        assert poly.area == 0.0

    def test_xrange_yrange(self):
        """xrange and yrange set correctly."""
        poly = Polygon(vertices=[(1, 2), (5, 2), (5, 6), (1, 6)])
        assert poly.xrange == [1, 5]
        assert poly.yrange == [2, 6]

    def test_concave_polygon_area(self):
        """L-shape (concave) area = 3."""
        verts = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
        poly = Polygon(vertices=verts)
        assert np.isclose(poly.area, 3.0, rtol=1e-5)

    def test_from_data_bounding_box(self):
        """Create polygon from data bounding box."""
        data = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
        poly = Polygon.from_data(data, method='bounding_box')
        assert poly.n_sides == 4
        assert poly.xrange == [1, 5]


# Keep original test function for backwards compatibility
def test_box():
    b1 = shapey.Box()
    b1.data = df
    b2 = copy.deepcopy(b1)
    b2.rotate(np.pi / 2)
    b3 = copy.deepcopy(b1)
    assert len(b3.select(df)) < len(df)
    assert len(b1) == len(b2)
    assert b2.angle != b1.angle
