#include <ButtonConstants.au3>
#include <EditConstants.au3>
#include <GUIConstantsEx.au3>
#include <StaticConstants.au3>
#include <WindowsConstants.au3>
#Region ### START Koda GUI section ### Form=
$Form1 = GUICreate("MdRenamer", 322, 286, 195, 167)
$Label1 = GUICtrlCreateLabel("Input Map", 8, 8, 52, 17)
$Label2 = GUICtrlCreateLabel("Mod Name", 8, 56, 56, 17)
$Label3 = GUICtrlCreateLabel("Short Name", 8, 104, 60, 17)
$Label4 = GUICtrlCreateLabel("Build Number", 8, 152, 67, 17)
$Label5 = GUICtrlCreateLabel("Output Directory", 8, 200, 81, 17)
$Input1 = GUICtrlCreateInput("", 96, 8, 217, 21)
$Input2 = GUICtrlCreateInput("", 96, 56, 217, 21)
$Input3 = GUICtrlCreateInput("", 96, 104, 217, 21)
$Input4 = GUICtrlCreateInput("", 96, 152, 217, 21)
$Input5 = GUICtrlCreateInput("", 96, 200, 217, 21)
$Label6 = GUICtrlCreateLabel("eg: C:\Users\Jake\Desktop\bloodgulch.map", 96, 32, 216, 17)
$Label7 = GUICtrlCreateLabel("eg: Best Mod", 96, 80, 66, 17)
$Label8 = GUICtrlCreateLabel("eg: bestmod", 96, 128, 61, 17)
$Label9 = GUICtrlCreateLabel("eg: 1", 96, 176, 27, 17)
$Label10 = GUICtrlCreateLabel("(Optional, defaults to same directory)", 96, 224, 216, 17)
$Button1 = GUICtrlCreateButton("Change Name", 16, 250, 289, 25)
GUISetState(@SW_SHOW)
#EndRegion ### END Koda GUI section ###

While 1
	$nMsg = GUIGetMsg()
	Switch $nMsg
		Case $Button1
			Run("mdrenamer.exe" & " " & GUICtrlRead($Input1) & " " & GUICtrlRead($Input2) & " " & GUICtrlRead($Input3) & " " & GUICtrlRead($Input4) & " " & GUICtrlRead($Input5))

		Case $GUI_EVENT_CLOSE
			Exit

	EndSwitch
WEnd
