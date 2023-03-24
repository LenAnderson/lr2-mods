$src = Get-Item '.\Parts\'
$dst = '.\Game\'
$partList = @(
	@('my-mods\Mods', 'game\Mods\_LenAnderson\'),
	@('mods-other', 'game\Mods\_Other')
)
$dstList = @()

foreach ($part in $partList) {
	$partDir = Join-Path $dst $part[1]
	$childList = Get-ChildItem -Path (Join-Path $src $part[0]) -Recurse -File
	foreach ($child in $childList) {
		if ($child.Extension -ne '.rpyc' || $child.Name -eq 'README.md' || $child.Parent.Name -eq 'README') {
			$childDst = Join-Path $partDir $child.FullName.Substring($src.FullName.Length + $part[0].Length + 1)
			$childDstDir = $childDst.Substring(0, $childDst.Length - $child.Name.Length - 1)
			if (!(Test-Path $childDstDir)) {
				New-Item -ItemType Directory $childDstDir
			}
			if (!$dstList.Contains($childDst)) {
				if ((Test-Path $childDst)) {
					Remove-Item $childDst
				}
				New-Item -ItemType HardLink -Name $childDst -Target $child.FullName
				$dstList += @($childDst.FullName)
			}
		}
	}
}