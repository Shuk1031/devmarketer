# DevMarketer

A social media automation platform for developers, built with Next.js 13 and Supabase.

## Features

- 🤖 AI-powered content generation
- 📊 A/B testing and analytics
- 📅 Smart scheduling
- 🔄 Multi-platform posting (Twitter, Reddit, Product Hunt)
- 🎨 Modern, responsive UI

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   NEXT_PUBLIC_API_BASE_URL=your_api_url
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

- `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Your Supabase anonymous key
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint

## Tech Stack

- Next.js 13 (App Router)
- TypeScript
- Tailwind CSS
- Supabase Auth
- shadcn/ui
- Recharts
- Axios

## License

MIT