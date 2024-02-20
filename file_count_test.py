import os




all_files = []
for root, dirs, files in os.walk("/home/ubuntu/OH/OH-Classifier-Framework-Basics/first_trimester_data/test"):
        file_paths = [os.path.join(root, file) for file in files]
        all_files.extend(file_paths)
        
        
        
print(len(all_files))