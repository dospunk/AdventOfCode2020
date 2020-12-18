$param1=$args[0]
Push-Location -Path "aocutils"
Invoke-Expression "tsc"
Pop-Location
Invoke-Expression "tsc $param1 --target es2020 --outDir ts-out --moduleResolution node"
$param1NoExt=$param1.Substring(0,$param1.length-3)
Invoke-Expression "node ts-out\$param1NoExt.js"