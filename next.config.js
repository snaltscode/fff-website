/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  experimental: {
    serverComponentsExternalPackages: ['node:sqlite'],
  },
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
