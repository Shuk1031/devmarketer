import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowRight, Sparkles, Target, Zap } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col">
      <section className="container space-y-6 py-8 md:py-12 lg:py-24">
        <div className="mx-auto flex max-w-[64rem] flex-col items-center gap-4 text-center">
          <h1 className="font-heading text-3xl sm:text-5xl md:text-6xl lg:text-7xl">
            Automate Your{' '}
            <span className="bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
              Developer Marketing
            </span>
          </h1>
          <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
            AI-powered social media automation for developers. Schedule posts, analyze engagement, and grow your audience with DevMarketer.
          </p>
          <div className="flex gap-4">
            <Button asChild size="lg">
              <Link href="/login">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" size="lg">
              Learn More
            </Button>
          </div>
        </div>
      </section>

      <section className="container py-8 md:py-12 lg:py-24">
        <div className="mx-auto grid justify-center gap-4 sm:grid-cols-2 md:max-w-[64rem] md:grid-cols-3">
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Sparkles className="h-12 w-12 text-purple-500" />
              <div className="space-y-2">
                <h3 className="font-bold">AI-Powered Content</h3>
                <p className="text-sm text-muted-foreground">
                  Generate engaging posts with GPT-4 technology.
                </p>
              </div>
            </div>
          </div>
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Target className="h-12 w-12 text-pink-500" />
              <div className="space-y-2">
                <h3 className="font-bold">A/B Testing</h3>
                <p className="text-sm text-muted-foreground">
                  Compare engagement across different platforms.
                </p>
              </div>
            </div>
          </div>
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Zap className="h-12 w-12 text-yellow-500" />
              <div className="space-y-2">
                <h3 className="font-bold">Smart Scheduling</h3>
                <p className="text-sm text-muted-foreground">
                  Post at optimal times for maximum reach.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}