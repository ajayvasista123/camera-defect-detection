import cv2
import numpy as np

def detect_defects(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load {image_path}")
        return

    # Load calibration data and undistort
    mtx = np.load('camera_matrix.npy')
    dist = np.load('distortion_coeffs.npy')
    h, w = img.shape[:2]
    newmtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    undistorted = cv2.undistort(img, mtx, dist, None, newmtx)

    # Convert to grayscale
    gray = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5,5), 0)

    # Edge detection
    edges = cv2.Canny(blurred, 30, 100)

    # Morphological operations to close gaps
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by area
    defects = [c for c in contours if 200 < cv2.contourArea(c) < 50000]

    # Draw results
    result = undistorted.copy()
    cv2.drawContours(result, defects, -1, (0, 0, 255), 2)

    for i, c in enumerate(defects):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(result, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(result, f'Defect {i+1}', (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    print(f"Image: {image_path}")
    print(f"Defects detected: {len(defects)}")

    cv2.imwrite(f'defect_output.jpg', result)
    print(f"Saved defect_output.jpg")
    return len(defects)

# Run on car damage images
import os
for img in ['../yolo_detection/car1.jpg', '../yolo_detection/car2.jpg', '../yolo_detection/car3.jpg']:
    if os.path.exists(img):
        detect_defects(img)
        break
EO
cat > detect_defects.py << 'EOF'
import cv2
import numpy as np

def detect_defects(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load {image_path}")
        return

    # Load calibration data and undistort
    mtx = np.load('camera_matrix.npy')
    dist = np.load('distortion_coeffs.npy')
    h, w = img.shape[:2]
    newmtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    undistorted = cv2.undistort(img, mtx, dist, None, newmtx)

    # Convert to grayscale
    gray = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5,5), 0)

    # Edge detection
    edges = cv2.Canny(blurred, 30, 100)

    # Morphological operations to close gaps
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by area
    defects = [c for c in contours if 200 < cv2.contourArea(c) < 50000]

    # Draw results
    result = undistorted.copy()
    cv2.drawContours(result, defects, -1, (0, 0, 255), 2)

    for i, c in enumerate(defects):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(result, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(result, f'Defect {i+1}', (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    print(f"Image: {image_path}")
    print(f"Defects detected: {len(defects)}")

    cv2.imwrite(f'defect_output.jpg', result)
    print(f"Saved defect_output.jpg")
    return len(defects)

# Run on car damage images
import os
for img in ['../yolo_detection/car1.jpg', '../yolo_detection/car2.jpg', '../yolo_detection/car3.jpg']:
    if os.path.exists(img):
        detect_defects(img)
        break
