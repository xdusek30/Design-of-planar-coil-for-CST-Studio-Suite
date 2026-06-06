# Planar Coil Design Tool for CST Studio Suite

This Python program generates coordinate data for geometric planar coils (spirals), optimized for direct path import into electromagnetic simulation software such as **CST Studio Suite**. 

It provides two methods for calculating coil geometry:
1. **Standard Rectangular/Square Planar Coil:** Sharp alternating horizontal and vertical segments extending outward from a central point.
2. **Planar Coil with Chamfered/Rounded Corners:** Incorporates a customizable corner mitigation offset (`Corner`) to reduce geometric discontinuities and structural simulation issues.

---

## Features

- **Custom Geometry Configuration:** Control total turns, width radius, height radius, and starting center coordinates.
- **Corner Mitigation:** Smooths out sharp 90-degree transitions to optimize high-frequency or high-current layout structures.
- **Visual Validation:** Generates visual 2D interactive plots using `matplotlib` to verify the trajectory before exporting.
- **CST-Ready Export:** Formats and exports data points directly into structured `.txt` files with 4-decimal precision suitable for curve/polygon imports.

---

## Configuration Variables

You can adjust the parameters directly in the script header:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `N` | Integer | `20` | Total number of spiral turns |
| `RW` | Float / Int | `150` | Full width radius of the coil (in mm) |
| `RH` | Float / Int | `120` | Full height radius of the coil (in mm) |
| `X0`, `Y0` | Float / Int | `0`, `0` | Center coordinates of the coil origin |
| `Corner` | Float / Int | `2` | Linear subtraction dimension applied to corners for chamfering |
| `step` | Integer | `4` | Geometric segments per single complete rotation loop |

---

## Output Files

The script automatically generates two text files containing the coordinate matrices `(X, Y)` formatted to four decimal places:

1. **`coil_points.txt`**: Coordinates representing the sharp standard square/rectangular spiral path.
2. **`coil_points_corner.txt`**: Coordinates representing the geometric path modified with the corner parameter.

## Requirements
Ensure you have a Python 3.x environment with the following dependencies installed:
- pip install numpy matplotlib


### Export Format Example:
```text
0.0000 0.0000
3.5000 0.0000
3.5000 4.0000
-3.5000 4.0000
...
