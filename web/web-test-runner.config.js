// NODE_ENV=test - Needed by "@snowpack/web-test-runner-plugin"
//
chromeLauncher = require('@web/test-runner').chromeLauncher
process.env.NODE_ENV = "test";

module.exports = {
  browsers: [chromeLauncher({ launchOptions: { args: ['--no-sandbox'] } })],
  plugins: [require("@snowpack/web-test-runner-plugin")()],
};
