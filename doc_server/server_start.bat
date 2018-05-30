@ECHO OFF

REM Write the static index.html pre data
TYPE index_pre.html.txt > index.html

REM Process all documentation locations (see doc_locations.txt for format)
FOR /F "TOKENS=1,2,3,4,5 EOL=;" %%a IN (%~dp0\doc_locations.txt) DO (
	
	REM Start live reload documentation
	CALL :StartLiveDoc %%a\%%b\%%c %%e
	
	REM Add corresponding entry to index.html
	ECHO ^<tr^> >> index.html
	ECHO ^<td^>^<a href="http://%COMPUTERNAME%.%USERDNSDOMAIN%:%%e"^>%%c^</a^>^</td^> >> index.html
	ECHO ^<td^>%%d^</td^> >> index.html
	ECHO ^<td^>%%e^</td^> >> index.html
	ECHO ^<td^>%%a\%%b\%%c^</td^> >> index.html
	ECHO ^</tr^> >> index.html
)

REM Write the static index.html pre data
TYPE index_post.html.txt >> index.html


REM change back to server directory
cd %~dp0

python -m http.server 1> server.log 2>&1

GOTO :EOF

REM parameter 1: base directory
REM parameter 2: port number for livehtml
:StartLiveDoc
	REM live html generation
	START CMD /K "cd /d %1\#_doc & make.bat livehtml %2"

	REM antiweb in daemon mode
	START CMD /K "cd /d %1 & antiweb -r -o #_doc\source\_antiweb -d"
GOTO :EOF
