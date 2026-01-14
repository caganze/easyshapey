# easyshapey

[![PyPI version](https://badge.fury.io/py/easyshapey.svg)](https://pypi.org/project/easyshapey/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tool for manipulating 2D shapes in plots. Select data points, create arbitrary polygons, and visualize shapes on matplotlib axes.

## Installation

```bash
pip install easyshapey
```

Or from source:

```bash
pip install git+https://github.com/caganze/easyshapey.git
```

## Features

- **Box**: Rectangular shapes fitted to data trends
- **RotatedBox**: Auto-rotated boxes minimizing bounding area
- **Oval**: Elliptical shapes fitted to data
- **Polygon**: Arbitrary N-sided polygons (triangles to any N)

All shapes support:
- Data point selection (`select()`)
- Point containment checking (`contains()`)
- Rotation (`rotate()`)
- Plotting on matplotlib axes (`plot()`)

## Quick Start

### Box

```python
import numpy as np
import pandas as pd
from easyshapey import Box

# Create data
x = np.random.random(100)
y = 2 * x + np.random.normal(0, 0.2, 100)
data = np.array([x, y])

# Fit box to data
box = Box()
box.data = data

# Select points inside
selected = box.select(data)

# Plot
box.plot()
```

### Polygon

```python
from easyshapey import Polygon

# Create triangle
tri = Polygon(vertices=[(0, 0), (1, 0), (0.5, 1)])
print(f"Sides: {tri.n_sides}, Area: {tri.area:.2f}")

# Create any N-sided polygon
hexagon = Polygon(vertices=[
    (1, 0), (0.5, 0.87), (-0.5, 0.87),
    (-1, 0), (-0.5, -0.87), (0.5, -0.87)
])

# Check point containment
inside = tri.contains([(0.5, 0.3)])  # [True]

# Rotate 45 degrees
tri.rotate(np.pi / 4)
```

### Interactive Polygon Creation

```python
from easyshapey import Polygon

# Click points on figure, press 'q' when done
poly = Polygon.from_clicks(min_points=3)
```

#### Using `from_clicks()` in Jupyter Notebooks

The interactive `from_clicks()` method requires an interactive matplotlib backend. The default `inline` backend renders static images and won't capture mouse clicks.

**Step 1:** Restart your kernel and use an interactive backend as the first command:

```python
# Use ONE of these (before any other matplotlib imports):
%matplotlib tk       # Opens separate window (recommended)
%matplotlib macosx   # macOS native backend
```

**Step 2:** Create your plot and click to define polygon vertices:

```python
import matplotlib.pyplot as plt
import numpy as np
from easyshapey import Polygon

x = np.random.rand(100)
y = 2*x + 0.3*np.random.randn(100)

fig, ax = plt.subplots()
ax.scatter(x, y)

# Click points on the figure, press 'q' when done
poly = Polygon.from_clicks(ax=ax)
```

**Step 3:** Display the result inline:

```python
%matplotlib inline

fig, ax = plt.subplots()
ax.scatter(x, y, alpha=0.7)
poly.plot(ax=ax, color='lightblue')
plt.show()
```

> ⚠️ **Important:** Always press **'q'** to finish selecting points. Do not close the figure window by clicking the X button, as this may crash the Jupyter kernel on some systems.

### Polygon from Data

```python
from easyshapey import Polygon
import numpy as np

data = np.random.rand(2, 50)  # 50 random points

# Bounding box
bbox = Polygon.from_data(data, method='bounding_box')

# Convex hull (requires scipy)
hull = Polygon.from_data(data, method='convex_hull')
```

### Selector

```python
from easyshapey import Box, Selector

# Combine multiple shapes
box1 = Box()
box1.data = data1

box2 = Box()
box2.data = data2

selector = Selector()
selector.shapes = [box1, box2]
selector.logic = 'and'  # or 'or'

# Select points in all shapes
result = selector.select()
```

## API Reference

### Polygon

| Property | Description |
|----------|-------------|
| `n_sides` | Number of sides |
| `vertices` | List of (x, y) tuples |
| `center` | Centroid (x, y) |
| `area` | Area (shoelace formula) |
| `angle` | First edge angle (radians) |

| Method | Description |
|--------|-------------|
| `contains(points)` | Check if points inside |
| `select(data)` | Select data points inside |
| `rotate(angle)` | Rotate around center |
| `plot(**kwargs)` | Plot on matplotlib axes |
| `from_clicks()` | Create interactively |
| `from_data()` | Create from data points |

### Box

| Property | Description |
|----------|-------------|
| `vertices` | Corner vertices |
| `center` | Center (x, y) |
| `area` | Bounding area |
| `coeffs` | Fitted line [slope, intercept] |

## Examples

See the [tutorial notebook](https://github.com/caganze/easyshapey/blob/master/examples/tutorial.ipynb) for more examples.

---

## Changelog

### [0.0.4] - 2025-01-07

**Added**
- Polygon class: arbitrary N-sided 2D polygons
- Interactive creation via `Polygon.from_clicks()`
- Data fitting via `Polygon.from_data()`
- Comprehensive test suite

**Changed**
- Streamlined code following [Abseil performance principles](https://abseil.io/fast/hints.html)
- Consistent NumPy-style docstrings
- ~40% leaner implementation

### [0.0.3] - 2025-01-07

**Security**
- Fixed deprecated pandas `.ix[]` with `.loc[]`
- Updated security policy

### [0.0.2] - 2022-05-04

- Version bump and package updates

### [0.0.1] - 2022-01-27

- Initial release

---

## Security

**Supported Versions**

| Version | Supported |
|---------|-----------|
| 0.0.4   | ✓ |
| 0.0.3   | ✓ |
| < 0.0.3 | ✗ |

**Reporting Vulnerabilities**

Email: caganze@gmail.com

Include: description, reproduction steps, impact, suggested fix.

Response time: 48 hours acknowledgment, 7 days initial assessment.

---

## License

MIT License

## Author

caganze - caganze@gmail.com

## Links

- [PyPI](https://pypi.org/project/easyshapey/)
- [GitHub](https://github.com/caganze/easyshapey)
