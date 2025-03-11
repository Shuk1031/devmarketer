'use client';

import { format } from 'date-fns';
import { useAuth } from '@/hooks/use-auth';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Loader2, Github, Twitter, Mail, Crown, Trash2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const providerIcons = {
  github: <Github className="h-4 w-4" />,
  twitter: <Twitter className="h-4 w-4" />,
  google: <Mail className="h-4 w-4" />,
};

export default function SettingsPage() {
  const { user, loading, upgradeToPro, disconnectProvider } = useAuth();
  const { toast } = useToast();

  if (loading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const handleUpgrade = async () => {
    try {
      await upgradeToPro();
      toast({
        title: 'Success',
        description: 'You have been upgraded to Pro plan!',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to upgrade plan. Please try again.',
        variant: 'destructive',
      });
    }
  };

  const handleDisconnect = async (provider: 'github' | 'twitter' | 'google') => {
    try {
      await disconnectProvider(provider);
      toast({
        title: 'Success',
        description: `Disconnected from ${provider}`,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: `Failed to disconnect from ${provider}`,
        variant: 'destructive',
      });
    }
  };

  if (!user) return null;

  return (
    <div className="container max-w-4xl space-y-8 py-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Settings</h1>
        <Badge variant={user.plan === 'pro' ? 'default' : 'outline'} className="text-sm">
          {user.plan === 'pro' ? (
            <span className="flex items-center gap-1">
              <Crown className="h-3 w-3" /> Pro Plan
            </span>
          ) : (
            'Free Plan'
          )}
        </Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Profile</CardTitle>
          <CardDescription>
            Manage your account settings and connected services
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center gap-4">
            <Avatar className="h-20 w-20">
              <AvatarImage src={user.avatar_url || ''} />
              <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
            </Avatar>
            <div>
              <h2 className="text-xl font-semibold">{user.name}</h2>
              <p className="text-sm text-muted-foreground">{user.email}</p>
              <p className="text-xs text-muted-foreground">
                Member since {format(new Date(user.created_at), 'MMMM yyyy')}
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="font-medium">Connected Accounts</h3>
            <div className="grid gap-4">
              {(['github', 'twitter', 'google'] as const).map((provider) => (
                <div
                  key={provider}
                  className="flex items-center justify-between rounded-lg border p-4"
                >
                  <div className="flex items-center gap-3">
                    {providerIcons[provider]}
                    <span className="capitalize">{provider}</span>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-muted-foreground hover:text-destructive"
                    onClick={() => handleDisconnect(provider)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
        {user.plan === 'free' && (
          <CardFooter>
            <Button
              className="w-full"
              size="lg"
              onClick={handleUpgrade}
            >
              <Crown className="mr-2 h-4 w-4" />
              Upgrade to Pro
            </Button>
          </CardFooter>
        )}
      </Card>

      {user.plan === 'free' && (
        <Card>
          <CardHeader>
            <CardTitle>Pro Plan Benefits</CardTitle>
            <CardDescription>
              Unlock advanced features and higher usage limits
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-lg border p-4">
              <h3 className="font-medium">Unlimited Posts</h3>
              <p className="text-sm text-muted-foreground">
                Schedule as many posts as you need
              </p>
            </div>
            <div className="rounded-lg border p-4">
              <h3 className="font-medium">Advanced Analytics</h3>
              <p className="text-sm text-muted-foreground">
                Deep insights into your content performance
              </p>
            </div>
            <div className="rounded-lg border p-4">
              <h3 className="font-medium">Priority Support</h3>
              <p className="text-sm text-muted-foreground">
                Get help when you need it most
              </p>
            </div>
            <div className="rounded-lg border p-4">
              <h3 className="font-medium">Custom Branding</h3>
              <p className="text-sm text-muted-foreground">
                Add your brand's personal touch
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}