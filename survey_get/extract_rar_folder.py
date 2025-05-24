import rarfile

# Set unrar path manually if needed
rarfile.UNRAR_TOOL = "/usr/bin/unrar"  # Replace 'yourusername' with your PythonAnywhere username

# Open the RAR file
rar = rarfile.RarFile("survey.rar")
rar.extractall("survey_output_folder")  # Extract to 'output_folder'
print("Extraction complete!")
