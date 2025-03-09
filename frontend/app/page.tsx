import { Button } from '@/components/ui/button';
import { ArrowRight, Bot, Calendar, LineChart } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between px-4 md:px-8">
          <div className="flex items-center gap-2 font-semibold">
            <Bot className="h-6 w-6" />
            <span>DevMarketer</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost">Log in</Button>
            </Link>
            <Link href="/login">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="px-4 py-20 md:py-32 md:px-8">
          <div className="container">
            <div className="mx-auto max-w-3xl text-center">
              <h1 className="mb-6 text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
                Automate Your Social Media Marketing with{' '}
                <span className="text-primary">AI</span>
              </h1>
              <p className="mb-8 text-lg text-muted-foreground md:text-xl">
                Save time and boost engagement with AI-powered content generation,
                smart scheduling, and analytics for X, Reddit, and Product Hunt.
              </p>
              <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
                <Link href="/login">
                  <Button size="lg" className="w-full sm:w-auto">
                    Start Free Trial
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
                <Button size="lg" variant="outline" className="w-full sm:w-auto">
                  Watch Demo
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="border-t bg-muted/50 px-4 py-20 md:px-8">
          <div className="container">
            <h2 className="mb-12 text-center text-3xl font-bold tracking-tight sm:text-4xl">
              Everything You Need to Scale Your Social Presence
            </h2>
            <div className="grid gap-8 md:grid-cols-3">
              <div className="rounded-lg border bg-card p-6">
                <Bot className="mb-4 h-8 w-8 text-primary" />
                <h3 className="mb-2 text-xl font-semibold">AI Content Generation</h3>
                <p className="text-muted-foreground">
                  Generate engaging posts with GPT-4, optimized for each platform's unique
                  audience and format.
                </p>
              </div>
              <div className="rounded-lg border bg-card p-6">
                <Calendar className="mb-4 h-8 w-8 text-primary" />
                <h3 className="mb-2 text-xl font-semibold">Smart Scheduling</h3>
                <p className="text-muted-foreground">
                  Schedule posts at optimal times and manage your content calendar with
                  ease.
                </p>
              </div>
              <div className="rounded-lg border bg-card p-6">
                <LineChart className="mb-4 h-8 w-8 text-primary" />
                <h3 className="mb-2 text-xl font-semibold">Analytics & A/B Testing</h3>
                <p className="text-muted-foreground">
                  Track performance and optimize your content strategy with detailed
                  analytics and A/B testing.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t px-4 py-6 md:px-8">
        <div className="container flex flex-col items-center justify-between gap-4 md:flex-row">
          <div className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            <span className="text-sm font-semibold">DevMarketer</span>
          </div>
          <p className="text-sm text-muted-foreground">
            © 2024 DevMarketer. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}