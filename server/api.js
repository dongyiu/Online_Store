import express from 'express'
import bodyParser from 'body-parser'
import { connectToDatabase, addItem, deleteItem } from '../database/mongodb'

const app = express()
const cache = new Map()

app.use(bodyParser.json())

connectToDatabase(cache)

app.get('/items', (req, res) => {
    res.json(Array.from(cache.values()))
})

app.post('/item', async (req, res) => {
    const { itemName, itemPrice, itemPicture } = req.query
    const item = await addItem(cache, itemName, itemPrice, itemPicture)
    res.json(item)
})

app.delete('/item', async (req, res) => {
    const { itemId } = req.query
    const item = await deleteItem(cache, itemId)
    res.json(item)
})

export default app
