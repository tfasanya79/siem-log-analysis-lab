# VMware Workstation VM Management Script with IP Retrieval
$vmPath1 = "C:\Users\Timothy\Virtual Machines\Ubuntu_VM\Ubuntu_VM.vmx"
$vmPath2 = "C:\Users\Timothy\Virtual Machines\Windows_Lab\Windows_Lab.vmx"
$vmPath3 = "C:\Users\Timothy\Virtual Machines\Splunk_VM\Splunk_VM.vmx"
$vmrunPath = "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"

function Show-Menu {
    Write-Host "VM Management Menu"
    Write-Host "1. Start Ubuntu VM"
    Write-Host "2. Start Windows VM"
    Write-Host "3. Start Splunk VM"
    Write-Host "4. Stop Ubuntu VM"
    Write-Host "5. Stop Windows VM"
    Write-Host "6. Stop Splunk VM"
    Write-Host "7. List Running VMs"
    Write-Host "8. Get IP Addresses of Running VMs"
    Write-Host "9. Exit"
}

function Get-VMIPs {
    Write-Host "`nFetching IP addresses of running VMs..."
    $runningVMs = & $vmrunPath list
    if ($runningVMs -match "Total running VMs: 0") {
        Write-Host "No VMs are currently running."
        return
    }
    
    foreach ($vm in $runningVMs) {
        if ($vm -match ".vmx") {
            $ipAddress = & $vmrunPath getGuestIPAddress "$vm" 2>$null
            Write-Host "$vm - IP: $ipAddress"
        }
    }
}

do {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-9)"

    switch ($choice) {
        1 { & $vmrunPath start "$vmPath1" nogui }
        2 { & $vmrunPath start "$vmPath2" nogui }
        3 { & $vmrunPath start "$vmPath3" nogui }
        4 { & $vmrunPath stop "$vmPath1" soft }
        5 { & $vmrunPath stop "$vmPath2" soft }
        6 { & $vmrunPath stop "$vmPath3" soft }
        7 { & $vmrunPath list }
        8 { Get-VMIPs }
        9 { Write-Host "Exiting..."; exit }
        default { Write-Host "Invalid selection! Please enter a number between 1 and 9." }
    }
} while ($true)