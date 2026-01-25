import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { BLOG_POSTS } from '@/data/blog-posts';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: "Blog de Expertos en Camping | Consejos, Guías y Análisis 2026",
    description: "Lee nuestras guías expertas sobre equipamiento de camping. Análisis a fondo de tiendas, sacos y material outdoor por profesionales del sector.",
};

export default function BlogPage() {
    return (
        <div className="min-h-screen flex flex-col font-sans text-white bg-slate-900">
            <Header />

            <main className="flex-grow pt-24 pb-20 px-4 sm:px-6 max-w-7xl mx-auto w-full">
                <div className="text-center mb-16">
                    <span className="inline-block py-1 px-3 rounded-full bg-blue-500/20 text-blue-300 text-xs font-semibold mb-4 border border-blue-500/30">
                        CONOCIMIENTO EXPERTO
                    </span>
                    <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">
                        Guías y Análisis de Camping
                    </h1>
                    <p className="text-lg text-slate-400 max-w-2xl mx-auto">
                        Consejos probados en campo, comparativas honestas y guías de compra para que elijas el mejor equipamiento.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {BLOG_POSTS.map((post) => (
                        <article key={post.slug} className="flex flex-col bg-slate-800/50 rounded-2xl overflow-hidden border border-slate-700/50 hover:border-blue-500/50 transition-all duration-300 group">
                            <Link href={`/blog/${post.slug}`} className="relative h-48 overflow-hidden">
                                <img
                                    src={post.image}
                                    alt={post.title}
                                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                />
                                <div className="absolute top-4 left-4 bg-slate-900/80 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-medium text-white border border-slate-700">
                                    {post.category}
                                </div>
                            </Link>

                            <div className="flex-grow p-6 flex flex-col">
                                <div className="flex items-center gap-2 text-xs text-slate-400 mb-3">
                                    <span>{post.date}</span>
                                    <span>•</span>
                                    <span>{post.readTime} lectura</span>
                                </div>

                                <h2 className="text-xl font-bold text-white mb-3 leading-tight group-hover:text-blue-400 transition-colors">
                                    <Link href={`/blog/${post.slug}`}>
                                        {post.title}
                                    </Link>
                                </h2>

                                <p className="text-slate-400 text-sm mb-6 flex-grow line-clamp-3">
                                    {post.excerpt}
                                </p>

                                <div className="flex items-center justify-between mt-auto">
                                    <div className="flex items-center gap-2">
                                        <div className="w-6 h-6 rounded-full bg-gradient-to-br from-blue-400 to-purple-500" />
                                        <span className="text-xs text-slate-300">{post.author}</span>
                                    </div>
                                    <Link href={`/blog/${post.slug}`} className="text-sm font-semibold text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-1">
                                        Leer más <span>→</span>
                                    </Link>
                                </div>
                            </div>
                        </article>
                    ))}
                </div>
            </main>

            <Footer />
        </div>
    );
}
