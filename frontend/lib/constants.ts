export const API_ENDPOINTS = {
  AUTH: {
    ME: '/auth/me',
    LOGOUT: '/auth/logout',
  },
  POSTS: {
    CREATE: '/posts/create',
    LIST: '/posts/list',
    GENERATE: '/posts/generate',
  },
  SCHEDULE: {
    LIST: '/schedule/jobs',
    CREATE: '/schedule/jobs',
    CANCEL: (id: string) => `/schedule/jobs/${id}`,
  },
  ANALYSIS: {
    ENGAGEMENTS: '/analysis/engagements',
    FETCH_LATEST: '/analysis/fetch-latest',
  },
};

export const PLATFORMS = {
  TWITTER: 'twitter',
  REDDIT: 'reddit',
  PRODUCTHUNT: 'producthunt',
} as const;

export const TONES = {
  PROFESSIONAL: 'professional',
  CASUAL: 'casual',
  ENTHUSIASTIC: 'enthusiastic',
} as const;

export const PLANS = {
  FREE: 'free',
  PRO: 'pro',
} as const;