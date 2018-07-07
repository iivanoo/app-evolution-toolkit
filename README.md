# app-evolution-toolkit

For installing the Python dependencies a requirements.txt is included in the repository. The dependencies can be installed using the package manager pip:

pip3 install -r requirements.txt

For installing the Android SDK’s, Build-tools and platform tools (normally included in the Android Studio installation), simply run the sdk_installer.py script included in the repository.

The repositories to be analysed can be manually cloned or moved to the repo_subfolder.

The static analysis tool can be changed by changing out the static_analyzer_success variable. The output will need to be the same as the format used with Infer.
- The output should be a .csv outputted in the folder repo_subfolder/<author> in the following format: <repository_name>_<commit_index>.csv.
- The data of the csv itself that is outputted should be the following strings per line:  ID, BUG_TYPE, FILE_PATH, LINE_NUMBER, BUG_DESCRIPTION

Then main.py can be run