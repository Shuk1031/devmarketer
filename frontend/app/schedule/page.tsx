'use client';

import { useState } from 'react';
import { format, parseISO } from 'date-fns';
import { Calendar } from '@/components/ui/calendar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useScheduleJobs } from '@/hooks/use-schedule-jobs';
import { Twitter, FileText, Award, Loader2, Calendar as CalendarIcon, List } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';

const platformIcons = {
  twitter: <Twitter className="h-4 w-4" />,
  reddit: <FileText className="h-4 w-4" />,
  producthunt: <Award className="h-4 w-4" />,
};

export default function SchedulePage() {
  const { jobs, loading, cancelJob } = useScheduleJobs();
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());
  const { toast } = useToast();

  const handleCancel = async (jobId: string) => {
    try {
      await cancelJob(jobId);
      toast({
        title: 'Post cancelled',
        description: 'The scheduled post has been cancelled successfully.',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to cancel the scheduled post.',
        variant: 'destructive',
      });
    }
  };

  if (loading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container max-w-7xl py-8">
      <Tabs defaultValue="calendar" className="space-y-8">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Scheduled Posts</h1>
          <TabsList>
            <TabsTrigger value="calendar" className="space-x-2">
              <CalendarIcon className="h-4 w-4" />
              <span>Calendar</span>
            </TabsTrigger>
            <TabsTrigger value="list" className="space-x-2">
              <List className="h-4 w-4" />
              <span>List</span>
            </TabsTrigger>
          </TabsList>
        </div>

        <TabsContent value="calendar" className="space-y-8">
          <div className="grid gap-8 lg:grid-cols-[1fr,300px]">
            <Card>
              <CardContent className="pt-6">
                <Calendar
                  mode="single"
                  selected={selectedDate}
                  onSelect={setSelectedDate}
                  className="rounded-md border"
                />
              </CardContent>
            </Card>

            <div className="space-y-4">
              <h2 className="text-lg font-semibold">
                Scheduled for{' '}
                {selectedDate && format(selectedDate, 'MMMM d, yyyy')}
              </h2>
              {jobs
                .filter(
                  (job) =>
                    job.status === 'pending' &&
                    format(parseISO(job.scheduledFor), 'yyyy-MM-dd') ===
                      format(selectedDate || new Date(), 'yyyy-MM-dd')
                )
                .map((job) => (
                  <Card key={job.id} className="transform transition-all hover:shadow-md">
                    <CardContent className="pt-6">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1 space-y-1">
                          <div className="flex items-center gap-2">
                            {platformIcons[job.platform]}
                            <span className="text-sm text-muted-foreground">
                              {format(parseISO(job.scheduledFor), 'h:mm a')}
                            </span>
                          </div>
                          <p className="text-sm">{job.content}</p>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleCancel(job.id)}
                        >
                          Cancel
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="list">
          <Card>
            <CardHeader>
              <CardTitle>All Scheduled Posts</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {jobs
                .filter((job) => job.status === 'pending')
                .map((job) => (
                  <div
                    key={job.id}
                    className="flex items-center justify-between gap-4 rounded-lg border p-4"
                  >
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center gap-2">
                        {platformIcons[job.platform]}
                        <span className="text-sm font-medium">
                          {format(parseISO(job.scheduledFor), 'MMM d, yyyy h:mm a')}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground">{job.content}</p>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleCancel(job.id)}
                    >
                      Cancel
                    </Button>
                  </div>
                ))}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}