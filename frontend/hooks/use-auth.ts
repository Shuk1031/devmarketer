'use client';

import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

export type UserProfile = {
  id: string;
  email: string;
  name: string;
  avatar_url: string | null;
  auth_provider: 'github' | 'twitter' | 'google';
  plan: 'free' | 'pro';
  created_at: string;
};

export function useAuth() {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      // Simulate API call
      setTimeout(() => {
        const mockUser: UserProfile = {
          id: '123',
          email: 'developer@example.com',
          name: 'John Developer',
          avatar_url: 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=180&h=180&fit=crop',
          auth_provider: 'github',
          plan: 'free',
          created_at: '2024-01-01T00:00:00Z',
        };
        setUser(mockUser);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching user:', error);
      setLoading(false);
    }
  };

  const upgradeToPro = async () => {
    console.log('Upgrading to Pro plan...');
    // In a real app, this would redirect to a payment page
    return true;
  };

  const disconnectProvider = async (provider: 'github' | 'twitter' | 'google') => {
    console.log(`Disconnecting ${provider}...`);
    // In a real app, this would call Supabase to unlink the provider
    return true;
  };

  return {
    user,
    loading,
    upgradeToPro,
    disconnectProvider,
  };
}