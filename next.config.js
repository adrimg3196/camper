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
            { protocol: 'https', hostname: '*.media-amazon.com', pathname: '/**' },
        ],
        unoptimized: true,
    },
};

module.exports = nextConfig;
