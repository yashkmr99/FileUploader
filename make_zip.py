import zipfile, os
from zipfile import ZipFile

# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
 
    # setup file paths variable
    filePaths = []
   
    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
         
    # return all paths
    return filePaths

def do_zip(file_dir_arr, roll_num, dir_images):

    homedir = os.path.expanduser('~')

    # Call the function to retrieve all files and folders
    # of the assigned directory
    filePaths = retrieve_file_paths(dir_images)

    zip_obj = zipfile.ZipFile(roll_num+'.zip','w')

    # Writing log files to zip
    for file_upload in file_dir_arr:
        if(file_upload.startswith('homedir')):
            file_upload = homedir+file_upload.lstrip('homedir+')
        try:
            zip_obj.write(file_upload)
        except:
            print(file_upload+" not present")

    # Writing the submitted images to the zip
    with zip_obj:
        # writing each file one by one
        for file in filePaths:
            zip_obj.write(file)
            
    zip_obj.close()