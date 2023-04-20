#
# Author:
# Andriy Babak <ababak@gmail.com>
#
# Build the docker image:
# docker build --rm -t ababak/cgcpp:1.6 .
# See README.md for details

FROM mcr.microsoft.com/windows/servercore:ltsc2019 as base

LABEL maintainer="ababak@gmail.com"

SHELL ["powershell", "-ExecutionPolicy", "RemoteSigned", "-Command"]

# Install BuildTools
RUN Invoke-WebRequest "https://aka.ms/vs/16/release/vs_buildtools.exe" -OutFile vs_buildtools.exe; \
    Start-Process vs_buildtools.exe -Wait -ArgumentList '\
    --quiet \
    --wait \
    --norestart \
    --nocache \
    --installPath C:/BuildTools \
    --add Microsoft.VisualStudio.Workload.MSBuildTools \
    --add Microsoft.VisualStudio.Workload.VCTools \ 
    --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 \ 
    --add Microsoft.VisualStudio.Component.Windows10SDK.18362 \ 
    --add Microsoft.VisualStudio.Component.VC.CMake.Project \ 
    --add Microsoft.VisualStudio.Component.TestTools.BuildTools \ 
    --add Microsoft.VisualStudio.Component.VC.ASAN \ 
    --add Microsoft.VisualStudio.Component.VC.140'; \
    Remove-Item c:/vs_buildtools.exe

# Install Chocolatey package manager
RUN [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    iex (New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')

# Install Chocolatey packages
RUN choco install -y \
    7zip \
    nasm \
    openssh \
    git

# Install Python
RUN choco install -y \
    python2
RUN choco install -y \
    python39
RUN choco install -y \
    python310

ENV PYTHONIOENCODING UTF-8

# Install Boost
RUN [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest "https://boost.teeks99.com/bin/1.67.0/boost_1_67_0-msvc-14.1-64.exe" -OutFile boost.exe; \
    Start-Process boost.exe -Wait -ArgumentList '/DIR="C:/local/boost_1_67_0" /SILENT'; \
    Remove-Item c:/boost.exe
RUN [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest "https://boost.teeks99.com/bin/1.76.0/boost_1_76_0-msvc-14.1-64.exe" -OutFile boost.exe; \
    Start-Process boost.exe -Wait -ArgumentList '/DIR="C:/local/boost_1_76_0" /SILENT'; \
    Remove-Item c:/boost.exe
RUN [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest "https://boost.teeks99.com/bin/1.80.0/boost_1_80_0-msvc-14.1-64.exe" -OutFile boost.exe; \
    Start-Process boost.exe -Wait -ArgumentList '/DIR="C:/local/boost_1_80_0" /SILENT'; \
    Remove-Item c:/boost.exe

ENV CMAKE_GENERATOR "NMake Makefiles"
RUN setx /M PATH $( \
    'c:/cmake' + ';' + \
    $env:PATH + ';' + \
    $env:PROGRAMFILES + '/NASM' \
    )

COPY cmake C:/cmake
COPY build.bat C:/build.bat

FROM base as prebuild

WORKDIR /build

ENTRYPOINT [ "C:/BuildTools/Common7/Tools/VsDevCmd.bat", "-arch=amd64", "&&" ]
CMD [ "c:/build.bat" ]
