'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

type Platform = 'twitter' | 'reddit' | 'producthunt';
type Tone = 'professional' | 'casual' | 'enthusiastic';
type Variant = { id: string; content: string };

export default function CreatePost() {
  const router = useRouter();
  const [platform, setPlatform] = useState<Platform>('twitter');
  const [keywords, setKeywords] = useState('');
  const [tone, setTone] = useState<Tone>('professional');
  const [variants, setVariants] = useState<Variant[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const generateMockVariants = () => {
    const mockVariants: Variant[] = [
      {
        id: 'a',
        content: `🚀 Just launched a game-changing feature for ${keywords}! As a developer, I'm excited to share how this will revolutionize your workflow. Check it out and let me know what you think! #DevTools #Innovation`,
      },
      {
        id: 'b',
        content: `💡 Want to boost your ${keywords} productivity? I've created a solution that makes development 10x faster. Early feedback has been incredible - would love your thoughts!`,
      },
      {
        id: 'c',
        content: `🔥 Developers, tired of struggling with ${keywords}? I built something special for you. Simple, powerful, and ready to use. Join the beta today! #Programming #DevExperience`,
      },
    ];

    setVariants(mockVariants);
    setIsGenerating(false);
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simulate API call delay
    setTimeout(generateMockVariants, 1500);
  };

  const handlePublish = (variant: Variant) => {
    console.log('Publishing variant:', variant);
    router.push('/posts');
  };

  const handleSchedule = (variant: Variant) => {
    console.log('Scheduling variant:', variant);
    router.push('/schedule');
  };

  return (
    <div className="container max-w-5xl py-8">
      <div className="mb-8 space-y-6">
        <div className="space-y-2">
          <Label htmlFor="platform">Platform</Label>
          <Select value={platform} onValueChange={(value: Platform) => setPlatform(value)}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select platform" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="twitter">Twitter</SelectItem>
              <SelectItem value="reddit">Reddit</SelectItem>
              <SelectItem value="producthunt">Product Hunt</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="keywords">Keywords</Label>
          <Input
            id="keywords"
            placeholder="Enter keywords (e.g., React, TypeScript, API)"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
          />
        </div>

        <div className="space-y-2">
          <Label>Tone</Label>
          <RadioGroup value={tone} onValueChange={(value: Tone) => setTone(value)}>
            <div className="flex space-x-4">
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="professional" id="professional" />
                <Label htmlFor="professional">Professional</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="casual" id="casual" />
                <Label htmlFor="casual">Casual</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="enthusiastic" id="enthusiastic" />
                <Label htmlFor="enthusiastic">Enthusiastic</Label>
              </div>
            </div>
          </RadioGroup>
        </div>

        <Button
          className="w-full"
          size="lg"
          onClick={handleGenerate}
          disabled={!keywords || isGenerating}
        >
          {isGenerating ? 'Generating...' : 'Generate Variants'}
        </Button>
      </div>

      {variants.length > 0 && (
        <div className="grid gap-6 md:grid-cols-3">
          {variants.map((variant) => (
            <Card
              key={variant.id}
              className="transform transition-all duration-200 hover:translate-y-[-4px] hover:shadow-xl"
            >
              <CardHeader>
                <CardTitle className="text-lg">Variant {variant.id.toUpperCase()}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="min-h-[120px] whitespace-pre-wrap text-sm">{variant.content}</p>
              </CardContent>
              <CardFooter className="flex gap-2">
                <Button
                  className="flex-1"
                  variant="default"
                  onClick={() => handlePublish(variant)}
                >
                  Publish Now
                </Button>
                <Button
                  className="flex-1"
                  variant="outline"
                  onClick={() => handleSchedule(variant)}
                >
                  Schedule
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}