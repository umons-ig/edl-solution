const puppeteer = require('puppeteer');
const { marked } = require('marked');
const fs = require('fs');
const path = require('path');

(async () => {
    console.log('📄 Génération du PDF pour TP-2.md...');

    // Lire le fichier Markdown
    const markdownPath = path.join(__dirname, '../docs/TP-2.md');
    const markdown = fs.readFileSync(markdownPath, 'utf-8');

    // Convertir Markdown en HTML
    const htmlContent = marked.parse(markdown);

    // Template HTML avec styles
    const html = `
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TP 2 - CI/CD avec GitHub Actions</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2563eb;
                border-bottom: 3px solid #2563eb;
                padding-bottom: 10px;
            }
            h2 {
                color: #1e40af;
                margin-top: 30px;
                border-bottom: 2px solid #93c5fd;
                padding-bottom: 5px;
            }
            h3 {
                color: #1e40af;
                margin-top: 20px;
            }
            code {
                background-color: #f3f4f6;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Monaco', 'Courier New', monospace;
                font-size: 0.9em;
            }
            pre {
                background-color: #1f2937;
                color: #e5e7eb;
                padding: 15px;
                border-radius: 6px;
                overflow-x: auto;
            }
            pre code {
                background-color: transparent;
                color: #e5e7eb;
                padding: 0;
            }
            blockquote {
                border-left: 4px solid #93c5fd;
                padding-left: 15px;
                color: #6b7280;
                font-style: italic;
            }
            ul, ol {
                padding-left: 25px;
            }
            li {
                margin: 5px 0;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #d1d5db;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f3f4f6;
                font-weight: 600;
            }
            hr {
                border: none;
                border-top: 2px solid #e5e7eb;
                margin: 30px 0;
            }
            .page-break {
                page-break-after: always;
            }
            /* Style pour les détails/summary */
            details {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 10px;
                margin: 10px 0;
                background-color: #f9fafb;
            }
            summary {
                cursor: pointer;
                font-weight: 600;
                color: #2563eb;
            }
        </style>
    </head>
    <body>
        ${htmlContent}
    </body>
    </html>
    `;

    // Lancer Puppeteer
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Charger le HTML
    await page.setContent(html, { waitUntil: 'networkidle0' });

    // Générer le PDF
    const outputPath = path.join(__dirname, '../docs/TP-2.pdf');
    await page.pdf({
        path: outputPath,
        format: 'A4',
        printBackground: true,
        margin: {
            top: '20mm',
            right: '15mm',
            bottom: '20mm',
            left: '15mm'
        }
    });

    await browser.close();

    console.log('✅ PDF généré avec succès !');
    console.log(`📄 Fichier: ${outputPath}`);
})();
