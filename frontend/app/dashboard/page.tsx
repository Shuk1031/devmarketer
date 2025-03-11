'use client';

import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PlusCircle, BarChart3, Calendar, Settings } from 'lucide-react';

const features = [
  {
    title: 'Create Post',
    description: 'Generate engaging content with AI',
    icon: <PlusCircle className="h-6 w-6" />,
    href: '/posts/create',
  },
  {
    title: 'Schedule',
    description: 'Manage your posting schedule',
    icon: <Calendar className="h-6 w-6" />,
    href: '/schedule',
  },
  {
    title: 'Analysis',
    description: 'Track your content performance',
    icon: <BarChart3 className="h-6 w-6" />,
    href: '/analysis',
  },
  {
    title: 'Settings',
    description: 'Configure your account',
    icon: <Settings className="h-6 w-6" />,
    href: '/settings',
  },
];

export default function DashboardPage() {
  return (
    <div className="container max-w-7xl py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Welcome to DevMarketer</h1>
        <p className="text-muted-foreground">
          Automate your social media presence and grow your audience
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {features.map((feature) => (
          <Card
            key={feature.title}
            className="transform transition-all duration-200 hover:scale-105 hover:shadow-lg"
          >
            <Link href={feature.href}>
              <CardHeader>
                <div className="mb-2 rounded-full bg-primary/10 p-2 w-fit">
                  {feature.icon}
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
            </Link>
          </Card>
        ))}
      </div>

      <div className="mt-12">
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Get started with these common tasks</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Button asChild className="w-full">
              <Link href="/posts/create">
                <PlusCircle className="mr-2 h-4 w-4" />
                New Post
              </Link>
            </Button>
            <Button asChild variant="outline" className="w-full">
              <Link href="/schedule">View Schedule</Link>
            </Button>
            <Button asChild variant="outline" className="w-full">
              <Link href="/analysis">View Analytics</Link>
            </Button>
            <Button asChild variant="outline" className="w-full">
              <Link href="/settings">Account Settings</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}