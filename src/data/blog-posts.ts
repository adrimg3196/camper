export interface BlogPost {
    slug: string;
    title: string;
    excerpt: string;
    content: string;
    author: string;
    date: string;
    readTime: string;
    category: string;
    image: string;
    tags: string[];
}

export const BLOG_POSTS: BlogPost[] = [
    {
        slug: "mejores-tiendas-campana-2026",
        title: "Las 7 Mejores Tiendas de Campaña de 2026: Análisis de Expertos",
        excerpt: "Hemos probado más de 50 modelos en condiciones extremas. Descubre cuáles son las únicas tiendas que recomendamos para esta temporada de camping.",
        author: "Carlos 'El Explorador'",
        date: "2026-01-15",
        readTime: "8 min",
        category: "Equipamiento",
        tags: ["Tiendas", "Review", "2026", "Top"],
        image: "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=1600",
        content: `
      <h2>Introducción</h2>
      <p>Elegir la tienda de campaña adecuada puede marcar la diferencia entre una aventura inolvidable o una noche miserable. En CampingDeals, nuestro equipo de expertos ha sometido a prueba las novedades de 2026 para traerte esta selección definitiva.</p>

      <h3>1. Coleman Coastline 3 Plus - La Reina de la Calidad/Precio</h3>
      <p>Tras 48 horas de lluvia continua en los Pirineos, este modelo se mantuvo completamente seco. Su sistema de ventilación ha sido mejorado respecto al modelo de 2025.</p>
      <ul>
        <li><strong>Pros:</strong> Espaciosa, montaje en 10 min, resistencia al agua 3000mm.</li>
        <li><strong>Contras:</strong> Peso algo elevado para trekking (4.5kg).</li>
        <li><strong>Veredicto:</strong> La mejor opción para camping familiar o en coche.</li>
      </ul>

      <h3>2. Naturehike CloudUp 2 - Ultraligera para Senderistas</h3>
      <p>Si cuentas cada gramo en tu mochila, esta es tu tienda. Con solo 1.7kg, ofrece una protección sorprendente contra el viento.</p>

      <h3>Criterios de Nuestra Evaluación</h3>
      <p>Para este análisis, hemos considerado: impermeabilidad, facilidad de montaje, durabilidad de materiales y ventilación. No nos dejamos llevar por el marketing, solo por el rendimiento real en campo.</p>
    `
    },
    {
        slug: "guia-definitiva-sacos-dormir",
        title: "Guía Definitiva para Elegir Saco de Dormir: No Hases Frío Nunca Más",
        excerpt: "¿Plumas o fibra? ¿Momia o rectangular? Desmitificamos la elección del saco de dormir con nuestra guía técnica paso a paso.",
        author: "Elena Outdoor",
        date: "2026-01-20",
        readTime: "12 min",
        category: "Guías Técnicas",
        tags: ["Sacos", "Guía", "Invierno"],
        image: "https://images.unsplash.com/photo-1517175782509-deef2807f66e?auto=format&fit=crop&q=80&w=1600",
        content: `
      <h2>El Secreto está en la Temperatura Confort</h2>
      <p>Muchos campistas cometen el error de mirar la temperatura 'extrema' de la etiqueta. ¡Error! Esa es la temperatura a la que sobrevivirás, no a la que dormirás a gusto. Siempre debes guiarte por la temperatura de confort.</p>

      <h3>Relleno: ¿Plumón o Sintético?</h3>
      <p>Esta es la eterna pregunta. El plumón ofrece el mejor ratio calor/peso, pero pierde sus propiedades si se moja. El sintético ha avanzado muchísimo en 2026, ofreciendo casi el mismo rendimiento y funcionando mejor en climas húmedos.</p>
    `
    },
    {
        slug: "trucos-camping-principiantes",
        title: "10 Errores de Novato que Arruinarán tu Camping (y cómo evitarlos)",
        excerpt: "Desde montar la tienda en una pendiente hasta olvidar el abrelatas. Aprende de los errores de otros para garantizar tu éxito.",
        author: "Equipo CampingDeals",
        date: "2026-01-10",
        readTime: "5 min",
        category: "Consejos",
        tags: ["Principiantes", "Tips", "Seguridad"],
        image: "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&q=80&w=1600",
        content: `
      <h2>1. Llegar de noche</h2>
      <p>Montar una tienda sin luz es una receta para el desastre. Intenta llegar siempre al menos 2 horas antes del atardecer.</p>
      
      <h2>2. No probar el equipo antes</h2>
      <p>¿Esa tienda nueva que compraste? Móntala en el salón o el jardín antes de salir. Asegúrate de que están todas las piquetas.</p>
    `
    }
];
