import database from 'mongoose'
import itemSchema from './itemSchema'

export async function connectToDatabase(cache) {
  database.connect('mongodb://localhost:27017/online_store', { useNewUrlParser: true, useUnifiedTopology: true })
  database.connection.on('connected', () => {
    process.stdout.write('[\'BOOT\'] Connected to MongoDB database!\n')
    cache ? createCache(cache) : null
  })
  database.connection.on('err', (err) => {
    process.stdout.write('[\'ERROR\'] Error connecting to MongoDB database!\n')
  })
  database.connection.on('disconnected', () => {
    process.stdout.write('[\'INFO\'] Disconnected from MongoDB database!\n')
  })
}

export async function createCache(cache) {
  const itemData = await itemSchema.find({});
  itemData.forEach(async (item) => {
    cache.set(item.itemId, item);
  });
}

export async function addItem(cache, itemName, itemPrice, itemPicture) {
  const item = new itemSchema({
    itemName: itemName,
    itemPrice: itemPrice,
    itemPicture: itemPicture
  });
  await item.save();
  cache.set(item.itemId, item);
  return item;
}

export async function deleteItem(cache, itemId) {
  await itemSchema.findOneAndDelete({ itemId: itemId });
  cache.delete(itemId);
  return cache;
}