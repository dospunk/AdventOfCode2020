$param1=$args[0]
Invoke-Expression "ghc --make $param1 -outputdir hs-out"
$param1NoExt=$param1.Substring(0,$param1.length-3)
Invoke-Expression ".\$param1NoExt.exe"