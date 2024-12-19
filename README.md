# ReverseATS

## Introduction

This guide will help you deploy the app locally using a development container.

# Link to demo video

[Link to demo video](https://www.loom.com/share/a5d81627f7644940a02ad84cb55f3d11?sid=ad97d970-9860-4555-8256-36145694e11c)

## Overview

The Reverse ATS is a simple app to allow users to track their ongoing applications. The app consists of the following components:

- A PostgreSQL database
- A FastAPI backend
- A React frontend

## Technologies Used

- Docker
- PostgreSQL
- FastAPI
- React
- Websockets

## Prerequisites

- Docker installed on your machine
- Visual Studio Code with the Remote - Containers extension

## Steps to Deploy

1. **Clone the Repository**

```sh
git clone https://github.com/kairisameshima/Reverse-ATS.git
cd reverse-ats
```

2. **Open in VS Code**
   Open the project directory in Visual Studio Code.

3. **Reopen in Container**

- Press `F1` to open the command palette.
- Type `Remote-Containers: Reopen in Container` and select it.

4. **Build and Start the Container**
   VS Code will automatically build the development container and start it.
   The databases, the fastAPI app and the react app will be started automatically.

5. **Access the Application**
   Once the container is running, you can access the application locally. The default setup should expose the necessary ports.

6. **Access the App in a Browser**
   Open a browser and navigate to `http://localhost:3000/` to view the application.

7. **Test out the App**

- You can now test out the app by either joining the slack workspace or updating the profile information of an existing user.

## Additional Information

- For any configuration changes, edit the `.devcontainer/devcontainer.json` file.
- Ensure your Docker daemon is running before starting the container.

## Troubleshooting

- If you encounter any issues, check the container logs in the VS Code terminal.
- Verify that all prerequisites are correctly installed and configured.
- Alembic migrations may have to be run manually if the database image is being created for the first time.
