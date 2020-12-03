$param1=$args[0]
Invoke-Expression "tsc $param1 --target es6 --outDir ts-out --moduleResolution node"