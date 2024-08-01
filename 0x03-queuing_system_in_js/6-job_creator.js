#!/usr/bin/env yarn dev
import { createQueue } from 'kue';

const notificationQueue = createQueue({ name: 'push_notification_code' });

const notificationJob = notificationQueue.create('push_notification_code', {
  phoneNumber: '01010267235',
  message: 'Account registered',
});

notificationJob
  .on('enqueue', () => {
    console.log(`Notification job created: ${notificationJob.id}`);
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed attempt', () => {
    console.error('Notification job failed');
  });

notificationJob.save();
