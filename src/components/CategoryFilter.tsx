'use client';

import { useState } from 'react';
import { CATEGORIES, CategoryInfo, ProductCategory } from '@/lib/types';

interface CategoryFilterProps {
    selectedCategory: ProductCategory | null;
    onCategoryChange: (category: ProductCategory | null) => void;
}

export default function CategoryFilter({ selectedCategory, onCategoryChange }: CategoryFilterProps) {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <div className="w-full">
            {/* Toggle for mobile */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="md:hidden w-full flex items-center justify-between p-4 bg-slate-800/50 rounded-xl border border-slate-700/50 text-white mb-4"
            >
                <span className="font-medium">
                    {selectedCategory
                        ? CATEGORIES.find(c => c.slug === selectedCategory)?.name
                        : 'Todas las categorías'
                    }
                </span>
                <svg
                    className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
            </button>

            {/* Category buttons */}
            <div className={`${isExpanded ? 'block' : 'hidden'} md:block`}>
                <div className="flex flex-wrap gap-2 md:gap-3">
                    {/* Botón "Todas" */}
                    <button
                        onClick={() => {
                            onCategoryChange(null);
                            setIsExpanded(false);
                        }}
                        className={`
              flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-300
              ${selectedCategory === null
                                ? 'bg-gradient-to-r from-forest-600 to-forest-500 text-white shadow-lg shadow-forest-500/25'
                                : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 hover:text-white border border-slate-700/50'
                            }
            `}
                    >
                        <span className="text-lg">🏕️</span>
                        <span>Todas</span>
                    </button>

                    {/* Botones de categoría */}
                    {CATEGORIES.map((category: CategoryInfo) => (
                        <button
                            key={category.slug}
                            onClick={() => {
                                onCategoryChange(category.slug);
                                setIsExpanded(false);
                            }}
                            className={`
                flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-300
                ${selectedCategory === category.slug
                                    ? 'bg-gradient-to-r from-forest-600 to-forest-500 text-white shadow-lg shadow-forest-500/25'
                                    : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 hover:text-white border border-slate-700/50'
                                }
              `}
                        >
                            <span className="text-lg">{category.icon}</span>
                            <span className="hidden sm:inline">{category.name}</span>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
