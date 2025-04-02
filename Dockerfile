#
# Author:
# Andriy Babak <ababak@gmail.com>
#
# Build the docker image:
# docker build --rm -t ababak/cgcpp:1.8 .
# docker run --rm -v "$(pwd):c:/source:ro" -r "$(pwd)/out:c:/out" ababak/cgcpp:1.8
# docker run --rm -v "$(pwd -W):c:/source:ro" -v "$(pwd -W)/out:c:/out" ababak/cgcpp:1.8
# See README.md for details

FROM ababak/boost:latest as base

LABEL maintainer="ababak@gmail.com"

COPY cmake C:/cmake
COPY build.bat C:/build.bat

FROM base as prebuild

WORKDIR /build

ENTRYPOINT [ "C:/BuildTools/Common7/Tools/VsDevCmd.bat", "-arch=amd64", "&&" ]
CMD [ "c:/build.bat" ]
