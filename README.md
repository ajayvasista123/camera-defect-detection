Camera Calibration and Surface Defect Detection

OpenCV pipeline for camera calibration and automated defect detection on vehicle surfaces.

What it does:
- Camera calibration using checkerboard pattern
- Computes camera matrix and distortion coefficients with 0.52 pixel reprojection error
- Undistorts images using calibration data
- Detects surface anomalies using edge detection and contour analysis
- Highlights defect regions with bounding boxes

Pipeline:
Raw image - Undistort - Grayscale - Blur - Edge detection - Contour analysis - Output

Results:
- Calibration RMS error: 0.5189 pixels
- Defects detected across 3 damaged car images: 4 total regions

Stack: Python, OpenCV, NumPy, Linux
