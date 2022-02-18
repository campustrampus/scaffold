# Source Data Portal
This web application will be used to replace the load sources tool and the SSOT spreadsheet. It is for 
internal use only.

## Requirements For Local UI Development
Follow [Project README](../README.md)
node.js
yarn (`npm install --global yarn`)

## Local install
Run `make up` from the root of this repository to bring up the environment

## Installing npm packages locally
In the `web` directory, you can run:
### `yarn install`

## Available Scripts
In the `web` directory, you can run:

### `yarn run start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more 
information.

### `yarn run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will 
remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right 
into your project so you have full control over them. All of the commands except `eject` will still work, but they will 
point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you 
shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t 
customize it when you are ready for it.

## Learn More
You can learn more in the 
[Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the 
[React documentation](https://reactjs.org/).

### Code Splitting
This section has moved here: 
[https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size
This section has moved here: 
[https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: 
[https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: 
[https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: 
[https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `yarn run build` fails to minify

This section has moved here: 
[https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

### Yarn & transitive dependencies

#### TL;DR
Add the desired version to the "resolutions" section in package.json

#### Long Version

A transitive dependency is when something we depend on depends on something else.  Normally, we'd be up the canal without a pole, but Yarn has [selective version resolution](https://classic.yarnpkg.com/en/docs/selective-version-resolutions/) which means we can just tell it to use a newer version anyways.  To do that, you just stick the desired version in the resolutions section in package.json.

#### Audit

Run `yarn audit` to see what it's not happy about and to test if your "resolutions" are working.  You can copy the package names and versions right out of the output.  In fact, I'm surpised it doesn't offer to do the update for you.
