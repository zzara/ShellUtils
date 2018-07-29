Get-PSDrive | Where-Object {$_.free -gt 1} | ForEach-Object {$c = 0; Write-Host "This step only runs once."}{$c = $c + 1; Write-Host "This section runs once for each object in the pipe." $c}{Write-Host "This step runs once enverything is done. The value of the c varible is" $c }

