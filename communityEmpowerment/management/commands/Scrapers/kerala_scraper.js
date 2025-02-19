const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const BASE_URL = 'https://bcdd.kerala.gov.in/en/schemes/educational-schemes/';
const ADDITIONAL_URLS = [
    'https://scdd.kerala.gov.in/index.php/schemes/educational-programmes',
    'https://scdd.kerala.gov.in/index.php/schemes/economic-development-programmes',
    'https://scdd.kerala.gov.in/index.php/schemes/social-development-schemes'
];

// Function to scrape all scholarship scheme URLs
async function scrapekerelascholarshipUrls() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(BASE_URL, { waitUntil: 'networkidle2' });

    const schemeUrls = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('.service-title-wrap a')).map(anchor => anchor.href);
    });

    console.log(`Found ${schemeUrls.length} scheme URLs`);
    await browser.close();
    return schemeUrls;
}

// Function to scrape details from individual scheme pages
async function scrapeSchemeDetails(schemeUrl) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    console.log(schemeUrl)
    await page.goto(schemeUrl, { waitUntil: 'networkidle2' });

    const schemeData = await page.evaluate(() => {
        const getTextContent = (selector) => {
            const element = document.querySelector(selector);
            return element ? element.textContent.trim() : 'N/A';
        };
    
       
        const getSecondParagraph = () => {
            const entryContent = document.querySelector('.entry-content');
            if (!entryContent) return 'N/A';
    
            const paragraphs = entryContent.querySelectorAll('p');
            return paragraphs.length > 1 ? paragraphs[1].textContent.trim() : 'N/A';
        };

        const scholarshipAmount = document.querySelector(".TFtable2 tbody :nth-child(3) :nth-child(3)").textContent
        const annualIncomeLimit = document.querySelector(".TFtable2 tbody :nth-child(4) :nth-child(3)").textContent
        const eligibilityCriteria = document.querySelector(".TFtable2 tbody :nth-child(6) :nth-child(3)").textContent
        const howToApply = document.querySelector(".TFtable2 tbody :nth-child(7) :nth-child(3)").textContent
        console.log("see thisss: ",{scholarshipAmount, annualIncomeLimit, eligibilityCriteria})
        return {
            title: getTextContent('strong'),
            description: getSecondParagraph(),
            annualIncomeLimit,
            scholarshipAmount,
            eligibilityCriteria,
            howToApply
          
        };
    });

    await browser.close();
    
    
    return { id: uuidv4(), schemeUrl, ...schemeData };
}

// Function to scrape additional schemes
async function scrapeAdditionalSchemes(url) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });

    const schemes = await page.evaluate(() => {
        const getTextContent = (element) => (element ? element.textContent.trim() : '');

        // Function to clean unwanted characters from description
        const cleanDescription = (description) =>
            description.replace(/\s*:\s*$/, '').replace(/^\s*[-:]+\s*/, '').replace(/<br>/g, ' ');

        const data = [];
        const container = document.querySelector('article.item-page');
        if (container) {
            const sections = container.querySelectorAll('p');
            let currentTitle = '';
            let currentDescription = '';

            sections.forEach((section) => {
                const strongElement = section.querySelector('strong');
                if (strongElement) {
                    if (currentTitle && currentDescription) {
                        data.push({
                            title: currentTitle.replace(/\s*:\s*$/, ''),
                            description: cleanDescription(currentDescription)
                        });
                        currentDescription = '';
                    }
                    currentTitle = getTextContent(strongElement);
                } else {
                    currentDescription += getTextContent(section) + ' ';
                }
            });

            if (currentTitle && currentDescription) {
                data.push({
                    title: currentTitle.replace(/\s*:\s*$/, ''),
                    description: cleanDescription(currentDescription)
                });
            }
        }
        return data;
    });

    await browser.close();
    

    return schemes.map(scheme => ({ id: uuidv4(), schemeUrl: url, ...scheme }));
}

// Main function to scrape and save all Kerala scholarships
async function scrapeKeralaScholarships() {
    let allData = [];

    try {
        const schemeUrls = await scrapekerelascholarshipUrls();
        
        for (const url of schemeUrls) {
            try {
                const schemeData = await scrapeSchemeDetails(url);
                allData.push(schemeData);
            } catch (error) {
                console.error(`Error scraping ${url}:`, error);
            }
        }

        for (const url of ADDITIONAL_URLS) {
            try {
                const data = await scrapeAdditionalSchemes(url);
                allData = allData.concat(data);
            } catch (error) {
                console.error(`Error scraping ${url}:`, error);
            }
        }

        // Save data to JSON file
        // const targetDir = path.join(__dirname, '..', '..', 'scrapedData');
        // if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });

        // const filePath = path.join(targetDir, 'kerala.json');
        return allData
    } catch (error) {
        console.error('Error during scraping:', error);
    }
}

async function main(){
    const schemedata = await scrapeKeralaScholarships()
    const targetDir = path.join(__dirname, '..','..','scrapedData', 'scrapedPdfs');
    const filePath = path.join(targetDir, 'kerala.json');
    await fs.writeFile(filePath, JSON.stringify(schemedata, null, 2))
}
scrapeKeralaScholarships();