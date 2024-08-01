#!/usr/bin/env yarn dev
import { createClient } from 'redis';

const redisClient = createClient();
const EXIT_MESSAGE = 'KILL_SERVER';

redisClient.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error.message}`);
});

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

redisClient.subscribe('holberton school channel');

redisClient.on('message', (error, message) => {
  if (error) {
    console.error(`Error receiving message: ${error.message}`);
    return;
  }
  console.log(message);
  if (message === EXIT_MESSAGE) {
    redisClient.unsubscribe();
    redisClient.quit();
  }
});
