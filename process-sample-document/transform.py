import cv2
import numpy as np

def perspective_transform(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detector to find edges
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with four corners (assuming the document is the largest contour)
    largest_contour = max(contours, key=cv2.contourArea)

    # Approximate the contour to a quadrilateral
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Draw the contour on the original image
    cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)

    # Perform perspective transformation to flatten the document
    pts1 = np.float32(approx)
    pts2 = np.float32([[0, 0], [0, 600], [800, 600], [800, 0]])  # Size of the output image

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, matrix, (800, 600))  # Adjust the output size as needed

    return result
