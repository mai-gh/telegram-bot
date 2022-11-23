const req = require('http-promise');
const HTMLParser = require('node-html-parser');



const main = async () => {
  const resp = await req({
    method: 'GET',
    protocol: 'https:',
    host: 'store.steampowered.com',
    path: '/app/1215170/Dawnthorn/'
  })
//  console.log(resp.data)
  const root = HTMLParser.parse(resp.data);
  console.log(root.querySelector('.release_date > .date').innerHTML)
}

main();
