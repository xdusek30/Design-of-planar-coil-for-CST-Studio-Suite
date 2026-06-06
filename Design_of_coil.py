""" Design of a planar coil """
""" This program is for the design of a planar coil, which gives XY points for CST."""
""" Polygonal curves function"""
""" Made by: Filip Dušek"""

# Importing libraries
import matplotlib.pyplot as plt


# Coil parameters (using units mm)
N = 20  # Number of turns
RW = 150  # Radius in width
RH = 120  # Radius in height

# Input parameters
X0 = 0  # X coordinate of the center
Y0 = 0  # Y coordinate of the center

Corner = 2

step = 4  # Step size for the points

Number_of_points = N*step+1  # Number of points for the coil + the center point
Distance_between_Xpoints = RW/N  # Distance between points in X direction
Distance_between_Ypoints =  RH/N  # Distance between points in Y direction
print("Number of points: ", Number_of_points)
print("Distance between points in X direction: ", Distance_between_Xpoints)
print("Distance between points in Y direction: ", Distance_between_Ypoints)

""" Generate points for the square coil """
""" ----------------------------------- """
""" ----------------------------------- """
points = []
NX = 0  # Counter for X direction
NY = 0  # Counter for Y direction
for i in range(Number_of_points):
    if i == 0:
        x = X0 
        y = Y0
    elif i > 0 and i % 2 == 1:  # Odd points (Y direction)
        if NY % 2 == 0:  # Even Y points
            y = abs(y) + Distance_between_Ypoints
        else:
            y = -1*(y)
        x = x
        NY += 1

    elif i > 0 and i % 2 == 0:  # Even points (X direction)
        if NX % 2 == 0:  # Even X points
            x = abs(x) + Distance_between_Xpoints
        else:
            x = -1*(x)
        y = y
        NX += 1
    points.append((x, y))


xpoints = [point[0] for point in points]
ypoints = [point[1] for point in points]

plt.figure(figsize=(7, 7))
plt.plot(xpoints, ypoints, '-x', color='blue', linewidth=1.5, label='Planar Coil')
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.axis('equal')
plt.legend()
plt.show()

output_file = "coil_points.txt"

# Writing points to the output file
with open(output_file, "w", encoding="utf-8") as f:
    for point in points:
        # Formátování na 4 desetinná místa (vhodné pro přesný import do CST)
        f.write(f"{point[0]:.4f} {point[1]:.4f}\n")

print(f"Body byly úspěšně exportovány do souboru: {output_file}")




""" Generate points for the square coil with corners """
""" ------------------------------------------------ """
""" ------------------------------------------------ """
pitchDistance_between_Xpoints = RW / N
pitchDistance_between_Ypoints = RH / N

print("Vzdálenost mezi závity X: ", pitchDistance_between_Xpoints)
print("Vzdálenost mezi závity Y: ", pitchDistance_between_Ypoints)

points = []

# Spirála začíná ve středu
x, y = X0, Y0
points.append((x, y))

points = []
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Total segmets
total_segments = N * step

for i in range(total_segments):
    # Defining current and next direction based on the segment index
    curr_dir = i % 4
    next_dir = (i + 1) % 4
    
    dx, dy = directions[curr_dir]
    ndx, ndy = directions[next_dir]
    
    # Calculate the length of the current segment. The length increases with each turn of the spiral
    if curr_dir in [0, 2]:  # Pohyb po ose X
        side_length = (i // 2 + 1) * (pitchDistance_between_Xpoints)
    else:                   # Pohyb po ose Y
        side_length = (i // 2 + 1) * (pitchDistance_between_Ypoints)
    
    # Subtract the corner length from the straight segment. For the first segment, we only subtract one corner length, for subsequent segments we subtract two (the start and end of the segment)
    reduction = Corner if i == 0 else (2 * Corner)
    straight_length = side_length - reduction
 
    # 1. Point: End of the straight segment 
    x += dx * straight_length
    y += dy * straight_length
    points.append((x, y))
    
    # 2. Point: Actual corner rounding (transition to new direction)
    x += (dx + ndx) * Corner
    y += (dy + ndy) * Corner
    points.append((x, y))

# PLOT
xpoints = [point[0] for point in points]
ypoints = [point[1] for point in points]

plt.figure(figsize=(7, 7))
plt.plot(xpoints, ypoints, '-x', color='blue', linewidth=1.5, label='Planar Coil with Corners')
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.axis('equal')
plt.legend()
plt.show()

# .Txt file export
output_file = "coil_points_corner.txt"

# Writing points to the output file
with open(output_file, "w", encoding="utf-8") as f:
    for point in points:
        # Formátování na 4 desetinná místa (vhodné pro přesný import do CST)
        f.write(f"{point[0]:.4f} {point[1]:.4f}\n")

print(f"Body byly úspěšně exportovány do souboru: {output_file}")