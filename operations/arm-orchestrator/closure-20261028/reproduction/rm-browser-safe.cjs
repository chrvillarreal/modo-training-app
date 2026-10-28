const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const original=chromium.launch.bind(chromium);
chromium.launch=async options=>{
 const browser=await original({...options,args:[...(options.args||[]),'--no-sandbox','--disable-dev-shm-usage']});
 const newPage=browser.newPage.bind(browser);
 browser.newPage=async(...args)=>{const page=await newPage(...args);await page.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());return page;};
 return browser;
};
require('/workspace/work/phase2-rm/tests/browser.cjs');
