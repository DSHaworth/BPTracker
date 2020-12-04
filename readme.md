# Process
1. `>md BPTracker`
2. `>cd BPTracker`
3. `>code .`

## Inside Visual Studio Code
1. Create new file `.gitignore`

        .DS_Store
        node_modules/
        /dist/
        env/
        __pycache__
        .vscode/

These are files and folders for git to ignore when committing changes.

Create two new folders:

    client
    server

The **client** folder is for the UI (VueJS)

The **server** folder is for the Python code.

## Server App

[VueJS Flask](https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/)