class ApiDrive(QApplication):
	def __init__(self):
        gauth = GoogleAuth()           
        drive = GoogleDrive(gauth) 

        upload_file_list = ['t.jpg']
        for upload_file in upload_file_list:
            gfile = drive.CreateFile()
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(upload_file)
            gfile.Upload() # Upload the file.