'''
This tool will multiple Android SDK API's and buildtools
NOTE: This process will take a while, and will take about 7 GB of storage space.

IMPORTANT NOTE! By using this tool, you agree to the License Agreement made by Google. The license agreement can be found
in the ANDROID_LICENSE_AGREEMENT.txt in the sdk folder
'''


import os, subprocess, glob


def main():
    start_tool()


def start_tool():
    unzip_sdk_tools()
    install_platforms_and_tools()


def unzip_sdk_tools():
    for file in glob.glob("*.zip"):
        call_string = "unzip " + str(file)
        subprocess.call(call_string, shell=True)
    os.chdir("tools/bin")


def sdkmanager_install(package):
    install_string = 'yes | ./sdkmanager ' + '\"' + package + '\"'
    package_name = package.split(";")[-1]
    print("I am now going to install %s, please be patient, this may take a while!" % (package_name))
    subprocess.call(install_string, shell=True)
    print("Installation of %s complete! Hooray!" % (package_name))


# Install Platform tools
def install_platforms_and_tools():
    sdkmanager_install("platform-tools")
    sdks_to_be_installed = ['platforms;android-28', 'platforms;android-27', 'platforms;android-26', 'platforms;android-25', 'platforms;android-24', 'platforms;android-23', 'platforms;android-22', 'platforms;android-21', 'platforms;android-20', 'platforms;android-19', 'platforms;android-18', 'platforms;android-17', 'platforms;android-16', 'platforms;android-15', 'platforms;android-14', 'platforms;android-13', 'platforms;android-12', 'platforms;android-11', 'platforms;android-10', 'platforms;android-9', 'platforms;android-8', 'platforms;android-7']
    build_tools_to_be_installed = ['build-tools;28.0.0-rc2', 'build-tools;28.0.0-rc1', 'build-tools;28.0.0', 'build-tools;27.0.3', 'build-tools;27.0.2', 'build-tools;27.0.1', 'build-tools;27.0.0', 'build-tools;26.0.3', 'build-tools;26.0.2', 'build-tools;26.0.1', 'build-tools;26.0.0', 'build-tools;25.0.3', 'build-tools;25.0.2', 'build-tools;25.0.1', 'build-tools;25.0.0', 'build-tools;24.0.3', 'build-tools;24.0.2', 'build-tools;24.0.1', 'build-tools;24.0.0', 'build-tools;23.0.3', 'build-tools;23.0.2', 'build-tools;23.0.1', 'build-tools;23.0.0', 'build-tools;22.0.1', 'build-tools;22.0.0', 'build-tools;21.1.1', 'build-tools;21.1.0', 'build-tools;21.0.2', 'build-tools;21.0.1', 'build-tools;21.0.0', 'build-tools;20.0.0', 'build-tools;19.1.0', 'build-tools;19.0.3', 'build-tools;19.0.2', 'build-tools;19.0.1', 'build-tools;19.0.0', 'build-tools;18.1.1', 'build-tools;18.1.0', 'build-tools;18.0.1', 'build-tools;17.0.0']

    for sdk in sdks_to_be_installed:
        sdkmanager_install(sdk)

    for bt in build_tools_to_be_installed:
        sdkmanager_install(bt)


if __name__ == '__main__':
    main()

