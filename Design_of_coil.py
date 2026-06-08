""" Design of a planar coil """
""" This program is for the design of a planar coil, which gives XY points for CST."""
""" Polygonal curves function"""
""" Made by: Filip Dušek"""

# Importing libraries
import matplotlib.pyplot as plt


# Coil parameters (using units mm)
N = 35  # Number of turns
RW = 130/2  # Radius in width
RH = 90/2  # Radius in height

# Input parameters
X0 = 50  # X coordinate of the center
Y0 = 50  # Y coordinate of the center

Corner = 2

step = 4  # Step size for the points

Number_of_points = N*step+1  # Number of points for the coil + the center point
Distance_between_Xpoints = (RW/2)/N  # Distance between points in X direction
Distance_between_Ypoints =  (RH/2)/N  # Distance between points in Y direction
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
        # Formating to 4 decimal places (suitable for precise import into CST)
        f.write(f"{point[0]:.4f} {point[1]:.4f}\n")

print(f"Points were successfully exported to file: {output_file}")




""" Generate points for the square coil with corners """
""" ------------------------------------------------ """
""" ------------------------------------------------ """


pitchDistance_between_Xpoints = RW / N
pitchDistance_between_Ypoints = RH / N

print("Distance between turns X: ", pitchDistance_between_Xpoints)
print("Distance between turns Y: ", pitchDistance_between_Ypoints)

points = []
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Start precisely on the inner corner threshold
x, y = X0, Y0
points.append((x, y))

total_segments = N * step

for i in range(total_segments):
    curr_dir = i % 4
    next_dir = (i + 1) % 4
    
    dx, dy = directions[curr_dir]
    ndx, ndy = directions[next_dir]
    
    # Calculate the expansion multiplier for a perfectly concentric spiral
    turn_index = i // 4
    
    # Base symmetrical lengths starting from your X0/Y0 inner hole walls
    if curr_dir == 0:    # Going UP (+Y)
        side_length = (2 * Y0) + (turn_index * pitchDistance_between_Ypoints)
    elif curr_dir == 1:  # Going LEFT (-X)
        side_length = (2 * X0) + (turn_index * pitchDistance_between_Xpoints) + (0.5 * pitchDistance_between_Xpoints)
    elif curr_dir == 2:  # Going DOWN (-Y)
        side_length = (2 * Y0) + (turn_index * pitchDistance_between_Ypoints) + (0.5 * pitchDistance_between_Ypoints)
    else:                # Going RIGHT (+X)
        side_length = (2 * X0) + ((turn_index + 1) * pitchDistance_between_Xpoints)

    # Apply corner reductions to clear the intersections
    reduction = Corner if i == 0 else (2 * Corner)
    straight_length = side_length - reduction
    
    if straight_length < 0:
        straight_length = 0
 
    # 1. Point: End of straight segment
    x += dx * straight_length
    y += dy * straight_length
    points.append((x, y))
    
    # 2. Point: Symmetrical corner cut transition
    x += (dx + ndx) * Corner
    y += (dy + ndy) * Corner
    points.append((x, y))


# NEW: Center the points symmetrically around (0,0)

# Find the current boundaries (min and max) of the coil
x_coords = [p[0] for p in points]
y_coords = [p[1] for p in points]

min_x, max_x = min(x_coords), max(x_coords)
min_y, max_y = min(y_coords), max(y_coords)

# Calculate the geometric center (offset)
offset_x = (min_x + max_x) / 2
offset_y = (min_y + max_y) / 2

# Shift every point so the new center is exactly (0,0)
points = [(p[0] - offset_x, p[1] - offset_y) for p in points]


# PLOT
xpoints = [point[0] for point in points]
ypoints = [point[1] for point in points]

plt.figure(figsize=(7, 7))
plt.plot(xpoints, ypoints, '-x', color='blue', linewidth=1.5)
# Add a red dot at (0,0) to verify it's perfectly centered
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.axis('equal')
plt.legend()
plt.show()

# .Txt file export
output_file = "coil_points_corner.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for point in points:
        f.write(f"{point[0]:.4f} {point[1]:.4f}\n")

print(f"Points successfully exported to: {output_file}")