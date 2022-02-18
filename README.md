# Scaffold

Scaffold API is a CRUD API used to start new API projects with a UI 


## Table of Contents

- [Scaffold](#scaffold)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Standing Up Local Resources](#standing-up-local-resources)
      - [Software Requirements:](#software-requirements)
      - [Additional Requirements:](#additional-requirements)
      - [Creating the Environment](#creating-the-environment)
      - [Troubleshooting](#troubleshooting)
      - [Accessing Local Resources](#accessing-local-resources)
    - [Setting Up A Local Development Environment](#setting-up-a-local-development-environment)
      - [Requirements](#requirements)
      - [Bringing Up The Environment](#bringing-up-the-environment)
    - [Testing](#testing)
  - [API Documentation](#api-documentation)
  - [Auth Flow](#auth-flow)
    - [API Access](#api-access)
    - [OAuth Access](#oauth-access)
  - [Creating SQLAlchemy DB Migration](#creating-sqlalchemy-db-migration)
  - [Running Terraform](#running-terraform)
  - [Using the Production Optimized Image Locally](#using-the-production-optimized-image-locally)
  - [Dumping and Restoring the Database](#dumping-and-restoring-the-database)
  - [Updating Secrets for Environments](#updating-secrets-for-environments)
  - [Deploying the App to Dev, Stage, and Prod](#deploying-the-app-to-dev-stage-and-prod)
## Getting Started

### Standing Up Local Resources
For the local devopment environment three open source projects k3d, Helm and Tilt
k3d is a project used to stand up light weight Kubernetes cluster using docker. Helm is used to deploy the application as well as any dependencies
such as databases, and ingress controllers to the k3d created cluster.  Lastly tilt watches for changes to certain files on the local machine and applies those
changes to pods in the running Kubernetes cluster.

#### Software Requirements:
* Docker: https://docs.docker.com/get-docker/
* asdf: https://asdf-vm.com/#/core-manage-asdf

#### Creating the Environment
* In order to create the local environment run the command `make up` from this directory.
* After the cluster starts up you will see tilt start up and see that resources are being created. **The first build will take a while to build the inital containers. 
Later builds will be faster because container layers will be cached**
* To get a more interactive view with Tilt either hit the enter key or from your browser got to [http://localhost:10350](http://localhost:10350)
    * This view will allow you to get logs and output and restart individual Kubernetes resources.
* After you finished with your Tilt session use `ctrl+c` to exit the session and run `make clean` to clean up the Kubernetes cluster

#### Troubleshooting
If you run into any errors you can clear out a created cluster by running `make clean`

#### Accessing Local Resources
Several of the services will have ports automaically forwarded to localhost
* postgres database: port 5432
* flower ui: port 8888
You can access the UI and API through [http://scaffold.localhost:8443](http://scaffold.localhost:8443)
* UI and Login can be accessed through the root `/`
* API can be accessed through `/api/v1/{endpoint}`
* Swagger UI can be accessed through `/api/v1/`
* Admin UI can be accessed through `/admin`

### Setting Up A Local Development Environment
#### Requirements
* Python 3.9
* [Poetry](https://pypi.org/project/poetry/)
* Node 16.4

#### Bringing Up The Environment 
* Run `make shell` to install the python packages and enter the virtual environment.
* To bring up the UI envrionment from the *web* directory run `yarn install` *You might see a bunch of warning which are ok to ignore*

### Testing

Unit tests can be run by the make target `make tests-unit`.  These tests are run against the local sqlite database which is populated via the ./app/api/seed_test_db.py file.

## API Documentation
OpenAPI docs can be viewed at https://scaffold.localhost:8443/api/v1


## Auth Flow

There are two separate auth flows included in this project one for API access only and one for OAuth access to the "[admin web ui]


### API Access

Note that the seeded token "admintoken123" exists only in the local environment and can be used with tilt immediately upon start up to authenticate. 

API access only users are kept in the Users table of the Postgres database along with a salted hash of their API token. To make a new token use the following steps: 
* Navigate to the admin panel located at $API_URL/admin
* Click on the User tab after you've authenticated with Auth0
* Click on the create tab
* Fill out a username
* Click "Get Token"
* Copy and save the provided token. It cannot be regenerated from the hash, so this is the only time it is downloadable

To use the token, base64 encode it and include it as a basic authorization header with your API request:

"Authorization: Basic $YOUR_BASE64_ENCODED_TOKEN_HERE"

All tokens currently have access to all parts of the API with the exception of the admin panel. There are no token roles or permission sets. 


### OAuth Access

We utilize Auth0 as the OAuth provider for the admin web ui of this project. To get started visit the login page (#TODO Create a login page) or visit the admin panel at $API_URL/admin to be redirected for auth0 login. After you have successfully logged into Auth0, a session cookie will be stored in your browser containing your permissions. These permissions are set in the Auth0 admin portal one of two ways: 
* A user is given an RBAC role with active permissions against the API
* A user is given API permissions directly on their user account

After a user has logged in, they are able to use their session cookie to make requests directly against the API. When a user first makes a request to the API from their browser, a user is added into the Users table of the database using their email address. This user does not have any API token access and is for audit logging purposes.

Admin console access requires write:admin scope.

#### Adding Read and Write Permissions to Objects

Read and write access permissions to objects via the API for OAuth users is 
controlled by scope permissions set in Auth0. When new `__read_scope__` 
and `__write_scope__` you must add those values as permissions to the roles 
in Auth0. To use these in our scope comparisons they must be accessed from 
the `AUTH0_SCOPES` environmental variable passed in via Helm values. If this 
is not done the API will not have access to the correct scope in the 
user token and access will be denied.

## Creating SQLAlchemy DB Migration

1. Run `make shell` to start the poetry environment which has dependencies available.
2. Run `make generate-migration MESSAGE="message"` to generate the 
   SQLAlchemy database migration file. The "message" is a commit message 
   similar to a git commit message. DB migration files save to
   /migrations/versions.
3. add, commit and push the new migration to github along with code changes that cause the change.

1:warning: You must commit code that is compatible with the current and your new database schema along with the database migration.  The code changes will be pushed _before_ the schema changes, so new code must be backward compatible to the currently running schema.

For more information please read [Deploying the App to Dev, Stage, and Prod](#deploying-the-app-to-dev-stage-and-prod)
  
## Running Terraform

Included in this repository are terraform builds for AWS resources. These files can be found in terraform/aws/*. A seperate CI/CD pipeline is used to run the terraform and can be found in deploy/tf_codefresh.yaml. README files and makefiles can be found in each of the environment folders in the terraform folder.

## Using the Production Optimized Image Locally 

The image used in deployments consists of static html & javascript files,
wheras the image normally used in local development is served dynamically from
npm.  

* If you want to try out the static image locally, you can set the Tilt
config variable by setting use_optimized_dockerfile to true or false (json
booleans) in tilt_config.json.
* You can even change which one live by running
  * `tilt args -- --use_optimized_dockerfile=false`
  * `tilt args -- --use_optimized_dockerfile=true`


## Deploying the App to Dev, Stage, and Prod
- Dev:
To deploy the app into the Dev environment simply merge your feature branch into the `main` branch.  This will trigger a codefresh pipeline which will deploy your change to the dev Kubernetes cluster.

- Stage:
In order promote what is in the dev environment to stage create a release  in github based off what is in the main branch. This will trigger a codefresh pipeline which will deploy your change to the stage Kubernetes cluster.  ***The release tag that is created must follow the semantic versioning format ex: `v1.0.1`. If the version tag does not match this regex `^v[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}$` the promotion to stage will be skipped.***

- Prod:
The production promotion requires a manual trigger of the [Prod Deploy Pipeline](https://g.codefresh.io/pipelines/edit/workflow?id=61145a5f4acb985991676682&pipeline=deploy-prod&projects=Sourcerer&projectId=611455c3c6599f9bd2cf719b&rightbar=variables&context=srv-infrastructure).  Update `IMAGE_TAG` pipeline variable to the release version that you want deployed and click the `RUN` button.

## Updating Secrets for Environments

All secrets for deployments are stored in the deploy/helm directory in files named `<environment>.secrets.yaml`.

To change a secret:
1. `sops  <filename>`
Will open an editor (your $EDITOR env var) you can change the file and save it.

### Database Migration Notes

Run `flask db` to get a help messge and find more.
