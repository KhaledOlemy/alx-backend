#!/usr/bin/env yarn dev
import { promisify } from 'util';
import { createClient, print } from 'redis';

const redisClient = createClient();

redisClient.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error.message}`);
});

const setNewSchool = (schoolName, value) => {
  redisClient.SET(schoolName, value, print);
};

const displaySchoolValue = async (schoolName) => {
  const getAsync = promisify(redisClient.GET).bind(redisClient);
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (error) {
    console.error(`Error fetching value for ${schoolName}: ${error.message}`);
  }
};

async function main() {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}

redisClient.on('connect', async () => {
  console.log('Redis client connected to the server');
  await main();
});
