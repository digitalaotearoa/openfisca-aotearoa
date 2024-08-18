## Setup OpenFisca Aotearoa in vscode with devcontainer

## Run the application using Docker

1. [Install Visual Studio Code](https://code.visualstudio.com/).
2. [Install Docker Desktop](https://www.docker.com/products/docker-desktop/).
3. Download/clone the openfisca-aotearoa repository
4. Start Visual Studio Code
5. Install the `ms-vscode-remote.vscode-remote-extensionpack` Visual Studio Code extension from the Extensions menu (Ctrl+Shift+X)
6. Click on "Open folder", then select the git repository folder downloaded in Step 3
7. A popup should appear stating the "Folder contians a Dev Container configuration file". Click on the "Reopen in Container" button.
8.  Click on "View Log" to see the environment set-up progress. Full set-up can take a minute or two. Wait for the packages to install. The VScode command prompt becomes active as soon as the container starts, not when Openfisca finishes installing. If the Openfisca commands fail, wait a few seconds, and then try again.

## Run the OpenFisca Web API or tests from the dev container

Once running in the devcontainer, the Visual Studio Code terminal should also be running in the container. This allows you access to a command prompt to do all the normal activities.
The `Makefile` provides a number of quick commands you can access also.

Refer to the `README.md` for instructions on how to run tests or serve the web API and be sure to run the commands in the VSCode terminal.
