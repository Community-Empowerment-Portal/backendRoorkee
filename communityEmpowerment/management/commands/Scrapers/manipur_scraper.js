const puppeteer = require('puppeteer');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

async function scrapeUkhrulDistrictSchemes(){
  const urls = [
    'https://ukhrul.nic.in/scheme/district-disability-rehabilitation-centre/',
    'https://ukhrul.nic.in/scheme/manipur-old-age-pension-scheme/',
    'https://ukhrul.nic.in/scheme/pradhan-mantri-matru-vandana-yojana-pmmvy/',
    'https://ukhrul.nic.in/scheme/prevention-of-alcoholism-substance-drugs-abuse/',
    'https://ukhrul.nic.in/scheme/composite-regional-centre-crc/',
    'https://ukhrul.nic.in/scheme/bal-bhavan/',
    'https://ukhrul.nic.in/scheme/mahila-shakti-kendra/',
    'https://ukhrul.nic.in/scheme/rajiv-gandhi-national-creche-schemes/',
    'https://ukhrul.nic.in/scheme/child-protection-servicescps-scheme-mission-vatsalya/',
    'https://ukhrul.nic.in/scheme/national-social-assistance-programmensap/',
    'https://ukhrul.nic.in/scheme/indira-gandhi-national-disable-pension-scheme-igndps/',
    'https://ukhrul.nic.in/scheme/grant-in-aid-ngos-disabled-handicapped/',
    'https://ukhrul.nic.in/scheme/indira-gandhi-national-widow-pension-scheme-ignwps/',
    'https://ukhrul.nic.in/scheme/i-indira-gandhi-national-old-age-pension-scheme-ignoaps/',
    // Add more URLs here if needed
  ];

  const scrapeData = async (page, url) => {
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000  });

    const data = await page.evaluate((url) => {
      const schemes = [];
      document.querySelectorAll('.scheme').forEach((schemeElement) => {
        const title = schemeElement.querySelector('h1')?.innerText.trim() || '';
        var date = schemeElement.querySelector('.schemeMeta strong')?.nextSibling?.nodeValue.trim() || '';
        date = date.replace(' -  |', '').trim();

        const beneficiary = schemeElement.querySelector('h2.heading4 + p')?.innerText.trim() || '';
        const benefits = schemeElement.querySelector('h2.heading4:nth-of-type(2) + p')?.innerText.trim() || '';
        const howToApply = schemeElement.querySelector('h3 + p')?.innerText.trim() || '';

        schemes.push({ title, date, beneficiary, benefits, howToApply, schemeUrl: url });
      });
      return schemes;
    },url);

    return data;
  };

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  let allSchemes = [];
  for (const url of urls) {
    const schemes = await scrapeData(page, url);
    const updatedSchemeData = {...schemes[0], id: uuidv4()}
    allSchemes = allSchemes.concat(updatedSchemeData);
  }
  await browser.close();
  return allSchemes
  


}



async function scrapeManipurScholarships(){
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://manipurminority.gov.in/?page_id=220")
  const result = await page.evaluate(()=>{
    const schemeNodes = document.querySelectorAll(".single-page-article div ul li")
    const schemeList = []

    schemeNodes.forEach((node)=>{
      const title = node.querySelector("h2").textContent.trim()
      const description = node.querySelector("p").textContent.trim()
      schemeList.push({
        title,
        description,
        id: self.crypto.randomUUID(),
        scheme_link: "https://scholarships.gov.in/"

      })
    })

    return schemeList
  })
  await browser.close()
  return result

}
scrapeManipurScholarships()

async function main(){
  const ukhrulDistrictSchemes = await scrapeUkhrulDistrictSchemes()
  const manipurScholarships = await scrapeManipurScholarships()
  const allSchemes = [...ukhrulDistrictSchemes, ...manipurScholarships]
  const targetDir = path.join(__dirname, '..','..','scrapedData');
  const filePath = path.join(targetDir, 'manipur.json');
  fs.writeFileSync(filePath, JSON.stringify(allSchemes, null, 2), 'utf-8');
}

main()