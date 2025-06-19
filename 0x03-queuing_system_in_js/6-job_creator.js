#!/usr/bin/node
import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
  phoneNumber: '+233246168395',
  message: 'Your account has been created successfully',
};

const job = queue.create('push_notification_code', jobData);
job.save((err) => {
    if (!err) console.log(`Notification job created: ${job.id}`);
  });

job.on('complete', (result) => {
  console.log('Notification job completed');
});

job.on('failed', (err) => {
  console.log('Notification job failed');
});