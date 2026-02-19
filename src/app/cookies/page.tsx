// Redirect /cookies to /politica-cookies for SEO consistency
import { redirect } from 'next/navigation';

export default function CookiesRedirect() {
    redirect('/politica-cookies');
}
