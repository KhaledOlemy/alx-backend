#!/usr/bin/env yarn dev
import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

const productsList = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

const getItemById = (id) => {
  const item = productsList.find((obj) => obj.itemId === id);
  return item ? { ...item } : null;
};

const app = express();
const redisClient = createClient();
const PORT = 1245;

/**
 * Modifies the reserved stock for a given item.
 * @param {number} itemId - The id of the item.
 * @param {number} stock - The stock of the item.
 * @returns {Promise<void>}
 */
const reserveStockById = async (itemId, stock) => {
  const setAsync = promisify(redisClient.SET).bind(redisClient);
  await setAsync(`item.${itemId}`, stock);
};

/**
 * Retrieves the reserved stock for a given item.
 * @param {number} itemId - The id of the item.
 * @returns {Promise<number>}
 */
const getCurrentReservedStockById = async (itemId) => {
  const getAsync = promisify(redisClient.GET).bind(redisClient);
  const result = await getAsync(`item.${itemId}`);
  return result ? parseInt(result, 10) : 0;
};

app.get('/list_products', (_, res) => {
  res.json(productsList);
});

app.get('/list_products/:itemId(\\d+)', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const productItem = getItemById(itemId);

  if (!productItem) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  productItem.currentQuantity = productItem.initialAvailableQuantity - reservedStock;
  res.json(productItem);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const productItem = getItemById(itemId);

  if (!productItem) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reservedStock = await getCurrentReservedStockById(itemId);

  if (reservedStock >= productItem.initialAvailableQuantity) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }

  await reserveStockById(itemId, reservedStock + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

const resetProductsStock = () => {
  const setAsync = promisify(redisClient.SET).bind(redisClient);
  return Promise.all(
    productsList.map((item) => setAsync(`item.${item.itemId}`, 0))
  );
};

app.listen(PORT, () => {
  resetProductsStock().then(() => {
    console.log(`API available on localhost port ${PORT}`);
  });
});

export default app;
