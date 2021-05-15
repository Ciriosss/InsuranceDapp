const HAMSAToken = artifacts.require("HAMSAToken");

module.exports = function (deployer) {
  deployer.deploy(HAMSAToken);
};
