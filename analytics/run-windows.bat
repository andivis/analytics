for /f "delims=" %%D in ('dir /a:d /b "%userprofile%\AppData\Local\Programs\Python"') do (
    echo %userprofile%\AppData\Local\Programs\Python\%%~nxD
    set pythonDirectory=%userprofile%\AppData\Local\Programs\Python\%%~nxD
)

%pythonDirectory%\python.exe -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

%pythonDirectory%\python.exe analytics.py