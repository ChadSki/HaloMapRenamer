#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=icon.ico
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
#include <ButtonConstants.au3>
#include <EditConstants.au3>
#include <GUIConstantsEx.au3>
#include <StaticConstants.au3>
#include <WindowsConstants.au3>
#Region ### START Koda GUI section ### Form=C:\Dropbox\Workbench\CodeProjects\Halo\mdrenamer\Form.kxf
$Form = GUICreate("MDRenamer Gui v1.1", 410, 218, 569, 369)
$InputMap = GUICtrlCreateLabel("Input Map", 8, 12, 52, 17)
$InputMapInput = GUICtrlCreateInput("", 96, 8, 217, 21)
$Browse1 = GUICtrlCreateButton("Browse", 320, 6, 81, 25, 0)
$ModName = GUICtrlCreateLabel("Mod Name", 8, 44, 56, 17)
$ModNameInput = GUICtrlCreateInput("", 96, 40, 217, 21)
$Label1 = GUICtrlCreateLabel("eg. Best Mod", 320, 44, 67, 17)
$ShortName = GUICtrlCreateLabel("Short Name", 8, 76, 60, 17)
$ShortNameInput = GUICtrlCreateInput("", 96, 72, 217, 21)
$Label2 = GUICtrlCreateLabel("eg. bestmod", 320, 76, 62, 17)
$BuildNumber = GUICtrlCreateLabel("Build Number", 8, 108, 67, 17)
$BuildNumberInput = GUICtrlCreateInput("", 96, 104, 217, 21)
$Label3 = GUICtrlCreateLabel("eg. 1", 320, 108, 28, 17)
$OutputDir = GUICtrlCreateLabel("Output Directory", 8, 140, 81, 17)
$OutputDirInput = GUICtrlCreateInput("", 96, 136, 217, 21)
$Browse2 = GUICtrlCreateButton("Browse", 320, 134, 81, 25, 0)
$Label4 = GUICtrlCreateLabel("(Optional, defaults to same directory)", 96, 160, 175, 17)
$ChangeName = GUICtrlCreateButton("Change Name", 96, 184, 217, 25, 0)
GUISetState(@SW_SHOW)
#EndRegion ### END Koda GUI section ###

While 1
	$nMsg = GUIGetMsg()
	Switch $nMsg
		Case $ChangeName
			Run("mdrenamer.exe" & ' "' & GUICtrlRead($InputMapInput) & '" "' & GUICtrlRead($ModNameInput) & '" "' & GUICtrlRead($ShortNameInput) & '" "' & GUICtrlRead($BuildNumberInput) & '" "' & GUICtrlRead($OutputDirInput) & '"')

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
