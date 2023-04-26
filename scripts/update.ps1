
$src = Get-Item '.\Parts\'
$dst = '.\Game\'
$partList = @(
	# renpy and .exe files for modded game
	@('Lab-Rats-2-renpy', ''),
	# bugfix (clone the git repository)
	@('bugfix\game', 'game\'),
	# unofficial expansion (clone the git repository)
	@('mod\Mods', 'game\Mods\'),
	# new map (and some other stuff) by silenced (clone the git repository)
	@('mods-silenced\Mods_Silence', 'game\Mods_Silence\'),
	# other mods that don't have to end up in the "game" dir
	@('mods-other', 'game\Mods_xxOther'),
	# my own mods
	@('my-mods\Mods', 'game\Mods_zzMine\'),
	# vanilla game
	@('Lab_Rats_2-v0.51.1-pc\game', 'game\')
)

Remove-Item -Force -Recurse .\Game\
New-Item -ItemType Directory -Name "Game"

function Test-Item {
	param (
		[string[]]$Skips,
		[io.FileInfo]$Item
	)

	if ($Item.Extension -eq '.rpyc') {
		return $false
	}
	if ($Item.Name -eq 'README.md') {
		return $false
	}
	if ($Item.FullName -contains '\README\') {
		return $false
	}
	foreach ($skip in $Skips) {
		if ($Item.FullName -like '*'+$skip+'*') {
			return $false
		}
	}
	return $true
}

foreach ($part in $partList) {
	$partDir = Join-Path $dst $part[1]
	$skips = @()
	$skipList = Get-ChildItem -Path (Join-Path $src $part[0]) -Recurse -File -Filter .skip
	foreach ($skip in $skipList) {
		$skips += $skip.Directory.FullName
	}

	$childList = Get-ChildItem -Path (Join-Path $src $part[0]) -Recurse -File
	foreach ($child in $childList) {
		if (Test-Item -Skips $skips -Item $child) {
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