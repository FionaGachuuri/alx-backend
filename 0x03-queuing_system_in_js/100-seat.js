import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const port = 1245;
const queue = kue.createQueue();

// Redis setup
const client = createClient();
client.on('error', (err) => console.error('Redis error:', err));
client.on('connect', () => console.log('Redis connected'));

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Global reservation toggle
let reservationEnabled = true;

// Initialize seats
const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return parseInt(seats || 0, 10);
};

// Set initial seat count
reserveSeat(50);

// Routes

// GET /available_seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// GET /reserve_seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
    } else {
      res.json({ status: 'Reservation failed' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  }).on('failed', (errMsg) => {
    console.log(`Seat reservation job ${job.id} failed: ${errMsg}`);
  });
});

// GET /process
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();

    if (currentSeats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    const updatedSeats = currentSeats - 1;
    await reserveSeat(updatedSeats);

    if (updatedSeats === 0) {
      reservationEnabled = false;
    }

    return done();
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
