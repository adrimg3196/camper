import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Camper Deals | Ofertas Camping +30% Descuento",
    description: "Las mejores ofertas de camping, camper y outdoor con más del 30% de descuento en Amazon. Tiendas de campaña, sacos de dormir, mochilas y más.",
    keywords: ["ofertas camping", "descuentos outdoor", "chollos camper", "tiendas campaña baratas", "amazon afiliados"],
    authors: [{ name: "Camper Deals" }],
    openGraph: {
        title: "Camper Deals | Ofertas Camping +30% Descuento",
        description: "Las mejores ofertas de camping y outdoor con más del 30% de descuento",
        type: "website",
        locale: "es_ES",
    },
    twitter: {
        card: "summary_large_image",
        title: "Camper Deals | Ofertas Camping +30% Descuento",
        description: "Las mejores ofertas de camping y outdoor con más del 30% de descuento",
    },
    robots: {
        index: true,
        follow: true,
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="es" className="dark">
            <body className="antialiased min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
                {children}
            </body>
        </html>
    );
}
