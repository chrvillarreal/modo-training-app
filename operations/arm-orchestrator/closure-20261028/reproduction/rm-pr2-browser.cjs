const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const launch=chromium.launch.bind(chromium);
chromium.launch=options=>launch({...options,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage']});
process.env.RM_TEST_URL=process.env.APP_URL+'/';
process.env.RM_EVIDENCE='/workspace/work/phase2/rm-pr2-screenshots';
require('/workspace/work/phase2-rm-pr2/tests/'+process.argv[2]);
