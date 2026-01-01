@echo off
for /L %%i in (12,1,23) do (
    mkdir "Chapter%%i"
    echo # Chapter %%i > "Chapter%%i\Readme.md"
)
echo Folders and files created successfully.
pause