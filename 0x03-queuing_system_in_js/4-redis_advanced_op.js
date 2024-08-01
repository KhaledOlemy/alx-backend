#!/usr/bin/env yarn dev
import { createClient, print } from 'redis';

const redisClient = createClient();

redisClient.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error.message}`);
});

const updateHash = (hashName, fieldName, fieldValue) => {
  redisClient.HSET(hashName, fieldName, fieldValue, print);
};

const printHash = (hashName) => {
  redisClient.HGETALL(hashName, (error, reply) => {
    if (error) {
      console.error(`Error fetching hash ${hashName}: ${error.message}`);
      return;
    }
    console.log(reply);
  });
};

function main() {
  const schoolData = {
    'Portland': 50,
    'Seattle': 80,
    'New York': 20,
    'Bogota': 20,
    'Cali': 40,
    'Paris': 2,
  };
  for (const [city, value] of Object.entries(schoolData)) {
    updateHash('HolbertonSchools', city, value);
  }
  printHash('HolbertonSchools');
}

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
  main();
});
