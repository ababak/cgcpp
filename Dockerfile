# escape=`
#
# Author:
# Andriy Babak <ababak@gmail.com>
#
# Build the docker image:
# docker build --rm -t cgcpp .
# See README.md for details


FROM mcr.microsoft.com/windows/servercore:ltsc2019 as base

LABEL maintainer="ababak@gmail.com"

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

ADD https://aka.ms/vscollect.exe C:\TEMP\collect.exe
ADD https://aka.ms/vs/16/release/channel C:\TEMP\VisualStudio.chman
ADD https://aka.ms/vs/16/release/vs_buildtools.exe C:\TEMP\vs_buildtools.exe

# Install MSVC C++ compiler, CMake, and MSBuild.
RUN C:\TEMP\vs_buildtools.exe `
    --quiet --wait --norestart --nocache `
    --installPath C:\BuildTools `
    --channelUri C:\TEMP\VisualStudio.chman `
    --installChannelUri C:\TEMP\VisualStudio.chman `
    --add Microsoft.VisualStudio.Workload.VCTools `
    --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended `
    --add Microsoft.Component.MSBuild `
    || IF "%ERRORLEVEL%"=="3010" EXIT 0

# Install Chocolatey package manager
RUN powershell.exe -ExecutionPolicy RemoteSigned `
    iex (New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'); `
    && SET "PATH=%PATH%;%ALLUSERSPROFILE%/chocolatey/bin"

# Install Chocolatey packages
RUN powershell.exe -ExecutionPolicy RemoteSigned `
    choco install python2 -y -o -ia "'/qn /norestart ALLUSERS=1 TARGETDIR=c:\Python27'"; `
    choco install 7zip -y; `
    choco install nasm -y; `
    choco install git -y; `
    choco install boost-msvc-14.1 --version 1.67.0 -y; `
    choco install ninja -y

RUN setx `
    PATH "%PATH%;%PROGRAMFILES%/Git/bin;%PROGRAMFILES%/NASM;%PROGRAMFILES%/7-Zip;C:/Python27/Scripts"

# Install Python packages
RUN powershell.exe -ExecutionPolicy RemoteSigned `
    python -m pip install --upgrade pip`
    pyside `
    pyopengl `
    jinja2

ENV PYTHONIOENCODING UTF-8

# Install Chocolatey Boost package
RUN powershell.exe -ExecutionPolicy RemoteSigned `
    choco install boost-msvc-14.1 --version 1.67.0 -y
ENV Boost_ROOT="C:\local\boost_1_67_0"
# Overcome the Boost 1.67 build bug: https://github.com/boostorg/python/issues/193
# Unfortunately, no neweer Boost versions available on Chocolatey: https://chocolatey.org/packages?q=boost
RUN mklink %BOOST_ROOT%\lib64-msvc-14.1\boost_pythonPY_MAJOR_VERSIONPY_MINOR_VERSION-vc141-mt-gd-x64-1_67.lib %BOOST_ROOT%\lib64-msvc-14.1\libboost_python27-vc141-mt-gd-x64-1_67.lib `
    && mklink %BOOST_ROOT%\lib64-msvc-14.1\libboost_pythonPY_MAJOR_VERSIONPY_MINOR_VERSION-vc141-mt-x64-1_67.lib %BOOST_ROOT%\lib64-msvc-14.1\libboost_python27-vc141-mt-x64-1_67.lib

#######################################################

COPY build.bat C:\build\build.bat
COPY cmake C:\cmake
RUN setx PATH "c:/cmake;%PATH%"
ENV CMAKE_GENERATOR "NMake Makefiles"

FROM base as prebuild


WORKDIR /build

ENTRYPOINT [ "C:\\BuildTools\\Common7\\Tools\\VsDevCmd.bat", "-arch=amd64", "&&" ]
CMD [ "build.bat" ]
