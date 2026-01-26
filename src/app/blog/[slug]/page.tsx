import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { BLOG_POSTS } from '@/data/blog-posts';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';
import Link from 'next/link';

interface Props {
    params: { slug: string };
}

// Generación de Metadatos SEO dinámicos
export async function generateMetadata({ params }: Props): Promise<Metadata> {
    const post = BLOG_POSTS.find((p) => p.slug === params.slug);

    if (!post) {
        return { title: 'Artículo no encontrado' };
    }

    return {
        title: `${post.title} | Blog CampingDeals`,
        description: post.excerpt,
        openGraph: {
            title: post.title,
            description: post.excerpt,
            type: 'article',
            publishedTime: post.date,
            authors: [post.author],
            images: [
                {
                    url: post.image,
                    width: 1200,
                    height: 630,
                    alt: post.title,
                },
            ],
        },
    };
}

export default function BlogPostPage({ params }: Props) {
    const post = BLOG_POSTS.find((p) => p.slug === params.slug);

    if (!post) {
        notFound();
    }

    // Schema.org Article Data
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post.title,
        "image": [post.image],
        "datePublished": post.date,
        "dateModified": post.date,
        "author": [{
            "@type": "Person",
            "name": post.author,
            "url": `${process.env.NEXT_PUBLIC_SITE_URL || 'https://camper-omega.vercel.app'}/blog`
        }],
        "publisher": {
            "@type": "Organization",
            "name": "CampingDeals España",
            "logo": {
                "@type": "ImageObject",
                "url": `${process.env.NEXT_PUBLIC_SITE_URL || 'https://camper-omega.vercel.app'}/logo.png`
            }
        },
        "description": post.excerpt
    };

    return (
        <div className="min-h-screen flex flex-col font-sans text-white bg-slate-900">
            <Header />
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />

            <article className="flex-grow pt-24 pb-20 px-4 sm:px-6">
                <div className="max-w-3xl mx-auto">
                    {/* Breadcrumb */}
                    <nav className="flex items-center gap-2 text-sm text-slate-400 mb-8">
                        <Link href="/" className="hover:text-white transition-colors">Inicio</Link>
                        <span>/</span>
                        <Link href="/blog" className="hover:text-white transition-colors">Blog</Link>
                        <span>/</span>
                        <span className="text-white truncate max-w-[200px]">{post.title}</span>
                    </nav>

                    {/* Header del Artículo */}
                    <header className="mb-10 text-center">
                        <div className="inline-flex items-center gap-2 mb-6">
                            <span className="px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs font-semibold text-blue-400">
                                {post.category}
                            </span>
                            <span className="text-slate-500 text-xs flex items-center gap-1">
                                🕒 {post.readTime}
                            </span>
                        </div>

                        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-6 leading-tight">
                            {post.title}
                        </h1>

                        <div className="flex items-center justify-center gap-4 text-sm">
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500" />
                                <span className="text-slate-200 font-medium">{post.author}</span>
                            </div>
                            <span className="text-slate-500">•</span>
                            <time className="text-slate-400">{post.date}</time>
                        </div>
                    </header>

                    {/* Imagen Principal */}
                    <div className="mb-12 rounded-2xl overflow-hidden shadow-2xl shadow-black/50 aspect-video relative">
                        <img
                            src={post.image}
                            alt={post.title}
                            className="w-full h-full object-cover"
                        />
                    </div>

                    {/* Contenido (Renderizado peligroso para la demo, en prod usar parser) */}
                    <div
                        className="prose prose-lg prose-invert max-w-none prose-headings:text-white prose-p:text-slate-300 prose-a:text-blue-400 prose-strong:text-white prose-li:text-slate-300"
                        dangerouslySetInnerHTML={{ __html: post.content }}
                    />

                    {/* Tags */}
                    <div className="mt-12 pt-8 border-t border-slate-800">
                        <h4 className="text-sm uppercase tracking-wider text-slate-500 mb-4 font-semibold">Temas relacionados</h4>
                        <div className="flex flex-wrap gap-2">
                            {post.tags.map(tag => (
                                <span key={tag} className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm rounded-lg transition-colors cursor-default">
                                    #{tag}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>
            </article>

            <Footer />
        </div>
    );
}
