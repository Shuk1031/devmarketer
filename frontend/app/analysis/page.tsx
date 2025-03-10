'use client';

import { usePostAnalysis } from '@/hooks/use-post-analysis';
import { EngagementChart } from '@/components/charts/engagement-chart';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Twitter, FileText, Award, Loader2, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils';

const platformIcons = {
  twitter: <Twitter className="h-4 w-4" />,
  reddit: <FileText className="h-4 w-4" />,
  producthunt: <Award className="h-4 w-4" />,
};

export default function AnalysisPage() {
  const { posts, selectedPost, setSelectedPost, loading, isFetching, fetchLatestMetrics } =
    usePostAnalysis();

  if (loading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container max-w-7xl space-y-8 py-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">A/B Test Analysis</h1>
        <div className="flex items-center gap-4">
          <Select
            value={selectedPost?.id}
            onValueChange={(value) => {
              const post = posts.find((p) => p.id === value);
              if (post) setSelectedPost(post);
            }}
          >
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Select post" />
            </SelectTrigger>
            <SelectContent>
              {posts.map((post) => (
                <SelectItem key={post.id} value={post.id}>
                  <div className="flex items-center gap-2">
                    {platformIcons[post.platform]}
                    <span>{post.title}</span>
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button
            variant="outline"
            size="icon"
            onClick={fetchLatestMetrics}
            disabled={isFetching}
          >
            <RefreshCw
              className={cn('h-4 w-4', isFetching && 'animate-spin')}
            />
          </Button>
        </div>
      </div>

      {selectedPost && (
        <div className="grid gap-8">
          <div className="grid gap-8 md:grid-cols-2">
            <Card
              className={cn(
                'transition-all duration-200',
                selectedPost.winner === 'A' &&
                  'border-2 border-primary bg-primary/5'
              )}
            >
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  Variant A
                  {selectedPost.winner === 'A' && (
                    <span className="rounded-full bg-primary px-2 py-1 text-xs text-primary-foreground">
                      Winner
                    </span>
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="mb-4 text-sm text-muted-foreground">
                  {selectedPost.variantA.content}
                </p>
                <div className="grid grid-cols-2 gap-4">
                  {Object.entries(selectedPost.variantA.metrics).map(
                    ([key, value]) => (
                      <div key={key} className="space-y-1">
                        <p className="text-sm capitalize text-muted-foreground">
                          {key}
                        </p>
                        <p className="text-2xl font-bold">{value}</p>
                      </div>
                    )
                  )}
                </div>
              </CardContent>
            </Card>

            <Card
              className={cn(
                'transition-all duration-200',
                selectedPost.winner === 'B' &&
                  'border-2 border-primary bg-primary/5'
              )}
            >
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  Variant B
                  {selectedPost.winner === 'B' && (
                    <span className="rounded-full bg-primary px-2 py-1 text-xs text-primary-foreground">
                      Winner
                    </span>
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="mb-4 text-sm text-muted-foreground">
                  {selectedPost.variantB.content}
                </p>
                <div className="grid grid-cols-2 gap-4">
                  {Object.entries(selectedPost.variantB.metrics).map(
                    ([key, value]) => (
                      <div key={key} className="space-y-1">
                        <p className="text-sm capitalize text-muted-foreground">
                          {key}
                        </p>
                        <p className="text-2xl font-bold">{value}</p>
                      </div>
                    )
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Engagement Comparison</CardTitle>
            </CardHeader>
            <CardContent>
              <EngagementChart
                variantA={selectedPost.variantA}
                variantB={selectedPost.variantB}
              />
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}