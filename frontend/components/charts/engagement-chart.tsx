'use client';

import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { PostVariant } from '@/hooks/use-post-analysis';

type EngagementChartProps = {
  variantA: PostVariant;
  variantB: PostVariant;
};

export function EngagementChart({ variantA, variantB }: EngagementChartProps) {
  const data = [
    {
      name: 'Likes',
      'Variant A': variantA.metrics.likes,
      'Variant B': variantB.metrics.likes,
    },
    {
      name: 'Comments',
      'Variant A': variantA.metrics.comments,
      'Variant B': variantB.metrics.comments,
    },
    {
      name: 'Shares',
      'Variant A': variantA.metrics.shares,
      'Variant B': variantB.metrics.shares,
    },
    {
      name: 'Clicks',
      'Variant A': variantA.metrics.clicks,
      'Variant B': variantB.metrics.clicks,
    },
  ];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar
          dataKey="Variant A"
          fill="hsl(var(--chart-1))"
          radius={[4, 4, 0, 0]}
          className="animate-in fade-in-50 duration-1000"
        />
        <Bar
          dataKey="Variant B"
          fill="hsl(var(--chart-2))"
          radius={[4, 4, 0, 0]}
          className="animate-in fade-in-50 duration-1000"
        />
      </BarChart>
    </ResponsiveContainer>
  );
}