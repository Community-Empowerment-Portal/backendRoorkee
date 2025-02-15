const puppeteer = require('puppeteer-extra');
const fs = require('fs').promises;
const { v4: uuidv4 } = require('uuid');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
async function generalSchemes(){
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-extensions'],
    });
    const page = await browser.newPage();

    try {
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
        await page.goto('http://esomsa.hp.gov.in/?q=schemes-3', { waitUntil: 'networkidle2' });
        await page.waitForSelector('.table-responsive .table-bordered', { timeout: 10000 });

        const schemes = await page.evaluate(() => {
            const rows = Array.from(document.querySelectorAll('.table-responsive .table-bordered tbody'));
            const schemesData = [];

            rows.forEach(row => {
                const scheme = {
                    id: null,
                    name: null,
                    objective: null,
                    assistance: null,
                    eligibility: null,
                    process: null,
                    contactOfficer: null,
                    formDownloadLink: null,
                    applyOnlineLink: null,
                    scheme_link: 'http://esomsa.hp.gov.in/?q=schemes-3'
                };

                const schemeName = row.querySelector('tr:nth-child(1) td')?.innerText?.trim() || 'N/A';
                scheme.name = schemeName;

                const dataRows = row.querySelectorAll('tr');
                dataRows.forEach((dataRow) => {
                    const keyElement = dataRow.querySelector('td:nth-child(1)');
                    const valueElement = dataRow.querySelector('td:nth-child(2)');

                    if (keyElement && valueElement) {
                        const key = keyElement.innerText.trim().replace(/\s+/g, '');
                        const value = valueElement.innerText.trim();

                        switch (key) {
                            case 'उद्देश्य':
                                scheme.objective = value;
                                break;
                            case 'सहायता':
                                scheme.assistance = value;
                                break;
                            case 'पात्रता':
                                scheme.eligibility = value;
                                break;
                            case 'प्रक्रिया':
                                scheme.process = value;
                                break;
                            case 'सम्पर्कअधिकारी':
                                scheme.contactOfficer = value;
                                break;
                            case 'डाउनलोडकरनेयोग्यफॉर्म':
                                const formLink = valueElement.querySelector('a');
                                if (formLink) {
                                    scheme.formDownloadLink = formLink.href;
                                }
                                break;
                            case 'ApplyOnlinethrough':
                                const applyOnlineLink = valueElement.querySelector('a');
                                if (applyOnlineLink) {
                                    scheme.applyOnlineLink = applyOnlineLink.href;
                                }
                                break;
                            default:
                                break;
                        }
                    }
                });

                schemesData.push(scheme);
            });

            return schemesData;
        });
        const enrichedSchemes = schemes.map(scheme => ({
            ...scheme,
            id: uuidv4(),
        }));
        return enrichedSchemes
    } catch (error) {
        console.error('An error occurred:', error);
    } finally {
        await browser.close();
    }
}

async function scrapeHimachalPrdeshScholarships(){
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    await page.goto("https://himachal.nic.in/index1.php?lang=1&dpt_id=16&level=2&lid=24092&sublinkid=24929")
    const result = await page.evaluate(()=>{
        const schemeUrls = []
        const schemeUrlNodes = document.querySelectorAll(".cmscontentSubLink div ul li")
        schemeUrlNodes.forEach((node)=>{
            const schemeUrl = node.querySelector("a").href
            schemeUrls.push(schemeUrl)
        })
        return schemeUrls
    })
    const finalSchemeUrls = []
    for (const scheme of result){
        await page.goto(scheme)
        const updatedResult = await page.evaluate(()=>{
            const schemeLink = document.querySelector(".cmscontentMain span a").href
            const title = document.querySelector(".cmscontentMain span a").title.trim()
            const lastUpdatedOn = document.querySelector(".lastupdate").textContent.trim()
            const dateMatch = lastUpdatedOn.match(/\d{1,2}\/\d{1,2}\/\d{4}/);
            const updatedDate = dateMatch[0]
            return {title, schemeUrl: schemeLink, updatedOn: updatedDate}
        })
        finalSchemeUrls.push({...updatedResult, id: uuidv4()})
    }
    await browser.close()
    return finalSchemeUrls
}


async function main(){
    const scholarshipData = await scrapeHimachalPrdeshScholarships()
    const generalSchemes = await generalSchemes()
    const allSchemes = [...scholarshipData, ...generalSchemes]
    const targetDir = path.join(__dirname, '..','..','scrapedData');
    const filePath = path.join(targetDir, 'himachalPradesh.json');
    await fs.writeFile(filePath, JSON.stringify(allSchemes, null, 2))
}

main()

