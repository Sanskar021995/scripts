# import pydicom
# import os
# import cv2
# all_files = []
# for root, dirs, files in os.walk("/home/ubuntu/OH/pixel-resolution-package/DICOM"):
#         file_paths = [os.path.join(root, file) for file in files]
#         all_files.extend(file_paths)
        
# def get_file_size(file_path):
#     size_in_bytes = os.path.getsize(file_path)
#     size_in_kb = size_in_bytes / 1024
#     return size_in_kb



# path = "/home/ubuntu/OH/testing_data/all_files/"
# for i in range(4):
#     dicom_data = pydicom.dcmread(all_files[i])
#     dicom_image = dicom_data.pixel_array
#     if get_file_size(all_files[i]) > 1000:
#                     continue
    
#     name =  all_files[i].split(".")[0].split("/")[-1] + ".png"
#     name = path +name
#     cv2.imwrite(name, dicom_image) 
#     print(i)


    
import cv2
import numpy as np

# Load the image in grayscale
image = cv2.imread('/home/ubuntu/OH/testing_data/all_files/3a6b7f8a-e2ad-43f6-9dd6-75b21cd91b92.png', cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur to reduce noise
# Apply Laplacian edge detector
laplacian = cv2.Laplacian(image, cv2.CV_64F)
edges = cv2.Canny(image, 120, 250)


kernel = np.ones((3, 3), np.uint8)

# Perform morphological opening
opening = cv2.morphologyEx(laplacian, cv2.MORPH_OPEN, kernel)



# Convert back to 8-bit unsigned integer format
laplacian_uint8 = np.uint8(np.absolute(laplacian))

# Display the original and Laplacian images
cv2.imshow('Original Image', image)
cv2.imshow('Laplacian Edges', laplacian_uint8)

# Wait for any key press to exit
cv2.waitKey(0)
cv2.destroyAllWindows()
        