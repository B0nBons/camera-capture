import cv2
import numpy as np
# Import the libraries
# To install opencv, run "pip install opencv-python"
# TODO: Test if this can run at all on a raspi
# TODO: Figure out rare cases of abnormal behavior

# Open the camera
# NOTE: You will likely need to change the camera number, as it varies from device to device
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame so its an actual representation
    frame = cv2.flip(frame, 1)

    # HSV is better for colour detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red is hard to define in HSV, so two ranges are used
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    # Mask: areas that are red for debgging purposes
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Split the frame into a 3x3 grid
    h, w, garbage = frame.shape
    cell_h = h // 3
    cell_w = w // 3

    red_count = 0
    total_cells = 9

    for row in range(3):
        for col in range(3):
            # Coordinates for the cell
            x1, y1 = col * cell_w, row * cell_h
            x2, y2 = (col + 1) * cell_w, (row + 1) * cell_h

            # Extract that cell from the mask
            cell_mask = mask[y1:y2, x1:x2]

            # Calculate how much of the cell is red
            red_ratio = cv2.countNonZero(cell_mask) / (cell_mask.size)

            # If more than 60% of this cell is red, count it as "red"
            if red_ratio > 0.6:
                red_count += 1
                color = (0, 0, 255)  # red rectangle if 60% of the box is red
            else:
                color = (255, 255, 255)  # white rectangle otherwise

            # Draw a rectangle around each grid cell
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # End program if all the squares are red
    if red_count == total_cells:
        print("Red has been detected in every box, now ending.")
        break

    # Show what the camera is detecting
    # Would recommend having both views side by side
    cv2.imshow("Camera", frame)
    cv2.imshow("Red Detected", mask)

    # Press 'q' to quit manually (if program is behaving abnormal)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

