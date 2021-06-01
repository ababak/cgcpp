@echo off
@cmake /source || exit /b !ERRORLEVEL!
@nmake install || exit /b !ERRORLEVEL!
@echo Build complete
