#!/usr/bin/env yarn dev
import { createClient, print } from 'redis';

const redisClient = createClient();

redisClient.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error.message}`);
});

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

const setNewSchool = (schoolName, value) => {
  redisClient.SET(schoolName, value, print);
};

const displaySchoolValue = (schoolName) => {
  redisClient.GET(schoolName, (error, reply) => {
    if (error) {
      console.error(`Error fetching value for ${schoolName}: ${error.message}`);
      return;
    }
    console.log(reply);
  });
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
