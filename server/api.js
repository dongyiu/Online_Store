import express from 'express'
import bodyParser from 'body-parser'
import { connectToDatabase, addItem, deleteItem } from '../database/mongodb'
import WebSocket from 'ws'

const app = express()
const cache = new Map()
const ws = new WebSocket.Server({ port: 8080 });
const clients = new Set();

ws.on('connection', (ws) => {
    clients.add(ws);
  
    ws.on('close', () => {
      clients.delete(ws);
    });
  });

  function broadcast(message) {
    for (const client of clients) {
      client.send(JSON.stringify(message));
    }
  }
app.use(bodyParser.json())

connectToDatabase(cache)

app.get('/items', (req, res) => {
    res.json(Array.from(cache.values()))
})

app.post('/item', async (req, res) => {
    const { itemName, itemPrice, itemPicture } = req.query
    const item = await addItem(cache, itemName, itemPrice, itemPicture)
    res.json(item)
    broadcast({ type: 'ADD', item })
})

app.delete('/item', async (req, res) => {
    const { itemId } = req.query
    const item = await deleteItem(cache, itemId)
    res.json(item)
    broadcast({ type: 'DELETE', itemId })
})

export default app
