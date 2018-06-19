*-----------------------------------------------------------------------------------------------------------------*
INSTRUCTIONS FOR sdk_installer.py

This tool is used in preparation for the Infer analysis experiment. Infer requires SDKs to be installed for the capture phase. Since many repositories contain different versions of the SDK APIs or build-tools, this tool can help to save time by installing all known APIs and build-tools up front.
NOTE: this tool was developed using SDK Tools 26.1.1 as a framework. Its functionality on newer or older versions is unknown.
IMPORTANT NOTE: By using this tool, you agree to the License Agreement made by Google. The license agreement can be found in the ANDROID_LICENSE_AGREEMENT.txt in the sdk folder

INSTRUCTIONS:
1. Download the SDK Tools from the official website. It can be found at https://developer.android.com/studio/ under the header "Command line tools only". Select either the Mac or Linux version for your OS.
2. Move the zip file to the "sdk" folder in SP2. Do not unzip it yet. Make sure it is the only zip file in sdk
3. Run sdk_installer.py : On the command line, navigate to the SP2 folder and use the following command: python3 sdk_installer.py

The tool will then proceed to install all defined platforms and build-tools. This might take a while depending on Download speed, and it will take at least 7GB of storage space.

This tool will download all platforms and build-tools available on 19-06-2018. When more platforms are added in the future, they can also be added to this tool.

Here are the instructions to do this:
1. Navigate to sdk/tools/bin
2. Execute the command: ./sdkmanager --list
3. Identify all newer platforms than 'platforms;android-28' and all newer build-tools than 'build-tools;28.0.0-rc2'
4. Copy the new platforms and paste them in the array sdks_to_be_installed in sdk_installer.py. The string should have the format "platforms;android-xx"
5. Copy the new build-tools and paste them in the array build_tools_to_be_installed in sdk_installer.py. The string should have the format "build-tools;xx.x.x"
6. Rerun sdk_installer.py
