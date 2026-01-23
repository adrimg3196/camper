/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        remotePatterns: [
            { protocol: 'https', hostname: 'm.media-amazon.com', pathname: '/**' },
            { protocol: 'https', hostname: 'images-na.ssl-images-amazon.com', pathname: '/**' },
            { protocol: 'https', hostname: 'images-eu.ssl-images-amazon.com', pathname: '/**' },
            { protocol: 'https', hostname: 'images-fe.ssl-images-amazon.com', pathname: '/**' },
            { protocol: 'https', hostname: 'images-amazon.com', pathname: '/**' },
            { protocol: 'https', hostname: 'www.amazon.es', pathname: '/**' },
            { protocol: 'https', hostname: 'images.unsplash.com', pathname: '/**' },
        ],
        // Keep unoptimized for now to avoid issues with external Amazon images
        unoptimized: true,
        deviceSizes: [640, 750, 828, 1080, 1200, 1920],
        imageSizes: [16, 32, 48, 64, 96, 128, 256],
    },
    compress: true,
    poweredByHeader: false,
    reactStrictMode: true,
};

module.exports = nextConfig;
// Force rebuild Fri Jan 23 20:55:59 UTC 2026
