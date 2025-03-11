'use client';

import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Github, Twitter, Mail } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useToast } from '@/hooks/use-toast';

export default function LoginPage() {
  const router = useRouter();
  const { toast } = useToast();

  const handleOAuthLogin = async (provider: 'github' | 'twitter' | 'google') => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider,
        options: {
          redirectTo: `${window.location.origin}/dashboard`,
        },
      });

      if (error) {
        throw error;
      }
    } catch (error) {
      toast({
        title: 'Authentication Error',
        description: 'Failed to sign in. Please try again.',
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-gradient-to-b from-background to-muted/20 p-4">
      <Card className="w-full max-w-md transform transition-all hover:translate-y-[-4px] hover:shadow-lg">
        <CardHeader className="space-y-2 text-center">
          <CardTitle className="text-3xl font-bold">Welcome Back</CardTitle>
          <CardDescription className="text-lg">
            Sign in to continue to DevMarketer
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 p-6">
          <Button
            variant="outline"
            size="lg"
            className="w-full gap-2 text-lg"
            onClick={() => handleOAuthLogin('github')}
          >
            <Github className="h-5 w-5" />
            Continue with GitHub
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="w-full gap-2 text-lg"
            onClick={() => handleOAuthLogin('twitter')}
          >
            <Twitter className="h-5 w-5" />
            Continue with Twitter
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="w-full gap-2 text-lg"
            onClick={() => handleOAuthLogin('google')}
          >
            <Mail className="h-5 w-5" />
            Continue with Google
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}