import mongoose from 'mongoose';
import { v4 as uuidv4 } from 'uuid';

const itemSchema = new mongoose.Schema({
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

export default mongoose.model('Item', itemSchema);
