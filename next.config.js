/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  experimental: {
    serverComponentsExternalPackages: ['node:sqlite'],
    workerThreads: false,
    cpus: 1,
  },
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
