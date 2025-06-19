import { createClient } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err);
});

await client.connect();

await client.hSet('HolbertonSchools', 'Portland', 50);
await client.hSet('HolbertonSchools', 'Seattle', 80);
await client.hSet('HolbertonSchools', 'New York', 20);
await client.hSet('HolbertonSchools', 'Bogota', 20);
await client.hSet('HolbertonSchools', 'Cali', 40);
await client.hSet('HolbertonSchools', 'Paris', 2);

const res = await client.hGetAll('HolbertonSchools');
console.log(res);

await client.quit();
