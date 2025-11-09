// src/routes/pdf-download/+server.ts

import type { RequestEvent } from '@sveltejs/kit';
import { generatePdfFromUrl } from '$lib/utils/api/pdf-gen'; // Adjust the path as needed

// 1. Define the handler for a GET request
export async function GET(event: RequestEvent) {
    try {
        const urlToConvert = event.url.searchParams.get('url');

        if (!urlToConvert) {
            return new Response('Missing "url" query parameter.', { status: 400 });
        }

        // --- SECURITY NOTE ---
        // Validate and sanitize the 'urlToConvert' if it comes from user input
        // to prevent SSRF (Server-Side Request Forgery) attacks.
        // For example, ensure it only points to your own domain.
        // --- END SECURITY NOTE ---

        // Get the auth token from locals (set by hooks.server.ts from cookies)
        const authToken = event.locals.authToken;

        // Generate the PDF with authentication
        // Pass the token so Puppeteer can set it as a cookie and render authenticated pages
        const pdfBuffer = await generatePdfFromUrl(urlToConvert, authToken);

        // Convert Buffer to Uint8Array for Web Response compatibility
        const pdfArray = new Uint8Array(pdfBuffer);

        // Return the PDF buffer with the correct headers
        return new Response(pdfArray, {
            status: 200,
            headers: {
                'Content-Type': 'application/pdf',

                'Content-Disposition': 'attachment; filename="document.pdf"',

                'Content-Length': pdfArray.length.toString(),

                'Cache-Control': 'private, max-age=0, must-revalidate',
            },
        });

    } catch (error) {
        console.error('Failed to generate or serve PDF:', error);
        return new Response('Internal Server Error: Could not generate PDF.', { status: 500 });
    }
}
