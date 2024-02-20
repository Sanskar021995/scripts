import os
import pydicom


all_files = []
for root, dirs, files in os.walk("/home/ubuntu/OH/pixel-resolution-package/DICOM"):
    file_paths = [os.path.join(root, file) for file in files]
    all_files.extend(file_paths)
    
def get_file_size(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_kb = size_in_bytes / 1024
    return size_in_kb

   
    
    
maufacturer_dict = {}
i = 0
for dicom_file in all_files:
    
    
    if get_file_size(dicom_file) > 1000:
                    i=i+1
                    continue
                
                
    print(i)
    dicom_data = pydicom.dcmread(dicom_file)
    dicom_image = dicom_data.pixel_array            
    
    manufacturer = dicom_data.Manufacturer
    maufacturer_dict[manufacturer] = 1+ maufacturer_dict.get(manufacturer, 0)
    i=i+1
    
    
print(maufacturer_dict)