//const req = require('http-promise');
const req = require('../http-promise/http-promise.js');
const HTMLParser = require('node-html-parser');
const {token, chatId} = require('./config.json')
const api = new URL(`https://api.telegram.org/bot${token}/sendMessage`);

const main = async () => {
  const resp = await req({
    method: 'GET',
    protocol: 'https:',
    host: 'store.steampowered.com',
    path: '/app/1215170/Dawnthorn/'
  })
  const root = HTMLParser.parse(resp.data);
  console.log(root.querySelector('.release_date > .date').innerHTML)
}

const main2 = async () => {
  const resp = await req({
    method: 'POST',
    protocol: api.protocol,
    host: api.host,
    path: api.path,
    data: {
      chat_id: chatId,
      text: 'aaaaaaa',
    },
  })
  console.log(resp)
//  const root = HTMLParser.parse(resp.data);
//  console.log(root.querySelector('.release_date > .date').innerHTML)
}

main2();
