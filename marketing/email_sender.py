#!/usr/bin/env python3
"""
Camping Deals - Email Marketing con Resend
Envío gratuito de hasta 3,000 emails/mes
"""

import os
from typing import List, Dict
from datetime import datetime

try:
    import resend
    HAS_RESEND = True
except ImportError:
    HAS_RESEND = False
    print("⚠️ resend no instalado. Email marketing deshabilitado.")


class FreeEmailMarketing:
    """Email marketing gratuito con Resend (3,000 emails/mes gratis)"""
    
    def __init__(self):
        self.api_key = os.environ.get('RESEND_API_KEY')
        
        if HAS_RESEND and self.api_key:
            resend.api_key = self.api_key
            self.enabled = True
            print("✅ Resend configurado correctamente")
        else:
            self.enabled = False
            print("⚠️ Email marketing no configurado")
        
        self.from_email = os.environ.get('EMAIL_FROM', 'deals@camping-offers.com')
        self.reply_to = os.environ.get('EMAIL_REPLY_TO', 'soporte@camping-offers.com')
    
    def send_daily_deals(self, email_list: List[str], deals: List[Dict]) -> int:
        """Envía el newsletter diario con las mejores ofertas"""
        if not self.enabled:
            print("⚠️ Email no enviado - Resend no configurado")
            return 0
        
        if not deals:
            print("⚠️ No hay ofertas para enviar")
            return 0
        
        # Ordenar por descuento y tomar top 10
        best_deals = sorted(deals, key=lambda x: x.get('discount', 0), reverse=True)[:10]
        
        html_content = self._generate_email_html(best_deals)
        subject = f"🏕️ {len(best_deals)} Ofertas Camping del Día - Hasta {best_deals[0]['discount']}% OFF"
        
        sent_count = 0
        
        for email in email_list:
            try:
                params = {
                    "from": self.from_email,
                    "to": [email],
                    "subject": subject,
                    "html": html_content,
                    "reply_to": self.reply_to,
                }
                
                resend.Emails.send(params)
                sent_count += 1
                
            except Exception as e:
                print(f"❌ Error enviando a {email}: {e}")
        
        print(f"📧 Emails enviados: {sent_count}/{len(email_list)}")
        return sent_count
    
    def _generate_email_html(self, deals: List[Dict]) -> str:
        """Genera el HTML del email con las ofertas"""
        
        deals_html = ""
        for deal in deals:
            savings = deal.get('original_price', 0) - deal.get('current_price', 0)
            
            deals_html += f"""
            <tr>
                <td style="padding: 20px; border-bottom: 1px solid #e5e5e5;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td width="120" style="vertical-align: top;">
                                <img src="{deal.get('image_url', '')}" alt="" width="100" style="border-radius: 8px;">
                            </td>
                            <td style="padding-left: 15px; vertical-align: top;">
                                <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #333;">
                                    {deal.get('title', '')[:80]}...
                                </h3>
                                <p style="margin: 0 0 5px 0;">
                                    <span style="color: #999; text-decoration: line-through;">€{deal.get('original_price', 0):.2f}</span>
                                    <span style="color: #22c55e; font-size: 20px; font-weight: bold; margin-left: 10px;">
                                        €{deal.get('current_price', 0):.2f}
                                    </span>
                                </p>
                                <p style="margin: 0 0 10px 0;">
                                    <span style="background: #ef4444; color: white; padding: 3px 8px; border-radius: 4px; font-size: 14px; font-weight: bold;">
                                        -{deal.get('discount', 0)}%
                                    </span>
                                    <span style="color: #22c55e; margin-left: 10px; font-size: 14px;">
                                        Ahorras €{savings:.2f}
                                    </span>
                                </p>
                                <a href="{deal.get('affiliate_url', '#')}" 
                                   style="display: inline-block; background: #22c55e; color: white; padding: 10px 20px; 
                                          text-decoration: none; border-radius: 6px; font-weight: bold;">
                                    Ver en Amazon →
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; background: #f5f5f5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background: #f5f5f5; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #14532d 0%, #16a34a 100%); padding: 30px; text-align: center;">
                                    <h1 style="margin: 0; color: white; font-size: 28px;">🏕️ Camping Deals</h1>
                                    <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px;">
                                        Las mejores ofertas de hoy
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Stats -->
                            <tr>
                                <td style="padding: 20px; background: #f0fdf4; text-align: center;">
                                    <p style="margin: 0; font-size: 24px; color: #16a34a; font-weight: bold;">
                                        🔥 {len(deals)} ofertas con más del 30% OFF
                                    </p>
                                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">
                                        Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Deals -->
                            {deals_html}
                            
                            <!-- Footer -->
                            <tr>
                                <td style="padding: 30px; background: #f9fafb; text-align: center;">
                                    <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">
                                        <a href="https://camping-offers.github.io" style="color: #16a34a; text-decoration: none;">
                                            Ver todas las ofertas →
                                        </a>
                                    </p>
                                    <p style="margin: 0; color: #999; font-size: 12px;">
                                        Como Afiliado de Amazon, obtenemos ingresos por compras adscritas.
                                    </p>
                                    <p style="margin: 10px 0 0 0; color: #999; font-size: 11px;">
                                        Recibes este email porque te suscribiste a nuestras ofertas.<br>
                                        <a href="#" style="color: #999;">Darse de baja</a>
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    
    def send_welcome_email(self, email: str) -> bool:
        """Envía email de bienvenida a nuevo suscriptor"""
        if not self.enabled:
            return False
        
        html = """
        <html>
        <body style="font-family: sans-serif; padding: 20px;">
            <h1>🏕️ ¡Bienvenido a Camping Deals!</h1>
            <p>Gracias por suscribirte. Recibirás las mejores ofertas de camping con más del 30% de descuento.</p>
            <p>Preparamos nuestro equipo y encontramos las mejores ofertas cada día.</p>
            <p><a href="https://camping-offers.github.io">Ver ofertas actuales →</a></p>
            <p>¡Buenas aventuras!</p>
            <hr>
            <p style="font-size: 12px; color: #666;">
                Como Afiliado de Amazon, obtenemos ingresos por compras adscritas.
            </p>
        </body>
        </html>
        """
        
        try:
            resend.Emails.send({
                "from": self.from_email,
                "to": [email],
                "subject": "🏕️ Bienvenido a Camping Deals",
                "html": html,
            })
            return True
        except Exception as e:
            print(f"❌ Error enviando welcome email: {e}")
            return False


if __name__ == '__main__':
    # Test
    email_client = FreeEmailMarketing()
    print(f"Email marketing enabled: {email_client.enabled}")
