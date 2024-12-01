# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change).

## Setting up Trello

You'll need to set-up a [Trello account](https://trello.com/signup), Trello board, a 'To-Do' list in that board, and create a [Trello API key](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#managing-your-api-key). 
Then create a API token:Create a API Token for Trello.
This can be done by clicking the “Token” link on the same page where your API key is displayed
![img.png](img.png)

Once you've done this, replace the TRELLO_API_KEY and TRELLO_API_TOKEN values in your .env file with you API key and token.



Finally, [get your board id](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#your-first-api-call) and replace the TRELLO_TO_DO_BOARD_ID with your board's ID. Do the same with the organisation id (the `idOrganization` field in the same API response), replacing the TRELLO_ORGANIZATION_ID with it.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing the App

Unit and integration tests can be found in the top level `tests` directory.

End to end (Selenium) tests can be found in the top level `e2eTests` directory.

To run all tests in the project from the terminal, run `poetry run pytest`

To run all tests in a specific file run `poetry run pytest <path>/<to>/<test file>.py`

To run a specific test on its own run `poetry run pytest <path>/<to>/<test file>.py::<name of test>`

## Preparing to deploy the App using Ansible

These instructions assume that the control node and managed nodes are already set-up, that the control node has git and python installed on it, and that the control node has ssh keys for accessing the mananged nodes.
There are many examples and tutorials on [how to set this up.](https://www.ibm.com/docs/en/storage-ceph/5?topic=installation-enabling-password-less-ssh-ansible)

ssh into the control node and clone the repo into an appropriate folder using `git clone https://github.com/Travis-Softwire/DevOps-Course-Starter.git`.

Check if ansible is installed using `ansible --version.` If it isn't, install it on the control node using `sudo pip install `

Create a file on the control node called `secrets.enc` using `touch secrets.enc`.

Using the text editor of your choice, e.g. `nano`, copy the contents of `ansible/secrets.enc.template` inside the project folder into a new file on the control node `ansible/secrets.enc`.
You then need to replace the placeholders in the file with your actual Trello secrets etc. Then on the command node run `ansible-vault encrypt <your project folder>/ansible/secrets.enc`. When prompted, enter a password - this will be used to decrypt the secrets when ansible requires them.
This file can now be safely committed to source control as the secrets within it are encrypted. You can also create multiple different secrets files for multiple environments if needed.

Finally, you can run the ansible playbook by running `ansible-playbook ./ansible/setup_todo.yaml -i ./ansible/inventory.ini -e @<path to project folder>/ansible/secrets.enc --ask-vault-pass` on the control node. When prompted, enter the password that you entered when you encrypted the secrets file.
When the playbook has finished running, you should be able to open the IP address of your managed node in the browser on your physical machine and immediately see the Todoapp running.

## Running the App in a container

### Setup

You will need [Docker](https://docs.docker.com/desktop/wsl/) installed on your machine (using WSL if on a Windows machine).

### Running the development build

You can run the development build in docker using the command `docker compose up development` from the root of your project. 
You should then be able to access the app via http://127.0.0.1:5000. 

The development build binds your local source files and uses Flask's web server, so it will reflect any changes you make in real time, just like running the app locally outside of a container.

### Running the production build

You can run the production build and deploy it to a docker using the command `docker compose up production` from the root of your project. 

### Manually deploying the production build to Azure App service

The pipeline on github actions will automatically deploy a build of master to Azure App service on merge.

To manually deploy a new version of the production build to Azure App service, first publish the latest build to docker hub:
- Run `docker login` to login to docker hub
- Use `docker build --target production --tag trwoodward/todo-app:latest .` to build and tag the image
- Then push the image with `docker push trwoodward/todo-app:latest`
The published image can be found [here](https://hub.docker.com/r/trwoodward/todo-app/tags)

To trigger the App service to pull the latest image and restart:
- Find the webhook url by logging into the Azure portal, navigating to the `travis-woodward-todo-app` App service, and then to Deployment -> Deployment Center -> Settings tab
- Invoke the webhook with `curl -v -X POST '<webhook>'` in a Bash shell

The deployed app should then be available at https://travis-woodward-todo-app.azurewebsites.net/ 

### Running the test suite

You can run all of the tests inside a container using the command `docker compose up runTests` from the root of your project.

### Having the tests run every time there is a code change

You can run the tests in watch mode using the command `docker compose up watchUnitTests` from the root of your project. This can be run alongside the development build above.

## Viewing architecture diagrams

The c4 architecture diagrams are in the `/architecture` folder at the root of the project. These are mermaid diagrams and can be viewed on any mermaid viewer - extensions for viewing mermaid diagrams are available for both Vs Code and Pycharm.