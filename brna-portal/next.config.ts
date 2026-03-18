import type { NextConfig } from "next";

const isDemo = process.env.NEXT_PUBLIC_DEMO === 'true';
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';

const nextConfig: NextConfig = {
  output: isDemo ? 'export' : undefined,
  basePath: basePath,
  assetPrefix: basePath,
  images: {
    unoptimized: isDemo ? true : undefined,
  },
};

export default nextConfig;
