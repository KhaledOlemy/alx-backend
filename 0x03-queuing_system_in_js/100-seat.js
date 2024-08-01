#!/usr/bin/env yarn dev
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const app = express();
const redisClient = createClient({ name: 'reserve_seat' });
const queue = createQueue();
const INITIAL_SEATS_COUNT = 50;
let reservationEnabled = false;
const PORT = 1245;

/**
 * Modifies the number of available seats.
 * @param {number} number - The new number of seats.
 * @returns {Promise<void>}
 */
const reserveSeat = async (number) => {
  const setAsync = promisify(redisClient.SET).bind(redisClient);
  await setAsync('available_seats', number);
};

/**
 * Retrieves the number of available seats.
 * @returns {Promise<number>}
 */
const getCurrentAvailableSeats = async () => {
  const getAsync = promisify(redisClient.GET).bind(redisClient);
  const result = await getAsync('available_seats');
  return result ? parseInt(result, 10) : 0;
};

app.get('/available_seats', async (_, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservations are blocked' });
    return;
  }
  try {
    const job = queue.create('reserve_seat');

    job.on('failed', (error) => {
      console.error(`Seat reservation job ${job.id} failed: ${error.message || error.toString()}`);
    });

    job.on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    });

    job.save();
    res.json({ status: 'Reservation in process' });
  } catch {
    res.json({ status: 'Reservation failed' });
  }
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats > 0) {
      await reserveSeat(availableSeats - 1);
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
    reservationEnabled = availableSeats > 1;
  });
});

const resetAvailableSeats = async (initialSeatsCount) => {
  const setAsync = promisify(redisClient.SET).bind(redisClient);
  await setAsync('available_seats', parseInt(initialSeatsCount, 10));
};

app.listen(PORT, async () => {
  await resetAvailableSeats(process.env.INITIAL_SEATS_COUNT || INITIAL_SEATS_COUNT);
  reservationEnabled = true;
  console.log(`API available on localhost port ${PORT}`);
});

export default app;
