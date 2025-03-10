'use client';

import { useState, useEffect } from 'react';

export type PostVariant = {
  id: string;
  content: string;
  metrics: {
    likes: number;
    comments: number;
    shares: number;
    clicks: number;
  };
};

export type Post = {
  id: string;
  title: string;
  platform: 'twitter' | 'reddit' | 'producthunt';
  variantA: PostVariant;
  variantB: PostVariant;
  winner?: 'A' | 'B';
};

export function usePostAnalysis() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);
  const [isFetching, setIsFetching] = useState(false);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    // Simulate API call
    setTimeout(() => {
      const mockPosts: Post[] = [
        {
          id: '1',
          title: 'DevTools Launch',
          platform: 'twitter',
          variantA: {
            id: 'a',
            content: '🚀 Launching our new developer tools! Check it out!',
            metrics: { likes: 150, comments: 45, shares: 30, clicks: 80 },
          },
          variantB: {
            id: 'b',
            content: '💻 New dev tools that boost productivity by 10x!',
            metrics: { likes: 180, comments: 60, shares: 40, clicks: 95 },
          },
          winner: 'B',
        },
        {
          id: '2',
          title: 'Product Hunt Launch',
          platform: 'producthunt',
          variantA: {
            id: 'a',
            content: 'Introducing the future of development workflows',
            metrics: { likes: 200, comments: 55, shares: 35, clicks: 120 },
          },
          variantB: {
            id: 'b',
            content: 'The tool every developer needs in their arsenal',
            metrics: { likes: 180, comments: 50, shares: 30, clicks: 100 },
          },
          winner: 'A',
        },
      ];
      setPosts(mockPosts);
      setSelectedPost(mockPosts[0]);
      setLoading(false);
    }, 1000);
  };

  const fetchLatestMetrics = async () => {
    setIsFetching(true);
    // Simulate API call
    setTimeout(() => {
      setPosts((prevPosts) =>
        prevPosts.map((post) => ({
          ...post,
          variantA: {
            ...post.variantA,
            metrics: {
              likes: post.variantA.metrics.likes + Math.floor(Math.random() * 20),
              comments: post.variantA.metrics.comments + Math.floor(Math.random() * 10),
              shares: post.variantA.metrics.shares + Math.floor(Math.random() * 5),
              clicks: post.variantA.metrics.clicks + Math.floor(Math.random() * 15),
            },
          },
          variantB: {
            ...post.variantB,
            metrics: {
              likes: post.variantB.metrics.likes + Math.floor(Math.random() * 20),
              comments: post.variantB.metrics.comments + Math.floor(Math.random() * 10),
              shares: post.variantB.metrics.shares + Math.floor(Math.random() * 5),
              clicks: post.variantB.metrics.clicks + Math.floor(Math.random() * 15),
            },
          },
        }))
      );
      setIsFetching(false);
    }, 1500);
  };

  return {
    posts,
    selectedPost,
    setSelectedPost,
    loading,
    isFetching,
    fetchLatestMetrics,
  };
}