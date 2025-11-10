import puppeteer from 'puppeteer';

export async function generatePdfFromUrl(url: string, authToken?: string | null) {
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox']
        });

        const page = await browser.newPage();

        // await page.emulateMediaFeatures([
        //     { name: 'prefers-color-scheme', value: 'dark' }
        // ]);

        if (authToken) {
            const urlObj = new URL(url);

            await page.setCookie({
                name: 'auth_token',
                value: authToken,
                domain: urlObj.hostname, // e.g., 'localhost' or 'yourdomain.com'
                path: '/',
                httpOnly: false, // Puppeteer needs to be able to set it
                sameSite: 'Lax',
                secure: urlObj.protocol === 'https:'
            });
        }

        await page.goto(url, {
            waitUntil: 'networkidle0',
            // waitUntil: 'domcontentloaded',
        });

        await page.addStyleTag({
            content: `
                @page {
                    margin: 0;
                    size: auto;
                }
                * {
                    page-break-inside: avoid;
                    page-break-before: avoid;
                    page-break-after: avoid;
                }
                body {
                    margin: 0;
                    padding: 0;
                }
            `
        });

        // Get the full height of the page content
        const contentHeight = await page.evaluate(() => {
            // Get the full height of the document
            const body = document.body;
            const html = document.documentElement;

            return Math.max(
                body.scrollHeight,
                body.offsetHeight,
                html.clientHeight,
                html.scrollHeight,
                html.offsetHeight
            );
        });

        const heightInInches = contentHeight / 96;

        const pdfBuffer = await page.pdf({
            preferCSSPageSize: true,
            width: '8.5in',  // Standard letter width (or use 'A4' width)
            height: `${heightInInches}in`,  // Dynamic height based on content
            printBackground: true,
            margin: {
                top: '0',
                right: '0',
                bottom: '0',
                left: '0'
            }
        });

        return pdfBuffer;

    } catch (error) {
        console.error('Error generating PDF:', error);
        throw error;
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}
