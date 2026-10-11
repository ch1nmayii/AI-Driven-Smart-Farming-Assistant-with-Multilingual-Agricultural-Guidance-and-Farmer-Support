/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: 'http://127.0.0.1:6000/api/:path*',
      },
    ];
  },
};

export default nextConfig;
