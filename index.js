const csv = require('csv-parser')
const fs = require('fs')
const { connectToDatabase, addItem } = require('./database')
connectToDatabase().then(() => {
    fs.createReadStream('./Online Store Project Items for Sale.csv')
    .pipe(csv())
    .on('data', async (row) => {
        const loop = Number(row['Number of items']) || 1
        for (let i = 0; i < loop; i++) {
            await addItem(row['Description'], row['Price(�)'] || row['Price (�)'], row['Item Picture'])
        }
    })
    .on('end', () => {
        console.log('CSV file successfully processed')
    })
})


