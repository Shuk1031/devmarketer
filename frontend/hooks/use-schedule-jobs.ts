'use client';

import { useState, useEffect } from 'react';

export type ScheduledJob = {
  id: string;
  content: string;
  platform: 'twitter' | 'reddit' | 'producthunt';
  scheduledFor: string;
  status: 'pending' | 'completed' | 'cancelled';
};

export function useScheduleJobs() {
  const [jobs, setJobs] = useState<ScheduledJob[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    // Simulate API call
    setTimeout(() => {
      const mockJobs: ScheduledJob[] = [
        {
          id: '1',
          content: '🚀 Excited to share my latest dev tool! Check it out and let me know what you think!',
          platform: 'twitter',
          scheduledFor: '2025-04-15T10:00:00Z',
          status: 'pending',
        },
        {
          id: '2',
          content: 'Just launched on Product Hunt! Would love your feedback on this new developer productivity tool.',
          platform: 'producthunt',
          scheduledFor: '2025-04-16T15:30:00Z',
          status: 'pending',
        },
        {
          id: '3',
          content: 'New blog post: "10x Your Development Workflow" - sharing my insights on building better tools.',
          platform: 'reddit',
          scheduledFor: '2025-04-17T08:00:00Z',
          status: 'pending',
        },
      ];
      setJobs(mockJobs);
      setLoading(false);
    }, 1000);
  };

  const cancelJob = async (jobId: string) => {
    // Simulate API call
    setJobs((prevJobs) =>
      prevJobs.map((job) =>
        job.id === jobId ? { ...job, status: 'cancelled' } : job
      )
    );
    return true;
  };

  return {
    jobs,
    loading,
    cancelJob,
  };
}