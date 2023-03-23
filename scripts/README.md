# Deploy Scripts

Two PowerShell scripts to quickly build a working version of the game out of the different sources.

You will have to set up a directory as follows.

```
/
├── Game/                          this folder will be created by the update script and will be used to play the game
├── Parts/                         this folder has all the different parts / sources used to assemble the final game folder
│   ├── bugfix/                    clone git repository https://github.com/Tristimdorion/Lab-Rats-2/
│   ├── Lab_Rats_2-v0.51.1-pc/     latest version of the untouched vanilla game, need to adjust the script if the version / folder name changes
│   ├── Lab-Rats-2-renpy/          latest version of the renpy files for the modded game (including the .exe files)
│   ├── mod/                       clone git repository https://gitgud.io/lab-rats-2-mods/lr2mods
│   ├── mods-other/                mods created by other people go here
│   └── my-mods/                   mods you have created yourself go here
├── update.ps1                     update script that recreates the Game folder
└── update_mine.ps1                update script that only adds new files from /Parts/my-mods/Mods/ to the Game folder
```

- Run `update.ps1` to completely generate the Game folder from scratch (existing folder will be deleted).
- Run `update_mine.ps1` if you have added new files in my-mods and want to push them to the Game folder.

All files in the Game folder are created as hardlinks, i.e. you can modify file contents in the Parts folder and the changes will be 
reflected in the Game folder as well. Only if you add or remove files will you have to re-run one of the update scripts.