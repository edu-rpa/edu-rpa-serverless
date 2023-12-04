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

    # Check if the contour is a quadrilateral
    if len(approx) != 4:
        raise Exception('The object in the image is not a document or not a clear picture.')

    # Rearrange the order of the points in the contour to be clockwise from the top left
    src = np.zeros((4, 1, 2), dtype="float32")
    for i in range(4):
        src[i] = approx[i]   
    dst, size = infer_dst(src)
    src = rearrange(src)

    # Perform perspective transformation to flatten the document
    matrix = cv2.getPerspectiveTransform(src, dst)
    result = cv2.warpPerspective(image, matrix, size)

    return result

def infer_dst(src_pts):
    dst_pts = np.zeros((4, 2), dtype="float32")
    size = np.zeros((2), dtype="float32")
    
    max_x, min_x, max_y, min_y = get_max_min_x_y(src_pts)

    if max_x - min_x > max_y - min_y:
        dst_pts[0] = [0, 0]
        dst_pts[1] = [0, 600]
        dst_pts[2] = [800, 600]
        dst_pts[3] = [800, 0]
        size = (800, 600)
    else:
        dst_pts[0] = [0, 0]
        dst_pts[1] = [0, 800]
        dst_pts[2] = [600, 800]
        dst_pts[3] = [600, 0]
        size = (600, 800)
    
    return dst_pts, size

def rearrange(src_pts):
    result = np.zeros((4, 1, 2), dtype="float32")

    max_x, min_x, max_y, min_y = get_max_min_x_y(src_pts)
    rec_size = (max_x - min_x, max_y - min_y)

    for i in range(4):
        if min_x <= src_pts[i][0][0] <= min_x + rec_size[0] / 2:
            if min_y <= src_pts[i][0][1] <= min_y + rec_size[1] / 2:
                result[0][0] = src_pts[i][0]
            else:
                result[1][0] = src_pts[i][0]
        else:
            if min_y <= src_pts[i][0][1] <= min_y + rec_size[1] / 2:
                result[3][0] = src_pts[i][0]
            else:
                result[2][0] = src_pts[i][0]

    return result

def get_max_min_x_y(pts):
    max_x = max(pts[:, :, 0])
    min_x = min(pts[:, :, 0])
    max_y = max(pts[:, :, 1])
    min_y = min(pts[:, :, 1])
    return max_x, min_x, max_y, min_y
