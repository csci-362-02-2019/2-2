'use strict';

function mgdlToMMOL(mgdl) {
  //return (Math.round((mgdl / 18) * 10).toFixed(1)/10); #Original Code
  return ((mgdl / 18) * 10).toFixed(1)/10); //Fault Injection #4
}

function mmolToMgdl(mgdl) {
  return Math.round(mgdl * 18);
}

function configure() {
  return {
    mgdlToMMOL: mgdlToMMOL
    , mmolToMgdl: mmolToMgdl
  };
}

// original export
// module.exports = configure;

// modified export
module.exports = {
  mmolToMgdl,
  mgdlToMMOL
}
