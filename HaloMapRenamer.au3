#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=icon.ico
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

; Copyright (c) 2014, Chad Zawistowski
; All rights reserved.
;
; Redistribution and use in source and binary forms, with or without
; modification, are permitted provided that the following conditions are met:
;     * Redistributions of source code must retain the above copyright
;       notice, this list of conditions and the following disclaimer.
;     * Redistributions in binary form must reproduce the above copyright
;       notice, this list of conditions and the following disclaimer in the
;       documentation and/or other materials provided with the distribution.
;
; THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
; ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
; WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
; DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
; DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
; (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
; ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
; (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
; SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#NoTrayIcon
#include <ButtonConstants.au3>
#include <EditConstants.au3>
#include <GUIConstantsEx.au3>
#include <StaticConstants.au3>
#include <WindowsConstants.au3>
#Region ### START Koda GUI section ### Form=c:\dropbox\workbench\codeprojects\halofiles\source code\mdrenamer\form.kxf
$Form = GUICreate("Halo Map Renamer v1.2", 410, 186, 261, 224)
$InputMap = GUICtrlCreateLabel("Input Map", 8, 12, 52, 17, 0)
$InputMapInput = GUICtrlCreateInput("", 96, 8, 217, 21, $GUI_SS_DEFAULT_INPUT)
$Browse1 = GUICtrlCreateButton("Browse", 320, 6, 81, 25, $BS_NOTIFY)
$ShortName = GUICtrlCreateLabel("New Name", 8, 44, 57, 17, 0)
$ShortNameInput = GUICtrlCreateInput("", 96, 40, 217, 21, $GUI_SS_DEFAULT_INPUT)
$Label2 = GUICtrlCreateLabel("eg. bestmod", 320, 44, 62, 17, 0)
$BuildNumber = GUICtrlCreateLabel("Build Number", 8, 76, 67, 17, 0)
$BuildNumberInput = GUICtrlCreateInput("", 96, 72, 217, 21, $GUI_SS_DEFAULT_INPUT)
$Label3 = GUICtrlCreateLabel("eg. 1", 320, 76, 28, 17, 0)
$OutputDirectory = GUICtrlCreateLabel("Output Directory", 8, 108, 81, 17, 0)
$OutputDirInput = GUICtrlCreateInput("", 96, 104, 217, 21, $GUI_SS_DEFAULT_INPUT)
$Browse2 = GUICtrlCreateButton("Browse", 320, 102, 81, 25, $BS_NOTIFY)
$Label4 = GUICtrlCreateLabel("(Optional, defaults to same directory)", 96, 128, 175, 17, 0)
$ChangeName = GUICtrlCreateButton("Change Name", 96, 152, 217, 25, $BS_NOTIFY)
GUISetState(@SW_SHOW)
#EndRegion ### END Koda GUI section ###

While 1
	$nMsg = GUIGetMsg()
	Switch $nMsg
		Case $ChangeName
			Run("renamer.exe" & ' "' & GUICtrlRead($InputMapInput) & '" "' & GUICtrlRead($ShortNameInput) & '" "' & GUICtrlRead($BuildNumberInput) & '" "' & GUICtrlRead($OutputDirInput) & '"')

		Case $Browse1
			$ans = FileOpenDialog("Open File", @ProgramFilesDir & "\Microsoft Games\Halo\MAPS\", "Halo Mapfiles (*.map)")
			GUICtrlSetData($InputMapInput, $ans)

		Case $Browse2
			$ans = FileSelectFolder("Open Folder", @DesktopDir & '\')
			GUICtrlSetData($OutputDirInput, $ans)

		Case $GUI_EVENT_CLOSE
			Exit

	EndSwitch
WEnd
