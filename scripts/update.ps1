$src = Get-Item '.\Parts\'
$dst = '.\Game\'
$partList = @(
	@('Lab-Rats-2-renpy', ''),
	@('bugfix\game', 'game\'),
	@('mod\Mods', 'game\Mods\'),
	@('my-mods\Mods', 'game\Mods\_LenAnderson\'),
	@('mods-other', 'game\Mods\_Other'),
	@('Lab_Rats_2-v0.51.1-pc\game', 'game\')
)

Remove-Item -Force -Recurse .\Game\
New-Item -ItemType Directory -Name "Game"

foreach ($part in $partList) {
	$partDir = Join-Path $dst $part[1]
	$childList = Get-ChildItem -Path (Join-Path $src $part[0]) -Recurse -File
	foreach ($child in $childList) {
		if (($child.Extension -ne '.rpyc') -and ($child.Name -ne 'README.md') -and ($child.Directory.Name -ne 'README') -and !(Test-Path (Join-Path $child.Directory.FullName '.skip'))) {
			$childDst = Join-Path $partDir $child.FullName.Substring($src.FullName.Length + $part[0].Length)
			$childDstDir = $childDst.Substring(0, $childDst.Length - $child.Name.Length - 1)
			if (!(Test-Path $childDstDir)) {
				New-Item -ItemType Directory $childDstDir
			}
			if (!(Test-Path $childDst)) {
				New-Item -ItemType HardLink -Name $childDst -Target $child.FullName
			}
		}
	}
}