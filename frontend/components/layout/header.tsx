'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { ModeToggle } from '@/components/mode-toggle';
import { Laptop2 } from 'lucide-react';

export default function Header() {
  const pathname = usePathname();
  const isLoggedIn = pathname !== '/login';

  const navigation = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Posts', href: '/posts' },
    { name: 'Schedule', href: '/schedule' },
    { name: 'Analysis', href: '/analysis' },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center">
        <div className="mr-4 flex">
          <Link href="/" className="flex items-center space-x-2">
            <Laptop2 className="h-6 w-6" />
            <span className="font-bold">DevMarketer</span>
          </Link>
        </div>
        
        {isLoggedIn && (
          <nav className="flex flex-1 items-center space-x-6">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`text-sm font-medium transition-colors hover:text-primary ${
                  pathname === item.href
                    ? 'text-foreground'
                    : 'text-foreground/60'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        )}

        <div className="flex items-center space-x-4">
          <ModeToggle />
          {isLoggedIn ? (
            <Button
              variant="outline"
              size="sm"
              asChild
            >
              <Link href="/settings">Settings</Link>
            </Button>
          ) : (
            <Button size="sm" asChild>
              <Link href="/login">Sign In</Link>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
}