#define MyAppName "FileScript"
#define MyAppVersion "1.0"
#define MyAppPublisher "cheese-dev"
#define MyAppURL "https://github.com/zxcheese-dev/FileScript"
#define MyProgExeName "FileScript.exe" 

[Setup]
AppId={{8A7B3C4D-E5F6-7A8B-9C0D-1E2F3A4B5C6D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableDirPage=no
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=userdocs:Inno Setup Outputs
OutputBaseFilename={#MyAppName}_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "modpath"; Description: "ƒобавить {#MyAppName} в переменную окружени€ PATH (рекомендуетс€)"; Flags: unchecked

[Files]
Source: "C:\Users\Lenovo\Desktop\FileScript\FileScript.exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyProgExeName}"

[Code]
function SendMessageTimeout(hWnd: HWND; Msg: UINT; wParam: WPARAM; lParam: string; fuFlags: UINT; uTimeout: UINT; var lpdwResult: DWORD): lResult;
  external 'SendMessageTimeoutW@user32.dll stdcall';

const
  EnvironmentKey = 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment';
  WM_SETTINGCHANGE = $001A;
  SMTO_ABORTIFHUNG = $0002;

procedure CurStepChanged(CurStep: TSetupStep);
var
  OldPath, NewPath: string;
  ResVal: DWORD;
begin
  if CurStep = ssPostInstall then
  begin
    if WizardIsTaskSelected('modpath') then
    begin
      if RegQueryStringValue(HKEY_LOCAL_MACHINE, EnvironmentKey, 'Path', OldPath) then
      begin
        if Pos(LowerCase(ExpandConstant('{app}')), LowerCase(OldPath)) = 0 then
        begin
          if (OldPath <> '') and (OldPath[Length(OldPath)] <> ';') then
            OldPath := OldPath + ';';
          NewPath := OldPath + ExpandConstant('{app}');
          if RegWriteStringValue(HKEY_LOCAL_MACHINE, EnvironmentKey, 'Path', NewPath) then
          begin
            SendMessageTimeout(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment', SMTO_ABORTIFHUNG, 5000, ResVal);
          end;
        end;
      end;
    end;
  end;
end;

procedure CurUninstallStepChanged(AnUninstallStep: TUninstallStep);
var
  OldPath, NewPath: string;
  AppPath: string;
  PathPos: Integer;
  ResVal: DWORD;
begin
  if AnUninstallStep = usPostUninstall then
  begin
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, EnvironmentKey, 'Path', OldPath) then
    begin
      AppPath := ExpandConstant('{app}');
      PathPos := Pos(LowerCase(AppPath), LowerCase(OldPath));
      if PathPos > 0 then
      begin
        Delete(OldPath, PathPos, Length(AppPath));
        StringChangeEx(OldPath, ';;', ';', True);
        if (OldPath <> '') and (OldPath[Length(OldPath)] = ';') then
          Delete(OldPath, Length(OldPath), 1);
        NewPath := OldPath;
        if RegWriteStringValue(HKEY_LOCAL_MACHINE, EnvironmentKey, 'Path', NewPath) then
        begin
          SendMessageTimeout(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment', SMTO_ABORTIFHUNG, 5000, ResVal);
        end;
      end;
    end;
  end;
end;