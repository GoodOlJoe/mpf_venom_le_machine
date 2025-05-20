# Setting up a new Python virtual environment

* for MPF development (if needed for any reason)
* don't normally need to do this once we have a venv set up for MPF. But who knows, maybe starting a new MPF machine i'll want to use updated packages without disturbing the python venv used for other machines?

```powershell
cd f:\MPFProjects
python -m venv {venv_name} # will create directory venv_name and install pythong and pkgs there
.\{venv_name}\Scripts\activate.ps1
pip install mpf --pre
pip install mpf-monitor --pre

### DON"T DO ANY OF THIS LANGUAGE SERVER STUFF, I NEVER COULD GET IT TO WORK IN VSCODE
# SO DON'T BOTHER MUNGING UP THE ENVIRONMENT

# install MPF Language Server, for which I first have to install pipx so I can use
# pipx to "inject MPFLS into MPF"...somehow? not sure what all this means yet
# pip is an installer of packages into a venv. But pipx is an installer of python
# programs, like running setup for a Windows program maybe?

# All of this i just to install MPF Language Server for the IDE. But 
# i'm not really sure what this did...did I switch out of the python 
# venv mode? Now these things are installed globally in some way? Or is venv
# mode still in force, as a development environment, where pipx installed
# a specific program, not realted to my dev project, globally? But then
# whey did I have to "install" mpf via pipx (just so I coudl "inject" mpfls into it?). Confusing

#
py -m pip install pipx
pipx install mpf
pipx inject mpf mpf-language-server --pip-args="--pre" --verbose --include-deps --include-apps
pipx ensurepath
```

# Creating a new MPF machine

```powershell
cd f:\MPFProjects\machines
mkdir {machine_name}
cd {machine_name}
mpf init
git init
# grab a .gitignore from another machine, commit it, create the github repo and push
# grab a .gitattributes from another machine, commit it, create the github repo and push
git lfs install #  initialize LFS for videos and images
```
# Then set up Godot project
   * Follow GMC steps to add GMC addons to Godot https://missionpinball.org/latest/start/quickstart/
     * open Godot
     * Download the latest GMC release    
         https://github.com/missionpinball/mpf-gmc/releases/ (under Assets > Source code).
     * Open the Godot Editor and create a new Project in the machine folder.
     * Extract the GMC download and copy the addons folder into your project folder.
     * In the Godot Editor, go to Project Settings > Plugins and check the Enable box for Godot MC. 
          (Godot will show lots of errors during this step and the next, ignore them).
     * In the Godot Editor Project Settings > Globals click the folder icon to add a new Autoload
     * Choose the file addons/mpf-gmc/mpd_gmc.gd. Set the Node name to MPF (all caps)
     * Press Add.
  * Save your Godot project and then in the editor menu select Project > Reload Current Project.



# Setting up Visual Pinball Bridge

Generally following these instructions https://missionpinball.org/latest/hardware/virtual/virtual_pinball_vpx/

  * clone the mpf-vpcom-bridge repo
  ```powershell
      cd 'F:\MPFProjects\mpf_open_source_repos"
      git clone https://github.com/missionpinball/mpf-vpcom-bridge
  ```
  * start Powershell as administrator, activate venv
  * go to folder containing register_vpcom.py, register the bridge
  ```powershell
      # this registers MPF.Controller in the Windows Registry as a COM object (which is used by VP)
      cd 'F:\MPFProjects\mpf_open_source_repos\mpf-vpcom-bridge'
      python register_vpcom.py –register
  ```
  * Had to update the demo MPF machine from config_version=5 to config_version=6 https://missionpinball.org/latest/config/instructions/config_v6/

  * Trying to set it up for the first time I was using the MPF machine inside the mp f-vpcom-brige repo so I didn't have to update the hardware platform there in config.yaml
  * It seems like the vpx bridge demo was designed to work with the MPF MC instead of MPF .80 with Godot. But I'm not sure whether it matters -- seems like if we don't do any media-conroller stuff we can mock it up with no media controllera at all (mpf mc OR godot)
    * I had to take out all references to slides in the VPX demo machine (and replace with a simple light show in one
    case just so there would be a step in the show)
  * WHAT DID NOT WORK is running mpf as 
  
```powershell
      mpf -xt --vpx
      # yielded "Runtime error
      # Failed to connect to MPF: [WinError 1225] The remote computer refused the network connection"
```

  * the -b options turns off the BCP protocol. VP  did not connect when started with -xt
  * doesn't entirely make sense since I assumed the bridge is using BCP to connect with MPF also, but I guess not since the following did work:

```powershell
      mpf -xtb --vpx
      # -b turns off BCP interface ()
```


  * so start mpf -xtb --vpx
  * You can also start mpf monitor in a separate window
  * start Visual Pinball IN ADMINISTRATOR MODE (it's at "C:\Visual Pinball\VPinballX4.exe", right click in Explorer and then "Run As Administrator")
  



# Trying the whole MPF thing with PIPX (wrong idea)

  * I started down this path then concluded that (as discussed at https://www.reddit.com/r/learnpython/comments/1gr84pw/using_pipx_and_venvs/) "pipx is not a tool for maning a project's virtual environment, it is for installing python command line apps implement as pythong packages in isolated environments, while making the CLI of those applications availabe globally (i.e. without needing to activate a virtual environment)."
  * also reference
    * how pipx works: https://pipx.pypa.io/stable/how-pipx-works/
    * pip comparison to other tools: https://pipx.pypa.io/stable/comparisons/
  * pipx relies heavily on a virtual environment (venv) set up by python
