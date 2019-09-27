tell application "System Events" to tell process "SystemUIServer"
	tell (menu bar item 1 of menu bar 1 where description is "text input")
		click
		-- always the same menu position regardless of input keyboards added
		click menu item -5 of menu 1
	end tell
end tell
return
