#define MyAppName "Link Grabber"
#define MyAppVersion "1.0"
#define MyAppPublisher "LinkGrabber"
#define MyAppExeName "LinkGrabber.exe"

[Setup]
; Basic setup info
AppId={{12345678-ABCD-1234-ABCD-123456789012}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=LinkGrabber_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons"

[Files]
; Main EXE
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Optional: copy icon.ico for Tkinter messageboxes
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start menu / program group icon - uses EXE embedded icon
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
; Desktop shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppExeName}"
; Uninstall icon
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"; IconFilename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
