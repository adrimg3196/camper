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
        excerpt: "Hemos analizado más de 30 modelos para esta temporada. Descubre cuáles son las mejores tiendas de campaña por precio, resistencia y facilidad de montaje.",
        author: "Carlos 'El Explorador'",
        date: "2026-01-15",
        readTime: "8 min",
        category: "Equipamiento",
        tags: ["Tiendas de Campaña", "Review", "2026", "Comparativa"],
        image: "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=1600",
        content: `
      <h2>Las Mejores Tiendas de Campaña para 2026</h2>
      <p>Elegir la tienda de campaña adecuada puede marcar la diferencia entre una aventura inolvidable y una noche miserable. Tras analizar más de 30 modelos disponibles en Amazon España, aquí tienes nuestra selección definitiva para 2026.</p>

      <h3>1. Coleman Coastline 3 Plus — La Mejor Calidad/Precio</h3>
      <p>La Coleman Coastline sigue siendo la referencia para camping familiar con coche. Su sistema de montaje en 10 minutos y su columna de agua de 3.000mm la hacen ideal para primavera-verano.</p>
      <ul>
        <li><strong>Pros:</strong> Espaciosa, montaje rápido, resistencia al agua probada, vestíbulo generoso.</li>
        <li><strong>Contras:</strong> Algo pesada para trekking (4.5kg), no recomendada para invierno.</li>
        <li><strong>Precio orientativo:</strong> 90–130€ en Amazon</li>
        <li><strong>Veredicto:</strong> La mejor opción para camping familiar o en festival.</li>
      </ul>

      <h3>2. Naturehike CloudUp 2 — Ultraligera para Senderistas</h3>
      <p>Si cuentas cada gramo en tu mochila, esta es tu tienda. Con solo 1.7kg ofrece una protección sorprendente contra el viento y la lluvia ligera. Perfecta para ruta de 2-3 días.</p>
      <ul>
        <li><strong>Pros:</strong> Muy ligera, compacta al empacar, buena ventilación.</li>
        <li><strong>Contras:</strong> Espacio justo para 2 personas con mochilas dentro.</li>
        <li><strong>Precio orientativo:</strong> 60–90€ en Amazon</li>
        <li><strong>Veredicto:</strong> La mejor ultraligera por precio.</li>
      </ul>

      <h3>3. MSR Hubba Hubba NX — La Profesional de Alta Gama</h3>
      <p>Para quien hace montañismo serio o quiere una tienda que dure 10 años. Doble capa, estructura geodésica y resistencia certificada a vientos fuertes.</p>
      <ul>
        <li><strong>Pros:</strong> Construcción premium, resistencia extrema, diseño inteligente.</li>
        <li><strong>Contras:</strong> Precio elevado (350-500€), puede ser excesiva para uso casual.</li>
        <li><strong>Veredicto:</strong> La mejor si vas a usarla regularmente durante años.</li>
      </ul>

      <h3>Qué Mirar al Comprar una Tienda de Campaña</h3>

      <h4>Columna de Agua: El Indicador Clave</h4>
      <p>La columna de agua mide la impermeabilidad. Busca al menos <strong>2.000mm</strong> para lluvia normal y <strong>3.000mm o más</strong> si vas a zonas con lluvias frecuentes. No confundas con la puntuación del tejido exterior.</p>

      <h4>Capacidad: Siempre Pide una Talla Más</h4>
      <p>Los fabricantes indican capacidad máxima, no cómoda. Una tienda de 3 personas es cómoda para 2. Si llevas mochilas grandes dentro, sube aún más la talla.</p>

      <h4>Temporadas</h4>
      <ul>
        <li><strong>2 estaciones:</strong> Primavera y verano sin lluvia fuerte. Las más económicas.</li>
        <li><strong>3 estaciones:</strong> Perfectas para el 80% de los campistas. Resistentes a lluvia y viento moderado.</li>
        <li><strong>4 estaciones:</strong> Para invierno, alta montaña o condiciones extremas.</li>
      </ul>

      <h3>Conclusión</h3>
      <p>Para camping familiar con coche, la <strong>Coleman Coastline</strong> sigue siendo nuestra recomendación principal. Para trekking con mochila, la <strong>Naturehike CloudUp</strong> ofrece el mejor precio/peso del mercado en 2026.</p>
    `
    },
    {
        slug: "guia-definitiva-sacos-dormir",
        title: "Guía Definitiva para Elegir Saco de Dormir: No Pases Frío Nunca Más",
        excerpt: "¿Plumas o fibra? ¿Momia o rectangular? Desmitificamos la elección del saco de dormir con nuestra guía técnica paso a paso para 2026.",
        author: "Elena Outdoor",
        date: "2026-01-20",
        readTime: "10 min",
        category: "Guías Técnicas",
        tags: ["Sacos de Dormir", "Guía", "Invierno", "Técnica"],
        image: "https://images.unsplash.com/photo-1517175782509-deef2807f66e?auto=format&fit=crop&q=80&w=1600",
        content: `
      <h2>La Guía Definitiva de Sacos de Dormir 2026</h2>
      <p>El saco de dormir es uno de los elementos más críticos de tu equipamiento de camping. Elegir mal puede costarte una noche en blanco tiritando de frío. Esta guía te explica todo lo que necesitas saber.</p>

      <h3>El Error Más Común: Confundir Temperatura Confort con Temperatura Extrema</h3>
      <p>Cada saco de dormir tiene tres temperaturas certificadas según la norma EN13537:</p>
      <ul>
        <li><strong>Temperatura de confort:</strong> La temperatura a la que una mujer adulta duerme cómodamente. <em>Esta es la que debes mirar.</em></li>
        <li><strong>Temperatura límite:</strong> La temperatura a la que un hombre adulto duerme sin tiritar.</li>
        <li><strong>Temperatura extrema:</strong> La temperatura de supervivencia. No para dormir cómodamente.</li>
      </ul>
      <p>Para evitar sorpresas, <strong>elige siempre un saco con temperatura de confort 5°C por debajo de la temperatura mínima prevista</strong>.</p>

      <h3>¿Plumón o Fibra Sintética?</h3>

      <h4>Relleno de Plumón</h4>
      <ul>
        <li><strong>Ventajas:</strong> Mejor ratio calor/peso, comprime mucho, muy duradero si se cuida bien.</li>
        <li><strong>Desventajas:</strong> Pierde propiedades si se moja, más caro, requiere cuidado especial.</li>
        <li><strong>Ideal para:</strong> Senderismo seco, expediciones de larga duración, donde el peso importa.</li>
      </ul>

      <h4>Relleno Sintético</h4>
      <ul>
        <li><strong>Ventajas:</strong> Mantiene calor incluso húmedo, más económico, fácil de lavar.</li>
        <li><strong>Desventajas:</strong> Más pesado y voluminoso que el plumón de igual calidad.</li>
        <li><strong>Ideal para:</strong> Camping húmedo, uso ocasional, presupuesto ajustado.</li>
      </ul>

      <h3>Forma: ¿Momia o Rectangular?</h3>
      <p>Los sacos <strong>momia</strong> son más eficientes térmicamente porque no hay espacio vacío que calentar. Los <strong>rectangulares</strong> son más cómodos para moverse y para temperaturas moderadas en camping con coche.</p>

      <h3>Nuestras Recomendaciones por Uso</h3>
      <ul>
        <li><strong>Camping de verano (&gt;10°C):</strong> Decathlon Arpenaz 10°C — excelente precio/calidad.</li>
        <li><strong>Senderismo primavera-otoño (0°C a 10°C):</strong> Naturehike CW300 — ligero y eficiente.</li>
        <li><strong>Invierno/alta montaña (&lt;-5°C):</strong> Marmot Trestles — fibra sintética premium.</li>
      </ul>

      <h3>Cómo Cuidar tu Saco de Dormir</h3>
      <ul>
        <li>Guárdalo extendido o en bolsa grande, nunca comprimido largo tiempo.</li>
        <li>Lávalo solo cuando sea necesario (máximo 1-2 veces/año).</li>
        <li>Usa sábana de seda interior para mantenerlo limpio más tiempo.</li>
        <li>Sécalo completamente antes de guardarlo.</li>
      </ul>
    `
    },
    {
        slug: "trucos-camping-principiantes",
        title: "10 Errores de Novato que Arruinarán tu Camping (y cómo evitarlos)",
        excerpt: "Desde montar la tienda en una pendiente hasta olvidar el abrelatas. Aprende de los errores de otros para garantizar que tu primer camping sea un éxito.",
        author: "Equipo CampingDeals",
        date: "2026-01-10",
        readTime: "6 min",
        category: "Consejos",
        tags: ["Principiantes", "Tips", "Seguridad", "Preparación"],
        image: "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&q=80&w=1600",
        content: `
      <h2>10 Errores de Principiante en Camping</h2>
      <p>Todo el mundo comete errores en su primer camping. El problema es que en plena naturaleza, algunos errores se pagan caro. Aquí tienes los más frecuentes con sus soluciones.</p>

      <h3>Error #1: Llegar de Noche</h3>
      <p>Montar una tienda sin luz es una pesadilla, especialmente la primera vez. Los arcos se confunden, las piquetas no quedan bien y acabas durmiendo en un ángulo rarísimo.</p>
      <p><strong>Solución:</strong> Llega siempre con al menos 2 horas de luz natural disponible.</p>

      <h3>Error #2: No Probar el Equipo Antes</h3>
      <p>La tienda nueva está preciosa en la caja. ¿Pero la has montado? ¿Están todas las piquetas? ¿El arco está completo?</p>
      <p><strong>Solución:</strong> Monta la tienda en casa al menos una vez antes de salir.</p>

      <h3>Error #3: Montar la Tienda en el Lugar Equivocado</h3>
      <p>Zonas bajas se inundan con la lluvia. Las pendientes hacen que te deslices durante toda la noche.</p>
      <p><strong>Solución:</strong> Busca terreno plano, algo elevado del entorno, bien drenado.</p>

      <h3>Error #4: Subestimar el Frío Nocturno</h3>
      <p>Hace 28°C durante el día y piensas que no necesitas saco. A las 3am la temperatura puede bajar a 10°C.</p>
      <p><strong>Solución:</strong> Lleva siempre un saco apropiado para la temperatura <em>nocturna mínima</em>, no la diurna.</p>

      <h3>Error #5: El Móvil Sin Batería</h3>
      <p>Te quedas sin batería el primer día y no puedes usar el mapa o llamar en emergencias.</p>
      <p><strong>Solución:</strong> Lleva siempre un powerbank. Los hay desde 15€ en Amazon.</p>

      <h3>Error #6: Olvidar la Iluminación</h3>
      <p>De noche, el camping sin luz es un campo de obstáculos: cuerdas, piedras, raíces...</p>
      <p><strong>Solución:</strong> Un frontal es mejor que una linterna (deja las manos libres). Con pilas de repuesto.</p>

      <h3>Error #7: Comida Inadecuada</h3>
      <p>Llevar solo latas sin abrelatas, o comida que necesita refrigeración sin nevera portátil.</p>
      <p><strong>Solución:</strong> Planifica el menú antes. Conservas fáciles de abrir, snacks que no se estropeen.</p>

      <h3>Error #8: Montar la Puerta al Viento</h3>
      <p>El viento entrando por la puerta cada vez que la abres es muy incómodo. Peor si llueve.</p>
      <p><strong>Solución:</strong> Orienta siempre la puerta en dirección contraria al viento predominante.</p>

      <h3>Error #9: Sin Esterilla ni Colchoneta</h3>
      <p>El suelo absorbe calor corporal aunque la temperatura sea agradable. Sin aislamiento del suelo, pasarás frío desde abajo.</p>
      <p><strong>Solución:</strong> Siempre lleva una esterilla de espuma o colchoneta inflable.</p>

      <h3>Error #10: Olvidar el Repelente</h3>
      <p>Los mosquitos arruinan noches perfectas. Un olvido que se paga caro.</p>
      <p><strong>Solución:</strong> Repelente en tu lista de imprescindibles, siempre.</p>

      <h3>Lista de Equipo Básico para tu Primer Camping</h3>
      <ul>
        <li>✅ Tienda de campaña + piquetas + cuerdas</li>
        <li>✅ Saco de dormir adecuado a la temperatura</li>
        <li>✅ Esterilla o colchoneta</li>
        <li>✅ Frontal con pilas de repuesto</li>
        <li>✅ Powerbank cargado</li>
        <li>✅ Ropa de abrigo extra</li>
        <li>✅ Kit básico de primeros auxilios</li>
        <li>✅ Botella de agua</li>
        <li>✅ Comida planificada + abrelatas</li>
        <li>✅ Repelente de insectos</li>
      </ul>
    `
    }
];
