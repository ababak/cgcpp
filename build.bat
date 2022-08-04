@echo off
@echo Configuring
@cmake /source || exit /b !ERRORLEVEL!
@echo Make install
@nmake install || exit /b !ERRORLEVEL!
@echo Build complete
