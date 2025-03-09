'use client';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/components/ui/use-toast';
import { zodResolver } from '@hookform/resolvers/zod';
import { Bot, Calendar, Loader2, Share2 } from 'lucide-react';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

const platforms = [
  { id: 'twitter', name: 'X (Twitter)' },
  { id: 'reddit', name: 'Reddit' },
  { id: 'producthunt', name: 'Product Hunt' },
] as const;

const formSchema = z.object({
  platform: z.enum(['twitter', 'reddit', 'producthunt']),
  keywords: z.string().min(1, 'Keywords are required'),
  content: z.string().min(1, 'Content is required'),
  scheduledFor: z.string().optional(),
});

export default function CreatePostPage() {
  const { toast } = useToast();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      platform: 'twitter',
      keywords: '',
      content: '',
    },
  });

  const [isGenerating, setIsGenerating] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const generateContent = async () => {
    const keywords = form.getValues('keywords');
    if (!keywords) {
      toast({
        title: 'Keywords required',
        description: 'Please enter keywords to generate content.',
        variant: 'destructive',
      });
      return;
    }

    setIsGenerating(true);
    // TODO: Implement GPT-4 content generation
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setSuggestions([
      'Just shipped a game-changing feature in my side project! 🚀 Check out the new AI-powered content generation that helps developers save hours on social media marketing. Try it out and let me know what you think! #DevTools #ProductivityHack',
      'Looking for beta testers! 🔍 Built a tool that automates social media marketing for developers. If you\'re tired of context-switching between coding and promotion, this might be for you. DM me for early access! #SideProject #DevMarketing',
    ]);
    setIsGenerating(false);
  };

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      // TODO: Implement post creation and scheduling
      console.log(values);
      toast({
        title: 'Success',
        description: 'Post created successfully.',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to create post.',
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="container py-8">
      <div className="mx-auto max-w-2xl">
        <h1 className="mb-8 text-3xl font-bold tracking-tight">Create Post</h1>

        <div className="space-y-8">
          <Card>
            <CardHeader>
              <CardTitle>Post Details</CardTitle>
              <CardDescription>
                Enter the details for your social media post
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Form {...form}>
                <form
                  onSubmit={form.handleSubmit(onSubmit)}
                  className="space-y-6"
                >
                  <FormField
                    control={form.control}
                    name="platform"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Platform</FormLabel>
                        <Select
                          onValueChange={field.onChange}
                          defaultValue={field.value}
                        >
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select a platform" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {platforms.map((platform) => (
                              <SelectItem
                                key={platform.id}
                                value={platform.id}
                              >
                                {platform.name}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="keywords"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Keywords</FormLabel>
                        <FormControl>
                          <Input
                            placeholder="Enter keywords for content generation"
                            {...field}
                          />
                        </FormControl>
                        <FormDescription>
                          Separate keywords with commas
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="flex justify-end">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={generateContent}
                      disabled={isGenerating}
                    >
                      {isGenerating ? (
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      ) : (
                        <Bot className="mr-2 h-4 w-4" />
                      )}
                      Generate Content
                    </Button>
                  </div>

                  {suggestions.length > 0 && (
                    <div className="space-y-4">
                      <h3 className="font-medium">Suggestions</h3>
                      <div className="space-y-2">
                        {suggestions.map((suggestion, index) => (
                          <div
                            key={index}
                            className="cursor-pointer rounded-lg border p-4 hover:bg-accent"
                            onClick={() =>
                              form.setValue('content', suggestion)
                            }
                          >
                            <p className="text-sm">{suggestion}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <FormField
                    control={form.control}
                    name="content"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Content</FormLabel>
                        <FormControl>
                          <Textarea
                            placeholder="Write your post content"
                            className="min-h-[120px]"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="scheduledFor"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Schedule</FormLabel>
                        <FormControl>
                          <Input
                            type="datetime-local"
                            {...field}
                          />
                        </FormControl>
                        <FormDescription>
                          Leave empty to post immediately
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="flex justify-end space-x-4">
                    <Button type="submit">
                      <Share2 className="mr-2 h-4 w-4" />
                      Create Post
                    </Button>
                    <Button type="submit" variant="outline">
                      <Calendar className="mr-2 h-4 w-4" />
                      Schedule
                    </Button>
                  </div>
                </form>
              </Form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}