import cv2
import numpy as np
import glob

CHECKERBOARD = (9, 6)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = []
imgpoints = []

objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

images = glob.glob('checkerboard_images/*.jpg')
print(f"Found {len(images)} images")

successful = 0
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    if ret:
        successful += 1
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imwrite(f'detected_{successful}.jpg', img)
        print(f"Corners found in {fname}")
    else:
        print(f"Corners NOT found in {fname}")

print(f"\nSuccessful: {successful}/{len(images)}")

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

print(f"\n--- Camera Calibration Results ---")
print(f"RMS Reprojection Error: {ret:.4f} pixels")
print(f"\nCamera Matrix:\n{mtx}")
print(f"\nDistortion Coefficients:\n{dist}")

np.save('camera_matrix.npy', mtx)
np.save('distortion_coeffs.npy', dist)
print("\nCalibration data saved!")
