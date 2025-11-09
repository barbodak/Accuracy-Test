import type { RequestEvent } from '@sveltejs/kit';
import { error, json } from '@sveltejs/kit';
import { generatePdfFromUrl } from '$lib/utils/api/pdf-gen';

const TARGET_URL = 'https://metasan.co/core/wp-json/metasan/v1/wil_email';

export async function POST(event: RequestEvent) {
    try {
        const body = await event.request.json().catch(() => ({}));
        let { url, email, name, title, body: emailBody } = body as {
            url?: string;
            email?: string;
            name?: string;
            title?: string;
            body?: string;
        };

        if (!email || !title || !emailBody) {
            console.log(email, "email")
            console.log(title, "title");
            console.log(emailBody, "emailBody");
            error(400, 'Missing required fields: url, email, name, title, body');
        }
        url = 'https://metasan.co/core/wp-json/metasan/v1/wil_email';

        const authToken = event.locals?.authToken ?? null;

        const pdfBuffer = await generatePdfFromUrl("http://10.82.203.254:5173/ValuTest/result", authToken);

        const pdfBase64 = Buffer.from(pdfBuffer).toString('base64');

        console.log(pdfBuffer);

        const res = await fetch(TARGET_URL, {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({
                pdf: pdfBase64,
                email: email,
                body: emailBody
            })
        });

        if (!res.ok) {
            const text = await res.text().catch(() => '');
            error(res.status, text || 'Upstream error');
        }

        const ct = res.headers.get('content-type') || '';
        const data = ct.includes('application/json') ? await res.json() : await res.text();


        return json({ ok: true, forwardedStatus: res.status, data });
    } catch (e: any) {
        if (e?.status) throw e;
        console.error('send-pdf-email error:', e);
        error(500, 'Internal Server Error');
    }
}
