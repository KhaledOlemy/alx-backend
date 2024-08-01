#!/usr/bin/env yarn dev
import { Queue, Job } from 'kue';

/**
 * Creates push notification jobs from the array of jobs info.
 * @param {Object[]} jobs - Array of job information objects.
 * @param {Queue} queue - Kue queue instance.
 */
export const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }
  for (const jobInfo of jobs) {
    const notificationJob = queue.create('push_notification_code_3', jobInfo);

    notificationJob
      .on('enqueue', () => {
        console.log(`Notification job created: ${notificationJob.id}`);
      })
      .on('complete', () => {
        console.log(`Notification job ${notificationJob.id} completed`);
      })
      .on('failed', (error) => {
        console.error(`Notification job ${notificationJob.id} failed: ${error.message || error.toString()}`);
      })
      .on('progress', (progress) => {
        console.log(`Notification job ${notificationJob.id} ${progress}% complete`);
      });
    notificationJob.save();
  }
};

export default createPushNotificationsJobs;
