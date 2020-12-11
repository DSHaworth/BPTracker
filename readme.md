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
### JWT

[python-jwt](https://github.com/davedoesdev/python-jwt) Last active 8/2020


    > pip install python_jwt


Follow tutorial at [VueJS Flask](https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/).
Follow tutorial at [Create Tables](https://www.sqlitetutorial.net/sqlite-python/create-tables/).

Follow tutorial at [flask-jwt-extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
GitHub for [flask-jwt-extended](https://github.com/vimalloc/flask-jwt-extended/tree/1fec4dc22fe97fd3bf579548079543a8c0b61e3e)

## Client App
### VueJS

#### [Installation:](https://cli.vuejs.org/guide/installation.html)

    $ npm install -g @vue/cli

#### Create VueJS Project

    $ vue create client

#### Launch VueJS Project

    $ npm run serve

#### Adding FontAwesome

    $ npm install --save @fortawesome/fontawesome-free

* Create **styles** folder under **src**
* Create **custom.scss** under new **styles**

*client\src\styles\custom.scss*

    // npm install --save @fortawesome/fontawesome-free
    $fa-font-path: "~@fortawesome/fontawesome-free/webfonts";
    @import '~@fortawesome/fontawesome-free/scss/fontawesome.scss';
    @import '~@fortawesome/fontawesome-free/scss/regular.scss';

*client\src\main.js*

    import './styles/custom.scss';

#### Adding [Vue-Material](https://vuematerial.io/)

    client> npm install vue-material --save

*client\src\main.js*

    import { MdButton, MdContent, MdTabs } from 'vue-material/dist/components'
    import 'vue-material/dist/vue-material.min.css'
    import 'vue-material/dist/theme/default.css'

    Vue.use(MdButton)


#### Adding Validators

    $ npm install vuelidate --save

#### Add Axios

    $ npm install axios
