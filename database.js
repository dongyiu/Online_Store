const database = require('mongoose');
const mongoose = require('mongoose');
const { v4: uuidv4 } = require('uuid');

const itemSchemaa = new mongoose.Schema({
  itemId: {
    type: String,
    unique: true,
    required: true,
    default: uuidv4,
  },
  itemName: {
    type: String,
    required: true,
  },
  itemPicture: {
    type: String,
    default: 'https://via.placeholder.com/350x150',
  },
  itemPrice: {
    type: Number,
    required: true,
  }
});

const itemSchema = mongoose.model('Item', itemSchemaa);

module.exports.connectToDatabase = async function() {
  await database.connect('mongodb://localhost:27017/online_store', { useNewUrlParser: true, useUnifiedTopology: true })
  database.connection.on('connected', () => {
    process.stdout.write('[\'BOOT\'] Connected to MongoDB database!\n')
  })
  database.connection.on('err', (err) => {
    process.stdout.write('[\'ERROR\'] Error connecting to MongoDB database!\n')
  })
  database.connection.on('disconnected', () => {
    process.stdout.write('[\'INFO\'] Disconnected from MongoDB database!\n')
  })
}

module.exports.addItem =  async function(itemName, itemPrice, itemPicture) {
  const item = new itemSchema({
    itemName: itemName,
    itemPrice: itemPrice,
    itemPicture: itemPicture
  });
  await item.save();
  return item;
}

module.exports.deleteItem =  async function(cache, itemId) {
  await itemSchema.findOneAndDelete({ itemId: itemId });
  return cache;
}