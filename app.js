// JavaScript source code for websocket server
// Credit to https://www.textcontrol.com/blog/2020/01/01/creating-a-websocket-server-project-with-nodejs/
const { WebSocketServer } = require('@txtextcontrol/tx-websocket-server');
const express = require('express');
const app = express();
const server = app.listen(8080);

var wsServer = new WebSocketServer(server);