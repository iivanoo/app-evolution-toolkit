import os, subprocess, timeit
os.chdir("sdk")
subprocess.call("unzip sdk-tools-darwin-4333796.zip", shell=True)
os.chdir("tools/bin")

def sdkmanager_install(package):
    install_string = 'yes | ./sdkmanager ' + '\"' + package + '\"'
    package_name = package.split(";")[-1]
    print("I am now going to install %s, please be patient, this may take a while!" % (package_name))
    subprocess.call(install_string, shell=True)
    print("Installation of %s complete! Hooray!" % (package_name))

# Install Platform tools
start_time = timeit.default_timer()
sdkmanager_install("platform-tools")
sdks_to_be_installed = ['platforms;android-28', 'platforms;android-27', 'platforms;android-26', 'platforms;android-25', 'platforms;android-24', 'platforms;android-23', 'platforms;android-22', 'platforms;android-21', 'platforms;android-20', 'platforms;android-19', 'platforms;android-18', 'platforms;android-17', 'platforms;android-16', 'platforms;android-15', 'platforms;android-14', 'platforms;android-13', 'platforms;android-12', 'platforms;android-11', 'platforms;android-10', 'platforms;android-9', 'platforms;android-8', 'platforms;android-7']
build_tools_to_be_installed = ['build-tools;28.0.0-rc2', 'build-tools;28.0.0-rc1', 'build-tools;28.0.0', 'build-tools;27.0.3', 'build-tools;27.0.2', 'build-tools;27.0.1', 'build-tools;27.0.0', 'build-tools;26.0.3', 'build-tools;26.0.2', 'build-tools;26.0.1', 'build-tools;26.0.0', 'build-tools;25.0.3', 'build-tools;25.0.2', 'build-tools;25.0.1', 'build-tools;25.0.0', 'build-tools;24.0.3', 'build-tools;24.0.2', 'build-tools;24.0.1', 'build-tools;24.0.0', 'build-tools;23.0.3', 'build-tools;23.0.2', 'build-tools;23.0.1', 'build-tools;23.0.0', 'build-tools;22.0.1', 'build-tools;22.0.0', 'build-tools;21.1.1', 'build-tools;21.1.0', 'build-tools;21.0.2', 'build-tools;21.0.1', 'build-tools;21.0.0', 'build-tools;20.0.0', 'build-tools;19.1.0', 'build-tools;19.0.3', 'build-tools;19.0.2', 'build-tools;19.0.1', 'build-tools;19.0.0', 'build-tools;18.1.1', 'build-tools;18.1.0', 'build-tools;18.0.1', 'build-tools;17.0.0']

for sdk in sdks_to_be_installed:
    sdkmanager_install(sdk)

for bt in build_tools_to_be_installed:
    sdkmanager_install(bt)

end_time = timeit.default_timer()

time_spent = end_time - start_time

print("Time spent installing Android necessities: " + str(time_spent))

