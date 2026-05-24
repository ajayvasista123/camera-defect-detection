import cv2
import numpy as np
import os

def detect_defects(image_path, output_name):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load {image_path}")
        return 0

    mtx = np.load('camera_matrix.npy')
    dist = np.load('distortion_coeffs.npy')
    h, w = img.shape[:2]
    newmtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    undistorted = cv2.undistort(img, mtx, dist, None, newmtx)

    gray = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blurred, 30, 100)
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    defects = [c for c in contours if 200 < cv2.contourArea(c) < 50000]

    result = undistorted.copy()
    cv2.drawContours(result, defects, -1, (0, 0, 255), 2)
    for i, c in enumerate(defects):
        x, y, w2, h2 = cv2.boundingRect(c)
        cv2.rectangle(result, (x,y), (x+w2, y+h2), (0,255,0), 2)
        cv2.putText(result, f'Defect {i+1}', (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    cv2.imwrite(output_name, result)
    print(f"{image_path} -> {len(defects)} defects detected -> saved {output_name}")
    return len(defects)

images = [
    ('../yolo_detection/car1.jpg', 'defect_car1.jpg'),
    ('../yolo_detection/car2.jpg', 'defect_car2.jpg'),
    ('../yolo_detection/car3.jpg', 'defect_car3.jpg'),
]

total = 0
for img_path, out_name in images:
    total += detect_defects(img_path, out_name)

print(f"\nTotal defects found across all images: {total}")
print("ALL DONE")
